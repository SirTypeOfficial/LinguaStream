import pyaudio
import numpy as np
import threading
import time
import config

from src.audio_handler import AudioHandler
from src.stt_engine import STTEngine
from src.translator import Translator
from src.tts_engine import TTSEngine

class LinguaStream:
    def __init__(self):
        self.audio_handler = AudioHandler()
        self.stt_engine = STTEngine()
        self.translator = Translator()
        self.tts_engine = TTSEngine()
        self.is_running = False

    def process_loop(self):
        """Main loop to capture, process, and play audio."""
        print("Starting real-time translation...")
        self.is_running = True
        
        while self.is_running:
            # 1. Capture audio chunk
            audio_chunk = self.audio_handler.capture_chunk()
            if audio_chunk is None:
                continue

            # 2. Speech-to-Text
            print("\nTranscribing...")
            farsi_text = self.stt_engine.transcribe(audio_chunk)
            print(f"Farsi: {farsi_text}")

            if not farsi_text:
                continue

            # 3. Translate
            print("Translating...")
            english_text = self.translator.translate(farsi_text)
            print(f"English: {english_text}")

            if not english_text:
                continue

            # 4. Text-to-Speech
            print("Synthesizing speech...")
            translated_audio_bytes = self.tts_engine.synthesize(english_text)
            
            if translated_audio_bytes:
                # 5. Play audio to virtual device
                self.audio_handler.play_audio(translated_audio_bytes)

    def run(self):
        try:
            # Run processing in a separate thread to keep main thread responsive
            processing_thread = threading.Thread(target=self.process_loop)
            processing_thread.start()
            
            # Keep the main thread alive
            while processing_thread.is_alive():
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nStopping LinguaStream...")
            self.is_running = False
        finally:
            self.audio_handler.cleanup()

if __name__ == "__main__":
    app = LinguaStream()
    app.run()