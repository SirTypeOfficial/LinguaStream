import pyaudio
import numpy as np
import threading
import time
import config
import io
import wave

class AudioHandler:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.is_recording = False
        self.audio_stream = None
        self.recording_thread = None
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        
        # تنظیمات صوتی
        self.sample_rate = config.SAMPLE_RATE
        self.chunk_size = config.CHUNK_SIZE
        self.channels = config.CHANNELS
        self.format = pyaudio.paInt16
        
        print(f"Audio Handler initialized - Sample Rate: {self.sample_rate}, Chunk Size: {self.chunk_size}")
    
    def start_recording(self):
        """شروع ضبط صدا از میکروفون"""
        if self.is_recording:
            return
            
        try:
            self.audio_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            
            self.is_recording = True
            self.audio_buffer = []
            print("Recording started...")
            
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.is_recording = False
    
    def stop_recording(self):
        """توقف ضبط صدا"""
        self.is_recording = False
        
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
            
        print("Recording stopped.")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback برای دریافت داده‌های صوتی"""
        if self.is_recording:
            with self.buffer_lock:
                # تبدیل بایت‌ها به آرایه numpy
                audio_data = np.frombuffer(in_data, dtype=np.int16)
                self.audio_buffer.append(audio_data)
                
                # محدود کردن اندازه بافر برای جلوگیری از مصرف بیش از حد حافظه
                if len(self.audio_buffer) > 100:  # حدود 10 ثانیه صدا
                    self.audio_buffer.pop(0)
        
        return (in_data, pyaudio.paContinue)
    
    def get_audio_data(self):
        """دریافت داده‌های صوتی ضبط شده"""
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
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(self.channels)
                wav_file.setsampwidth(self.audio.get_sample_size(self.format))
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(audio_data.tobytes())
            print(f"Audio saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving audio: {e}")
            return False
    
    def play_audio(self, audio_bytes):
        """پخش فایل صوتی"""
        try:
            # ایجاد stream خروجی
            output_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                output=True
            )
            
            # پخش صدا
            output_stream.write(audio_bytes)
            output_stream.stop_stream()
            output_stream.close()
            
        except Exception as e:
            print(f"Error playing audio: {e}")
    
    def cleanup(self):
        """پاک‌سازی منابع"""
        self.stop_recording()
        if self.audio:
            self.audio.terminate()
        print("Audio Handler cleaned up.")
    
    def get_available_devices(self):
        """دریافت لیست دستگاه‌های صوتی موجود"""
        devices = []
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            devices.append({
                'index': i,
                'name': device_info['name'],
                'channels': device_info['maxInputChannels'],
                'sample_rate': device_info['defaultSampleRate']
            })
        return devices
