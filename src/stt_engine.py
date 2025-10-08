try:
    import whisper
except ImportError:
    try:
        from openai import whisper
    except ImportError:
        print("❌ Neither 'whisper' nor 'openai-whisper' is installed!")
        print("Please install: pip install openai-whisper")
        raise
import config
import numpy as np
import os
import tempfile
import soundfile as sf

class STTEngine:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        print("STT Engine initialized. Model will be loaded on first use.")

    def _load_model(self):
        """بارگذاری مدل Whisper (فقط یک بار)"""
        if self.model_loaded:
            return
            
        try:
            print("Loading Whisper model...")
            # مدل به صورت خودکار دانلود می‌شود اگر موجود نباشد
            self.model = whisper.load_model(config.WHISPER_MODEL)
            self.model_loaded = True
            print(f"Whisper model '{config.WHISPER_MODEL}' loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise

    def transcribe(self, audio_data):
        """
        تبدیل داده‌های صوتی (numpy array) به متن فارسی
        """
        if audio_data is None or len(audio_data) == 0:
            return ""
            
        # بارگذاری مدل در صورت نیاز
        if not self.model_loaded:
            self._load_model()
        
        try:
            # نرمال‌سازی داده‌های صوتی
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # نرمال‌سازی دامنه صدا
            if np.max(np.abs(audio_data)) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # تشخیص گفتار با Whisper
            result = self.model.transcribe(
                audio_data, 
                language="fa",  # زبان فارسی
                fp16=False,    # سازگاری با CPU
                verbose=False   # کاهش خروجی
            )
            
            text = result["text"].strip()
            
            # پاک‌سازی متن
            if text:
                print(f"Transcribed: {text}")
                return text
            else:
                return ""
                
        except Exception as e:
            print(f"Error in transcription: {e}")
            return ""

    def transcribe_file(self, file_path):
        """
        تبدیل فایل صوتی به متن
        """
        try:
            if not self.model_loaded:
                self._load_model()
                
            result = self.model.transcribe(file_path, language="fa", fp16=False)
            return result["text"].strip()
            
        except Exception as e:
            print(f"Error transcribing file {file_path}: {e}")
            return ""

    def get_model_info(self):
        """دریافت اطلاعات مدل"""
        if not self.model_loaded:
            return "Model not loaded"
        
        return {
            "model_name": config.WHISPER_MODEL,
            "language": "Persian (fa)",
            "device": "CPU" if not config.TTS_USE_GPU else "GPU"
        }