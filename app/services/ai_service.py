import logging
import requests
from config import Config

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    pass


class AIService:
    MAX_GECMIS = 10   # Groq'a gönderilecek en fazla önceki mesaj sayısı
    TIMEOUT = 30      # saniye

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = 'openai/gpt-oss-20b'
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'

    def _sistem_talimati(self):
        return Config.BUSINESS_CONTEXT

    def _gecmisi_temizle(self, gecmis, mesaj):
        """
        Frontend'den gelen geçmişi Groq'un beklediği formata çevirir.
        Gelen:  {"role": "user" | "bot", "text": "..."}
        Giden:  {"role": "user" | "assistant", "content": "..."}
        """
        temiz = []
        for m in gecmis or []:
            if not isinstance(m, dict):
                continue

            icerik = m.get("content") or m.get("text")
            if not icerik or not isinstance(icerik, str):
                continue

            rol_ham = m.get("role")
            if rol_ham in ("bot", "assistant"):
                rol = "assistant"
            elif rol_ham == "user":
                rol = "user"
            else:
                continue  # "system" vb. rolleri istemciden kabul etme

            temiz.append({"role": rol, "content": icerik})

        # Frontend güncel mesajı geçmişe de ekliyor; aynı mesaj iki kez gitmesin
        if temiz and temiz[-1]["role"] == "user" and temiz[-1]["content"].strip() == mesaj.strip():
            temiz.pop()

        return temiz[-self.MAX_GECMIS:]

    def yanit_uret(self, mesaj, gecmis=None):
        if not self.api_key:
            return "Demo modundayiz: API anahtari tanimli degil. Gercek yanit icin GROQ_API_KEY ayarlanmali."

        mesajlar = [{"role": "system", "content": self._sistem_talimati()}]
        mesajlar.extend(self._gecmisi_temizle(gecmis, mesaj))
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
            response = requests.post(
                self.api_url, headers=headers, json=payload, timeout=self.TIMEOUT
            )
        except requests.exceptions.RequestException as e:
            logger.error("Groq baglanti hatasi: %s", e)
            raise AIServiceError(f"Yapay zeka servisine ulasilamadi: {str(e)}")

        if not response.ok:
            # Groq'un asil hata sebebi Render loglarinda gorunsun
            logger.error("GROQ HATASI %s: %s", response.status_code, response.text)
            raise AIServiceError(
                f"Yapay zeka servisi hata verdi ({response.status_code}): {response.text[:300]}"
            )

        try:
            veri = response.json()
            icerik = veri['choices'][0]['message'].get('content')
        except (ValueError, KeyError, IndexError, TypeError) as e:
            logger.error("Groq beklenmeyen yanit: %s", e)
            raise AIServiceError(f"API yaniti beklenmeyen formatta: {str(e)}")

        if not icerik:
            raise AIServiceError("Yapay zeka bos yanit dondurdu.")

        return icerik


ai_service = AIService()