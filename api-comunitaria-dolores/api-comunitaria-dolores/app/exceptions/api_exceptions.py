"""
Excepciones personalizadas para la API.
"""


class APIError(Exception):
    """Excepción base para errores de API"""

    def __init__(self, message: str, status_code: int = 400, payload: dict = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self) -> dict:
        rv = dict(self.payload)
        rv['error'] = self.__class__.__name__
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        rv['success'] = False
        return rv


class ResourceNotFoundError(APIError):
    def __init__(self, resource: str, resource_id):
        super().__init__(
            message=f"{resource} con id {resource_id} no encontrado",
            status_code=404
        )


class ValidationError(APIError):
    def __init__(self, errors: dict):
        super().__init__(
            message="Error de validación",
            status_code=400,
            payload={'validation_errors': errors}
        )


class BusinessRuleError(APIError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=422
        )


class DuplicateResourceError(APIError):
    def __init__(self, resource: str, field: str, value):
        super().__init__(
            message=f"{resource} con {field} '{value}' ya existe",
            status_code=409
        )
