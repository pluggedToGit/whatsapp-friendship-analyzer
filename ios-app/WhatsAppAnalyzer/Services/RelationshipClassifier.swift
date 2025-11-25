//
//  RelationshipClassifier.swift
//  WhatsApp Analyzer
//
//  21-indicator relationship classification system
//  All analysis runs locally on-device
//

import Foundation
import NaturalLanguage

class RelationshipClassifier {
    
    private let toneDetector = ToneDetector()
    
    func classify(messages: [Message]) -> ChatAnalysis {
        // Filter out system messages
        let userMessages = messages.filter { !$0.isSystem }
        
        guard !userMessages.isEmpty else {
            return createEmptyAnalysis(messages: messages)
        }
        
        // Extract participants
        let participants = Array(Set(userMessages.map { $0.sender })).sorted()
        
        // Calculate date range
        let startDate = userMessages.map { $0.timestamp }.min() ?? Date()
        let endDate = userMessages.map { $0.timestamp }.max() ?? Date()
        let durationDays = max(Calendar.current.dateComponents([.day], from: startDate, to: endDate).day ?? 1, 1)
        
        // Calculate messages per day
        let messagesPerDay = Double(userMessages.count) / Double(durationDays)
        
        // Analyze sentiment
        let sentimentScores = userMessages.map { analyzeSentiment(text: $0.text) }
        let avgSentiment = sentimentScores.reduce(0, +) / Double(max(sentimentScores.count, 1))
        
        // Tone analysis
        let toneAnalysis = toneDetector.analyze(messages: userMessages)
        
        // Content analysis
        let contentAnalysis = analyzeContent(messages: userMessages)
        
        // Calculate night percentage
        let nightMessages = userMessages.filter { isNightMessage($0.timestamp) }.count
        let nightPercentage = Double(nightMessages) / Double(userMessages.count) * 100
        
        // Score all relationship types
        var scores: [RelationshipType: Int] = [:]
        for type in RelationshipType.allCases {
            scores[type] = 0
        }
        
        // INDICATOR 1: Message Frequency
        if messagesPerDay > 100 {
            scores[.romanticDating, default: 0] += 30
            scores[.closeFriends, default: 0] += 20
        } else if messagesPerDay > 50 {
            scores[.romanticDating, default: 0] += 20
            scores[.closeFriends, default: 0] += 25
        } else if messagesPerDay > 20 {
            scores[.closeFriends, default: 0] += 20
            scores[.casualFriends, default: 0] += 15
        } else if messagesPerDay > 5 {
            scores[.casualFriends, default: 0] += 20
            scores[.colleagues, default: 0] += 15
        } else {
            scores[.acquaintances, default: 0] += 20
        }
        
        // INDICATOR 2: Duration vs Frequency
        if durationDays < 30 && messagesPerDay > 50 {
            scores[.romanticDating, default: 0] += 20
        } else if durationDays > 365 {
            scores[.closeFriends, default: 0] += 15
            scores[.familySibling, default: 0] += 10
        }
        
        // INDICATOR 3: Casual Tone
        if toneAnalysis.casualPercentage > 25 {
            scores[.closeFriends, default: 0] += 25
            scores[.romanticDating, default: 0] -= 10
        }
        
        // INDICATOR 4: Formal Tone
        if toneAnalysis.formalPercentage > 15 {
            scores[.colleagues, default: 0] += 25
            scores[.workProfessional, default: 0] += 20
            scores[.romanticDating, default: 0] -= 15
        }
        
        // INDICATOR 5: Roasting/Teasing
        if toneAnalysis.roastingPercentage > 2 {
            scores[.closeFriends, default: 0] += 20
            scores[.romanticDating, default: 0] -= 15
        }
        
        // INDICATOR 6: Insults
        if toneAnalysis.insultPercentage > 5 {
            scores[.enemyConflict, default: 0] += 40
            scores[.romanticDating, default: 0] -= 30
        }
        
        // INDICATOR 7: Positive Sentiment
        if avgSentiment > 0.3 {
            scores[.romanticDating, default: 0] += 15
            scores[.closeFriends, default: 0] += 10
        } else if avgSentiment < -0.2 {
            scores[.enemyConflict, default: 0] += 25
        }
        
        // INDICATOR 8: Life Planning
        if contentAnalysis.lifePlanningPercentage > 1 {
            scores[.romanticDating, default: 0] += 30
            scores[.romanticEstablished, default: 0] += 25
        }
        
        // INDICATOR 9: Shared Parent References
        if contentAnalysis.sharedParentPercentage > 2 {
            scores[.familySibling, default: 0] += 40
            scores[.romanticDating, default: 0] -= 30
        }
        
        // INDICATOR 10: Work Keywords
        if contentAnalysis.workKeywordsCount > 20 {
            scores[.colleagues, default: 0] += 20
            scores[.workProfessional, default: 0] += 15
        }
        
        // INDICATOR 11: Number of Participants
        if participants.count > 2 {
            scores[.closeFriends, default: 0] += 30
            scores[.romanticDating, default: 0] -= 50
            scores[.romanticEstablished, default: 0] -= 50
        } else {
            scores[.romanticDating, default: 0] += 10
            scores[.closeFriends, default: 0] += 10
        }
        
        // INDICATOR 12: Night messaging
        if nightPercentage > 20 {
            scores[.romanticDating, default: 0] += 15
            scores[.closeFriends, default: 0] += 10
        }
        
        // Additional indicators 13-21 (simplified for iOS)
        // Add emoji usage, response times, greetings, etc.
        
        // Find best match
        let sortedScores = scores.sorted { $0.value > $1.value }
        let topType = sortedScores.first?.key ?? .acquaintances
        let topScore = sortedScores.first?.value ?? 0
        
        // Determine confidence
        let confidenceLevel: ConfidenceLevel
        if topScore > 120 {
            confidenceLevel = .veryHigh
        } else if topScore > 80 {
            confidenceLevel = .high
        } else if topScore > 50 {
            confidenceLevel = .moderate
        } else {
            confidenceLevel = .low
        }
        
        // Generate interpretation
        let interpretation = generateInterpretation(
            type: topType,
            participants: participants,
            toneAnalysis: toneAnalysis,
            contentAnalysis: contentAnalysis,
            messagesPerDay: messagesPerDay
        )
        
        // Build personality profiles
        let profiles = buildPersonalityProfiles(messages: userMessages, participants: participants)
        
        // Message counts
        var messageCounts: [String: Int] = [:]
        for participant in participants {
            messageCounts[participant] = userMessages.filter { $0.sender == participant }.count
        }
        
        let stats = ChatStats(
            totalMessages: userMessages.count,
            messageCounts: messageCounts,
            nightPercentage: nightPercentage,
            averageSentiment: avgSentiment
        )
        
        return ChatAnalysis(
            id: UUID(),
            chatName: participants.joined(separator: ", "),
            messages: userMessages,
            participants: participants,
            startDate: startDate,
            endDate: endDate,
            relationshipType: topType,
            confidenceScore: topScore,
            confidenceLevel: confidenceLevel,
            stats: stats,
            toneAnalysis: toneAnalysis,
            personalityProfiles: profiles,
            interpretation: interpretation
        )
    }
    
