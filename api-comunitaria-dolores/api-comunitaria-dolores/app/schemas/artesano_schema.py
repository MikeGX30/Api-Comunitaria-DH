"""
Esquemas para validación y serialización de artesanos.
"""
from typing import Dict, Any, List


class ArtesanoSchema:

    REQUIRED_FIELDS = ['nombre', 'oficio']

    FIELD_TYPES = {
        'nombre': str,
        'oficio': str,
        'comunidad': str,
        'años_experiencia': int,
        'activo': bool
    }

    DEFAULTS = {
        'comunidad': 'No especificada',
        'años_experiencia': 0,
        'activo': True
    }

    @classmethod
    def validate_create(cls, data: Dict[str, Any]) -> Dict[str, List[str]]:
        errors = {}

        for field in cls.REQUIRED_FIELDS:
            if field not in data:
                errors[field] = ['Campo requerido']
            elif not isinstance(data[field], cls.FIELD_TYPES[field]):
                errors[field] = [f'Debe ser de tipo {cls.FIELD_TYPES[field].__name__}']

        for field, expected_type in cls.FIELD_TYPES.items():
            if field in data and field not in errors:
                if not isinstance(data[field], expected_type):
                    errors[field] = [f'Debe ser de tipo {expected_type.__name__}']

        if 'años_experiencia' in data and isinstance(data['años_experiencia'], int):
            if data['años_experiencia'] < 0:
                errors['años_experiencia'] = ['No puede ser negativo']
            elif data['años_experiencia'] > 100:
                errors['años_experiencia'] = ['Valor poco realista (máximo 100)']

        return errors

    @classmethod
    def validate_update(cls, data: Dict[str, Any]) -> Dict[str, List[str]]:
        errors = {}

        for field, value in data.items():
            if field in cls.FIELD_TYPES:
                if not isinstance(value, cls.FIELD_TYPES[field]):
                    errors[field] = [f'Debe ser de tipo {cls.FIELD_TYPES[field].__name__}']

        if 'años_experiencia' in data and isinstance(data.get('años_experiencia'), int):
            if data['años_experiencia'] < 0:
                errors['años_experiencia'] = ['No puede ser negativo']
            elif data['años_experiencia'] > 100:
                errors['años_experiencia'] = ['Valor poco realista']

        return errors

    @classmethod
    def prepare_for_create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        prepared = cls.DEFAULTS.copy()
        prepared.update(data)
        return prepared

    @classmethod
    def serialize(cls, artesano: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': artesano.get('id'),
            'nombre': artesano.get('nombre'),
            'oficio': artesano.get('oficio'),
            'comunidad': artesano.get('comunidad'),
            'años_experiencia': artesano.get('años_experiencia'),
            'activo': artesano.get('activo', True)
        }

    @classmethod
    def serialize_many(cls, artesanos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [cls.serialize(a) for a in artesanos]
