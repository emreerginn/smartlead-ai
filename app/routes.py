import hmac
from flask import Blueprint, request, jsonify, render_template
from config import Config
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

sayfalar_bp = Blueprint('sayfalar', __name__)
api_bp = Blueprint('api', __name__)


def yetkili_mi(kullanici, sifre):
    if not Config.DASH_USER or not Config.DASH_PASS:
        return False
    if not isinstance(kullanici, str) or not isinstance(sifre, str):
        return False
    return (
        hmac.compare_digest(kullanici.encode(), Config.DASH_USER.encode())
        and hmac.compare_digest(sifre.encode(), Config.DASH_PASS.encode())
    )


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
    gecmis = veri.get('gecmis', [])  # Varsa önceki mesaj geçmişini alır

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