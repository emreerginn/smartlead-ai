import requests
from config import Config

class AIServiceError(Exception):
    pass

class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = 'openai/gpt-oss-20b'   
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'

    def _sistem_talimati(self):
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        if not self.api_key:
            return "Demo modundayiz: API anahtari tanimli degil. Gercek yanit icin GROQ_API_KEY ayarlanmali."
        
        mesajlar = [{"role": "system", "content": self._sistem_talimati()}]
        if gecmis:
            mesajlar.extend(gecmis)
        mesajlar.append({"role": "user", "content": mesaj})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": mesajlar
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            veri = response.json()
            return veri['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zeka servisine ulasilamadi: {str(e)}")
        except (KeyError, IndexError) as e:
            raise AIServiceError(f"API yaniti beklenmeyen formatta: {str(e)}")

ai_service = AIService()