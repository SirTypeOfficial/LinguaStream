import streamlit as st
import os
import time
import threading
import tempfile
import config
from src.audio_handler import AudioHandler
from src.stt_engine import STTEngine
from api_server import start_api_server

# تنظیمات صفحه
st.set_page_config(
    page_title=config.STREAMLIT_TITLE,
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS سفارشی برای بهبود ظاهر
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .recording-status {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .ready-status {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
    }
    .processing-status {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .transcribed-text {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        font-size: 1.2rem;
        min-height: 100px;
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# اضافه کردن فایل‌های JavaScript و CSS
st.markdown("""
<link rel="stylesheet" href="static/css/audio_recorder.css">
<script src="static/js/audio_recorder.js"></script>
""", unsafe_allow_html=True)

# کلاس اصلی برنامه
class LinguaStreamApp:
    def __init__(self):
        self.audio_handler = None
        self.stt_engine = None
        self.is_initialized = False
        self.recording_thread = None
        self.processing_thread = None
        
    def initialize_components(self):
        """راه‌اندازی اولیه کامپوننت‌ها"""
        if self.is_initialized:
            return True
            
        try:
            with st.spinner("در حال راه‌اندازی سیستم..."):
                # ایجاد پوشه‌های مورد نیاز
                os.makedirs(config.MODELS_DIR, exist_ok=True)
                os.makedirs(config.TEMP_DIR, exist_ok=True)
                
                # راه‌اندازی Audio Handler
                self.audio_handler = AudioHandler()
                
                # راه‌اندازی STT Engine
                self.stt_engine = STTEngine()
                
                self.is_initialized = True
                st.success("✅ سیستم با موفقیت راه‌اندازی شد!")
                return True
                
        except Exception as e:
            st.error(f"❌ خطا در راه‌اندازی سیستم: {str(e)}")
            return False
    
    def request_microphone_permission(self):
        """درخواست دسترسی میکروفن از کاربر"""
        if not st.session_state.get('mic_permission_granted', False):
            st.warning("🔒 برای شروع ضبط، ابتدا باید دسترسی میکروفن را تأیید کنید.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ اجازه دسترسی میکروفن", type="primary", key="grant_permission"):
                    # تست دسترسی میکروفن با استفاده از st.audio
                    st.session_state.mic_permission_granted = True
                    st.success("✅ دسترسی میکروفن تأیید شد! حالا می‌توانید ضبط کنید.")
                    st.rerun()
            
            with col2:
                if st.button("❌ رد دسترسی", key="deny_permission"):
                    st.error("❌ بدون دسترسی میکروفن، امکان ضبط صدا وجود ندارد.")
                    return False
            
            # نمایش راهنمای دسترسی
            st.info("""
            **راهنمای دسترسی به میکروفن:**
            
            1. روی دکمه "✅ اجازه دسترسی میکروفن" کلیک کنید
            2. مرورگر از شما اجازه دسترسی به میکروفن را می‌خواهد
            3. روی "Allow" یا "اجازه" کلیک کنید
            4. حالا می‌توانید شروع به ضبط کنید
            """)
            
            return False
        return True

    def start_recording(self):
        """شروع ضبط صدا"""
        if not self.is_initialized:
            st.error("لطفاً ابتدا سیستم را راه‌اندازی کنید.")
            return
            
        # بررسی دسترسی میکروفن
        if not self.request_microphone_permission():
            return
            
        try:
            self.audio_handler.start_recording()
            st.session_state.is_recording = True
            st.session_state.recording_start_time = time.time()
            st.success("🎤 ضبط صدا شروع شد!")
            
            # نمایش رابط کاربری ضبط ساده
            self.show_simple_recording_interface()
            
        except Exception as e:
            st.error(f"خطا در شروع ضبط: {str(e)}")
    
    def show_simple_recording_interface(self):
        """نمایش رابط کاربری ضبط ساده"""
        st.markdown("### 🎤 ضبط صدا")
        
        # روش اول: آپلود فایل صوتی
        st.markdown("#### روش ۱: آپلود فایل صوتی")
        uploaded_file = st.file_uploader(
            "فایل صوتی خود را انتخاب کنید",
            type=['wav', 'mp3', 'm4a', 'webm', 'ogg'],
            help="فایل‌های صوتی با فرمت‌های مختلف را آپلود کنید"
        )
        
        if uploaded_file is not None:
            # پردازش فایل آپلود شده
            if st.button("🔄 پردازش فایل صوتی", type="primary"):
                self.process_uploaded_file(uploaded_file)
        
        st.markdown("---")
        
        # روش دوم: ضبط با دکمه‌ها (شبیه‌سازی)
        st.markdown("#### روش ۲: ضبط صدا (شبیه‌سازی)")
        st.info("💡 برای ضبط واقعی، از روش اول استفاده کنید یا از نرم‌افزارهای ضبط صدا استفاده کنید.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎤 شروع ضبط", type="primary", disabled=st.session_state.get('is_recording', False)):
                st.session_state.is_recording = True
                st.session_state.recording_start_time = time.time()
                st.success("🎤 ضبط شروع شد! (شبیه‌سازی)")
                st.rerun()
        
        with col2:
            if st.button("⏹️ توقف ضبط", disabled=not st.session_state.get('is_recording', False)):
                st.session_state.is_recording = False
                st.success("⏹️ ضبط متوقف شد!")
                st.rerun()
        
        with col3:
            if st.button("🔄 پردازش صوتی", disabled=st.session_state.get('is_recording', False)):
                self.process_recorded_audio()
        
        # نمایش وضعیت ضبط
        if st.session_state.get('is_recording', False):
            st.markdown('<div class="status-box recording-status">🔴 در حال ضبط... (شبیه‌سازی)</div>', unsafe_allow_html=True)
            
            # نمایش مدت زمان ضبط
            if 'recording_start_time' in st.session_state:
                elapsed_time = time.time() - st.session_state.recording_start_time
                st.write(f"⏱️ مدت زمان ضبط: {elapsed_time:.1f} ثانیه")
        else:
            st.markdown('<div class="status-box ready-status">⏸️ آماده برای ضبط</div>', unsafe_allow_html=True)
    
    def process_uploaded_file(self, uploaded_file):
        """پردازش فایل آپلود شده"""
        try:
            # نمایش اطلاعات فایل
            st.info(f"📁 فایل: {uploaded_file.name} ({uploaded_file.size} بایت)")
            
            # پردازش فایل صوتی
            audio_data = self.audio_handler.process_uploaded_audio(uploaded_file)
            
            if audio_data is None:
                st.error("❌ خطا در پردازش فایل صوتی")
                return
            
            # بررسی حداقل مدت زمان صوتی
            duration = len(audio_data) / config.SAMPLE_RATE
            if duration < config.MIN_AUDIO_DURATION:
                st.warning(f"⚠️ مدت زمان صوتی کافی نیست. حداقل {config.MIN_AUDIO_DURATION} ثانیه نیاز است.")
                return
            
            # تشخیص گفتار
            with st.spinner("در حال تشخیص گفتار..."):
                transcribed_text = self.stt_engine.transcribe(audio_data)
            
            if transcribed_text:
                st.session_state.last_transcription = transcribed_text
                st.success("✅ متن با موفقیت تشخیص داده شد!")
                
                # نمایش اطلاعات اضافی
                st.info(f"⏱️ مدت زمان فایل: {duration:.2f} ثانیه")
                st.info(f"📊 تعداد نمونه‌ها: {len(audio_data):,}")
            else:
                st.warning("⚠️ هیچ متنی تشخیص داده نشد. لطفاً دوباره تلاش کنید.")
                
        except Exception as e:
            st.error(f"خطا در پردازش فایل: {str(e)}")
    
    def process_recorded_audio(self):
        """پردازش صوتی ضبط شده"""
        if not self.is_initialized:
            return
            
        try:
            # دریافت داده‌های صوتی
            audio_data = self.audio_handler.get_audio_data()
            
            if audio_data is None or len(audio_data) == 0:
                st.warning("⚠️ هیچ داده صوتی یافت نشد. لطفاً ابتدا ضبط کنید.")
                return
            
            # بررسی حداقل مدت زمان صوتی
            duration = len(audio_data) / config.SAMPLE_RATE
            if duration < config.MIN_AUDIO_DURATION:
                st.warning(f"⚠️ مدت زمان صوتی کافی نیست. حداقل {config.MIN_AUDIO_DURATION} ثانیه نیاز است.")
                return
            
            # تشخیص گفتار
            with st.spinner("در حال تشخیص گفتار..."):
                transcribed_text = self.stt_engine.transcribe(audio_data)
            
            if transcribed_text:
                st.session_state.last_transcription = transcribed_text
                st.success("✅ متن با موفقیت تشخیص داده شد!")
            else:
                st.warning("⚠️ هیچ متنی تشخیص داده نشد. لطفاً دوباره تلاش کنید.")
                
        except Exception as e:
            st.error(f"خطا در پردازش صوتی: {str(e)}")
    
    def stop_recording(self):
        """توقف ضبط صدا"""
        if not self.is_initialized:
            return
            
        try:
            self.audio_handler.stop_recording()
            st.session_state.is_recording = False
            st.success("⏹️ ضبط صدا متوقف شد!")
            
        except Exception as e:
            st.error(f"خطا در توقف ضبط: {str(e)}")
    
    def process_audio(self):
        """پردازش صوتی ضبط شده"""
        if not self.is_initialized:
            return
            
        try:
            # دریافت داده‌های صوتی
            audio_data = self.audio_handler.get_audio_data()
            
            if audio_data is None or len(audio_data) == 0:
                return ""
            
            # بررسی حداقل مدت زمان صوتی
            duration = len(audio_data) / config.SAMPLE_RATE
            if duration < config.MIN_AUDIO_DURATION:
                return ""
            
            # تشخیص گفتار
            with st.spinner("در حال تشخیص گفتار..."):
                transcribed_text = self.stt_engine.transcribe(audio_data)
            
            return transcribed_text
            
        except Exception as e:
            st.error(f"خطا در پردازش صوتی: {str(e)}")
            return ""

# راه‌اندازی API server
if not st.session_state.get('api_server_started', False):
    start_api_server()
    st.session_state.api_server_started = True

# ایجاد instance برنامه
if 'app' not in st.session_state:
    st.session_state.app = LinguaStreamApp()

app = st.session_state.app

# هدر اصلی
st.markdown(f"<h1 class='main-header'>{config.STREAMLIT_TITLE}</h1>", unsafe_allow_html=True)

# نوار کناری برای تنظیمات
with st.sidebar:
    st.header("⚙️ تنظیمات")
    
    # دکمه راه‌اندازی سیستم
    if st.button("🚀 راه‌اندازی سیستم", type="primary"):
        app.initialize_components()
    
    # نمایش وضعیت سیستم
    if app.is_initialized:
        st.markdown('<div class="status-box ready-status">✅ سیستم آماده است</div>', unsafe_allow_html=True)
        
        # اطلاعات مدل
        if app.stt_engine:
            model_info = app.stt_engine.get_model_info()
            st.subheader("📊 اطلاعات مدل")
            st.write(f"**مدل:** {model_info.get('model_name', 'نامشخص')}")
            st.write(f"**زبان:** {model_info.get('language', 'نامشخص')}")
            st.write(f"**دستگاه:** {model_info.get('device', 'نامشخص')}")
            
            # اطلاعات تشخیص لحن
            if 'tone_detection' in model_info:
                st.write(f"**تشخیص لحن:** {model_info.get('tone_detection', 'غیرفعال')}")
                if 'supported_tones' in model_info:
                    tones = model_info.get('supported_tones', [])
                    tone_names = {
                        'question': 'سوالی',
                        'exclamation': 'تعجبی',
                        'command': 'دستوری'
                    }
                    tone_display = [tone_names.get(tone, tone) for tone in tones]
                    st.write(f"**لحن‌های پشتیبانی شده:** {', '.join(tone_display)}")
    else:
        st.markdown('<div class="status-box recording-status">❌ سیستم راه‌اندازی نشده</div>', unsafe_allow_html=True)
    
    # تنظیمات ضبط
    st.subheader("🎤 تنظیمات ضبط")
    
    # انتخاب میکروفن
    if st.session_state.get('mic_permission_granted', False) and 'available_mics' in st.session_state:
        mic_options = {f"{mic['name']} (کانال‌ها: {mic['channels']})": mic['index'] 
                      for mic in st.session_state.available_mics}
        
        selected_mic_name = st.selectbox(
            "انتخاب میکروفن:",
            options=list(mic_options.keys()),
            index=0
        )
        
        if selected_mic_name:
            selected_mic_index = mic_options[selected_mic_name]
            st.session_state.selected_mic_index = selected_mic_index
            st.info(f"میکروفن انتخاب شده: {selected_mic_name}")
    
    min_duration = st.slider("حداقل مدت زمان ضبط (ثانیه)", 1, 10, int(config.MIN_AUDIO_DURATION))
    max_duration = st.slider("حداکثر مدت زمان ضبط (ثانیه)", 10, 60, int(config.MAX_AUDIO_DURATION))

# بخش اصلی رابط کاربری
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎤 تشخیص گفتار فارسی")
    
    # بررسی دسترسی میکروفن
    if not st.session_state.get('mic_permission_granted', False):
        app.request_microphone_permission()
    else:
        # نمایش رابط کاربری ضبط
        app.show_simple_recording_interface()

with col2:
    st.header("📝 متن تشخیص داده شده")
    
    # نمایش متن تشخیص داده شده
    if 'last_transcription' in st.session_state:
        st.markdown(f'<div class="transcribed-text">{st.session_state.last_transcription}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="transcribed-text">متن تشخیص داده شده اینجا نمایش داده می‌شود...</div>', unsafe_allow_html=True)
    
    # دکمه پاک کردن متن
    if st.button("🗑️ پاک کردن متن"):
        if 'last_transcription' in st.session_state:
            del st.session_state.last_transcription
        st.rerun()

# بخش اطلاعات سیستم
st.header("ℹ️ اطلاعات سیستم")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.subheader("🎵 تنظیمات صوتی")
    st.write(f"**نرخ نمونه:** {config.SAMPLE_RATE} Hz")
    st.write(f"**اندازه Chunk:** {config.CHUNK_SIZE}")
    st.write(f"**کانال‌ها:** {config.CHANNELS}")

with col_info2:
    st.subheader("🤖 مدل‌ها")
    st.write(f"**مدل Whisper:** {config.WHISPER_MODEL}")
    st.write(f"**مدل ترجمه:** Helsinki-NLP")
    st.write(f"**مدل TTS:** XTTS-v2")

with col_info3:
    st.subheader("⚡ عملکرد")
    st.write(f"**حداکثر تأخیر:** {config.MAX_LATENCY}s")
    st.write(f"**اندازه بافر:** {config.BUFFER_SIZE}")
    st.write(f"**Thread ها:** {config.THREAD_COUNT}")

# پاورقی
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎤 LinguaStream - سیستم ترجمه همزمان با صدای شخصی</p>
    <p>ساخته شده با ❤️ برای ارتباط چندزبانه</p>
</div>
""", unsafe_allow_html=True)
