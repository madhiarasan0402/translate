# Deployment Guide for Render

## Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)
- Your code pushed to a GitHub repository

## Step-by-Step Deployment

### 1. Prepare Your Repository
```bash
# Create .env file for local development (don't commit this!)
cp .env.example .env

# Initialize git if not already done
git init
git add .
git commit -m "Prepare for Render deployment"

# Push to GitHub
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### 2. Deploy to Render

#### Option A: Using render.yaml (Recommended)
1. Go to https://dashboard.render.com
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click "Apply" to create all services

#### Option B: Manual Setup
1. **Create PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Name: `video-translator-db`
   - Choose free tier
   - Click "Create Database"
   - Save the connection details

2. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** `video-translator`
     - **Environment:** `Python 3`
     - **Build Command:** `./build.sh`
     - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type:** Free

3. **Set Environment Variables:**
   Go to your web service → Environment tab and add:
   ```
   DB_TYPE=postgresql
   DATABASE_HOST=<from-render-postgres-internal-url>
   DATABASE_USER=<from-render-postgres>
   DATABASE_PASSWORD=<from-render-postgres>
   DATABASE_NAME=video_translator
   ENVIRONMENT=production
   ```

### 3. Initialize Database
After deployment, you need to create the database tables:

1. Go to your web service in Render
2. Click "Shell" tab
3. Run:
   ```bash
   python init_db.py
   ```

### 4. Access Your Application
Your app will be available at: `https://video-translator.onrender.com`
(or whatever name you chose)

## Important Notes

### Free Tier Limitations
- **Spin down after inactivity:** Free services sleep after 15 minutes of inactivity
- **Cold starts:** First request after sleep takes 30-60 seconds
- **Storage:** Ephemeral - files are deleted on each deploy
- **Database:** 90-day expiration on free tier

### Handling Large Files
Since Render uses ephemeral storage:
- Downloaded videos are temporary
- Consider using cloud storage (AWS S3, Cloudinary) for persistent storage
- Or process and delete files immediately

### FFmpeg
FFmpeg is installed via `build.sh` script during deployment.

### Whisper Models
The Whisper model will be downloaded on first use. This may cause:
- Longer first request time
- Higher memory usage
- Consider pre-downloading in build.sh (commented out)

## Troubleshooting

### Build Fails
- Check `build.sh` has execute permissions: `chmod +x build.sh`
- Review build logs in Render dashboard
- Ensure all dependencies in `requirements.txt` are correct

### Database Connection Issues
- Verify environment variables are set correctly
- Use internal database URL (not external)
- Check database is in same region as web service

### Application Crashes
- Check logs in Render dashboard
- Verify FFmpeg is installed
- Check memory usage (free tier has 512MB limit)

### Slow Performance
- First request after sleep is slow (cold start)
- Consider upgrading to paid tier for always-on service
- Optimize Whisper model size (use 'tiny' or 'base' instead of 'large')

## Monitoring
- View logs: Render Dashboard → Your Service → Logs
- Health check: `https://your-app.onrender.com/api/health`
- Monitor metrics in Render dashboard

## Updating Your App
```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main
```
Render will automatically redeploy on push (if auto-deploy is enabled).

## Cost Optimization
- Use smaller Whisper models ('tiny', 'base')
- Clean up downloaded files immediately
- Consider caching translated videos
- Upgrade to paid tier if you need:
  - No cold starts
  - More memory/CPU
  - Persistent storage
  - Custom domains

## Security Recommendations
1. Never commit `.env` file
2. Use Render's environment variables for secrets
3. Set up proper CORS origins in production
4. Consider rate limiting for API endpoints
5. Add authentication if needed

## Support
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
