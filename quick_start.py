#!/usr/bin/env python3
"""
Quick Start Script for WhatsApp Friendship Analyzer

This script helps you get started quickly with analyzing your WhatsApp chats.
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse


def create_directory_structure():
    """Create necessary directory structure."""
    directories = [
        "data/raw",
        "data/processed", 
        "data/embeddings",
        "data/analysis",
        "models",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        "pandas", "numpy", "chromadb", "sentence-transformers", 
        "textblob", "emoji", "networkx", "plotly"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall them with: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True


def setup_environment():
    """Setup the environment and install dependencies."""
    print("🔧 Setting up environment...")
    
    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        
        # Determine activation script path based on OS
        if os.name == 'nt':  # Windows
            activate_script = "venv\\Scripts\\activate"
            pip_path = "venv\\Scripts\\pip"
        else:  # Unix/Linux/Mac
            activate_script = "venv/bin/activate"
            pip_path = "venv/bin/pip"
        
        print(f"Virtual environment created. Activate it with: source {activate_script}")
        
        # Install requirements
        if Path("requirements.txt").exists():
            print("Installing requirements...")
            subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    create_directory_structure()


def process_sample_data():
    """Process sample WhatsApp data if available."""
    raw_data_path = Path("data/raw")
    txt_files = list(raw_data_path.glob("*.txt"))
    
    if not txt_files:
        print("📱 No WhatsApp export files found in data/raw/")
        print("Please export your WhatsApp chats and place the .txt files in data/raw/")
        print("\nTo export WhatsApp chats:")
        print("1. Open WhatsApp on your phone")
        print("2. Go to a chat → Menu → More → Export chat")
        print("3. Choose 'Without Media' for faster processing")
        print("4. Save the .txt file to data/raw/")
        return False
    
    print(f"📊 Found {len(txt_files)} WhatsApp export files")
    
    # Run the parser
    print("🔄 Processing WhatsApp exports...")
    try:
        subprocess.run([
            sys.executable, 
            "src/parsers/whatsapp_parser.py",
            "--input", "data/raw",
            "--output", "data/processed"
        ], check=True)
        print("✅ Chat parsing complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error processing chats: {e}")
        return False


def generate_embeddings():
    """Generate embeddings for processed chat data."""
    processed_files = list(Path("data/processed").glob("*_processed.json"))
    
    if not processed_files:
        print("❌ No processed chat files found. Run processing first.")
        return False
    
    print("🧠 Generating embeddings for RAG system...")
    try:
        subprocess.run([
            sys.executable,
            "src/rag/embeddings.py", 
            "--data", "data/processed",
            "--output", "data/embeddings"
        ], check=True)
        print("✅ Embedding generation complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating embeddings: {e}")
        return False


def run_pattern_analysis():
    """Run friendship pattern analysis."""
    print("🔍 Analyzing friendship patterns...")
    try:
        subprocess.run([
            sys.executable,
            "src/analysis/friendship_patterns.py",
            "--data", "data/processed", 
            "--output", "data/analysis"
        ], check=True)
        print("✅ Pattern analysis complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in pattern analysis: {e}")
        return False


def start_agent():
    """Start the conversational agent."""
    print("🤖 Starting conversational agent...")
    try:
        subprocess.run([
            sys.executable,
            "src/agent/chat_agent.py"
        ])
    except KeyboardInterrupt:
        print("\n👋 Agent stopped by user")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")


def main():
    parser = argparse.ArgumentParser(description="WhatsApp Friendship Analyzer Quick Start")
    parser.add_argument("--setup", action="store_true", help="Setup environment and dependencies")
    parser.add_argument("--process", action="store_true", help="Process WhatsApp export files")
    parser.add_argument("--embeddings", action="store_true", help="Generate embeddings")
    parser.add_argument("--analyze", action="store_true", help="Run pattern analysis")
    parser.add_argument("--agent", action="store_true", help="Start conversational agent")
    parser.add_argument("--full", action="store_true", help="Run full pipeline")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        # Interactive mode
        print("🔮 WhatsApp Friendship Analyzer - Quick Start")
        print("=" * 50)
        print("This tool will help you analyze your WhatsApp friendship patterns using AI!")
        print()
        
        while True:
            print("What would you like to do?")
            print("1. 🔧 Setup environment and dependencies")
            print("2. 📱 Process WhatsApp export files")
            print("3. 🧠 Generate embeddings for RAG")
            print("4. 🔍 Analyze friendship patterns")
            print("5. 🤖 Start conversational agent")
            print("6. 🚀 Run complete pipeline")
            print("7. ❌ Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                setup_environment()
            elif choice == "2":
                if not check_dependencies():
                    continue
                process_sample_data()
            elif choice == "3":
                if not check_dependencies():
                    continue
                generate_embeddings()
            elif choice == "4":
                if not check_dependencies():
                    continue
                run_pattern_analysis()
            elif choice == "5":
                if not check_dependencies():
                    continue
                start_agent()
            elif choice == "6":
                if not check_dependencies():
                    print("Please install dependencies first (option 1)")
                    continue
                
                print("🚀 Running complete pipeline...")
                success = (
                    process_sample_data() and
                    generate_embeddings() and
                    run_pattern_analysis()
                )
                
                if success:
                    print("\n🎉 Pipeline complete! Starting agent...")
                    start_agent()
                else:
                    print("❌ Pipeline failed. Check the errors above.")
            elif choice == "7":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
            print("\n" + "=" * 50)
    
    else:
        # Command line mode
        if args.setup:
            setup_environment()
        
        if args.process:
            if check_dependencies():
                process_sample_data()
        
        if args.embeddings:
            if check_dependencies():
                generate_embeddings()
        
        if args.analyze:
            if check_dependencies():
                run_pattern_analysis()
        
        if args.agent:
            if check_dependencies():
                start_agent()
        
        if args.full:
            if check_dependencies():
                print("🚀 Running complete pipeline...")
                success = (
                    process_sample_data() and
                    generate_embeddings() and
                    run_pattern_analysis()
                )
                
                if success:
                    print("\n🎉 Pipeline complete! Starting agent...")
                    start_agent()


if __name__ == "__main__":
    main()