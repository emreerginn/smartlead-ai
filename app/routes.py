from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from app.database import lead_ekle, tum_leadler, ogretmen_bul, ogretmen_ekle
from app.services.ai_service import ai_service, AIServiceError

sayfalar_bp = Blueprint('sayfalar', __name__)
api_bp = Blueprint('api', __name__)


def yetkili_mi(kullanici, sifre):
    if not isinstance(kullanici, str) or not isinstance(sifre, str):
        return False
    ogretmen = ogretmen_bul(kullanici)
    if not ogretmen:
        return False
    return check_password_hash(ogretmen['sifre_hash'], sifre)


@sayfalar_bp.route('/')
def anasayfa():
    return render_template('index.html')

@sayfalar_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json() or {}
    mesaj = veri.get('mesaj')
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alani zorunlu."}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj=mesaj, gecmis=gecmis)
        return jsonify({"basari": True, "cevap": cevap}), 200
    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), 503

@api_bp.route('/leads', methods=['POST'])
def leads_ekle():
    veri = request.get_json() or {}
    isim = veri.get('isim')
    telefon = veri.get('telefon')
    mesaj = veri.get('mesaj', '')
    seviye = veri.get('seviye', '')

    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "Isim ve telefon zorunlu."}), 400

    try:
        lead_ekle(isim, telefon, mesaj, seviye)
        return jsonify({"basari": True, "mesaj": "Kayit alindi."}), 201
    except Exception as e:
        return jsonify({"basari": False, "hata": str(e)}), 500

@api_bp.route('/leads/listele', methods=['POST'])
def leads_listele():
    veri = request.get_json(silent=True) or {}
    if not yetkili_mi(veri.get('kullanici'), veri.get('sifre')):
        return jsonify({"basari": False, "hata": "Yetkisiz."}), 401

    try:
        kayitlar = tum_leadler()
        return jsonify({"basari": True, "leadler": kayitlar}), 200
    except Exception:
        return jsonify({"basari": False, "hata": "Sunucu hatasi."}), 500

@api_bp.route('/ogretmen/ekle', methods=['POST'])
def ogretmen_ekle_endpoint():
    veri = request.get_json(silent=True) or {}

    # Basit koruma: sadece SECRET_KEY'i bilen ekleyebilsin
    if veri.get('anahtar') != Config.SECRET_KEY:
        return jsonify({"basari": False, "hata": "Yetkisiz."}), 401

    kullanici_adi = veri.get('kullanici_adi')
    sifre = veri.get('sifre')
    ad_soyad = veri.get('ad_soyad', '')

    if not kullanici_adi or not sifre:
        return jsonify({"basari": False, "hata": "Kullanici adi ve sifre zorunlu."}), 400

    try:
        sifre_hash = generate_password_hash(sifre)
        ogretmen_ekle(kullanici_adi, sifre_hash, ad_soyad)
        return jsonify({"basari": True, "mesaj": f"'{kullanici_adi}' eklendi."}), 201
    except Exception as e:
        return jsonify({"basari": False, "hata": str(e)}), 500