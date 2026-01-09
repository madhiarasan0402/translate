import os
import time
import uuid
import asyncio
import subprocess
import yt_dlp
import whisper
from deep_translator import GoogleTranslator
from typing import Optional
import edge_tts
import torch
import scipy.io.wavfile as wavfile
from transformers import AutoProcessor, BarkModel

# Paths
# Paths
if os.name == 'nt':
    ffmpeg_dir = r'C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin'
    if ffmpeg_dir not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + ffmpeg_dir
    ffmpeg_cmd = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
    ffprobe_cmd = os.path.join(ffmpeg_dir, 'ffprobe.exe')
else:
    ffmpeg_cmd = 'ffmpeg'
    ffprobe_cmd = 'ffprobe'

# Model Cache
_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        print(f"[{time.strftime('%H:%M:%S')}] Loading Whisper tiny model... This might take a minute the first time.", flush=True)
        _whisper_model = whisper.load_model("tiny")
        print(f"[{time.strftime('%H:%M:%S')}] Whisper model loaded.", flush=True)
    return _whisper_model

# Model Cache for Bark
_bark_model = None
_bark_processor = None

def get_bark_model():
    global _bark_model, _bark_processor
    if _bark_model is None:
        print(f"[{time.strftime('%H:%M:%S')}] Loading Bark model (small)... This may take a while.", flush=True)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _bark_processor = AutoProcessor.from_pretrained("suno/bark-small")
        _bark_model = BarkModel.from_pretrained("suno/bark-small").to(device)
        print(f"[{time.strftime('%H:%M:%S')}] Bark model loaded.", flush=True)
    return _bark_model, _bark_processor

async def text_to_speech_bark(text: str, voice_preset: str, output_dir: str = "static/audio"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f"{uuid.uuid4()}.wav"
    output_path = os.path.join(output_dir, filename)
    
    model, processor = get_bark_model()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Bark works best with short phrases, but we'll try it on the segment
    inputs = processor(text, voice_preset=voice_preset).to(device)
    
    with torch.no_grad():
        audio_array = model.generate(**inputs)
        audio_array = audio_array.cpu().numpy().squeeze()
    
    sample_rate = model.generation_config.sample_rate
    wavfile.write(output_path, rate=sample_rate, data=audio_array)
    
    return output_path

def download_video_and_audio(youtube_url: str, output_dir: str = "downloads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    unique_id = uuid.uuid4()
    video_path = os.path.join(output_dir, f"{unique_id}_video.mp4")
    audio_path = os.path.join(output_dir, f"{unique_id}_audio.mp3")
    
    print(f"[{time.strftime('%H:%M:%S')}] Target Video URL: {youtube_url}", flush=True)
    
    # Standard format selection
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': video_path,
        'quiet': False,
        'no_warnings': False,
        'noplaylist': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"[{time.strftime('%H:%M:%S')}] Starting download with yt-dlp for: {youtube_url}", flush=True)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] yt-dlp error: {e}", flush=True)
        raise e
    
    if not os.path.exists(video_path):
        print(f"[{time.strftime('%H:%M:%S')}] ERROR: Video file not found at {video_path}", flush=True)
        raise Exception("Download failed: Video file not created.")
        
    print(f"[{time.strftime('%H:%M:%S')}] Download successful. Extracting audio...", flush=True)
    
    # Extract audio for transcription
    cmd = [
        ffmpeg_cmd,
        '-y', '-i', video_path,
        '-vn', '-acodec', 'libmp3lame', '-ar', '16000',
        audio_path
    ]
    # No capture_output so we see errors/progress in terminal
    subprocess.run(cmd, check=True)
    
    return video_path, audio_path

def transcribe_audio(audio_path: str):
    print(f"[{time.strftime('%H:%M:%S')}] Starting transcription...", flush=True)
    model = get_whisper_model()
    # Task 'transcribe' returns segments with timestamps
    result = model.transcribe(audio_path, fp16=False)
    print(f"[{time.strftime('%H:%M:%S')}] Transcription complete.", flush=True)
    return result

def translate_text(text: str, target_lang: str):
    if not text.strip():
        return "No speech detected."
    
    print(f"[{time.strftime('%H:%M:%S')}] Translating text...", flush=True)
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(text)
        print(f"[{time.strftime('%H:%M:%S')}] Translation complete.", flush=True)
        return translated
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Translation error: {e}", flush=True)
        return text # Fallback to original

