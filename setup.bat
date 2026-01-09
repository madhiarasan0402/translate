@echo off
echo Setting up environment for local development...

REM Create .env file from template
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created! Please update with your database credentials.
) else (
    echo .env file already exists.
)

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Update .env file with your database credentials
echo 2. Run: python init_db.py (to initialize database)
echo 3. Run: python app/main.py (to start the server)
echo.
pause
