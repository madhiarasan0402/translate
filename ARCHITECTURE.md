# Video Language Translator - Technical Architecture

## 1. Project Overview
The Video Language Translator is an end-to-end AI/ML application that accepts a YouTube video URL, extracts its audio, transcribes the speech, translates it into a target language, generates synthesized speech, and allows the user to download the result.

## 2. System Architecture

The system follows a typical 3-tier web architecture:

```mermaid
graph TD
    User[User / Browser] <-->|HTTP Requests| Frontend[Frontend UI]
    Frontend <-->|API Calls| Backend[Backend API (FastAPI)]
    Backend <-->|Store/Retrieve| DB[(MySQL Database)]
    Backend -->|Process| AL[Audio Logic (yt-dlp, ffmpeg)]
    Backend -->|Inference| AI[AI Models (Whisper, Translation, TTS)]
```

### 2.1 Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla).
- **Backend**: Python 3.10+ using **FastAPI** (for asynchronous task handling).
- **Database**: **MySQL** (Relational data storage).
- **AI/ML Models & Tools**:
    - **Audio Extraction**: `yt-dlp`
    - **Audio Processing**: `ffmpeg`
    - **Speech-to-Text (ASR)**: OpenAI `Whisper` (Local or API)
    - **Translation**: `deep-translator` (Google Translate wrapper) or HuggingFace `MarianMT`
    - **Text-to-Speech (TTS)**: `gTTS` (Google Text-to-Speech) or `edge-tts` (Microsoft Edge TTS - higher quality/free).

## 3. Detailed Component Design

### 3.1 Database Design (MySQL)
We will use a relational schema to track translation requests and cache results to avoid re-processing identical requests.

**Table: `translations`**
| Column | Type | Description |
|--------|------|-------------|
| `id` | INT (PK, Auto Inc) | Unique identifier |
| `video_url` | VARCHAR(255) | YouTube URL |
| `video_title` | VARCHAR(255) | Title of the video |
| `source_lang` | VARCHAR(10) | Detected source language code (e.g., 'en') |
| `target_lang` | VARCHAR(10) | Target language code (e.g., 'es') |
| `status` | ENUM | 'pending', 'processing', 'completed', 'failed' |
| `input_audio_path` | VARCHAR(255) | Path to extracted original audio |
| `output_audio_path` | VARCHAR(255) | Path to generated translated audio |
| `transcript_text` | LONGTEXT | Original transcript |
| `translated_text` | LONGTEXT | Translated text |
| `created_at` | DATETIME | Timestamp of request |

### 3.2 Backend Workflow (The Pipeline)
The backend orchestrates the long-running process asynchronously using background tasks.

1.  **Request Handling**: Endpoint `/api/translate` receives `url` and `target_lang`.
2.  **Validation**: Check if valid YouTube URL.
3.  **Check Cache**: Query DB for existing `video_url` AND `target_lang` with `status='completed'`. If found, return immediate result.
4.  **Audio Extraction**:
    *   Use `yt-dlp` to download audio stream as `.webm` or `.m4a`.
    *   Use `ffmpeg` to convert to `.wav` (16kHz mono) for optimal AI processing.
5.  **Transcription (ASR)**:
    *   Load `Whisper` model (e.g., `base` or `small`).
    *   Transcribe audio to text.
    *   *Optional*: Extract timestamps for subtitle generation.
6.  **Translation**:
    *   Take transcript segments.
    *   Pass through Translation engine (English -> Target).
    *   Store `translated_text`.
7.  **Speech Synthesis (TTS)**:
    *   Convert `translated_text` to audio using `TTS`.
    *   Save file to `/static/audio/`.
8.  **Finalize**:
    *   Update DB record status to 'completed'.
    *   Return download URL and text to Frontend.

### 3.3 Frontend Design
- **Input Section**: Form for URL link and Language Dropdown.
- **Status Indicator**: Progress bar or spinner while processing (Polling backend for status).
- **Result Section**:
    - Audio Player (HTML5 `<audio>`) for the result.
    - Text Area showing Original vs Translated text.
    - Download button.

## 4. Directory Structure

```
/video-translator-project
├── /app
│   ├── main.py              # FastAPI entry point
│   ├── database.py          # MySQL connection logic
│   ├── models.py            # SQLModel/SQLAlchemy definitions
│   ├── pipeline.py          # AI/ML logic (Download -> Transcribe -> Translate -> TTS)
│   └── /routers
│       └── translation.py   # API endpoints
├── /static
│   ├── /css
│   │   └── style.css
│   ├── /js
│   │   └── script.js
│   └── /audio               # Stored audio files
├── /templates
│   └── index.html           # Main UI
├── /downloads               # Temp folder for downloads
├── requirements.txt         # Python dependencies
└── README.md
```

## 5. Implementation Steps
1.  **Setup Environment**: Install Python, MySQL, FFmpeg.
2.  **Initialize DB**: Create database and tables.
3.  **Backend Core**: Setup FastAPI and DB connection.
4.  **ML Integration**: Implement separate functions for Download, Transcribe, Translate, TTS.
5.  **Frontend**: Build the UI to interact with the API.
6.  **Integration**: Connect the UI form to the Backend pipeline.
