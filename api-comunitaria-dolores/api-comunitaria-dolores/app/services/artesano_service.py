"""
Servicio de artesanos.
Contiene toda la lógica de negocio.
"""
from typing import List, Dict, Any, Optional
from ..repositories.artesano_repository_impl import InMemoryArtesanoRepository
from ..models.interfaces.artesano_repository import ArtesanoRepository
from ..schemas.artesano_schema import ArtesanoSchema
from ..exceptions.api_exceptions import (
    ResourceNotFoundError,
    ValidationError,
    BusinessRuleError
)


class ArtesanoService:

    def __init__(self, repository: Optional[ArtesanoRepository] = None):
        self.repository = repository or InMemoryArtesanoRepository()

    def get_all_artesanos(self) -> List[Dict[str, Any]]:
        artesanos = self.repository.get_all()
        return ArtesanoSchema.serialize_many(artesanos)

    def get_artesano_by_id(self, artesano_id: int) -> Dict[str, Any]:
        artesano = self.repository.get_by_id(artesano_id)
        if not artesano:
            raise ResourceNotFoundError('Artesano', artesano_id)
        return ArtesanoSchema.serialize(artesano)

    def create_artesano(self, data: Dict[str, Any]) -> Dict[str, Any]:
        errors = ArtesanoSchema.validate_create(data)
        if errors:
            raise ValidationError(errors)

        prepared_data = ArtesanoSchema.prepare_for_create(data)

        # Regla de negocio: no duplicar mismo nombre en misma comunidad
        existing = self.repository.find_by_comunidad(prepared_data.get('comunidad', ''))
        for artesano in existing:
            if artesano.get('nombre', '').lower() == prepared_data.get('nombre', '').lower():
                raise BusinessRuleError(
                    f"Ya existe un artesano llamado '{prepared_data['nombre']}' "
                    f"en la comunidad '{prepared_data['comunidad']}'"
                )

        created = self.repository.create(prepared_data)
        return ArtesanoSchema.serialize(created)

    def update_artesano(self, artesano_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        existing = self.repository.get_by_id(artesano_id)
        if not existing:
            raise ResourceNotFoundError('Artesano', artesano_id)

        errors = ArtesanoSchema.validate_update(data)
        if errors:
            raise ValidationError(errors)

        updated = self.repository.update(artesano_id, data)
        return ArtesanoSchema.serialize(updated)

    def delete_artesano(self, artesano_id: int) -> None:
        existing = self.repository.get_by_id(artesano_id)
        if not existing:
            raise ResourceNotFoundError('Artesano', artesano_id)

        deleted = self.repository.delete(artesano_id)
        if not deleted:
            raise BusinessRuleError(f"No se pudo eliminar el artesano {artesano_id}")

    def find_artesanos_by_oficio(self, oficio: str) -> List[Dict[str, Any]]:
        artesanos = self.repository.find_by_oficio(oficio)
        return ArtesanoSchema.serialize_many(artesanos)

    def find_artesanos_by_comunidad(self, comunidad: str) -> List[Dict[str, Any]]:
        artesanos = self.repository.find_by_comunidad(comunidad)
        return ArtesanoSchema.serialize_many(artesanos)
