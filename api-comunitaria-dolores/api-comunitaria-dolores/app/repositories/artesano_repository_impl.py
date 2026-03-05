"""
Implementación en memoria del repositorio de artesanos.
Útil para desarrollo y pruebas sin base de datos.
"""
from typing import List, Optional, Dict, Any
from ..models.interfaces.artesano_repository import ArtesanoRepository
from ..models.dummy_data import artesanos_dummy


class InMemoryArtesanoRepository(ArtesanoRepository):

    def __init__(self):
        self._artesanos = [a.copy() for a in artesanos_dummy]
        self._next_id = len(self._artesanos) + 1

    def get_all(self) -> List[Dict[str, Any]]:
        return [a for a in self._artesanos if a.get('activo', True)]

    def get_by_id(self, artesano_id: int) -> Optional[Dict[str, Any]]:
        for artesano in self._artesanos:
            if artesano['id'] == artesano_id:
                return artesano.copy()
        return None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        new_artesano = data.copy()
        new_artesano['id'] = self._next_id
        self._next_id += 1
        self._artesanos.append(new_artesano)
        return new_artesano.copy()

    def update(self, artesano_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for i, artesano in enumerate(self._artesanos):
            if artesano['id'] == artesano_id:
                self._artesanos[i].update(data)
                return self._artesanos[i].copy()
        return None

    def delete(self, artesano_id: int) -> bool:
        for i, artesano in enumerate(self._artesanos):
            if artesano['id'] == artesano_id:
                self._artesanos.pop(i)
                return True
        return False

    def find_by_oficio(self, oficio: str) -> List[Dict[str, Any]]:
        return [
            a for a in self._artesanos
            if a.get('activo', True) and
            a.get('oficio', '').lower() == oficio.lower()
        ]

    def find_by_comunidad(self, comunidad: str) -> List[Dict[str, Any]]:
        return [
            a for a in self._artesanos
            if a.get('activo', True) and
            a.get('comunidad', '').lower() == comunidad.lower()
        ]
