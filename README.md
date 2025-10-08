# LinguaStream - سیستم ترجمه همزمان صوتی با کلون صدا

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)](https://github.com/yourusername/LinguaStream)

## 🎯 نمای کلی

**LinguaStream** یک سیستم پیشرفته ترجمه همزمان صوتی است که برای پردازش آفلاین و کم تأخیر گفتار فارسی به انگلیسی با صدای کلون شده کاربر طراحی شده است. این سیستم از مدل XTTS-v2 استفاده می‌کند که امکان کلون کردن صدا از نمونه 6 ثانیه‌ای کاربر را فراهم می‌کند و ترجمه را با صدای خود کاربر ارائه می‌دهد.

### ویژگی‌های کلیدی

- **🔄 پردازش همزمان**: خط لوله ترجمه صوتی با تأخیر فوق‌العاده کم
- **🌐 عملکرد آفلاین**: استقلال کامل از اتصال اینترنت
- **🎤 فارسی به انگلیسی**: تشخیص گفتار فارسی و ترجمه تخصصی
- **🎭 کلون صدا**: استفاده از صدای کاربر برای ترجمه با مدل XTTS-v2
- **🗣️ کیفیت بالا**: سنتز گفتار با کیفیت 24kHz و حفظ ویژگی‌های صوتی
- **🌍 چندزبانه**: پشتیبانی از 17 زبان مختلف
- **🔒 حریم خصوصی اول**: تمام پردازش‌ها محلی روی دستگاه شما انجام می‌شود
- **🎧 رابط کاربری**: رابط Streamlit برای آپلود صدا و مدیریت سیستم

### ویژگی‌های جدید

- **🎤 مدیریت دسترسی میکروفن**: درخواست دسترسی میکروفن قبل از شروع ضبط و انتخاب دستگاه از لیست موجود
- **🎭 تشخیص لحن و علامت‌گذاری**: تشخیص لحن سوالی، تعجبی و دستوری با اضافه کردن خودکار علامت‌گذاری مناسب
- **📚 مستندات سازماندهی شده**: تمام مستندات فنی در فولدر `docs/` با ساختار حرفه‌ای

## 🏗️ معماری سیستم

سیستم یک خط لوله سه مرحله‌ای پیاده‌سازی می‌کند:

```
ورودی صوتی → ASR (گفتار به متن) → MT (ترجمه ماشینی) → TTS (متن به گفتار با صدای کلون شده) → خروجی صوتی
```

### اجزای اصلی

- **مدیر صوتی**: مدیریت ورودی میکروفون و خروجی دستگاه صوتی مجازی
- **موتور STT**: تشخیص گفتار فارسی مبتنی بر Whisper
- **مترجم**: Hugging Face Transformers برای ترجمه فارسی به انگلیسی
- **موتور TTS**: سنتز گفتار انگلیسی با صدای کلون شده کاربر (XTTS-v2)
- **رابط کاربری**: رابط Streamlit برای آپلود نمونه صدای کاربر

## 🚀 شروع سریع

### پیش‌نیازها

- Python 3.8 یا بالاتر
- Windows 10/11 یا Linux
- **GPU**: NVIDIA RTX 3060 یا بالاتر (حداقل 6GB VRAM)
- **RAM**: حداقل 16GB، توصیه شده 32GB
- **CPU**: Intel i7 یا AMD Ryzen 7
- میکروفون و بلندگو/هدفون
- فضای ذخیره: حداقل 10GB

### نصب

1. **کلون کردن مخزن**
   ```bash
   git clone https://github.com/yourusername/LinguaStream.git
   cd LinguaStream
   ```

2. **نصب وابستگی‌ها**
   ```bash
   pip install -r requirements.txt
   ```

3. **نصب CUDA** (برای GPU)
   ```bash
   # اطمینان حاصل کنید که CUDA نصب شده است
   nvidia-smi
   ```

4. **پیکربندی سیستم**
   ```bash
   # ویرایش config.py با تنظیمات مورد نظر شما
   python config.py
   ```

5. **دانلود مدل XTTS-v2** (اجرای اول به صورت خودکار دانلود می‌کند)
   ```bash
   python main.py
   ```

6. **اجرای رابط کاربری Streamlit**
   ```bash
   streamlit run app.py
   ```

7. **آپلود نمونه صدای خود** (6 ثانیه، فرمت WAV)

## 📋 نیازمندی‌ها

### نیازمندی‌های سخت‌افزاری

| مؤلفه | حداقل | توصیه شده |
|--------|--------|------------|
| GPU | NVIDIA GTX 1060 (6GB VRAM) | NVIDIA RTX 3060+ (8GB+ VRAM) |
| RAM | 16GB | 32GB+ |
| CPU | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 |
| ذخیره‌سازی | 10GB فضای آزاد | 20GB+ فضای آزاد |
| صوتی | میکروفون داخلی | میکروفون USB خارجی |

### وابستگی‌های نرم‌افزاری

- **PyAudio**: عملیات ورودی/خروجی صوتی
- **Whisper**: پردازش گفتار به متن
- **Transformers**: ترجمه ماشینی
- **TTS (Coqui)**: سنتز متن به گفتار با کلون صدا
- **Streamlit**: رابط کاربری وب
- **NumPy**: محاسبات عددی
- **CUDA**: شتاب‌دهی GPU (اجباری)

## 🎛️ پیکربندی

سیستم از طریق `config.py` قابل پیکربندی است:

```python
# پیکربندی مدل‌ها
WHISPER_MODEL = "base"  # گزینه‌ها: tiny, base, small, medium, large
TRANSLATION_MODEL_NAME = "Helsinki-NLP/opus-mt-fa-en"
TTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
TTS_SPEAKER_WAV = None  # مسیر فایل صوتی نمونه صدای کاربر
TTS_LANGUAGE = "en"     # زبان خروجی TTS
TTS_USE_GPU = True      # استفاده از GPU برای XTTS-v2

# تنظیمات صوتی
SAMPLE_RATE = 24000     # نرخ نمونه برای XTTS-v2
CHUNK_SIZE = 1024
CHANNELS = 1
```

## 🔧 استفاده

### استفاده پایه

```python
from main import LinguaStream
import streamlit as st

# راه‌اندازی سیستم
app = LinguaStream()

# آپلود نمونه صدای کاربر
uploaded_file = st.file_uploader("آپلود نمونه صدای خود (6 ثانیه)", type=['wav'])
if uploaded_file:
    # ذخیره فایل موقت
    with open("temp_voice.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # تنظیم صدای کاربر در TTS
    app.tts_engine.load_speaker_model("temp_voice.wav")
    
    # شروع ترجمه با صدای کاربر
    app.run()
```

### استفاده پیشرفته

```python
# پیکربندی چندگانه صدا
voices = {
    "کاربر اصلی": "user_main_voice.wav",
    "صدای رسمی": "user_formal_voice.wav", 
    "صدای غیررسمی": "user_casual_voice.wav"
}

# انتخاب صدا بر اساس نوع محتوا
def synthesize_with_voice(text, voice_type="کاربر اصلی"):
    speaker_wav = voices.get(voice_type)
    return app.tts_engine.synthesize(text, speaker_wav)
```

## 📊 معیارهای عملکرد

| معیار | مقدار |
|--------|-------|
| تأخیر | < 3 ثانیه (با GPU) |
| دقت | > 90% (تشخیص فارسی) |
| کیفیت ترجمه | امتیاز BLEU > 0.7 |
| کیفیت صدا | 24kHz، حفظ ویژگی‌های کاربر |
| استفاده از منابع | < 6GB RAM + 8GB VRAM |
| استفاده از GPU | < 80% (RTX 3060) |

## 🛠️ توسعه

### ساختار پروژه

```
LinguaStream/
├── main.py                 # نقطه ورود اصلی برنامه
├── app.py                  # رابط کاربری Streamlit
├── config.py              # تنظیمات پیکربندی
├── requirements.txt       # وابستگی‌های Python
├── src/
│   ├── audio_handler.py   # مدیریت ورودی/خروجی صوتی
│   ├── stt_engine.py      # موتور گفتار به متن
│   ├── translator.py      # موتور ترجمه
│   └── tts_engine.py      # موتور متن به گفتار (XTTS-v2)
├── models/                # ذخیره‌سازی مدل‌های محلی
├── docs/                  # مستندات فنی (API، معماری، استقرار، عملکرد)
│   ├── API.md            # مستندات API
│   ├── ARCHITECTURE.md   # معماری سیستم
│   ├── CONTRIBUTING.md   # راهنمای مشارکت
│   ├── DEPLOYMENT.md     # راهنمای استقرار
│   ├── PERFORMANCE.md    # راهنمای عملکرد
│   └── README.md         # فهرست مستندات
└── temp/                 # فایل‌های موقت
```

### مشارکت

ما از مشارکت‌ها استقبال می‌کنیم! لطفاً [CONTRIBUTING.md](docs/CONTRIBUTING.md) را برای راهنمایی‌ها ببینید.

## 🗺️ نقشه راه

### فاز 1 (فعلی)
- [x] خط لوله ترجمه همزمان پایه
- [x] تشخیص گفتار فارسی
- [x] ترجمه فارسی به انگلیسی
- [x] TTS انگلیسی با صدای کلون شده (XTTS-v2)
- [x] رابط کاربری Streamlit
- [x] آپلود نمونه صدای کاربر

### فاز 2 (برنامه‌ریزی شده)
- [ ] پشتیبانی چندزبانه (عربی، ترکی، چینی)
- [ ] بهینه‌سازی عملکرد GPU
- [ ] سازگاری با پلتفرم موبایل
- [ ] ادغام همگام‌سازی لب برای ترجمه مبتنی بر آواتار

### فاز 3 (آینده)
- [ ] ترجمه ویدیو همزمان
- [ ] گزینه‌های استقرار ابری
- [ ] ادغام سرویس API
- [ ] کلونینگ پیشرفته صدا با احساسات

## 🐛 عیب‌یابی

### مشکلات رایج

**GPU کار نمی‌کند**
- اطمینان حاصل کنید که CUDA نصب شده است
- بررسی کنید که GPU شما حداقل 6GB VRAM دارد
- از دستور `nvidia-smi` برای بررسی وضعیت GPU استفاده کنید

**مدل XTTS-v2 بارگذاری نمی‌شود**
- اطمینان حاصل کنید که حداقل 10GB فضای آزاد دارید
- بررسی کنید که اتصال اینترنت برای دانلود مدل موجود است
- از دستور `python -c "import torch; print(torch.cuda.is_available())"` برای بررسی CUDA استفاده کنید

**کیفیت صدا ضعیف است**
- اطمینان حاصل کنید که نمونه صدای شما حداقل 6 ثانیه است
- کیفیت میکروفون را بررسی کنید
- نمونه صدای شما باید واضح و بدون نویز باشد

**تأخیر بالا**
- از GPU قدرتمندتر استفاده کنید
- اندازه chunk را در config کاهش دهید
- برنامه‌های غیرضروری را ببندید

## 📄 مجوز

این پروژه تحت مجوز MIT مجوزدهی شده است - برای جزئیات فایل [LICENSE](LICENSE) را ببینید.

## 🙏 تشکر و قدردانی

- [OpenAI Whisper](https://github.com/openai/whisper) برای تشخیص گفتار
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) برای مدل‌های ترجمه
- [Coqui TTS](https://github.com/coqui-ai/TTS) برای مدل XTTS-v2 و کلون صدا
- [Hugging Face Transformers](https://huggingface.co/transformers) برای ادغام مدل
- [Streamlit](https://streamlit.io) برای رابط کاربری وب

## 📞 پشتیبانی

- 📧 ایمیل: support@linguastream.dev
- 💬 Discord: [به جامعه ما بپیوندید](https://discord.gg/linguastream)
- 📖 مستندات: [مستندات کامل](docs/) - شامل API، معماری، استقرار و عملکرد
- 🐛 مسائل: [GitHub Issues](https://github.com/yourusername/LinguaStream/issues)

---

**ساخته شده با ❤️ برای ارتباط چندزبانه با صدای شخصی**