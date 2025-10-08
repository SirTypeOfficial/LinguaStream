import whisper
import config

class STTEngine:
    def __init__(self):
        print("Loading Whisper model...")
        # The model will be downloaded if not found
        self.model = whisper.load_model(config.WHISPER_MODEL)
        print("Whisper model loaded.")

    def transcribe(self, audio_data):
        """
        Transcribes audio data (numpy array) to text.
        """
        result = self.model.transcribe(audio_data, language="fa", fp16=False) # fp16=False for CPU compatibility
        return result["text"]