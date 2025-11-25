//
//  ToneDetector.swift
//  WhatsApp Analyzer
//
//  Keyword-based tone detection across 5 categories
//

import Foundation

class ToneDetector {
    
    private let toneKeywords: [String: [String]] = [
        "casual": ["bro", "dude", "bruh", "yo", "hey", "sup", "wassup", "lol", "lmao", "rofl", "haha", "yeah", "yep", "nah", "gonna", "wanna", "cool", "awesome"],
        "formal": ["please", "thank you", "sir", "madam", "kindly", "appreciate", "regards", "certainly", "indeed", "however"],
        "playful": ["just kidding", "jk", "joking", "teasing", "silly", "goofy", "funny", "hilarious"],
        "insult": ["shut up", "stfu", "stupid", "dumb", "idiot", "annoying", "hate you"],
        "roasting": ["loser", "dummy", "nerd", "weirdo", "clown", "embarrassing", "cringe"]
    ]
    
    func analyze(messages: [Message]) -> ToneAnalysis {
        guard !messages.isEmpty else {
            return ToneAnalysis(
                casualPercentage: 0,
                formalPercentage: 0,
                playfulPercentage: 0,
                insultPercentage: 0,
                roastingPercentage: 0
            )
        }
        
        var toneCounts: [String: Int] = [
            "casual": 0,
            "formal": 0,
            "playful": 0,
            "insult": 0,
            "roasting": 0
        ]
        
        for message in messages {
            let lowercased = message.text.lowercased()
            
            for (tone, keywords) in toneKeywords {
                for keyword in keywords {
                    if lowercased.contains(keyword) {
                        toneCounts[tone, default: 0] += 1
                        break // Count once per message per tone
                    }
                }
            }
        }
        
        let total = Double(messages.count)
        
        return ToneAnalysis(
            casualPercentage: Double(toneCounts["casual"] ?? 0) / total * 100,
            formalPercentage: Double(toneCounts["formal"] ?? 0) / total * 100,
            playfulPercentage: Double(toneCounts["playful"] ?? 0) / total * 100,
            insultPercentage: Double(toneCounts["insult"] ?? 0) / total * 100,
            roastingPercentage: Double(toneCounts["roasting"] ?? 0) / total * 100
        )
    }
}
