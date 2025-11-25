//
//  ResultsView.swift
//  WhatsApp Analyzer
//
//  Detailed results display with native iOS design
//

import SwiftUI

struct ResultsView: View {
    let analysis: ChatAnalysis
    @ObservedObject var viewModel: AnalyzerViewModel
    @Environment(\.dismiss) var dismiss
    @State private var showingShareSheet = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 25) {
                    // Header card
                    HeaderCardView(analysis: analysis)
                        .padding(.horizontal)
                        .padding(.top)
                    
                    // Stats grid
                    StatsGridView(analysis: analysis)
                        .padding(.horizontal)
                    
                    // Tone analysis
                    ToneAnalysisView(toneAnalysis: analysis.toneAnalysis)
                        .padding(.horizontal)
                    
                    // Message distribution
                    MessageDistributionView(stats: analysis.stats)
                        .padding(.horizontal)
                    
                    // Personality profiles
                    if !analysis.personalityProfiles.isEmpty {
                        PersonalityProfilesView(profiles: analysis.personalityProfiles)
                            .padding(.horizontal)
                    }
                    
                    // Key insights
                    KeyInsightsView(analysis: analysis)
                        .padding(.horizontal)
                        .padding(.bottom, 30)
                }
            }
            .background(
                LinearGradient(
                    colors: [Color(hex: "667eea").opacity(0.1), Color(hex: "764ba2").opacity(0.1)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
            )
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Done") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showingShareSheet = true
                    }) {
                        Image(systemName: "square.and.arrow.up")
                    }
                }
            }
            .sheet(isPresented: $showingShareSheet) {
                ShareSheet(activityItems: [viewModel.exportAsText(analysis: analysis)])
            }
        }
    }
}

struct HeaderCardView: View {
    let analysis: ChatAnalysis
    
    var body: some View {
        VStack(spacing: 15) {
            Text(analysis.relationshipType.emoji)
                .font(.system(size: 70))
            
            Text(analysis.relationshipType.rawValue)
                .font(.system(size: 28, weight: .bold))
                .foregroundColor(Color(hex: "667eea"))
            
            HStack {
                Text("Confidence:")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                Text(analysis.confidenceLevel.rawValue)
                    .font(.subheadline.bold())
                    .foregroundColor(confidenceLevelColor(analysis.confidenceLevel))
                
                Text("(\(analysis.confidenceScore))")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Text(analysis.interpretation)
                .font(.body)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal)
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color.white)
        .cornerRadius(20)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
    
    private func confidenceLevelColor(_ level: ConfidenceLevel) -> Color {
        switch level {
        case .veryHigh: return .green
        case .high: return .blue
        case .moderate: return .orange
        case .low: return .red
        }
    }
}

struct StatsGridView: View {
    let analysis: ChatAnalysis
    
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Overview")
                .font(.title3.bold())
                .foregroundColor(.primary)
            
            LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 15) {
                StatBoxView(label: "Messages", value: "\(analysis.stats.totalMessages)", icon: "bubble.left.and.bubble.right.fill")
                StatBoxView(label: "Duration", value: "\(analysis.durationDays) days", icon: "calendar")
                StatBoxView(label: "Daily Avg", value: String(format: "%.0f", analysis.messagesPerDay), icon: "chart.line.uptrend.xyaxis")
                StatBoxView(label: "Participants", value: "\(analysis.participants.count)", icon: "person.2.fill")
            }
        }
    }
}

struct StatBoxView: View {
    let label: String
    let value: String
    let icon: String
    
    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(.white)
            
            Text(value)
                .font(.title2.bold())
                .foregroundColor(.white)
            
            Text(label)
                .font(.caption)
                .foregroundColor(.white.opacity(0.9))
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(
            LinearGradient(
                colors: [Color(hex: "667eea"), Color(hex: "764ba2")],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .cornerRadius(15)
    }
}

struct ToneAnalysisView: View {
    let toneAnalysis: ToneAnalysis
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Tone Analysis")
                .font(.title3.bold())
                .foregroundColor(.primary)
            
            VStack(spacing: 12) {
                ToneBarView(label: "😎 Casual", percentage: toneAnalysis.casualPercentage, color: .blue)
                ToneBarView(label: "👔 Formal", percentage: toneAnalysis.formalPercentage, color: .purple)
                ToneBarView(label: "🎭 Playful", percentage: toneAnalysis.playfulPercentage, color: .green)
                ToneBarView(label: "😤 Insults", percentage: toneAnalysis.insultPercentage, color: .red)
                ToneBarView(label: "🔥 Roasting", percentage: toneAnalysis.roastingPercentage, color: .orange)
            }
            .padding()
            .background(Color.white)
            .cornerRadius(15)
            .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
        }
    }
}

