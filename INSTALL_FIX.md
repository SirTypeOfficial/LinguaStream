# راهنمای نصب LinguaStream - حل مشکلات Python 3.13

## ⚠️ مشکل اصلی
شما از **Python 3.13** استفاده می‌کنید که هنوز بسیاری از پکیج‌ها با آن سازگار نیستند.

## 🔧 راه‌حل‌های پیشنهادی:

### راه‌حل 1: استفاده از Python 3.11 (توصیه شده)

```bash
# نصب Python 3.11 از python.org
# یا استفاده از pyenv/conda

# با pyenv:
pyenv install 3.11.9
pyenv local 3.11.9

# با conda:
conda create -n linguastream python=3.11
conda activate linguastream
```

### راه‌حل 2: نصب تدریجی پکیج‌ها

```bash
# ابتدا پکیج‌های اصلی
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers
pip install openai-whisper
pip install streamlit
pip install numpy scipy
pip install librosa soundfile

# PyAudio (مشکل‌دار)
pip install pipwin
pipwin install pyaudio
```

### راه‌حل 3: استفاده از requirements محدود

```bash
# فقط پکیج‌های ضروری
pip install torch torchaudio transformers openai-whisper streamlit numpy scipy librosa soundfile
```

## 🚀 نصب سریع (Python 3.11)

```bash
# 1. ایجاد محیط مجازی
python -m venv linguastream_env
linguastream_env\Scripts\activate  # Windows
# source linguastream_env/bin/activate  # Linux/Mac

# 2. نصب وابستگی‌ها
pip install -r requirements.txt

# 3. راه‌اندازی سیستم
python setup.py

# 4. اجرای برنامه
streamlit run app.py
```

## 🔍 تشخیص مشکل

```bash
# بررسی ورژن Python
python --version

# بررسی پکیج‌های نصب شده
pip list | findstr torch
pip list | findstr whisper
```

## ⚡ نصب سریع PyAudio

### Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

### Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### macOS:
```bash
brew install portaudio
pip install pyaudio
```

## 🎯 تست نصب

```bash
python -c "import torch; print('✅ PyTorch OK')"
python -c "import whisper; print('✅ Whisper OK')"
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import pyaudio; print('✅ PyAudio OK')"
```

## 📝 نکات مهم

1. **Python 3.11** بهترین گزینه است
2. **PyAudio** همیشه مشکل‌ساز است - از pipwin استفاده کنید
3. **TTS** را برای فاز اول حذف کردیم
4. **Whisper** را به `openai-whisper` تغییر دادیم

## 🆘 اگر همچنان مشکل دارید

```bash
# نصب دستی هر پکیج
pip install torch==2.1.0
pip install transformers==4.35.0
pip install openai-whisper==20231117
pip install streamlit==1.28.0
```
