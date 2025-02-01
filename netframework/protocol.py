import json
from abc import ABC, abstractmethod
from typing import Any
from .errors import ProtocolError

class Protocol(ABC):
    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        """Serialize data to bytes."""
        pass
        
    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        """Deserialize bytes to data."""
        pass
        
    @abstractmethod
    def process(self, data: bytes) -> Any:
        """Process received data."""
        pass

class JSONProtocol(Protocol):
    def __init__(self):
        self.delimiter = b'\n'
        
    def serialize(self, data: Any) -> bytes:
        """Serialize data to JSON format with delimiter."""
        try:
            json_data = json.dumps(data)
            return json_data.encode('utf-8') + self.delimiter
        except Exception as e:
            raise ProtocolError(f"Serialization failed: {e}")
            
    def deserialize(self, data: bytes) -> Any:
        """Deserialize JSON data."""
        try:
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            raise ProtocolError(f"Deserialization failed: {e}")
            
    def process(self, data: bytes) -> Any:
        """Process received JSON data."""
        return self.deserialize(data)