async def text_to_speech_edge(text: str, lang: str, gender: str = "female", output_dir: str = "static/audio"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(output_dir, filename)
    
    print(f"[{time.strftime('%H:%M:%S')}] Generating TTS voice...", flush=True)
    
    voices_map = {
        'hi': {'male': 'hi-IN-MadhurNeural', 'female': 'hi-IN-SwaraNeural'},
        'ta': {'male': 'ta-IN-ValluvarNeural', 'female': 'ta-IN-PallaviNeural'},
        'ml': {'male': 'ml-IN-MidhunNeural', 'female': 'ml-IN-SobhanaNeural'},
        'es': {'male': 'es-MX-JorgeNeural', 'female': 'es-MX-DaliaNeural'},
        'fr': {'male': 'fr-FR-HenriNeural', 'female': 'fr-FR-DeniseNeural'},
        'de': {'male': 'de-DE-KillianNeural', 'female': 'de-DE-KatjaNeural'},
        'ja': {'male': 'ja-JP-KeitaNeural', 'female': 'ja-JP-NanamiNeural'},
        'en': {'male': 'en-US-AndrewNeural', 'female': 'en-US-EmmaNeural'}
    }
    
    lang_key = lang.lower()[:2]
    lang_voices = voices_map.get(lang_key, voices_map['en'])
    
    # If a specific voice name is provided, use it directly
    if str(gender).startswith('en-') or str(gender).startswith('hi-') or str(gender).startswith('ta-') or str(gender).startswith('ml-'):
        voice = gender
    else:
        voice = lang_voices.get(gender.lower(), lang_voices['female'])
    
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"[{time.strftime('%H:%M:%S')}] TTS complete.", flush=True)
    return output_path

