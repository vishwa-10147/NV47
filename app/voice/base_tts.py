from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseTTSProvider(ABC):
    """Base interface for all Text-to-Speech providers."""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the TTS engine. Return True if successful."""
        pass
        
    @abstractmethod
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Return a list of available voices. 
        Each dict should contain: id, name, language, gender
        """
        pass
        
    @abstractmethod
    def speak(self, text: str, voice_id: str, rate: int = 150, volume: float = 1.0) -> bool:
        """
        Speak the provided text synchronously (or blocking within its own thread).
        """
        pass
        
    @abstractmethod
    def stop(self) -> None:
        """Stop current speech synthesis."""
        pass
        
    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the provider can be used (e.g., online or engine available)."""
        pass
