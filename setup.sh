#!/bin/bash
# LinkedIn Automation - Quick Setup (Mac/Linux)
# This script sets everything up with one click

clear
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║  LinkedIn Automation - One-Click Setup         ║"
echo "║  For: Arab Global Crypto Exchange              ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo ""
    echo "Please download and install Docker Desktop from:"
    echo "  https://docker.com/products/docker-desktop"
    echo ""
    echo "After installation, run this script again."
    exit 1
fi

echo "✓ Docker found!"
echo ""
echo "Starting your LinkedIn Automation system..."
echo ""

# Build and start containers
docker-compose up -d

# Wait for service to start
echo "Waiting for dashboard to start (this takes 30 seconds)..."
sleep 30

# Check if service is running
if ! docker-compose ps | grep -q "Up"; then
    echo ""
    echo "❌ Something went wrong. Checking logs..."
    docker-compose logs
    exit 1
fi

# Open browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:5000
fi

echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║  ✓ System is running!                          ║"
echo "║  Dashboard available at: http://localhost:5000 ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

echo ""
echo "NEXT STEPS:"
echo "───────────────────────────────────────────────────"
echo "1. Open browser and go to: http://localhost:5000"
echo ""
echo "2. Go to the 'Setup' tab"
echo ""
echo "3. Add your credentials:"
echo "   - API Provider key (Google/Anthropic/OpenAI)"
echo "   - LinkedIn Access Token"
echo "   - Your LinkedIn ID"
echo ""
echo "4. Click 'Test API Connection' & 'Test LinkedIn Connection'"
echo ""
echo "5. Go to 'Schedule' tab:"
echo "   - Set posting time (e.g., 11:00 AM)"
echo "   - UNCHECK 'Test Mode' to enable live posting"
echo ""
echo "6. Go to 'Generate Post' tab"
echo "   - Click 'Generate Post Preview'"
echo "   - See your AI-generated post!"
echo ""
echo "Need help getting credentials?"
echo "───────────────────────────────────────────────────"
echo "• Google Gemini (Free):"
echo "  https://aistudio.google.com/app/apikeys"
echo ""
echo "• LinkedIn Credentials:"
echo "  https://linkedin.com/developers/apps"
echo ""
echo "To STOP the system:"
echo "  docker-compose down"
echo ""
