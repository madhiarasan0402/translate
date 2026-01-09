# Video Language Translator (AIML)

A full-stack AI/ML application that automatically translates the spoken content of YouTube videos into a target language.

## Key Features
- **YouTube Audio Extraction**: Downloads audio directly from YouTube links.
- **Speech-to-Text**: Uses OpenAI's Whisper model for accurate transcription.
- **Translation**: Translates text into supported languages.
- **Text-to-Speech**: Generates natural-sounding audio in the target language using Edge-TTS.
- **Database History**: Stores all translations in MySQL/PostgreSQL for easy retrieval.
- **Voice Selection**: Choose from multiple AI voices for translation output.

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- MySQL Server (for local development)
- FFmpeg (must be in system PATH)

### Installation

#### Windows
```bash
# Run the setup script
setup.bat

# Or manually:
# 1. Create .env file
copy .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python init_db.py

# 4. Start the server
python app/main.py
```

#### Linux/Mac
```bash
# 1. Create .env file
cp .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python init_db.py

# 4. Start the server
python app/main.py
```

### Configuration
Edit the `.env` file with your database credentials:
```env
DB_TYPE=mysql
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=video_translator
PORT=8001
```

### Access the Application
Open your browser and navigate to: `http://localhost:8001`

## Deployment to Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions.

### Quick Deploy
1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Render will auto-detect `render.yaml` and deploy
4. Set environment variables in Render dashboard
5. Initialize database using Render shell

## Project Structure
```
translate/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database connection
│   ├── pipeline.py       # Translation pipeline
│   └── routers/
│       └── translation.py # API routes
├── static/               # Frontend assets
├── templates/            # HTML templates
├── downloads/            # Temporary video storage
├── requirements.txt      # Python dependencies
├── render.yaml          # Render deployment config
├── build.sh             # Render build script
├── .env.example         # Environment template
└── DEPLOYMENT.md        # Deployment guide

```

## API Endpoints
- `GET /` - Main application interface
- `GET /api/health` - Health check endpoint
- `POST /api/translate` - Video translation endpoint
- `GET /api/history` - Translation history

## Technologies Used
- **Backend**: FastAPI, Python
- **AI/ML**: OpenAI Whisper, Edge-TTS
- **Database**: MySQL (local), PostgreSQL (production)
- **Video Processing**: yt-dlp, MoviePy, FFmpeg
- **Translation**: Deep Translator
- **Deployment**: Render

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment mode | `development` |
| `DB_TYPE` | Database type (mysql/postgresql) | `mysql` |
| `DATABASE_HOST` | Database host | `localhost` |
| `DATABASE_USER` | Database user | `root` |
| `DATABASE_PASSWORD` | Database password | `` |
| `DATABASE_NAME` | Database name | `video_translator` |
| `PORT` | Server port | `8001` |

## Troubleshooting

### FFmpeg not found
- **Windows**: Download from https://ffmpeg.org and add to PATH
- **Linux**: `sudo apt-get install ffmpeg`
- **Mac**: `brew install ffmpeg`

### Database connection failed
- Ensure MySQL/PostgreSQL is running
- Check credentials in `.env` file
- Verify database exists: `CREATE DATABASE video_translator;`

### Module not found errors
```bash
pip install -r requirements.txt
```

### Port already in use
Change the `PORT` in `.env` file to a different port.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License

## Support
For deployment help, see [DEPLOYMENT.md](DEPLOYMENT.md)

For technical details, see [ARCHITECTURE.md](ARCHITECTURE.md)
