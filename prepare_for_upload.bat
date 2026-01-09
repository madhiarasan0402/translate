@echo off
echo ============================================
echo   Preparing Files for GitHub Upload
echo ============================================
echo.

REM Create a clean directory for upload
set UPLOAD_DIR=translate_upload
if exist %UPLOAD_DIR% rmdir /s /q %UPLOAD_DIR%
mkdir %UPLOAD_DIR%

echo Copying files to %UPLOAD_DIR%...
echo.

REM Copy all Python files
xcopy /Y *.py %UPLOAD_DIR%\ >nul 2>&1
echo [OK] Copied Python files

REM Copy all markdown files
xcopy /Y *.md %UPLOAD_DIR%\ >nul 2>&1
echo [OK] Copied documentation files

REM Copy configuration files
xcopy /Y *.txt %UPLOAD_DIR%\ >nul 2>&1
xcopy /Y *.yaml %UPLOAD_DIR%\ >nul 2>&1
xcopy /Y *.yml %UPLOAD_DIR%\ >nul 2>&1
xcopy /Y Procfile %UPLOAD_DIR%\ >nul 2>&1
xcopy /Y .env.example %UPLOAD_DIR%\ >nul 2>&1
xcopy /Y .gitignore %UPLOAD_DIR%\ >nul 2>&1
xcopy /Y *.sh %UPLOAD_DIR%\ >nul 2>&1
xcopy /Y *.bat %UPLOAD_DIR%\ >nul 2>&1
echo [OK] Copied configuration files

REM Copy directories
xcopy /E /I /Y app %UPLOAD_DIR%\app >nul 2>&1
xcopy /E /I /Y static %UPLOAD_DIR%\static >nul 2>&1
xcopy /E /I /Y templates %UPLOAD_DIR%\templates >nul 2>&1
echo [OK] Copied app, static, and templates folders

REM Clean up __pycache__ from copied files
for /d /r %UPLOAD_DIR% %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo [OK] Cleaned up cache files

echo.
echo ============================================
echo   Files Ready for Upload!
echo ============================================
echo.
echo Your files are in the '%UPLOAD_DIR%' folder
echo.
echo Next steps:
echo 1. Open File Explorer
echo 2. Go to: %CD%\%UPLOAD_DIR%
echo 3. Select ALL files and folders
echo 4. Go to: https://github.com/madihaaraan0402/translate
echo 5. Click "uploading an existing file"
echo 6. Drag and drop all files
echo 7. Commit changes
echo.
echo Opening the folder now...
explorer %UPLOAD_DIR%
echo.
pause
