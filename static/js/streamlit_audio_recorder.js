// Streamlit Audio Recorder - کامپوننت ضبط صدا برای Streamlit
class StreamlitAudioRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.audioStream = null;
        this.audioContext = null;
        this.analyser = null;
        this.microphone = null;
        this.dataArray = null;
        this.animationId = null;
        this.timerInterval = null;
        this.startTime = null;
        
        // تنظیمات ضبط
        this.config = {
            sampleRate: 16000,
            channelCount: 1,
            mimeType: 'audio/webm;codecs=opus',
            chunkInterval: 100
        };
        
        console.log('StreamlitAudioRecorder initialized');
    }
    
    async requestMicrophonePermission() {
        try {
            // بررسی پشتیبانی مرورگر
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('مرورگر شما از ضبط صدا پشتیبانی نمی‌کند');
            }
            
            // درخواست دسترسی به میکروفن
            this.audioStream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    sampleRate: this.config.sampleRate,
                    channelCount: this.config.channelCount,
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            
            // ایجاد AudioContext برای پردازش صدا
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
                sampleRate: this.config.sampleRate
            });
            
            // ایجاد Analyser برای نمایش سطح صدا
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            this.microphone = this.audioContext.createMediaStreamSource(this.audioStream);
            this.microphone.connect(this.analyser);
            
            this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
            
            // ذخیره وضعیت دسترسی
            localStorage.setItem('microphonePermission', 'granted');
            
            console.log('Microphone access granted');
            return true;
        } catch (error) {
            console.error('Error accessing microphone:', error);
            localStorage.removeItem('microphonePermission');
            return false;
        }
    }
    
    async startRecording() {
        try {
            // بررسی دسترسی میکروفن
            if (!this.audioStream) {
                const hasPermission = await this.requestMicrophonePermission();
                if (!hasPermission) {
                    throw new Error('دسترسی به میکروفن رد شد');
                }
            }
            
            // ایجاد MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.audioStream, {
                mimeType: this.config.mimeType
            });
            
            this.audioChunks = [];
            this.isRecording = true;
            
            // ذخیره داده‌های صوتی
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            // شروع ضبط
            this.mediaRecorder.start(this.config.chunkInterval);
            
            // شروع تایمر
            this.startTime = Date.now();
            this.timerInterval = setInterval(() => this.updateTimer(), 100);
            
            // شروع نمایش سطح صدا
            this.startAudioLevelMonitoring();
            
            console.log('Recording started');
            return true;
        } catch (error) {
            console.error('Error starting recording:', error);
            return false;
        }
    }
    
    async stopRecording() {
        try {
            if (!this.mediaRecorder || !this.isRecording) {
                return null;
            }
            
            return new Promise((resolve) => {
                this.mediaRecorder.onstop = () => {
                    // ترکیب تمام chunk های صوتی
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                    this.isRecording = false;
                    
                    // توقف تایمر و نمایش سطح صدا
                    if (this.timerInterval) {
                        clearInterval(this.timerInterval);
                        this.timerInterval = null;
                    }
                    this.stopAudioLevelMonitoring();
                    
                    console.log('Recording stopped');
                    resolve(audioBlob);
                };
                
                this.mediaRecorder.stop();
            });
        } catch (error) {
            console.error('Error stopping recording:', error);
            return null;
        }
    }
    
    updateTimer() {
        if (!this.startTime) return;
        
        const elapsed = Date.now() - this.startTime;
        const minutes = Math.floor(elapsed / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        
        const timerElement = document.getElementById('recordingTimer');
        if (timerElement) {
            timerElement.textContent = 
                String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
        }
    }
    
    startAudioLevelMonitoring() {
        if (!this.analyser || !this.dataArray) return;
        
        const updateLevel = () => {
            if (this.isRecording) {
                this.analyser.getByteFrequencyData(this.dataArray);
                
                // محاسبه میانگین سطح صدا
                let sum = 0;
                for (let i = 0; i < this.dataArray.length; i++) {
                    sum += this.dataArray[i];
                }
                const level = sum / this.dataArray.length;
                const percentage = Math.min(level * 2, 100);
                
                const levelBar = document.getElementById('audioLevelBar');
                if (levelBar) {
                    levelBar.style.width = percentage + '%';
                }
                
                this.animationId = requestAnimationFrame(updateLevel);
            }
        };
        updateLevel();
    }
    
    stopAudioLevelMonitoring() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        
        const levelBar = document.getElementById('audioLevelBar');
        if (levelBar) {
            levelBar.style.width = '0%';
        }
    }
    
    async processRecordedAudio(audioBlob) {
        try {
            // ارسال فایل به سرور برای پردازش
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');
            
            const response = await fetch('/api/process_audio', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                return result;
            } else {
                throw new Error('خطا در ارسال فایل به سرور');
            }
        } catch (error) {
            console.error('Error processing audio:', error);
            return { success: false, error: error.message };
        }
    }
    
    cleanup() {
        this.stopAudioLevelMonitoring();
        
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        
        if (this.audioStream) {
            this.audioStream.getTracks().forEach(track => track.stop());
            this.audioStream = null;
        }
        
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
        
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.startTime = null;
        
        console.log('StreamlitAudioRecorder cleaned up');
    }
    
    // متدهای کمکی برای UI
    updateUI(status, message) {
        const statusElement = document.getElementById('recordingStatus');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.style.color = this.getStatusColor(status);
        }
    }
    
    getStatusColor(status) {
        const colors = {
            'ready': '#666',
            'recording': '#ff4444',
            'processing': '#ff9800',
            'success': '#4CAF50',
            'error': '#f44336'
        };
        return colors[status] || '#666';
    }
}

