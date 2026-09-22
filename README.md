# SmartLead AI — CodeF Academy

Ziyaretçilerle yapay zekâ üzerinden sohbet eden ve iletişim bilgilerini (lead) toplayan, Flask backend + Wix Velo frontend mimarisiyle kurulmuş bir sistem. **CodeF Academy** (online kodlama akademisi) konseptine uyarlanmıştır.

## Canlı Bağlantılar

| | |
|---|---|
| **Wix Sitesi (canlı)** | https://emreerginn390.wixsite.com/codefacademy |
| **Yönetim Paneli (Dashboard)** | https://emreerginn390.wixsite.com/codefacademy/dashboard |
| **Backend API (Render)** | https://smartlead-ai-xd2r.onrender.com |
| **GitHub Reposu** | https://github.com/emreerginn/smartlead-ai |

## Projenin Amacı

CodeF Academy, üniversite öğrencilerine, kariyer değiştirenlere ve yazılıma yeni başlayanlara proje odaklı, birebir mentorluklu eğitim sunan bir online kodlama akademisidir. Site üzerindeki yapay zekâ asistanı ziyaretçilerin deneyim seviyesini öğrenip uygun kursu önerir ve iletişim bilgisi bırakmaya yönlendirir; toplanan lead'ler backend'de saklanır ve bir yönetim panelinde listelenir.

## Mimari

Separation of Concerns ilkesine göre katmanlara ayrılmış Flask backend:

```
smartlead_ai/
├── run.py                  # Sunucu giriş noktası
├── config.py                # Ayarlar ve .env okuma
├── requirements.txt
├── .env                     # (Git'e dahil değil)
├── .gitignore
└── app/
    ├── __init__.py           # Uygulama fabrikası (create_app)
    ├── database.py           # SQLite işlemleri (SADECE burada SQL var)
    ├── routes.py             # HTTP rotaları (yönlendirme, iş mantığı yok)
    └── services/
        └── ai_service.py     # Groq AI çağrıları (SADECE burada)
```

- **database.py** dışında hiçbir yerde SQL sorgusu yoktur; parametreler `?` yer tutucusuyla geçilir (SQL Injection koruması).
- **ai_service.py** dışında hiçbir yerde yapay zekâ API çağrısı yoktur.
- **routes.py** yalnızca bu iki katmanın fonksiyonlarını çağırır, doğrulama yapar ve JSON döner.
- Frontend (Wix Velo), backend'e yalnızca REST API üzerinden `wix-fetch` ile bağlanır.

## Kullanılan Teknolojiler

- **Backend:** Python, Flask, Flask-CORS, SQLite, Gunicorn
- **Yapay Zekâ:** Groq API (`openai/gpt-oss-20b` modeli)
- **Frontend:** Wix Editor + Velo (JavaScript)
- **Barındırma:** Render (backend), Wix (frontend)
- **Versiyon Kontrolü:** GitHub

## API Uç Noktaları

| Metod | Yol | Açıklama |
|---|---|---|
| GET | `/health` | Sunucu canlılık kontrolü |
| POST | `/api/sohbet` | Kullanıcı mesajını AI'a iletir, yanıt döner |
| POST | `/api/leads` | Yeni lead kaydı ekler (isim, telefon zorunlu) |
| GET | `/api/leads` | Tüm lead kayıtlarını listeler |

### Örnek istek — `/api/sohbet`
```json
POST /api/sohbet
{ "mesaj": "Python kursunuz var mı?" }

→ { "basari": true, "cevap": "Evet! Başlangıç seviyesi..." }
```

### Örnek istek — `/api/leads`
```json
POST /api/leads
{ "isim": "Ahmet Yılmaz", "telefon": "05551234567", "mesaj": "...", "seviye": "baslangic" }

→ { "basari": true, "mesaj": "Kayit alindi." }
```

## Yerelde Çalıştırma

```bash
git clone https://github.com/emreerginn/smartlead-ai.git
cd smartlead-ai
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

`.env` dosyası oluştur:
```
GROQ_API_KEY=gsk_...
SECRET_KEY=gelistirme-anahtari
DATABASE_URL=leads.db
AI_PROVIDER=groq
CORS_ORIGINS=*
```

```bash
python run.py
```

Tarayıcıda `http://localhost:5000/health` adresi `{"durum": "aktif"}` dönerse ortam hazırdır.

## Wix Velo Entegrasyonu

Wix Editor'de **Dev Mode** açılarak iki sayfaya kod eklendi:

- **Home sayfası:** Sohbet kutusu (`txtMesaj`, `btnSor`, `txtCevap`) ve lead formu (`txtIsim`, `txtTelefon`, `btnKaydet`, `txtDurum`) elemanları, `wix-fetch` ile `/api/sohbet` ve `/api/leads` uç noktalarına bağlanır.
- **Dashboard sayfası:** Bir `Repeater` bileşeni, sayfa yüklendiğinde `GET /api/leads`'ten veri çekip her lead için bir kart (`txtRepIsim`, `txtRepTelefon`, `txtRepMesaj`, `txtRepTarih`) oluşturur.

## Güvenlik Notları

- `GROQ_API_KEY` ve `SECRET_KEY` yalnızca `.env` dosyasında tutulur; `.gitignore` ile GitHub'a gönderilmesi engellenmiştir.
- SQL sorgularında parametre birleştirme yerine `?` yer tutucusu kullanılmıştır.
- Dış servis çağrıları (Groq API, veritabanı) `try/except` ile sarılmış, hata durumunda kullanıcıya güvenli bir JSON hata mesajı döner (500/503 durum kodları).

## Yayınlama

- Backend, GitHub reposundan Render'a bağlanarak **Web Service** olarak deploy edildi (Build: `pip install -r requirements.txt`, Start: `gunicorn run:app`, Free plan).
- Ortam değişkenleri Render panelinden ayrıca tanımlandı.
- Wix sitesi Publish edilerek canlıya alındı.

---
*CodeF Academy — SmartLead AI Bitirme Projesi*
