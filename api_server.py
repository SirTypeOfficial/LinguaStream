import streamlit as st
from flask import Flask, request, jsonify
import threading
import tempfile
import os
from src.audio_handler import AudioHandler
from src.stt_engine import STTEngine

# ایجاد Flask app برای API
api_app = Flask(__name__)

# ایجاد instance های سراسری
audio_handler = None
stt_engine = None

def initialize_api_components():
    """راه‌اندازی کامپوننت‌های API"""
    global audio_handler, stt_engine
    
    if audio_handler is None:
        audio_handler = AudioHandler()
    
    if stt_engine is None:
        stt_engine = STTEngine()

@api_app.route('/api/microphone-permission', methods=['POST'])
def handle_microphone_permission():
    """مدیریت درخواست دسترسی میکروفن"""
    try:
        data = request.get_json()
        if data and data.get('granted'):
            # در اینجا می‌توانید session state را به‌روزرسانی کنید
            return jsonify({'success': True, 'message': 'دسترسی میکروفن تأیید شد'})
        else:
            return jsonify({'success': False, 'error': 'دسترسی میکروفن رد شد'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_app.route('/api/process-audio', methods=['POST'])
def process_audio():
    """پردازش فایل صوتی آپلود شده"""
    try:
        # بررسی وجود فایل صوتی
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'فایل صوتی یافت نشد'})
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'فایل صوتی انتخاب نشده'})
        
        # راه‌اندازی کامپوننت‌ها
        initialize_api_components()
        
        # پردازش فایل صوتی
        audio_data = audio_handler.process_uploaded_audio(audio_file)
        
        if audio_data is None:
            return jsonify({'success': False, 'error': 'خطا در پردازش فایل صوتی'})
        
        # تشخیص گفتار
        transcribed_text = stt_engine.transcribe(audio_data)
        
        if transcribed_text:
            return jsonify({
                'success': True,
                'transcription': transcribed_text,
                'duration': len(audio_data) / 16000  # مدت زمان بر حسب ثانیه
            })
        else:
            return jsonify({'success': False, 'error': 'هیچ متنی تشخیص داده نشد'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@api_app.route('/api/health', methods=['GET'])
def health_check():
    """بررسی وضعیت API"""
    return jsonify({
        'status': 'healthy',
        'components': {
            'audio_handler': audio_handler is not None,
            'stt_engine': stt_engine is not None
        }
    })

def run_api_server(port=5000):
    """اجرای سرور API"""
    try:
        api_app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    except Exception as e:
        print(f"Error running API server: {e}")

# اجرای API در thread جداگانه
def start_api_server():
    """شروع سرور API در thread جداگانه"""
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()
    print(f"API server started on port 5000")