def get_audio_duration(file_path):
    cmd = [
        ffprobe_cmd,
        '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

async def mix_audio_and_video_segmented(video_path, original_audio, segments, target_lang, voice_id, output_dir="static/video"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    temp_dir = os.path.join("downloads", "temp_segments")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    output_filename = f"translated_{uuid.uuid4()}.mp4"
    output_video_path = os.path.join(output_dir, output_filename)
    
    audio_filters = []
    input_files = [video_path, original_audio]
    
    print(f"[{time.strftime('%H:%M:%S')}] Generating segmented TTS and processing speed...", flush=True)
    
    processed_segments = 0
    for i, seg in enumerate(segments):
        start = seg['start']
        end = seg['end']
        duration = end - start
        text = seg['text'].strip()
        
        if not text:
            continue
            
        translated_text = translate_text(text, target_lang)
        
        if str(voice_id).startswith("hf_"):
            # voice_id format: hf_bark_en_speaker_0 -> v2/en_speaker_0
            preset = voice_id.replace("hf_bark_", "v2/")
            seg_audio_path = await text_to_speech_bark(translated_text, preset, output_dir=temp_dir)
        else:
            seg_audio_path = await text_to_speech_edge(translated_text, target_lang, voice_id, output_dir=temp_dir)
        
        # Add a small delay to prevent "connection failed" errors from rapid requests
        await asyncio.sleep(0.5)
        
        tts_duration = get_audio_duration(seg_audio_path)
        
        # Calculate speed factor if TTS is longer than original duration
        # We cap speed at 2.0x to keep it somewhat intelligible
        speed_factor = 1.0
        if tts_duration > duration and duration > 0:
            speed_factor = min(tts_duration / duration, 2.0)
        
        # Add to FFmpeg inputs
        input_files.append(seg_audio_path)
        input_idx = len(input_files) - 1
        
        # Prepare filter for this segment: speed up, boost volume, then delay
        delay_ms = int(start * 1000)
        # We boost volume by 3.0x to ensure it's very audible
        if speed_factor != 1.0:
            # atempo filter for speed without changing pitch
            filter_str = f"[{input_idx}:a]atempo={speed_factor},volume=3.0,adelay={delay_ms}|{delay_ms}[a{i}]"
        else:
            filter_str = f"[{input_idx}:a]volume=3.0,adelay={delay_ms}|{delay_ms}[a{i}]"
        
        audio_filters.append(filter_str)
        processed_segments += 1

    if processed_segments == 0:
        # Fallback to simple mixing if no segments were processed
        return mix_audio_and_video(video_path, original_audio, original_audio, output_dir)

    # Combine all segments and original audio (at lower volume)
    # [1:a] is original audio
    mix_inputs = "".join([f"[a{i}]" for i in range(len(segments))])
    # Ensure we only include indices that were actually added to audio_filters
    valid_indices = [i for i, seg in enumerate(segments) if seg['text'].strip()]
    mix_inputs = "".join([f"[a{i}]" for i in valid_indices])
    
    amix_filter = f"[1:a]volume=0.1[bg_low];{';'.join(audio_filters)};[bg_low]{mix_inputs}amix=inputs={processed_segments + 1}:duration=first,volume=2.0[outa]"
    
    cmd = [ffmpeg_cmd, '-y']
    for f in input_files:
        cmd.extend(['-i', f])
        
    cmd.extend([
        '-filter_complex', amix_filter,
        '-map', '0:v',
        '-map', '[outa]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        output_video_path
    ])
    
    subprocess.run(cmd, check=True)
    
    # Cleanup temp segments
    for f in input_files[2:]:
        try: os.remove(f)
        except: pass
        
    print(f"[{time.strftime('%H:%M:%S')}] Segmented mixing complete.", flush=True)
    return f"/static/video/{output_filename}"

def mix_audio_and_video(video_path, original_audio, translated_audio, output_dir="static/video"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_filename = f"translated_{uuid.uuid4()}.mp4"
    output_video_path = os.path.join(output_dir, output_filename)
    
    cmd = [
        ffmpeg_cmd,
        '-y',
        '-i', video_path, 
        '-i', original_audio, 
        '-i', translated_audio, 
        '-filter_complex', 
        "[1:a]volume=0.1[a1];[2:a]volume=2.5[a2];[a1][a2]amix=inputs=2:duration=first[outa]", 
        '-map', '0:v', 
        '-map', '[outa]', 
        '-c:v', 'copy', 
        '-c:a', 'aac', 
        '-shortest',
        output_video_path
    ]
    subprocess.run(cmd, check=True)
    return f"/static/video/{output_filename}"

async def run_pipeline(youtube_url: str, target_lang: str, voice_id: str = "female", input_file: Optional[str] = None):
    pipeline_start = time.time()
    def log_progress(msg):
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] {msg}", flush=True)
        with open("pipeline_progress.log", "a") as f:
            f.write(f"[{timestamp}] {msg}\n")
    
    # Clear previous log
    with open("pipeline_progress.log", "w") as f:
        f.write(f"--- Pipeline Started at {time.ctime()} ---\n")

    log_progress(f"PIPELINE STARTED for {youtube_url or input_file}")
    
    # 1. Download or Prep
    if input_file:
        log_progress(f"Using uploaded file: {input_file}")
        video_file = input_file
        unique_id = uuid.uuid4()
        audio_file = os.path.join("downloads", f"{unique_id}_audio.mp3")
        cmd = [
            ffmpeg_cmd,
            '-y', '-i', video_file,
            '-vn', '-acodec', 'libmp3lame', '-ar', '16000',
            audio_file
        ]
        subprocess.run(cmd, check=True)
    else:
        log_progress("Downloading video and audio...")
        video_file, audio_file = download_video_and_audio(youtube_url)
    
    # 2. Transcribe
    log_progress("Transcribing audio with Whisper...")
    transcription_result = transcribe_audio(audio_file)
    original_text = transcription_result['text']
    source_lang = transcription_result['language']
    segments = transcription_result['segments']
    log_progress(f"Transcription complete ({len(segments)} segments)")
    
    # 3. Translate the full text for UI display
    log_progress("Translating text...")
    translated_text = translate_text(original_text, target_lang)
    
    # 4 & 5. TTS and Mix (Segmented)
    log_progress("Starting segmented TTS and mixing...")
    video_url = await mix_audio_and_video_segmented(
        video_file, audio_file, segments, target_lang, voice_id
    )
    log_progress(f"Mixing complete. Output: {video_url}")
    
    # Cleanup
    print(f"[{time.strftime('%H:%M:%S')}] Starting cleanup...", flush=True)
    try:
        time.sleep(1)
        if not input_file and os.path.exists(video_file): os.remove(video_file)
        if os.path.exists(audio_file): os.remove(audio_file)
        print(f"[{time.strftime('%H:%M:%S')}] Cleanup complete.", flush=True)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Cleanup warning: {e}", flush=True)
        
    print(f"[{time.strftime('%H:%M:%S')}] PIPELINE COMPLETE in {time.time() - pipeline_start:.2f}s", flush=True)
    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "output_video_url": video_url,
        "source_lang": source_lang
    }
