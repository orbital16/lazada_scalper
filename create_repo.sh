#!/bin/bash
# Create GitHub repository via API

echo "Creating repository: orbital16/lazada-stock-monitor"

# Create repo (you'll need to provide GitHub token)
# Using SSH to create via web is safer

# For now, let's use the GitHub web interface approach
echo ""
echo "Opening GitHub to create repository..."
open "https://github.com/new" 2>/dev/null || echo "Please open: https://github.com/new"

echo ""
echo "Please create the repository with these settings:"
echo "  - Repository name: lazada-stock-monitor"
echo "  - Description: Real-time Lazada stock monitoring with UI"
echo "  - Privacy: PRIVATE ⚠️ IMPORTANT"
echo "  - DO NOT initialize with README"
echo ""
echo "After creating, press ENTER to push..."
read

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "🔗 Repository: https://github.com/orbital16/lazada-stock-monitor"
    echo ""
    echo "Next: Deploy to Streamlit Cloud"
    echo "1. Go to: https://share.streamlit.io/deploy"
    echo "2. Repository: orbital16/lazada-stock-monitor"
    echo "3. Branch: main"
    echo "4. Main file: stock_monitor_ui.py"
else
    echo "❌ Push failed. Check SSH key and repository exists."
fi
