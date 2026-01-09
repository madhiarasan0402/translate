@echo off
echo ============================================
echo   Git Installation Check and Setup
echo ============================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Visit: https://git-scm.com/download/win
    echo 2. Download and install
    echo 3. Restart this terminal
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

echo [OK] Git is installed!
git --version
echo.

REM Initialize Git repository
echo Initializing Git repository...
git init
echo.

REM Configure Git (if not already configured)
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo Please enter your name for Git commits:
    set /p username="Your Name: "
    git config --global user.name "%username%"
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo Please enter your email for Git commits:
    set /p useremail="Your Email: "
    git config --global user.email "%useremail%"
)

echo.
echo [OK] Git is configured!
echo Name: 
git config user.name
echo Email: 
git config user.email
echo.

REM Add all files
echo Adding files to Git...
git add .
echo.

REM Create initial commit
echo Creating initial commit...
git commit -m "Prepare for Render deployment"
echo.

echo ============================================
echo   SUCCESS! Git repository is ready!
echo ============================================
echo.
echo Next steps:
echo 1. Create a repository on GitHub.com
echo 2. Copy the repository URL
echo 3. Run: git remote add origin YOUR_REPO_URL
echo 4. Run: git push -u origin main
echo.
echo Or use GitHub Desktop for easier management:
echo https://desktop.github.com/
echo.
pause