// ایجاد instance سراسری
window.streamlitAudioRecorder = new StreamlitAudioRecorder();

// توابع سراسری برای استفاده در HTML
window.startWebRecording = async function() {
    const success = await window.streamlitAudioRecorder.startRecording();
    if (success) {
        // تغییر وضعیت UI
        document.getElementById('recordBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'inline-block';
        window.streamlitAudioRecorder.updateUI('recording', 'در حال ضبط...');
    } else {
        alert('خطا در شروع ضبط: دسترسی به میکروفن رد شد');
    }
};

window.stopWebRecording = async function() {
    const audioBlob = await window.streamlitAudioRecorder.stopRecording();
    if (audioBlob) {
        // تغییر وضعیت UI
        document.getElementById('recordBtn').style.display = 'inline-block';
        document.getElementById('stopBtn').style.display = 'none';
        window.streamlitAudioRecorder.updateUI('processing', 'پردازش صدا...');
        
        // پردازش فایل صوتی
        const result = await window.streamlitAudioRecorder.processRecordedAudio(audioBlob);
        
        if (result.success) {
            window.streamlitAudioRecorder.updateUI('success', 
                `✅ متن تشخیص داده شد: ${result.transcription}`);
        } else {
            window.streamlitAudioRecorder.updateUI('error', 
                `❌ خطا: ${result.error}`);
        }
    }
};

// بررسی دسترسی میکروفن هنگام بارگذاری صفحه
window.addEventListener('load', async () => {
    try {
        // بررسی پشتیبانی مرورگر
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.error('مرورگر شما از ضبط صدا پشتیبانی نمی‌کند');
            return;
        }
        
        // بررسی دسترسی قبلی
        const permission = localStorage.getItem('microphonePermission');
        if (permission === 'granted') {
            console.log('دسترسی میکروفن قبلاً تأیید شده است');
            // درخواست دسترسی برای اطمینان
            const success = await window.streamlitAudioRecorder.requestMicrophonePermission();
            if (success) {
                console.log('دسترسی میکروفن تأیید شد');
            } else {
                console.log('دسترسی میکروفن رد شد');
                localStorage.removeItem('microphonePermission');
            }
        } else {
            console.log('دسترسی میکروفن هنوز تأیید نشده است');
        }
    } catch (error) {
        console.error('Error checking microphone permission:', error);
    }
});
