from transformers import pipeline
import config

class Translator:
    def __init__(self):
        print("Loading translation model...")
        self.translator = pipeline("translation", model=config.TRANSLATION_MODEL_NAME)
        print("Translation model loaded.")

    def translate(self, text):
        """
        Translates text from Farsi to English.
        """
        if not text:
            return ""
        translated = self.translator(text)
        return translated[0]['translation_text']