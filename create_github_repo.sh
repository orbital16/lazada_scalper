#!/bin/bash
# Create GitHub repository and push

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         📦 CREATE GITHUB REPOSITORY                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if we can use gh CLI
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI to create repository..."
    gh repo create orbital16/lazada-stock-monitor --private --description "Real-time Lazada stock monitoring with UI" --source=. --remote=origin --push

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Repository created and code pushed!"
        echo "🔗 https://github.com/orbital16/lazada-stock-monitor"
        exit 0
    fi
fi

# Fallback: Manual instructions
echo "⚠️  GitHub CLI not available. Manual steps required:"
echo ""
echo "1️⃣  Create repository on GitHub:"
echo "   https://github.com/new"
echo ""
echo "   Settings:"
echo "   • Owner: orbital16"
echo "   • Name: lazada-stock-monitor"
echo "   • Privacy: Private"
echo "   • DO NOT initialize with README"
echo ""
echo "2️⃣  Then run:"
echo "   git push -u origin main"
echo ""
echo "3️⃣  Repository will be at:"
echo "   https://github.com/orbital16/lazada-stock-monitor"
echo ""
