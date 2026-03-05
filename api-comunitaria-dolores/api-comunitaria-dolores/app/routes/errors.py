"""
Manejadores de errores HTTP personalizados.
"""
from flask import Blueprint, jsonify

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Recurso no encontrado',
        'message': 'La URL solicitada no existe en esta API',
        'success': False,
        'status_code': 404
    }), 404


@errors_bp.app_errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({
        'error': 'Método no permitido',
        'message': 'El verbo HTTP utilizado no está soportado para esta URL',
        'success': False,
        'status_code': 405
    }), 405


@errors_bp.app_errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Error interno del servidor',
        'message': 'Ha ocurrido un error inesperado',
        'success': False,
        'status_code': 500
    }), 500
