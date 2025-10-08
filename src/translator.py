from transformers import pipeline
import config

class Translator:
    def __init__(self):
        self.translator = None
        self.model_loaded = False
        print("Translator initialized. Model will be loaded on first use.")

    def _load_model(self):
        """بارگذاری مدل ترجمه (فقط یک بار)"""
        if self.model_loaded:
            return
            
        try:
            print("Loading translation model...")
            # مدل به صورت خودکار دانلود می‌شود اگر موجود نباشد
            self.translator = pipeline("translation", model=config.TRANSLATION_MODEL_NAME)
            self.model_loaded = True
            print(f"Translation model '{config.TRANSLATION_MODEL_NAME}' loaded successfully.")
        except Exception as e:
            print(f"Error loading translation model: {e}")
            raise

    def translate(self, text):
        """
        ترجمه متن از فارسی به انگلیسی
        """
        if not text or not text.strip():
            return ""
            
        # بارگذاری مدل در صورت نیاز
        if not self.model_loaded:
            self._load_model()
        
        try:
            # ترجمه متن
            translated = self.translator(text)
            result = translated[0]['translation_text']
            
            if result:
                print(f"Translated: {result}")
                return result
            else:
                return ""
                
        except Exception as e:
            print(f"Error in translation: {e}")
            return ""

    def get_model_info(self):
        """دریافت اطلاعات مدل"""
        if not self.model_loaded:
            return "Model not loaded"
        
        return {
            "model_name": config.TRANSLATION_MODEL_NAME,
            "source_language": "Persian (fa)",
            "target_language": "English (en)"
        }