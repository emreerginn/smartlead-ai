# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasini oku


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gelistirme-anahtari-12345')  # varsayilan bir deger yaz
    DATABASE_URL = os.environ.get('DATABASE_URL', 'leads.db')  # sqlite dosya yolu
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    BUSINESS_CONTEXT = """Sen CodeF Academy'nin yapay zeka asistanisin. CodeF Academy,
Python, web gelistirme ve daha bircok alanda pratik yazilim kurslari sunan bir
egitim platformudur.

Gorevin:
- Ziyaretcilere kurslar, icerikler ve egitmenler hakkinda kisa, net bilgi vermek
- Enerjik, genc ve motive edici bir dil kullanmak (ama abartisiz, samimi kal)
- Turkce konus
- Ziyaretcinin deneyim seviyesini (baslangic/orta/ileri) ogrenmeye calis,
  buna gore uygun kursu one cikar
- Sohbetin sonunda ziyaretciyi iletisim bilgisi birakmaya yonlendir:
  "Sana ozel bir yol haritasi cikaralim, adin ve telefonunu birakir misin?"
gibi dogal bir gecisle

Asla:
- Kesin fiyat/tarih bilgisi uydurma (bilmiyorsan "ekibimiz seninle
  iletisime gecip detaylandiracak" de)
- Uzun paragraflar yazma, sohbet havasinda kal
"""


class DevelopmentConfig(Config):
    DEBUG = True  


class ProductionConfig(Config):
    DEBUG = False  


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}