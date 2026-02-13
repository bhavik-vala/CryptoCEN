@echo off
REM LinkedIn Automation - Quick Setup (Windows)
REM This script sets everything up with one click

echo.
echo ╔════════════════════════════════════════════════╗
echo ║  LinkedIn Automation - One-Click Setup         ║
echo ║  For: Arab Global Crypto Exchange              ║
echo ╚════════════════════════════════════════════════╝
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop is not installed!
    echo.
    echo Please download and install Docker Desktop from:
    echo   https://docker.com/products/docker-desktop
    echo.
    echo After installation, run this script again.
    pause
    exit /b 1
)

echo ✓ Docker found!
echo.
echo Starting your LinkedIn Automation system...
echo.

REM Build and start containers
docker-compose up -d

REM Wait for service to start
echo Waiting for dashboard to start (this takes 30 seconds)...
timeout /t 30 /nobreak

REM Check if service is running
docker-compose ps | find "Up" >nul
if errorlevel 1 (
    echo.
    echo ❌ Something went wrong. Checking logs...
    docker-compose logs
    pause
    exit /b 1
)

REM Open browser
echo.
echo ╔════════════════════════════════════════════════╗
echo ║  ✓ System is running!                          ║
echo ║  Opening dashboard in 3 seconds...              ║
echo ╚════════════════════════════════════════════════╝
echo.

start http://localhost:5000
timeout /t 3 /nobreak

echo.
echo NEXT STEPS:
echo ───────────────────────────────────────────────────
echo 1. Dashboard should open in your browser
echo    (If not, go to: http://localhost:5000)
echo.
echo 2. Go to the "Setup" tab
echo.
echo 3. Add your credentials:
echo    - API Provider key (Google/Anthropic/OpenAI)
echo    - LinkedIn Access Token
echo    - Your LinkedIn ID
echo.
echo 4. Click "Test API Connection" & "Test LinkedIn Connection"
echo.
echo 5. Go to "Schedule" tab:
echo    - Set posting time (e.g., 11:00 AM)
echo    - UNCHECK "Test Mode" to enable live posting
echo.
echo 6. Go to "Generate Post" tab
echo    - Click "Generate Post Preview"
echo    - See your AI-generated post!
echo.
echo Need help getting credentials?
echo ───────────────────────────────────────────────────
echo • Google Gemini (Free):
echo   https://aistudio.google.com/app/apikeys
echo.
echo • LinkedIn Credentials:
echo   https://linkedin.com/developers/apps
echo.
echo To STOP the system:
echo   docker-compose down
echo.
pause
