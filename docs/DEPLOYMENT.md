# مستندات استقرار

## نمای کلی

این سند دستورالعمل‌های جامع استقرار VoiceBridge در محیط‌های مختلف، شامل توسعه محلی، استقرار تولید و راه‌حل‌های کانتینری ارائه می‌دهد.

## پیش‌نیازها

### نیازمندی‌های سیستم

#### حداقل سخت‌افزار
- **CPU**: پردازنده دو هسته 2.0GHz
- **RAM**: 4GB حافظه سیستم
- **ذخیره‌سازی**: 2GB فضای آزاد دیسک
- **صوتی**: میکروفون و بلندگو/هدفون
- **شبکه**: اتصال اینترنت برای دانلود اولیه مدل

#### سخت‌افزار توصیه شده
- **CPU**: پردازنده چهار هسته 3.0GHz+
- **RAM**: 8GB+ حافظه سیستم
- **ذخیره‌سازی**: 5GB+ فضای آزاد دیسک (SSD توصیه می‌شود)
- **صوتی**: میکروفون USB خارجی، خروجی صوتی با کیفیت
- **GPU**: اختیاری NVIDIA GPU با پشتیبانی CUDA

### نیازمندی‌های نرم‌افزاری

#### سیستم‌عامل‌ها
- **Windows**: 10/11 (64-bit)
- **Linux**: Ubuntu 20.04+، CentOS 8+، Debian 11+
- **macOS**: 10.15+ (Intel/Apple Silicon)

#### محیط Python
- **Python**: 3.8+ (3.10+ توصیه می‌شود)
- **pip**: آخرین نسخه
- **محیط مجازی**: توصیه می‌شود

## راه‌اندازی توسعه محلی

### 1. آماده‌سازی محیط

#### راه‌اندازی Windows

```powershell
# نصب Python (در صورت عدم نصب)
winget install Python.Python.3.10

# ایجاد محیط مجازی
python -m venv voicebridge-env
voicebridge-env\Scripts\activate

# ارتقای pip
python -m pip install --upgrade pip
```

#### راه‌اندازی Linux/macOS

```bash
# نصب Python (Ubuntu/Debian)
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# ایجاد محیط مجازی
python3 -m venv voicebridge-env
source voicebridge-env/bin/activate

# ارتقای pip
python -m pip install --upgrade pip
```

### 2. نصب پروژه

```bash
# کلون کردن مخزن
git clone https://github.com/yourusername/VoiceBridge.git
cd VoiceBridge

# نصب وابستگی‌ها
pip install -r requirements.txt

# نصب وابستگی‌های اضافی سیستم
# Windows
pip install pyaudio

# Linux
sudo apt install portaudio19-dev python3-pyaudio

# macOS
brew install portaudio
pip install pyaudio
```

### 3. راه‌اندازی پیکربندی

```bash
# کپی کردن قالب پیکربندی
cp config.py.example config.py

# ویرایش پیکربندی
nano config.py  # یا از ویرایشگر مورد نظر خود استفاده کنید
```

#### گزینه‌های پیکربندی

```python
# config.py
import os

# پیکربندی صوتی
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
CHANNELS = 1
BIT_DEPTH = 16

# پیکربندی مدل
WHISPER_MODEL = "base"  # tiny, base, small, medium, large
TRANSLATION_MODEL_NAME = "Helsinki-NLP/opus-mt-fa-en"
TTS_VOICE_MODEL_PATH = "models/en_US-amy-medium.onnx"

# پیکربندی عملکرد
MAX_LATENCY = 2.0
BUFFER_SIZE = 4096
THREAD_COUNT = 4

# پیکربندی مسیر
MODEL_CACHE_DIR = os.path.expanduser("~/.voicebridge/models")
LOG_DIR = os.path.expanduser("~/.voicebridge/logs")
```

### 4. دانلود مدل

```bash
# اجرای برنامه برای شروع دانلود مدل
python main.py

# مدل‌ها به صورت خودکار در اولین اجرا دانلود می‌شوند
# این ممکن است چند دقیقه طول بکشد بسته به سرعت اینترنت
```

