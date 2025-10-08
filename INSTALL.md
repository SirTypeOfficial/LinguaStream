# راهنمای نصب LinguaStream - فاز اول

## 🚀 نصب سریع

### مرحله 1: نصب وابستگی‌های اصلی

```bash
pip install torch torchaudio
pip install transformers
pip install whisper
pip install streamlit
pip install numpy scipy
pip install librosa soundfile
```

### مرحله 2: نصب PyAudio

#### در Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

#### در Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

#### در macOS:
```bash
brew install portaudio
pip install pyaudio
```

### مرحله 3: راه‌اندازی سیستم

```bash
python setup.py
```

### مرحله 4: اجرای رابط کاربری

```bash
streamlit run app.py
```

## 🔧 عیب‌یابی

### مشکل PyAudio
اگر PyAudio نصب نمی‌شود:

1. **Windows**: از pipwin استفاده کنید
2. **Linux**: portaudio19-dev را نصب کنید
3. **macOS**: portaudio را از Homebrew نصب کنید

### مشکل CUDA
اگر GPU دارید:
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### مشکل فضای دیسک
مدل‌ها حدود 2GB فضا نیاز دارند:
- Whisper base: ~150MB
- Helsinki-NLP: ~500MB
- سایر وابستگی‌ها: ~1GB

## ✅ تست نصب

```bash
python -c "import config; print('✅ Config OK')"
python -c "import whisper; print('✅ Whisper OK')"
python -c "import streamlit; print('✅ Streamlit OK')"
```

## 🎯 استفاده

1. `streamlit run app.py` را اجرا کنید
2. در مرورگر به `http://localhost:8501` بروید
3. روی "🚀 راه‌اندازی سیستم" کلیک کنید
4. منتظر دانلود مدل‌ها باشید
5. شروع به استفاده کنید!
