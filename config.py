# پیکربندی LinguaStream

# تنظیمات مدل‌ها
WHISPER_MODEL = "base"  # گزینه‌ها: tiny, base, small, medium, large
TRANSLATION_MODEL_NAME = "facebook/m2m100_418M"
TTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
TTS_SPEAKER_WAV = None  # مسیر فایل صوتی نمونه صدای کاربر
TTS_LANGUAGE = "en"     # زبان خروجی TTS
TTS_USE_GPU = True      # استفاده از GPU برای XTTS-v2

# تنظیمات صوتی
SAMPLE_RATE = 16000     # نرخ نمونه برای Whisper (16kHz)
CHUNK_SIZE = 1024       # اندازه chunk صوتی
CHANNELS = 1            # کانال‌های صوتی (مونو)
BIT_DEPTH = 16          # عمق بیت

# تنظیمات عملکرد
MAX_LATENCY = 3.0       # حداکثر تأخیر مجاز (ثانیه)
BUFFER_SIZE = 4096      # اندازه بافر صوتی
THREAD_COUNT = 4        # تعداد thread های پردازش

# تنظیمات Streamlit
STREAMLIT_TITLE = "LinguaStream - ترجمه همزمان با صدای شخصی"
STREAMLIT_PORT = 8501   # پورت Streamlit
MAX_FILE_SIZE = 25     # حداکثر اندازه فایل آپلود (MB)

# تنظیمات کلون صدا
MIN_VOICE_DURATION = 6  # حداقل مدت زمان نمونه صدا (ثانیه)
MAX_VOICE_DURATION = 10 # حداکثر مدت زمان نمونه صدا (ثانیه)
VOICE_SAMPLE_RATE = 24000  # نرخ نمونه برای نمونه صدای کاربر

# تنظیمات مدل‌ها و مسیرها
MODELS_DIR = "models"   # پوشه ذخیره مدل‌ها
TEMP_DIR = "temp"       # پوشه فایل‌های موقت

# تنظیمات رابط کاربری
UI_REFRESH_RATE = 0.5   # نرخ به‌روزرسانی UI (ثانیه)
SHOW_DEBUG_INFO = True  # نمایش اطلاعات دیباگ
ENABLE_VOICE_PREVIEW = True  # فعال‌سازی پیش‌نمایش صدا

# تنظیمات تشخیص گفتار
MIN_AUDIO_DURATION = 1.0  # حداقل مدت زمان صوتی برای پردازش (ثانیه)
MAX_AUDIO_DURATION = 30.0 # حداکثر مدت زمان صوتی برای پردازش (ثانیه)
VOICE_ACTIVITY_THRESHOLD = 0.01  # آستانه تشخیص فعالیت صوتی
