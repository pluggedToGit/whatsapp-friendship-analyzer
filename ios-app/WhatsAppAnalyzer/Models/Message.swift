//
//  Message.swift
//  WhatsApp Analyzer
//
//  On-device chat analysis - all data stays local
//

import Foundation

struct Message: Identifiable, Codable {
    let id: UUID
    let timestamp: Date
    let sender: String
    let text: String
    let isSystem: Bool
    
    // Analysis fields
    var sentiment: Double = 0.0  // -1 to 1
    var containsEmoji: Bool = false
    var emojiCount: Int = 0
    var wordCount: Int = 0
    
    init(timestamp: Date, sender: String, text: String, isSystem: Bool = false) {
        self.id = UUID()
        self.timestamp = timestamp
        self.sender = sender
        self.text = text
        self.isSystem = isSystem
        self.wordCount = text.split(separator: " ").count
        
        // Simple emoji detection
        self.emojiCount = text.unicodeScalars.filter { $0.properties.isEmoji }.count
        self.containsEmoji = emojiCount > 0
    }
}

struct ChatAnalysis: Identifiable, Codable {
    let id: UUID
    let chatName: String
    let messages: [Message]
    let participants: [String]
    let startDate: Date
    let endDate: Date
    let relationshipType: RelationshipType
    let confidenceScore: Int
    let confidenceLevel: ConfidenceLevel
    let stats: ChatStats
    let toneAnalysis: ToneAnalysis
    let personalityProfiles: [String: PersonalityProfile]
    let interpretation: String
    
    var durationDays: Int {
        Calendar.current.dateComponents([.day], from: startDate, to: endDate).day ?? 0
    }
    
    var messagesPerDay: Double {
        let days = max(durationDays, 1)
        return Double(messages.count) / Double(days)
    }
}

struct ChatStats: Codable {
    let totalMessages: Int
    let messageCounts: [String: Int]
    let nightPercentage: Double
    let averageSentiment: Double
}

struct ToneAnalysis: Codable {
    let casualPercentage: Double
    let formalPercentage: Double
    let playfulPercentage: Double
    let insultPercentage: Double
    let roastingPercentage: Double
}

struct PersonalityProfile: Codable {
    let communicationStyle: String
    let responseStyle: String
    let textingPattern: String
    let expressionStyle: String
}

enum RelationshipType: String, Codable, CaseIterable {
    case romanticDating = "Romantic/Dating"
    case romanticEstablished = "Romantic (Established)"
    case closeFriends = "Close Friends"
    case casualFriends = "Casual Friends"
    case familySibling = "Family (Sibling)"
    case familyParent = "Family (Parent-Child)"
    case colleagues = "Colleagues"
    case workProfessional = "Work/Professional"
    case bossSubordinate = "Boss/Subordinate"
    case acquaintances = "Acquaintances"
    case enemyConflict = "Enemy/Conflict"
    case newAcquaintance = "New Acquaintance"
    
    var emoji: String {
        switch self {
        case .romanticDating: return "💕"
        case .romanticEstablished: return "❤️"
        case .closeFriends: return "👥"
        case .casualFriends: return "🤝"
        case .familySibling: return "👨‍👩‍👧‍👦"
        case .familyParent: return "👨‍👩‍👧"
        case .colleagues: return "💼"
        case .workProfessional: return "🏢"
        case .bossSubordinate: return "👔"
        case .acquaintances: return "👋"
        case .enemyConflict: return "⚔️"
        case .newAcquaintance: return "✨"
        }
    }
    
    var color: String {
        switch self {
        case .romanticDating, .romanticEstablished: return "pink"
        case .closeFriends, .casualFriends: return "blue"
        case .familySibling, .familyParent: return "green"
        case .colleagues, .workProfessional, .bossSubordinate: return "purple"
        case .acquaintances, .newAcquaintance: return "gray"
        case .enemyConflict: return "red"
        }
    }
}

enum ConfidenceLevel: String, Codable {
    case veryHigh = "VERY HIGH"
    case high = "HIGH"
    case moderate = "MODERATE"
    case low = "LOW"
    
    var color: String {
        switch self {
        case .veryHigh: return "green"
        case .high: return "blue"
        case .moderate: return "orange"
        case .low: return "red"
        }
    }
}
