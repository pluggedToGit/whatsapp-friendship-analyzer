//
//  ContentView.swift
//  WhatsApp Analyzer
//
//  Main app interface with file import and analysis display
//

import SwiftUI
import UniformTypeIdentifiers

struct ContentView: View {
    @StateObject private var viewModel = AnalyzerViewModel()
    @State private var showingFilePicker = false
    @State private var showingResults = false
    
    var body: some View {
        NavigationView {
            ZStack {
                // Background gradient
                LinearGradient(
                    colors: [Color(hex: "667eea"), Color(hex: "764ba2")],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: 30) {
                    // Header
                    VStack(spacing: 10) {
                        Image(systemName: "chart.bar.doc.horizontal")
                            .font(.system(size: 60))
                            .foregroundColor(.white)
                        
                        Text("WhatsApp Analyzer")
                            .font(.system(size: 32, weight: .bold))
                            .foregroundColor(.white)
                        
                        Text("100% On-Device Analysis")
                            .font(.subheadline)
                            .foregroundColor(.white.opacity(0.9))
                        
                        Text("🔒 Your data never leaves this device")
                            .font(.caption)
                            .foregroundColor(.white.opacity(0.8))
                    }
                    .padding(.top, 50)
                    
                    Spacer()
                    
                    // Main action button
                    if viewModel.analyses.isEmpty {
                        VStack(spacing: 20) {
                            Button(action: {
                                showingFilePicker = true
                            }) {
                                VStack(spacing: 15) {
                                    Image(systemName: "doc.badge.plus")
                                        .font(.system(size: 50))
                                    
                                    Text("Import WhatsApp Chat")
                                        .font(.title3.bold())
                                }
                                .frame(maxWidth: .infinity)
                                .padding(40)
                                .background(Color.white)
                                .foregroundColor(Color(hex: "667eea"))
                                .cornerRadius(20)
                                .shadow(color: .black.opacity(0.2), radius: 10, x: 0, y: 5)
                            }
                            .padding(.horizontal, 40)
                            
                            VStack(spacing: 8) {
                                Text("How to export:")
                                    .font(.caption.bold())
                                    .foregroundColor(.white)
                                
                                Text("Open WhatsApp → Chat → ⋮ → More → Export chat → Without Media")
                                    .font(.caption)
                                    .foregroundColor(.white.opacity(0.9))
                                    .multilineTextAlignment(.center)
                                    .padding(.horizontal, 40)
                            }
                        }
                    } else {
                        // Show saved analyses
                        VStack(spacing: 20) {
                            Text("Saved Analyses")
                                .font(.title2.bold())
                                .foregroundColor(.white)
                            
                            ScrollView {
                                VStack(spacing: 15) {
                                    ForEach(viewModel.analyses) { analysis in
                                        AnalysisRowView(analysis: analysis)
                                            .onTapGesture {
                                                viewModel.selectedAnalysis = analysis
                                                showingResults = true
                                            }
                                    }
                                }
                                .padding(.horizontal)
                            }
                            
                            Button(action: {
                                showingFilePicker = true
                            }) {
                                HStack {
                                    Image(systemName: "plus.circle.fill")
                                    Text("Import Another Chat")
                                }
                                .font(.headline)
                                .foregroundColor(Color(hex: "667eea"))
                                .padding()
                                .frame(maxWidth: .infinity)
                                .background(Color.white)
                                .cornerRadius(15)
                            }
                            .padding(.horizontal, 40)
                        }
                        .padding(.vertical)
                    }
                    
                    Spacer()
                }
            }
            .fileImporter(
                isPresented: $showingFilePicker,
                allowedContentTypes: [.plainText],
                allowsMultipleSelection: false
            ) { result in
                Task {
                    switch result {
                    case .success(let urls):
                        if let url = urls.first {
                            _ = url.startAccessingSecurityScopedResource()
                            await viewModel.importAndAnalyze(fileURL: url)
                            url.stopAccessingSecurityScopedResource()
                            
                            if viewModel.errorMessage == nil {
                                showingResults = true
                            }
                        }
                    case .failure(let error):
                        viewModel.errorMessage = error.localizedDescription
                    }
                }
            }
            .sheet(isPresented: $showingResults) {
                if let analysis = viewModel.selectedAnalysis {
                    ResultsView(analysis: analysis, viewModel: viewModel)
                }
            }
            .alert("Error", isPresented: .constant(viewModel.errorMessage != nil)) {
                Button("OK") {
                    viewModel.errorMessage = nil
                }
            } message: {
                if let error = viewModel.errorMessage {
                    Text(error)
                }
            }
            .overlay {
                if viewModel.isProcessing {
                    ZStack {
                        Color.black.opacity(0.4)
                            .ignoresSafeArea()
                        
                        VStack(spacing: 20) {
                            ProgressView()
                                .scaleEffect(1.5)
                                .tint(.white)
                            
                            Text("Analyzing chat...")
                                .font(.headline)
                                .foregroundColor(.white)
                        }
                        .padding(40)
                        .background(Color(hex: "667eea"))
                        .cornerRadius(20)
                    }
                }
            }
        }
        .onAppear {
            viewModel.loadAnalyses()
        }
    }
}

struct AnalysisRowView: View {
    let analysis: ChatAnalysis
    
    var body: some View {
        HStack {
            Text(analysis.relationshipType.emoji)
                .font(.largeTitle)
            
            VStack(alignment: .leading, spacing: 5) {
                Text(analysis.chatName)
                    .font(.headline)
                    .foregroundColor(.white)
                
                Text("\(analysis.relationshipType.rawValue) • \(analysis.confidenceLevel.rawValue)")
                    .font(.caption)
                    .foregroundColor(.white.opacity(0.9))
                
                Text("\(analysis.stats.totalMessages) messages over \(analysis.durationDays) days")
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.7))
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .foregroundColor(.white.opacity(0.6))
        }
        .padding()
        .background(Color.white.opacity(0.2))
        .cornerRadius(15)
    }
}

// Color extension for hex colors
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
