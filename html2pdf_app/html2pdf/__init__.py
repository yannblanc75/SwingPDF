# __init__.py
from flask import Flask, render_template
from .extensions import csrf
from .blueprints.main import main_bp
import os
import logging

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['LOG_FILE']), exist_ok=True)
    # Logging
    logging.basicConfig(
        filename=app.config['LOG_FILE'],
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
    )
    # Sécurité headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
    # Extensions
    csrf.init_app(app)
    # Blueprints
    app.register_blueprint(main_bp)
    # Gestion erreurs
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404
    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        # Utilise UTC ou local selon ton besoin
        return {"current_year": datetime.utcnow().year}
    return app
