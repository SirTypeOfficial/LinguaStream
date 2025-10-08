import pyaudio
import numpy as np
import threading
import time
import config
import sys
import os

# اضافه کردن مسیر src به sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.audio_handler import AudioHandler
from src.stt_engine import STTEngine
from src.translator import Translator
from src.tts_engine import TTSEngine

class LinguaStream:
    def __init__(self):
        print("🚀 راه‌اندازی LinguaStream...")
        
        # راه‌اندازی کامپوننت‌ها
        self.audio_handler = AudioHandler()
        self.stt_engine = STTEngine()
        self.translator = Translator()
        self.tts_engine = TTSEngine()
        
        self.is_running = False
        print("✅ LinguaStream آماده است!")

    def process_loop(self):
        """حلقه اصلی برای ضبط، پردازش و پخش صوتی"""
        print("🎤 شروع ترجمه همزمان...")
        self.is_running = True
        
        while self.is_running:
            try:
                # 1. ضبط chunk صوتی
                audio_chunk = self.audio_handler.capture_chunk()
                if audio_chunk is None:
                    time.sleep(0.1)
                    continue

                # بررسی حداقل مدت زمان صوتی
                duration = len(audio_chunk) / config.SAMPLE_RATE
                if duration < config.MIN_AUDIO_DURATION:
                    continue

                # 2. گفتار به متن
                print("\n🔄 تشخیص گفتار...")
                farsi_text = self.stt_engine.transcribe(audio_chunk)
                print(f"📝 متن فارسی: {farsi_text}")

                if not farsi_text.strip():
                    continue

                # 3. ترجمه
                print("🌐 ترجمه...")
                english_text = self.translator.translate(farsi_text)
                print(f"📝 متن انگلیسی: {english_text}")

                if not english_text.strip():
                    continue

                # 4. متن به گفتار
                print("🔊 سنتز گفتار...")
                translated_audio_bytes = self.tts_engine.synthesize(english_text)
                
                if translated_audio_bytes:
                    # 5. پخش صدا
                    self.audio_handler.play_audio(translated_audio_bytes)
                    print("✅ ترجمه کامل شد!")

            except KeyboardInterrupt:
                print("\n⏹️ توقف توسط کاربر...")
                break
            except Exception as e:
                print(f"❌ خطا در پردازش: {e}")
                time.sleep(1)

    def run(self):
        """اجرای سیستم"""
        try:
            print("🎯 شروع سیستم ترجمه همزمان...")
            print("برای توقف، Ctrl+C را فشار دهید")
            
            # اجرای پردازش در thread جداگانه
            processing_thread = threading.Thread(target=self.process_loop)
            processing_thread.daemon = True
            processing_thread.start()
            
            # نگه داشتن thread اصلی
            while processing_thread.is_alive():
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n🛑 توقف LinguaStream...")
            self.is_running = False
        finally:
            self.cleanup()

    def cleanup(self):
        """پاک‌سازی منابع"""
        self.is_running = False
        if self.audio_handler:
            self.audio_handler.cleanup()
        print("🧹 منابع پاک‌سازی شدند")

def main():
    """تابع اصلی"""
    print("=" * 60)
    print("🎤 LinguaStream - سیستم ترجمه همزمان با صدای شخصی")
    print("=" * 60)
    
    try:
        app = LinguaStream()
        app.run()
    except Exception as e:
        print(f"❌ خطای کلی: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)