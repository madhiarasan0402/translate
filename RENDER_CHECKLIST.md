# Render Deployment Checklist

## ✅ Files Created/Modified for Render

### New Files
- [x] `render.yaml` - Render Blueprint configuration
- [x] `build.sh` - Build script for installing FFmpeg and dependencies
- [x] `Procfile` - Alternative deployment configuration
- [x] `.env.example` - Environment variables template
- [x] `.gitignore` - Git ignore file
- [x] `DEPLOYMENT.md` - Complete deployment guide
- [x] `setup.bat` - Windows setup script for local development

### Modified Files
- [x] `requirements.txt` - Added production dependencies (gunicorn, python-dotenv, psycopg2-binary)
- [x] `app/main.py` - Added environment variable support, CORS, and production configuration
- [x] `app/database.py` - Added PostgreSQL support and environment variables
- [x] `init_db.py` - Added PostgreSQL support and environment variables
- [x] `README.md` - Updated with comprehensive setup and deployment instructions

## 🚀 Quick Deployment Steps

### 1. Local Setup (First Time)
```bash
# Create .env file
copy .env.example .env

# Edit .env with your local MySQL credentials

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Test locally
python app/main.py
```

### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Prepare for Render deployment"
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### 3. Deploy on Render
1. Go to https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click "Apply"

### 4. Configure Environment Variables
In Render Dashboard → Your Web Service → Environment:
```
DB_TYPE=postgresql
DATABASE_HOST=<internal-database-url>
DATABASE_USER=<from-render-db>
DATABASE_PASSWORD=<from-render-db>
DATABASE_NAME=video_translator
ENVIRONMENT=production
```

### 5. Initialize Database
In Render Dashboard → Your Web Service → Shell:
```bash
python init_db.py
```

## 🔍 What Changed?

### Database Support
- **Before**: MySQL only, hardcoded localhost
- **After**: Both MySQL (local) and PostgreSQL (Render) with environment variables

### Server Configuration
- **Before**: Bound to 127.0.0.1:8001
- **After**: Bound to 0.0.0.0 with configurable PORT

### Dependencies
- **Added**: gunicorn, python-dotenv, psycopg2-binary, uvicorn[standard]
- **Purpose**: Production server and database support

### Security
- **Added**: .gitignore to prevent committing sensitive files
- **Added**: .env.example as template
- **Changed**: All credentials now use environment variables

## ⚠️ Important Notes

### Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds (cold start)
- Ephemeral storage (files deleted on redeploy)
- PostgreSQL database expires after 90 days on free tier

### FFmpeg
- Automatically installed via `build.sh` on Render
- Must be manually installed for local development

### Whisper Models
- Downloaded on first use (may cause initial delay)
- Consider pre-downloading in `build.sh` for faster startup

### File Storage
- Downloads are temporary on Render (ephemeral storage)
- Consider using cloud storage (S3, Cloudinary) for production

## 🧪 Testing

### Local Testing
```bash
# Start server
python app/main.py

# Test health endpoint
curl http://localhost:8001/api/health

# Open in browser
http://localhost:8001
```

### Production Testing
```bash
# Test health endpoint
curl https://your-app.onrender.com/api/health

# Check logs
# Go to Render Dashboard → Your Service → Logs
```

## 📝 Next Steps

1. **Create .env file locally**
   ```bash
   copy .env.example .env
   # Edit with your MySQL credentials
   ```

2. **Test locally**
   ```bash
   python init_db.py
   python app/main.py
   ```

3. **Commit and push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

4. **Deploy on Render**
   - Follow steps in DEPLOYMENT.md

5. **Configure environment variables on Render**

6. **Initialize database on Render**

7. **Test your deployed application**

## 🆘 Troubleshooting

### Local Development
- **Database connection failed**: Check MySQL is running and credentials in `.env`
- **FFmpeg not found**: Install FFmpeg and add to PATH
- **Module not found**: Run `pip install -r requirements.txt`

### Render Deployment
- **Build failed**: Check `build.sh` syntax and logs
- **Database connection failed**: Verify environment variables
- **Application crashed**: Check logs in Render dashboard
- **Slow response**: Normal for first request after sleep (cold start)

## 📚 Documentation
- **Setup Guide**: README.md
- **Deployment Guide**: DEPLOYMENT.md
- **Architecture**: ARCHITECTURE.md

## ✨ Features Preserved
- YouTube video download
- Speech-to-text (Whisper)
- Translation
- Text-to-speech (Edge-TTS)
- Voice selection
- Database history
- Web interface

All existing functionality remains intact!
