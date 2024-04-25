import abc
import json
from typing import Any, Optional, Dict


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния."""

    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище."""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Получить состояние из хранилища."""
        pass


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл."""

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        if self.file_path:
            with open(self.file_path, 'w') as file:
                json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        if not self.file_path:
            return {}
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        current_state = self.storage.retrieve_state()
        current_state[key] = value
        self.storage.save_state(current_state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        current_state = self.storage.retrieve_state()
        return current_state.get(key, None)