struct ToneBarView: View {
    let label: String
    let percentage: Double
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: 5) {
            HStack {
                Text(label)
                    .font(.subheadline)
                Spacer()
                Text(String(format: "%.1f%%", percentage))
                    .font(.subheadline.bold())
                    .foregroundColor(color)
            }
            
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    Rectangle()
                        .fill(Color.gray.opacity(0.2))
                        .frame(height: 8)
                        .cornerRadius(4)
                    
                    Rectangle()
                        .fill(color)
                        .frame(width: geometry.size.width * CGFloat(min(percentage, 100) / 100), height: 8)
                        .cornerRadius(4)
                }
            }
            .frame(height: 8)
        }
    }
}

struct MessageDistributionView: View {
    let stats: ChatStats
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Message Distribution")
                .font(.title3.bold())
                .foregroundColor(.primary)
            
            VStack(spacing: 10) {
                ForEach(stats.messageCounts.sorted(by: { $0.value > $1.value }), id: \.key) { participant, count in
                    HStack {
                        Text(participant)
                            .font(.subheadline.bold())
                            .foregroundColor(.primary)
                        
                        Spacer()
                        
                        Text("\(count)")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Text("(\(String(format: "%.1f%%", Double(count) / Double(stats.totalMessages) * 100)))")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(10)
                }
            }
        }
    }
}

struct PersonalityProfilesView: View {
    let profiles: [String: PersonalityProfile]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Personality Profiles")
                .font(.title3.bold())
                .foregroundColor(.primary)
            
            ForEach(profiles.sorted(by: { $0.key < $1.key }), id: \.key) { participant, profile in
                VStack(alignment: .leading, spacing: 10) {
                    Text(participant)
                        .font(.headline)
                        .foregroundColor(Color(hex: "667eea"))
                    
                    VStack(alignment: .leading, spacing: 5) {
                        ProfileTraitView(trait: profile.communicationStyle)
                        ProfileTraitView(trait: profile.responseStyle)
                        ProfileTraitView(trait: profile.textingPattern)
                        ProfileTraitView(trait: profile.expressionStyle)
                    }
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.white)
                .cornerRadius(15)
                .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
            }
        }
    }
}

struct ProfileTraitView: View {
    let trait: String
    
    var body: some View {
        HStack(spacing: 5) {
            Image(systemName: "checkmark.circle.fill")
                .font(.caption)
                .foregroundColor(.green)
            
            Text(trait)
                .font(.subheadline)
                .foregroundColor(.primary)
        }
    }
}

struct KeyInsightsView: View {
    let analysis: ChatAnalysis
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Key Insights")
                .font(.title3.bold())
                .foregroundColor(.primary)
            
            VStack(spacing: 12) {
                InsightItemView(
                    icon: "moon.stars.fill",
                    text: "Night messaging: \(String(format: "%.1f%%", analysis.stats.nightPercentage))"
                )
                
                InsightItemView(
                    icon: "heart.fill",
                    text: "Average sentiment: \(sentimentDescription(analysis.stats.averageSentiment))"
                )
                
                if analysis.participants.count > 2 {
                    InsightItemView(
                        icon: "person.3.fill",
                        text: "Group conversation with \(analysis.participants.count) participants"
                    )
                } else {
                    InsightItemView(
                        icon: "person.2.fill",
                        text: "One-on-one conversation"
                    )
                }
            }
            .padding()
            .background(Color.white)
            .cornerRadius(15)
            .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
        }
    }
    
    private func sentimentDescription(_ sentiment: Double) -> String {
        if sentiment > 0.3 {
            return "Very positive 😊"
        } else if sentiment > 0.1 {
            return "Positive 🙂"
        } else if sentiment > -0.1 {
            return "Neutral 😐"
        } else if sentiment > -0.3 {
            return "Negative 🙁"
        } else {
            return "Very negative 😢"
        }
    }
}

struct InsightItemView: View {
    let icon: String
    let text: String
    
    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(Color(hex: "667eea"))
                .frame(width: 30)
            
            Text(text)
                .font(.subheadline)
                .foregroundColor(.primary)
            
            Spacer()
        }
    }
}

// Share sheet for exporting
struct ShareSheet: UIViewControllerRepresentable {
    let activityItems: [Any]
    
    func makeUIViewController(context: Context) -> UIActivityViewController {
        let controller = UIActivityViewController(activityItems: activityItems, applicationActivities: nil)
        return controller
    }
    
    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}
