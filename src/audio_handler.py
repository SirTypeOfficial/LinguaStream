import numpy as np
import threading
import time
import config
import io
import wave
import tempfile
import os
from pydub import AudioSegment
from pydub.utils import which

class AudioHandler:
    def __init__(self):
        self.is_recording = False
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        
        # تنظیمات صوتی
        self.sample_rate = config.SAMPLE_RATE
        self.chunk_size = config.CHUNK_SIZE
        self.channels = config.CHANNELS
        
        print(f"Audio Handler initialized - Sample Rate: {self.sample_rate}, Chunk Size: {self.chunk_size}")
    
    def process_uploaded_audio(self, audio_file):
        """پردازش فایل صوتی آپلود شده"""
        try:
            # ذخیره فایل موقت
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
            temp_file.write(audio_file.read())
            temp_file.close()
            
            # تبدیل به فرمت مناسب
            audio_segment = AudioSegment.from_file(temp_file.name)
            
            # تبدیل به مونو و نرخ نمونه مناسب
            audio_segment = audio_segment.set_channels(1)
            audio_segment = audio_segment.set_frame_rate(self.sample_rate)
            
            # تبدیل به numpy array
            audio_data = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
            
            # نرمال‌سازی
            if len(audio_data) > 0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # پاک کردن فایل موقت
            os.unlink(temp_file.name)
            
            return audio_data
            
        except Exception as e:
            print(f"Error processing uploaded audio: {e}")
            return None
    
    def start_recording(self):
        """شروع ضبط صدا (برای سازگاری با کد قدیمی)"""
        self.is_recording = True
        self.audio_buffer = []
        print("Recording started (Web-based)...")
    
    def stop_recording(self):
        """توقف ضبط صدا (برای سازگاری با کد قدیمی)"""
        self.is_recording = False
        print("Recording stopped.")
    
    def get_audio_data(self):
        """دریافت داده‌های صوتی ضبط شده (برای سازگاری با کد قدیمی)"""
        with self.buffer_lock:
            if not self.audio_buffer:
                return None
                
            # ترکیب تمام chunk های صوتی
            audio_data = np.concatenate(self.audio_buffer)
            
            # پاک کردن بافر
            self.audio_buffer = []
            
            return audio_data
    
    def get_audio_duration(self):
        """محاسبه مدت زمان صوتی موجود در بافر"""
        with self.buffer_lock:
            if not self.audio_buffer:
                return 0
            total_samples = sum(len(chunk) for chunk in self.audio_buffer)
            return total_samples / self.sample_rate
    
    def save_audio_to_file(self, filename, audio_data):
        """ذخیره داده‌های صوتی در فایل WAV"""
        try:
            # تبدیل numpy array به AudioSegment
            audio_segment = AudioSegment(
                audio_data.tobytes(),
                frame_rate=self.sample_rate,
                sample_width=2,  # 16-bit
                channels=1
            )
            
            # ذخیره فایل
            audio_segment.export(filename, format="wav")
            print(f"Audio saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
    
    def play_audio(self, audio_data):
        """پخش فایل صوتی"""
        try:
            # تبدیل به AudioSegment
            audio_segment = AudioSegment(
                audio_data.tobytes(),
                frame_rate=self.sample_rate,
                sample_width=2,
                channels=1
            )
            
            # پخش صدا
            audio_segment.play()
            
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def cleanup(self):
        """پاک‌سازی منابع"""
        self.stop_recording()
        print("Audio Handler cleaned up.")
    
    def get_available_devices(self):
        """دریافت لیست دستگاه‌های صوتی موجود (برای سازگاری)"""
        # در نسخه وب، این اطلاعات از مرورگر دریافت می‌شود
        return [{
            'index': 0,
            'name': 'Default Microphone (Web)',
            'channels': 1,
            'sample_rate': self.sample_rate
        }]
