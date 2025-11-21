#!/bin/bash

# GitHub Repository Setup Script
# This script helps you push your WhatsApp Friendship Analyzer to GitHub

echo "🚀 WhatsApp Friendship Analyzer - GitHub Setup"
echo "=============================================="
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI detected!"
    echo ""
    read -p "Would you like to create a new repo using GitHub CLI? (y/n): " use_gh_cli
    
    if [ "$use_gh_cli" = "y" ]; then
        echo ""
        read -p "Enter repository name (default: whatsapp-friendship-analyzer): " repo_name
        repo_name=${repo_name:-whatsapp-friendship-analyzer}
        
        read -p "Make repository public? (y/n, default: n): " is_public
        visibility="private"
        if [ "$is_public" = "y" ]; then
            visibility="public"
        fi
        
        echo ""
        echo "Creating $visibility repository: $repo_name"
        gh repo create "$repo_name" --$visibility --source=. --remote=origin --push
        
        echo ""
        echo "✅ Repository created and pushed!"
        echo "🌐 View at: https://github.com/$(gh api user -q .login)/$repo_name"
    fi
else
    echo "❌ GitHub CLI not found. Manual setup required."
    echo ""
    echo "📝 Manual Setup Instructions:"
    echo "=============================================="
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository (suggested name: whatsapp-friendship-analyzer)"
    echo "3. DO NOT initialize with README, .gitignore, or license"
    echo "4. After creating, run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "Replace YOUR_USERNAME and REPO_NAME with your actual values"
    echo ""
    echo "=============================================="
    echo ""
    read -p "Press Enter to open GitHub in your browser..."
    open "https://github.com/new"
fi

echo ""
echo "📚 Don't forget to:"
echo "  - Update README.md with your GitHub username"
echo "  - Add a description and topics to your repo"
echo "  - Star ⭐ the repository if you like it!"
echo ""
