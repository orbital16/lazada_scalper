#!/bin/bash
# Deploy Lazada Stock Monitor to GitHub and Streamlit Cloud

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     🚀 DEPLOY LAZADA STOCK MONITOR TO STREAMLIT          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Create GitHub Repository
echo "📦 STEP 1: Create GitHub Repository"
echo "──────────────────────────────────────────────────────────"
echo ""
echo "Opening GitHub in your browser..."
sleep 1

# Try to open browser
if command -v open &> /dev/null; then
    open "https://github.com/organizations/orbital16/repositories/new" 2>/dev/null || open "https://github.com/new"
else
    echo "Please open: https://github.com/new"
fi

echo ""
echo "⚠️  IMPORTANT: Use these settings:"
echo "  ┌─────────────────────────────────────────────────────┐"
echo "  │ Owner: orbital16                                    │"
echo "  │ Repository name: lazada-stock-monitor              │"
echo "  │ Description: Real-time stock monitoring with UI    │"
echo "  │ Privacy: ⚠️  PRIVATE (contains trading logic)       │"
echo "  │ Initialize: ❌ DO NOT check any boxes              │"
echo "  └─────────────────────────────────────────────────────┘"
echo ""
echo "After creating the repository, press ENTER to continue..."
read

# Step 2: Push to GitHub
echo ""
echo "📤 STEP 2: Pushing Code to GitHub"
echo "──────────────────────────────────────────────────────────"
echo ""

git push -u origin main

if [ $? -ne 0 ]; then
    echo "❌ Push failed!"
    echo "   Please check:"
    echo "   1. Repository was created correctly"
    echo "   2. Repository name is: lazada-stock-monitor"
    echo "   3. Owner is: orbital16"
    exit 1
fi

echo ""
echo "✅ Code pushed successfully!"
echo ""

# Step 3: Deploy to Streamlit Cloud
echo "🌐 STEP 3: Deploy to Streamlit Cloud"
echo "──────────────────────────────────────────────────────────"
echo ""
echo "Opening Streamlit Cloud..."
sleep 1

if command -v open &> /dev/null; then
    open "https://share.streamlit.io/deploy"
fi

echo ""
echo "🎯 Use these deployment settings:"
echo "  ┌─────────────────────────────────────────────────────┐"
echo "  │ Repository: orbital16/lazada-stock-monitor         │"
echo "  │ Branch: main                                       │"
echo "  │ Main file path: stock_monitor_ui.py                │"
echo "  │ App URL: (choose your subdomain)                   │"
echo "  └─────────────────────────────────────────────────────┘"
echo ""
echo "⚠️  IMPORTANT NOTES:"
echo "  • Make sure repo is PUBLIC for Streamlit (or upgrade plan)"
echo "  • Streamlit free tier requires public repos"
echo "  • Remove cookie file before deploying (security)"
echo ""

# Step 4: Update .gitignore if needed
echo "🔒 STEP 4: Security Check"
echo "──────────────────────────────────────────────────────────"
echo ""

if [ -f "lazada_cookies.json" ]; then
    echo "⚠️  WARNING: Cookie file found!"
    echo "   Remove it before making repo public:"
    echo "   rm lazada_cookies.json"
    echo "   git add -u && git commit -m 'Remove cookies' && git push"
else
    echo "✅ No sensitive files detected"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    ✅ DEPLOYMENT GUIDE                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1️⃣  Verify GitHub repo:"
echo "   https://github.com/orbital16/lazada-stock-monitor"
echo ""
echo "2️⃣  Deploy on Streamlit Cloud:"
echo "   https://share.streamlit.io/deploy"
echo ""
echo "3️⃣  After deployment, your app will be at:"
echo "   https://your-app-name.streamlit.app"
echo ""
echo "4️⃣  Test the app:"
echo "   - Add a Lazada product URL"
echo "   - Start monitoring"
echo "   - Check activity log"
echo ""
echo "💡 TIP: For private repos on Streamlit, you need:"
echo "   - Streamlit Cloud Teams plan, or"
echo "   - Make repo public (remove sensitive data first)"
echo ""
echo "═══════════════════════════════════════════════════════════"
