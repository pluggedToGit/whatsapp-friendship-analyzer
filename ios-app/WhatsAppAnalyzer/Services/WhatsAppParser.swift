//
//  WhatsAppParser.swift
//  WhatsApp Analyzer
//
//  Parses exported WhatsApp chat .txt files (4 formats supported)
//  All processing happens on-device
//

import Foundation

class WhatsAppParser {
    
    // System message keywords
    private let systemKeywords = [
        "created group", "added", "removed", "left",
        "changed the subject", "changed this group",
        "Messages and calls are end-to-end encrypted",
        "security code changed", "changed their phone number",
        "You're now an admin", "is now an admin"
    ]
    
    // Regex patterns for different WhatsApp export formats
    private let patterns: [NSRegularExpression] = {
        return [
            // Format 1: [11/05/24, 12:01:23 AM] John: Hello!
            try! NSRegularExpression(pattern: #"\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2})\s+(AM|PM)\]\s+([^:]+):\s+(.+)"#),
            
            // Format 2: 11/5/24, 12:01 - John: Hello!
            try! NSRegularExpression(pattern: #"(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2})\s+-\s+([^:]+):\s+(.+)"#),
            
            // Format 3: [11/05/24, 12:01:23] John: Hello!
            try! NSRegularExpression(pattern: #"\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2})\]\s+([^:]+):\s+(.+)"#),
            
            // Format 4: 05/11/24, 12:01 - John: Hello! (EU format)
            try! NSRegularExpression(pattern: #"(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2})\s+-\s+([^:]+):\s+(.+)"#)
        ]
    }()
    
    func parse(fileURL: URL) throws -> [Message] {
        let content = try String(contentsOf: fileURL, encoding: .utf8)
        return parse(text: content)
    }
    
    func parse(text: String) -> [Message] {
        var messages: [Message] = []
        var currentMessage: Message?
        
        let lines = text.components(separatedBy: .newlines)
        
        for line in lines {
            guard !line.isEmpty else { continue }
            
            if let parsed = parseLine(line) {
                // New message - save previous if exists
                if let current = currentMessage {
                    messages.append(current)
                }
                currentMessage = parsed
            } else if var current = currentMessage {
                // Continuation of previous message (multi-line)
                current = Message(
                    timestamp: current.timestamp,
                    sender: current.sender,
                    text: current.text + "\n" + line,
                    isSystem: current.isSystem
                )
                currentMessage = current
            }
        }
        
        // Add last message
        if let current = currentMessage {
            messages.append(current)
        }
        
        return messages
    }
    
    private func parseLine(_ line: String) -> Message? {
        let nsLine = line as NSString
        let range = NSRange(location: 0, length: line.count)
        
        // Try each pattern
        for (index, pattern) in patterns.enumerated() {
            guard let match = pattern.firstMatch(in: line, range: range) else {
                continue
            }
            
            switch index {
            case 0: // Bracketed AM/PM format
                return parseFormat1(match: match, in: nsLine)
            case 1, 3: // US/EU format without seconds
                return parseFormat2(match: match, in: nsLine)
            case 2: // Bracketed format without AM/PM
                return parseFormat3(match: match, in: nsLine)
            default:
                continue
            }
        }
        
        return nil
    }
    
    private func parseFormat1(match: NSTextCheckingResult, in line: NSString) -> Message? {
        guard match.numberOfRanges >= 6 else { return nil }
        
        let dateStr = line.substring(with: match.range(at: 1))
        let timeStr = line.substring(with: match.range(at: 2))
        let ampm = line.substring(with: match.range(at: 3))
        let sender = line.substring(with: match.range(at: 4)).trimmingCharacters(in: .whitespaces)
        let text = line.substring(with: match.range(at: 5))
        
        guard let timestamp = parseTimestampAMPM(date: dateStr, time: timeStr, ampm: ampm) else {
            return nil
        }
        
        let isSystem = isSystemMessage(sender: sender, text: text)
        let finalSender = isSystem ? "System" : sender
        
        return Message(timestamp: timestamp, sender: finalSender, text: text, isSystem: isSystem)
    }
    
    private func parseFormat2(match: NSTextCheckingResult, in line: NSString) -> Message? {
        guard match.numberOfRanges >= 5 else { return nil }
        
        let dateStr = line.substring(with: match.range(at: 1))
        let timeStr = line.substring(with: match.range(at: 2))
        let sender = line.substring(with: match.range(at: 3)).trimmingCharacters(in: .whitespaces)
        let text = line.substring(with: match.range(at: 4))
        
        guard let timestamp = parseTimestamp24Hour(date: dateStr, time: timeStr) else {
            return nil
        }
        
        let isSystem = isSystemMessage(sender: sender, text: text)
        let finalSender = isSystem ? "System" : sender
        
        return Message(timestamp: timestamp, sender: finalSender, text: text, isSystem: isSystem)
    }
    
    private func parseFormat3(match: NSTextCheckingResult, in line: NSString) -> Message? {
        guard match.numberOfRanges >= 5 else { return nil }
        
        let dateStr = line.substring(with: match.range(at: 1))
        let timeStr = line.substring(with: match.range(at: 2))
        let sender = line.substring(with: match.range(at: 3)).trimmingCharacters(in: .whitespaces)
        let text = line.substring(with: match.range(at: 4))
        
        guard let timestamp = parseTimestamp24Hour(date: dateStr, time: timeStr + ":00") else {
            return nil
        }
        
        let isSystem = isSystemMessage(sender: sender, text: text)
        let finalSender = isSystem ? "System" : sender
        
        return Message(timestamp: timestamp, sender: finalSender, text: text, isSystem: isSystem)
    }
    
    private func parseTimestampAMPM(date: String, time: String, ampm: String) -> Date? {
        // Parse: "11/05/24" and "12:01:23" and "AM"
        let components = date.split(separator: "/").map { Int($0) }
        guard components.count == 3,
              let month = components[0],
              let day = components[1],
              let year = components[2] else {
            return nil
        }
        
        let timeComponents = time.split(separator: ":").map { Int($0) }
        guard timeComponents.count >= 2,
              var hour = timeComponents[0],
              let minute = timeComponents[1] else {
            return nil
        }
        let second = timeComponents.count >= 3 ? (timeComponents[2] ?? 0) : 0
        
        // Convert to 24-hour
        if ampm == "PM" && hour != 12 {
            hour += 12
        } else if ampm == "AM" && hour == 12 {
            hour = 0
        }
        
        let fullYear = year < 100 ? 2000 + year : year
        
        var dateComponents = DateComponents()
        dateComponents.year = fullYear
        dateComponents.month = month
        dateComponents.day = day
        dateComponents.hour = hour
        dateComponents.minute = minute
        dateComponents.second = second
        
        return Calendar.current.date(from: dateComponents)
    }
    
    private func parseTimestamp24Hour(date: String, time: String) -> Date? {
        // Parse: "11/05/24" and "12:01" or "12:01:23"
        let components = date.split(separator: "/").map { Int($0) }
        guard components.count == 3,
              let month = components[0],
              let day = components[1],
              let year = components[2] else {
            return nil
        }
        
        let timeComponents = time.split(separator: ":").map { Int($0) }
        guard timeComponents.count >= 2,
              let hour = timeComponents[0],
              let minute = timeComponents[1] else {
            return nil
        }
        let second = timeComponents.count >= 3 ? (timeComponents[2] ?? 0) : 0
        
        let fullYear = year < 100 ? 2000 + year : year
        
        var dateComponents = DateComponents()
        dateComponents.year = fullYear
        dateComponents.month = month
        dateComponents.day = day
        dateComponents.hour = hour
        dateComponents.minute = minute
        dateComponents.second = second
        
        return Calendar.current.date(from: dateComponents)
    }
    
    private func isSystemMessage(sender: String, text: String) -> Bool {
        let combined = (sender + " " + text).lowercased()
        return systemKeywords.contains { combined.contains($0.lowercased()) }
    }
}