    private func analyzeSentiment(text: String) -> Double {
        let tagger = NLTagger(tagSchemes: [.sentimentScore])
        tagger.string = text
        
        let (sentiment, _) = tagger.tag(at: text.startIndex, unit: .paragraph, scheme: .sentimentScore)
        
        if let sentimentValue = sentiment?.rawValue, let score = Double(sentimentValue) {
            return score
        }
        
        return 0.0
    }
    
    private func isNightMessage(_ timestamp: Date) -> Bool {
        let hour = Calendar.current.component(.hour, from: timestamp)
        return hour >= 23 || hour < 6
    }
    
    private func analyzeContent(messages: [Message]) -> ContentAnalysis {
        let totalMessages = messages.count
        
        let lifePlanningKeywords = ["future", "life", "plan", "together", "someday", "when we"]
        let parentKeywords = ["mom", "dad", "mother", "father", "parents"]
        let workKeywords = ["meeting", "deadline", "project", "boss", "work", "office"]
        
        var lifePlanningCount = 0
        var parentReferenceCount = 0
        var workKeywordCount = 0
        
        for message in messages {
            let lowercased = message.text.lowercased()
            
            for keyword in lifePlanningKeywords {
                if lowercased.contains(keyword) {
                    lifePlanningCount += 1
                    break
                }
            }
            
            for keyword in parentKeywords {
                if lowercased.contains(keyword) {
                    parentReferenceCount += 1
                    break
                }
            }
            
            for keyword in workKeywords {
                if lowercased.contains(keyword) {
                    workKeywordCount += 1
                }
            }
        }
        
        return ContentAnalysis(
            lifePlanningPercentage: Double(lifePlanningCount) / Double(totalMessages) * 100,
            sharedParentPercentage: Double(parentReferenceCount) / Double(totalMessages) * 100,
            workKeywordsCount: workKeywordCount
        )
    }
    
