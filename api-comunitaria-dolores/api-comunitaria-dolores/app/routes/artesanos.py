"""
Blueprint de artesanos.
"""
from flask import Blueprint, jsonify, request
from ..services.artesano_service import ArtesanoService
from ..exceptions.api_exceptions import APIError
import logging

artesanos_bp = Blueprint('artesanos', __name__, url_prefix='/api/artesanos')
artesano_service = ArtesanoService()
logger = logging.getLogger(__name__)


@artesanos_bp.route('/', methods=['GET'])
def listar_artesanos():
    """
    GET /api/artesanos/
    Query params opcionales: ?oficio=Alfarería  |  ?comunidad=El Llanito
    """
    try:
        oficio = request.args.get('oficio')
        comunidad = request.args.get('comunidad')

        if oficio:
            artesanos = artesano_service.find_artesanos_by_oficio(oficio)
            message = f"Artesanos filtrados por oficio: {oficio}"
        elif comunidad:
            artesanos = artesano_service.find_artesanos_by_comunidad(comunidad)
            message = f"Artesanos filtrados por comunidad: {comunidad}"
        else:
            artesanos = artesano_service.get_all_artesanos()
            message = "Listado completo de artesanos"

        logger.info(f"GET /artesanos - {len(artesanos)} artesanos retornados")
        return jsonify({
            'success': True,
            'message': message,
            'data': artesanos,
            'total': len(artesanos)
        }), 200

    except Exception as e:
        logger.error(f"Error en listar_artesanos: {str(e)}")
        raise


@artesanos_bp.route('/', methods=['POST'])
def crear_artesano():
    """
    POST /api/artesanos/
    Body JSON: { "nombre": "...", "oficio": "..." }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Se requieren datos en formato JSON'}), 400

        nuevo_artesano = artesano_service.create_artesano(data)
        logger.info(f"POST /artesanos - Creado artesano ID: {nuevo_artesano['id']}")

        return jsonify({
            'success': True,
            'message': 'Artesano creado exitosamente',
            'data': nuevo_artesano
        }), 201

    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error en crear_artesano: {str(e)}")
        raise


@artesanos_bp.route('/<int:artesano_id>', methods=['GET'])
def obtener_artesano(artesano_id):
    """GET /api/artesanos/{id}"""
    try:
        artesano = artesano_service.get_artesano_by_id(artesano_id)
        logger.info(f"GET /artesanos/{artesano_id} - Encontrado")
        return jsonify({'success': True, 'data': artesano}), 200
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error en obtener_artesano: {str(e)}")
        raise


@artesanos_bp.route('/<int:artesano_id>', methods=['PUT'])
def actualizar_artesano_completo(artesano_id):
    """PUT /api/artesanos/{id} — Reemplazo completo"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Se requieren datos en formato JSON'}), 400

        artesano = artesano_service.update_artesano(artesano_id, data)
        logger.info(f"PUT /artesanos/{artesano_id} - Actualizado completamente")
        return jsonify({
            'success': True,
            'message': 'Artesano actualizado completamente',
            'data': artesano
        }), 200
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error en actualizar_artesano_completo: {str(e)}")
        raise


@artesanos_bp.route('/<int:artesano_id>', methods=['PATCH'])
def actualizar_artesano_parcial(artesano_id):
    """PATCH /api/artesanos/{id} — Actualización parcial"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Se requieren datos en formato JSON'}), 400

        artesano = artesano_service.update_artesano(artesano_id, data)
        logger.info(f"PATCH /artesanos/{artesano_id} - Actualizado parcialmente")
        return jsonify({
            'success': True,
            'message': 'Artesano actualizado parcialmente',
            'data': artesano
        }), 200
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error en actualizar_artesano_parcial: {str(e)}")
        raise


@artesanos_bp.route('/<int:artesano_id>', methods=['DELETE'])
def eliminar_artesano(artesano_id):
    """DELETE /api/artesanos/{id}"""
    try:
        artesano_service.delete_artesano(artesano_id)
        logger.info(f"DELETE /artesanos/{artesano_id} - Eliminado")
        return '', 204
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Error en eliminar_artesano: {str(e)}")
        raise
