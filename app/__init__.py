from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app.database import init_db
from app.routes import sayfalar_bp, api_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    with app.app_context():
        init_db(app)

    app.register_blueprint(sayfalar_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/health')
    def health_check():
        return jsonify({
            "basari": True,
            "durum": "aktif",
            "mesaj": "Sunucu sorunsuz calisiyor."
        }), 200

    return app
