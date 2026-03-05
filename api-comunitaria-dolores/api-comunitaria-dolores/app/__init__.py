"""
Fábrica de aplicaciones Flask.
"""
from flask import Flask, jsonify
from .config import active_config
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    """Configura logging profesional"""
    if not os.path.exists('logs'):
        os.mkdir('logs')

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )

    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=1024 * 1024,
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL'], logging.INFO))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)


def register_blueprints(app):
    """Registra todos los blueprints"""
    from .routes import health_bp, artesanos_bp, errors_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(artesanos_bp)
    app.register_blueprint(errors_bp)
    app.logger.debug("Blueprints registrados correctamente")


def register_error_handlers(app):
    """Registra manejadores de errores globales"""
    from .exceptions.api_exceptions import APIError

    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'not_found',
            'message': 'Recurso no encontrado',
            'status_code': 404,
            'success': False
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Error interno: {error}")
        return jsonify({
            'error': 'internal_server_error',
            'message': 'Error interno del servidor',
            'status_code': 500,
            'success': False
        }), 500


def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(active_config)

    setup_logging(app)
    register_blueprints(app)
    register_error_handlers(app)

    app.logger.info(f"✅ {app.config['PROJECT_NAME']} iniciada correctamente")
    app.logger.info(f"🔧 Modo: {app.config.get('FLASK_CONFIG', 'dev')}")
    return app
