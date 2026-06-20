import os
from google import genai
from google.genai import errors

class AIService:
    """PDF metinlerini yapay zeka ile özetleyen ve soru-cevaplayan servis."""
    
    def __init__(self):
        # API anahtarını çevre değişkenlerinden (Environment Variables) güvenli bir şekilde okuyoruz
        self.api_key = os.getenv("GEMINI_API_KEY")
        self._client = None

    @property
    def client(self) -> genai.Client:
        """İhtiyaç anında (Lazy Initialization) Gemini Client'ını başlatır."""
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY bulunamadı! Lütfen API anahtarınızı ayarlayın.")
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def summarize_text(self, text: str) -> str:
        """Verilen metnin profesyonel bir yönetici özetini çıkarır."""
        if not text.strip():
            return "Özetlenecek metin bulunamadı."
            
        prompt = (
            f"Aşağıdaki metni analiz et ve kurumsal bir dille, "
            f"en önemli maddeleri vurgulayarak profesyonel bir yönetici özeti çıkar:\n\n{text}"
        )
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except errors.APIError as e:
            return f"Yapay Zeka API Hatası: {str(e)}"
        except Exception as e:
            return f"Beklenmedik bir hata oluştu: {str(e)}"