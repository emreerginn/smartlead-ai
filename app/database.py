import sqlite3
from datetime import datetime
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_URL'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db(app):
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                seviye TEXT,
                tarih TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS ogretmenler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT NOT NULL UNIQUE,
                sifre_hash TEXT NOT NULL,
                ad_soyad TEXT
            )
        ''')
        db.commit()

def lead_ekle(isim, telefon, mesaj, seviye):
    db = get_db()
    tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute(
        'INSERT INTO leads (isim, telefon, mesaj, seviye, tarih) VALUES (?, ?, ?, ?, ?)',
        (isim, telefon, mesaj, seviye, tarih)
    )
    db.commit()

def tum_leadler():
    db = get_db()
    satirlar = db.execute('SELECT * FROM leads ORDER BY id DESC').fetchall()
    return [dict(satir) for satir in satirlar]

def ogretmen_ekle(kullanici_adi, sifre_hash, ad_soyad=''):
    db = get_db()
    db.execute(
        'INSERT INTO ogretmenler (kullanici_adi, sifre_hash, ad_soyad) VALUES (?, ?, ?)',
        (kullanici_adi, sifre_hash, ad_soyad)
    )
    db.commit()

def ogretmen_bul(kullanici_adi):
    db = get_db()
    satir = db.execute(
        'SELECT * FROM ogretmenler WHERE kullanici_adi = ?', (kullanici_adi,)
    ).fetchone()
    return dict(satir) if satir else None