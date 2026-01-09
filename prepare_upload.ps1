# PowerShell script to prepare files for GitHub upload

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Preparing Files for GitHub Upload" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$uploadDir = "translate_upload"

# Remove old upload directory if exists
if (Test-Path $uploadDir) {
    Remove-Item -Recurse -Force $uploadDir
    Write-Host "[OK] Cleaned old upload folder" -ForegroundColor Green
}

# Create new upload directory
New-Item -ItemType Directory -Path $uploadDir | Out-Null
Write-Host "[OK] Created upload folder" -ForegroundColor Green

# Files to exclude
$excludePatterns = @(
    "*.log",
    "error_log.txt",
    "translate_upload",
    "downloads",
    "__pycache__",
    ".env"
)

# Copy all files except excluded ones
Write-Host ""
Write-Host "Copying files..." -ForegroundColor Yellow

# Copy Python files
Get-ChildItem -Path "." -Filter "*.py" | Copy-Item -Destination $uploadDir
Write-Host "[OK] Copied Python files" -ForegroundColor Green

# Copy Markdown files
Get-ChildItem -Path "." -Filter "*.md" | Copy-Item -Destination $uploadDir
Write-Host "[OK] Copied documentation files" -ForegroundColor Green

# Copy text files
Get-ChildItem -Path "." -Filter "*.txt" | Where-Object { $_.Name -ne "error_log.txt" } | Copy-Item -Destination $uploadDir
Write-Host "[OK] Copied text files" -ForegroundColor Green

# Copy configuration files
Copy-Item -Path "requirements.txt" -Destination $uploadDir -ErrorAction SilentlyContinue
Copy-Item -Path "render.yaml" -Destination $uploadDir -ErrorAction SilentlyContinue
Copy-Item -Path "Procfile" -Destination $uploadDir -ErrorAction SilentlyContinue
Copy-Item -Path ".env.example" -Destination $uploadDir -ErrorAction SilentlyContinue
Copy-Item -Path ".gitignore" -Destination $uploadDir -ErrorAction SilentlyContinue
Copy-Item -Path "build.sh" -Destination $uploadDir -ErrorAction SilentlyContinue
Copy-Item -Path "*.bat" -Destination $uploadDir -ErrorAction SilentlyContinue
Write-Host "[OK] Copied configuration files" -ForegroundColor Green

# Copy directories
Copy-Item -Path "app" -Destination $uploadDir -Recurse -Force
Copy-Item -Path "static" -Destination $uploadDir -Recurse -Force
Copy-Item -Path "templates" -Destination $uploadDir -Recurse -Force
Write-Host "[OK] Copied app, static, and templates folders" -ForegroundColor Green

# Remove __pycache__ directories
Get-ChildItem -Path $uploadDir -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Write-Host "[OK] Cleaned up cache files" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Files Ready for Upload!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your files are in the '$uploadDir' folder" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Open File Explorer (opening now...)" -ForegroundColor White
Write-Host "2. Go to the '$uploadDir' folder" -ForegroundColor White
Write-Host "3. Select ALL files and folders (Ctrl+A)" -ForegroundColor White
Write-Host "4. Go to: https://github.com/madihaaraan0402/translate" -ForegroundColor White
Write-Host "5. Click 'uploading an existing file'" -ForegroundColor White
Write-Host "6. Drag and drop all files" -ForegroundColor White
Write-Host "7. Add commit message: 'Initial commit'" -ForegroundColor White
Write-Host "8. Click 'Commit changes'" -ForegroundColor White
Write-Host ""

# Open the folder in Explorer
Start-Process explorer.exe -ArgumentList (Get-Location).Path\$uploadDir

Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