### 5. پیکربندی دستگاه صوتی

#### راه‌اندازی صوتی Windows

1. **نصب Virtual Audio Cable** (اختیاری)
   - دانلود از: https://vb-audio.com/Cable/
   - نصب و پیکربندی به عنوان دستگاه پخش پیش‌فرض

2. **پیکربندی میکروفون**
   - کلیک راست روی آیکون بلندگو → تنظیمات صدا
   - انتخاب دستگاه ورودی
   - تست سطح میکروفون

#### راه‌اندازی صوتی Linux

```bash
# نصب ابزارهای ALSA
sudo apt install alsa-utils

# لیست دستگاه‌های صوتی
arecord -l  # دستگاه‌های ورودی
aplay -l    # دستگاه‌های خروجی

# تست میکروفون
arecord -f cd -d 5 test.wav
aplay test.wav
```

#### راه‌اندازی صوتی macOS

```bash
# نصب Homebrew (در صورت عدم نصب)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# نصب ابزارهای صوتی
brew install portaudio
```

### 6. تأیید

```bash
# تست نصب
python -c "import whisper, transformers, piper; print('تمام وابستگی‌ها با موفقیت نصب شدند')"

# اجرای تست پایه
python -c "
from src.stt_engine import STTEngine
from src.translator import Translator
from src.tts_engine import TTSEngine
print('تمام اجزا با موفقیت import شدند')
"
```

## Production Deployment

### 1. Server Setup

#### Ubuntu Server Deployment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.10 python3.10-venv python3-pip python3-dev
sudo apt install portaudio19-dev libasound2-dev
sudo apt install ffmpeg  # For audio processing

# Create application user
sudo useradd -m -s /bin/bash linguastream
sudo usermod -aG audio linguastream

# Switch to application user
sudo su - linguastream
```

#### CentOS/RHEL Deployment

```bash
# Install EPEL repository
sudo yum install epel-release

# Install Python and dependencies
sudo yum install python3.10 python3.10-pip python3-devel
sudo yum install portaudio-devel alsa-lib-devel
sudo yum install ffmpeg

# Create application user
sudo useradd -m linguastream
sudo usermod -aG audio linguastream
```

### 2. Application Deployment

```bash
# Clone repository
git clone https://github.com/yourusername/LinguaStream.git
cd LinguaStream

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production dependencies
pip install gunicorn supervisor
```

### 3. System Service Configuration

#### Create Systemd Service

```bash
sudo nano /etc/systemd/system/linguastream.service
```

```ini
[Unit]
Description=LinguaStream Real-Time Translation Service
After=network.target sound.target

[Service]
Type=simple
User=linguastream
Group=linguastream
WorkingDirectory=/home/linguastream/LinguaStream
Environment=PATH=/home/linguastream/LinguaStream/venv/bin
ExecStart=/home/linguastream/LinguaStream/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable linguastream
sudo systemctl start linguastream
sudo systemctl status linguastream
```

### 4. Process Management

#### Supervisor Configuration

```bash
sudo nano /etc/supervisor/conf.d/linguastream.conf
```

```ini
[program:linguastream]
command=/home/linguastream/LinguaStream/venv/bin/python main.py
directory=/home/linguastream/LinguaStream
user=linguastream
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/linguastream.log
environment=PATH="/home/linguastream/LinguaStream/venv/bin"
```

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start linguastream
```

## Docker Deployment

### 1. Dockerfile

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 linguastream && \
    chown -R linguastream:linguastream /app
USER linguastream

# Expose port (if web interface added)
EXPOSE 8000

# Run application
CMD ["python", "main.py"]
```

### 2. Docker Compose

```yaml
version: '3.8'

