// Audio Recorder برای ضبط صدا در مرورگر
class AudioRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.stream = null;
        this.audioContext = null;
        this.analyser = null;
        this.microphone = null;
        this.dataArray = null;
        this.animationId = null;
    }

    async requestMicrophonePermission() {
        try {
            // درخواست دسترسی به میکروفن
            this.stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    sampleRate: 16000,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });

            // ایجاد AudioContext برای پردازش صدا
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
                sampleRate: 16000
            });

            // ایجاد Analyser برای نمایش سطح صدا
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            this.microphone = this.audioContext.createMediaStreamSource(this.stream);
            this.microphone.connect(this.analyser);

            this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);

            console.log('Microphone access granted');
            return true;
        } catch (error) {
            console.error('Error accessing microphone:', error);
            return false;
        }
    }

    startRecording() {
        if (!this.stream) {
            console.error('No microphone stream available');
            return false;
        }

        try {
            // ایجاد MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, {
                mimeType: 'audio/webm;codecs=opus'
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
            this.mediaRecorder.start(100); // جمع‌آوری داده هر 100ms

            console.log('Recording started');
            return true;
        } catch (error) {
            console.error('Error starting recording:', error);
            return false;
        }
    }

    stopRecording() {
        if (!this.mediaRecorder || !this.isRecording) {
            return null;
        }

        return new Promise((resolve) => {
            this.mediaRecorder.onstop = () => {
                // ترکیب تمام chunk های صوتی
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                this.isRecording = false;
                console.log('Recording stopped');
                resolve(audioBlob);
            };

            this.mediaRecorder.stop();
        });
    }

    getAudioLevel() {
        if (!this.analyser || !this.dataArray) {
            return 0;
        }

        this.analyser.getByteFrequencyData(this.dataArray);
        
        // محاسبه میانگین سطح صدا
        let sum = 0;
        for (let i = 0; i < this.dataArray.length; i++) {
            sum += this.dataArray[i];
        }
        
        return sum / this.dataArray.length;
    }

    startAudioLevelMonitoring(callback) {
        const updateLevel = () => {
            if (this.isRecording) {
                const level = this.getAudioLevel();
                callback(level);
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
    }

    cleanup() {
        this.stopAudioLevelMonitoring();
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        
        if (this.audioContext) {
            this.audioContext.close();
        }
        
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
    }

    // تبدیل Blob به ArrayBuffer برای ارسال به سرور
    async blobToArrayBuffer(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsArrayBuffer(blob);
        });
    }

    // تبدیل ArrayBuffer به WAV (ساده)
    async convertToWav(arrayBuffer) {
        // این یک پیاده‌سازی ساده است
        // در عمل، ممکن است نیاز به کتابخانه‌های پیچیده‌تری باشد
        return arrayBuffer;
    }
}

// ایجاد instance سراسری
window.audioRecorder = new AudioRecorder();
