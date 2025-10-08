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
import re

class STTEngine:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.tone_patterns = {
            'question': [
                r'آیا\s+.*\?',
                r'چرا\s+.*\?',
                r'چطور\s+.*\?',
                r'کجا\s+.*\?',
                r'کی\s+.*\?',
                r'چه\s+.*\?',
                r'مگه\s+.*\?',
                r'.*\?$'
            ],
            'exclamation': [
                r'وای\s+.*!',
                r'آه\s+.*!',
                r'اوه\s+.*!',
                r'.*!$'
            ],
            'command': [
                r'بکن\s+.*',
                r'کن\s+.*',
                r'برو\s+.*',
                r'بیا\s+.*',
                r'بده\s+.*',
                r'بگیر\s+.*'
            ]
        }
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

    def detect_tone_and_punctuation(self, text):
        """تشخیص لحن و اضافه کردن علامت‌گذاری مناسب"""
        if not text or not text.strip():
            return text
            
        text = text.strip()
        detected_tone = None
        
        # تشخیص لحن بر اساس الگوها
        for tone_type, patterns in self.tone_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected_tone = tone_type
                    break
            if detected_tone:
                break
        
        # اضافه کردن علامت‌گذاری بر اساس لحن تشخیص داده شده
        if detected_tone == 'question':
            if not text.endswith('؟') and not text.endswith('?'):
                text += '؟'
        elif detected_tone == 'exclamation':
            if not text.endswith('!') and not text.endswith('!'):
                text += '!'
        elif detected_tone == 'command':
            # برای دستورات، معمولاً علامت خاصی اضافه نمی‌کنیم
            pass
        else:
            # اگر لحن خاصی تشخیص داده نشد، بررسی کنیم آیا جمله کامل است
            if not text.endswith('.') and not text.endswith('؟') and not text.endswith('!'):
                text += '.'
        
        return text, detected_tone

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
            
            # پاک‌سازی متن و تشخیص لحن
            if text:
                # تشخیص لحن و اضافه کردن علامت‌گذاری
                processed_text, detected_tone = self.detect_tone_and_punctuation(text)
                
                print(f"Transcribed: {processed_text}")
                if detected_tone:
                    print(f"Detected tone: {detected_tone}")
                
                return processed_text
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
            text = result["text"].strip()
            
            if text:
                # تشخیص لحن و اضافه کردن علامت‌گذاری
                processed_text, detected_tone = self.detect_tone_and_punctuation(text)
                return processed_text
            else:
                return ""
            
        except Exception as e:
            print(f"Error transcribing file {file_path}: {e}")
            return ""

    def get_model_info(self):
        """دریافت اطلاعات مدل"""
        if not self.model_loaded:
            return {
                "model_name": "مدل بارگذاری نشده",
                "language": "نامشخص",
                "device": "نامشخص"
            }
        
        return {
            "model_name": config.WHISPER_MODEL,
            "language": "Persian (fa)",
            "device": "CPU" if not config.TTS_USE_GPU else "GPU",
            "tone_detection": "Enabled",
            "supported_tones": list(self.tone_patterns.keys())
        }