services:
  linguastream:
    build: .
    container_name: linguastream
    volumes:
      - ./models:/app/models
      - ./config.py:/app/config.py
      - /dev/snd:/dev/snd  # Audio device access
    devices:
      - /dev/snd:/dev/snd
    environment:
      - PULSE_RUNTIME_PATH=/tmp/pulse
    network_mode: host
    restart: unless-stopped
    
  # Optional: Add monitoring service
  monitoring:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
```

### 3. Build and Run

```bash
# Build Docker image
docker build -t linguastream .

# Run container
docker run -d \
  --name linguastream \
  --device /dev/snd:/dev/snd \
  -v $(pwd)/models:/app/models \
  linguastream

# Or use Docker Compose
docker-compose up -d
```

## Cloud Deployment

### 1. AWS EC2 Deployment

#### Launch Instance

```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx
```

#### Configure Instance

```bash
# Connect to instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip git -y

# Clone and setup application
git clone https://github.com/yourusername/LinguaStream.git
cd LinguaStream
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Google Cloud Platform

#### Create VM Instance

```bash
# Create VM instance
gcloud compute instances create linguastream-vm \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-medium \
  --zone us-central1-a
```

#### Deploy Application

```bash
# Connect to instance
gcloud compute ssh linguastream-vm --zone us-central1-a

# Install and setup
sudo apt update
sudo apt install python3 python3-pip git -y
git clone https://github.com/yourusername/LinguaStream.git
cd LinguaStream
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Azure VM Deployment

#### Create VM

```bash
# Create resource group
az group create --name linguastream-rg --location eastus

# Create VM
az vm create \
  --resource-group linguastream-rg \
  --name linguastream-vm \
  --image UbuntuLTS \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys
```

## Monitoring and Logging

### 1. Application Logging

```python
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linguastream.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 2. System Monitoring

#### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'linguastream'
    static_configs:
      - targets: ['localhost:8000']
```

#### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "LinguaStream Metrics",
    "panels": [
      {
        "title": "Translation Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "linguastream_translation_latency_seconds"
          }
        ]
      }
    ]
  }
}
```

### 3. Health Checks

```python
# health_check.py
import requests
import time

def check_application_health():
    try:
        # Check if application is responding
        response = requests.get('http://localhost:8000/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def monitor_application():
    while True:
        if not check_application_health():
            print("Application health check failed")
            # Restart application or send alert
        time.sleep(30)
```

## Security Considerations

### 1. Network Security

```bash
# Configure firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 8000/tcp  # If web interface enabled
```

### 2. Application Security

```python
# Secure configuration
import os
from cryptography.fernet import Fernet

class SecureConfig:
    def __init__(self):
        self.key = os.environ.get('CONFIG_KEY', Fernet.generate_key())
        self.cipher = Fernet(self.key)
    
    def encrypt_config(self, data):
        return self.cipher.encrypt(data.encode())
    
    def decrypt_config(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data).decode()
```

### 3. Data Protection

```python
# Data sanitization
import re

def sanitize_audio_data(audio_data):
    # Remove any potential malicious data
    return re.sub(r'[^\x00-\x7F]+', '', str(audio_data))

def secure_text_processing(text):
    # Sanitize text input
    return text.strip()[:1000]  # Limit length
```

## Troubleshooting

### Common Deployment Issues

1. **Audio Device Not Found**
   ```bash
   # Check audio devices
   arecord -l
   aplay -l
   
   # Test audio
   speaker-test -t wav
   ```

2. **Model Download Failures**
   ```bash
   # Manual model download
   python -c "import whisper; whisper.load_model('base')"
   ```

3. **Permission Issues**
   ```bash
   # Fix audio permissions
   sudo usermod -a -G audio $USER
   sudo chmod 666 /dev/snd/*
   ```

4. **Memory Issues**
   ```bash
   # Monitor memory usage
   free -h
   top -p $(pgrep python)
   ```

### Performance Optimization

```bash
# CPU optimization
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Memory optimization
echo 1 | sudo tee /proc/sys/vm/drop_caches
```

This deployment documentation provides comprehensive guidance for deploying LinguaStream across various environments, from local development to production cloud deployments.
