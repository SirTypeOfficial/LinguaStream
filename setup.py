import os
import sys
import time
import config
from pathlib import Path

def create_directories():
    """ایجاد پوشه‌های مورد نیاز"""
    directories = [config.MODELS_DIR, config.TEMP_DIR]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ پوشه {directory} ایجاد شد")

def check_model_download():
    """بررسی و دانلود مدل‌های مورد نیاز"""
    print("🔍 بررسی مدل‌های مورد نیاز...")
    
    # بررسی مدل Whisper
    try:
        import whisper
        print("📥 در حال دانلود مدل Whisper...")
        
        # نمایش پیشرفت دانلود
        def progress_callback(progress):
            if progress % 10 == 0:  # نمایش هر 10%
                print(f"📊 پیشرفت دانلود: {progress}%")
        
        # دانلود مدل Whisper
        model = whisper.load_model(config.WHISPER_MODEL)
        print(f"✅ مدل Whisper '{config.WHISPER_MODEL}' با موفقیت دانلود شد")
        
        # ذخیره اطلاعات مدل
        model_info = {
            "name": config.WHISPER_MODEL,
            "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "size": "~150MB"
        }
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در دانلود مدل Whisper: {e}")
        return False

def check_translation_model():
    """بررسی مدل ترجمه"""
    try:
        print("📥 در حال دانلود مدل ترجمه...")
        from transformers import pipeline
        
        # دانلود مدل ترجمه
        translator = pipeline("translation", model=config.TRANSLATION_MODEL_NAME)
        print(f"✅ مدل ترجمه '{config.TRANSLATION_MODEL_NAME}' با موفقیت دانلود شد")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در دانلود مدل ترجمه: {e}")
        return False

def check_tts_model():
    """بررسی مدل TTS (اختیاری برای فاز اول)"""
    try:
        print("📥 در حال بررسی مدل TTS...")
        # برای فاز اول، TTS اختیاری است
        print("ℹ️ مدل TTS برای فاز بعدی برنامه‌ریزی شده است")
        return True
        
    except Exception as e:
        print(f"⚠️ مدل TTS در دسترس نیست: {e}")
        return True  # اختیاری است

def check_dependencies():
    """بررسی وابستگی‌های Python"""
    print("🔍 بررسی وابستگی‌ها...")
    
    required_packages = [
        'torch', 'transformers', 'whisper', 'streamlit', 
        'pyaudio', 'numpy', 'scipy', 'librosa', 'soundfile'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ پکیج‌های زیر نصب نشده‌اند: {', '.join(missing_packages)}")
        print("لطفاً دستور زیر را اجرا کنید:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    """تابع اصلی برای راه‌اندازی سیستم"""
    print("🚀 شروع راه‌اندازی LinguaStream...")
    print("=" * 50)
    
    # بررسی وابستگی‌ها
    if not check_dependencies():
        print("\n❌ راه‌اندازی متوقف شد. لطفاً وابستگی‌ها را نصب کنید.")
        return False
    
    # ایجاد پوشه‌ها
    create_directories()
    
    # بررسی و دانلود مدل‌ها
    print("\n📥 دانلود مدل‌ها...")
    
    whisper_ok = check_model_download()
    translation_ok = check_translation_model()
    tts_ok = check_tts_model()
    
    print("\n" + "=" * 50)
    
    if whisper_ok and translation_ok and tts_ok:
        print("✅ تمام مدل‌ها با موفقیت آماده شدند!")
        print("\n🎉 سیستم آماده استفاده است!")
        print("برای اجرای رابط کاربری، دستور زیر را اجرا کنید:")
        print("streamlit run app.py")
        return True
    else:
        print("❌ برخی مدل‌ها با مشکل مواجه شدند.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
