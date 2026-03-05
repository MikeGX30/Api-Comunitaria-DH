"""
Endpoints de salud de la API.
"""
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix='/api/health')


@health_bp.route('/', methods=['GET'])
def health():
    """GET /api/health/ — Estado general de la API"""
    return jsonify({
        'status': 'ok',
        'message': 'API Comunitaria Dolores Hidalgo funcionando correctamente',
        'success': True
    }), 200


@health_bp.route('/ping', methods=['GET'])
def ping():
    """GET /api/health/ping — Ping simple"""
    return jsonify({'ping': 'pong', 'success': True}), 200


@health_bp.route('/version', methods=['GET'])
def version():
    """GET /api/health/version — Información de versión"""
    from flask import current_app
    return jsonify({
        'version': current_app.config.get('API_VERSION', 'v1'),
        'project': current_app.config.get('PROJECT_NAME', ''),
        'environment': current_app.config.get('FLASK_CONFIG', 'dev'),
        'success': True
    }), 200