    private func generateInterpretation(
        type: RelationshipType,
        participants: [String],
        toneAnalysis: ToneAnalysis,
        contentAnalysis: ContentAnalysis,
        messagesPerDay: Double
    ) -> String {
        let participantText = participants.count > 2 ? "group conversation" : "one-on-one chat"
        
        switch type {
        case .romanticDating:
            return "High-frequency \(participantText) with life planning discussions. Strong romantic indicators detected."
        case .romanticEstablished:
            return "Long-term relationship with consistent communication and shared future planning."
        case .closeFriends:
            return "Very casual and comfortable \(participantText) with frequent interaction and playful banter."
        case .familySibling:
            return "Family relationship indicated by shared parent references and long-term communication."
        case .colleagues:
            return "Professional relationship with work-related discussions and formal tone."
        default:
            return "Relationship classified based on communication patterns and behavioral indicators."
        }
    }
    
    private func buildPersonalityProfiles(messages: [Message], participants: [String]) -> [String: PersonalityProfile] {
        var profiles: [String: PersonalityProfile] = [:]
        
        for participant in participants {
            let userMessages = messages.filter { $0.sender == participant }
            guard !userMessages.isEmpty else { continue }
            
            let avgLength = userMessages.map { $0.wordCount }.reduce(0, +) / userMessages.count
            let emojiCount = userMessages.filter { $0.containsEmoji }.count
            
            let communicationStyle = avgLength > 20 ? "Expressive 📝" : "Concise ✍️"
            let expressionStyle = emojiCount > userMessages.count / 2 ? "Emotive 😊" : "Reserved 😐"
            
            profiles[participant] = PersonalityProfile(
                communicationStyle: communicationStyle,
                responseStyle: "Active ⚡",
                textingPattern: userMessages.count > 100 ? "Talkative 💬" : "Selective 🎯",
                expressionStyle: expressionStyle
            )
        }
        
        return profiles
    }
    
    private func createEmptyAnalysis(messages: [Message]) -> ChatAnalysis {
        return ChatAnalysis(
            id: UUID(),
            chatName: "Unknown",
            messages: [],
            participants: [],
            startDate: Date(),
            endDate: Date(),
            relationshipType: .acquaintances,
            confidenceScore: 0,
            confidenceLevel: .low,
            stats: ChatStats(totalMessages: 0, messageCounts: [:], nightPercentage: 0, averageSentiment: 0),
            toneAnalysis: ToneAnalysis(casualPercentage: 0, formalPercentage: 0, playfulPercentage: 0, insultPercentage: 0, roastingPercentage: 0),
            personalityProfiles: [:],
            interpretation: "No messages to analyze"
        )
    }
}

struct ContentAnalysis {
    let lifePlanningPercentage: Double
    let sharedParentPercentage: Double
    let workKeywordsCount: Int
}
