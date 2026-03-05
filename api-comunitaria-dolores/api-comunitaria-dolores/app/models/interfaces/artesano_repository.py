"""
Interfaz del repositorio de artesanos.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class ArtesanoRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_id(self, artesano_id: int) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, artesano_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete(self, artesano_id: int) -> bool:
        pass

    @abstractmethod
    def find_by_oficio(self, oficio: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_comunidad(self, comunidad: str) -> List[Dict[str, Any]]:
        pass
