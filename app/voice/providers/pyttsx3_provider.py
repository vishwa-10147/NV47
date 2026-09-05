import pyttsx3
import threading
from typing import List, Dict, Any
from app.voice.base_tts import BaseTTSProvider

class Pyttsx3Provider(BaseTTSProvider):
    """Offline system TTS provider using pyttsx3."""
    
    def __init__(self):
        self.engine = None
        self._lock = threading.Lock()
        self._is_speaking = False
        
    def initialize(self) -> bool:
        try:
            self.engine = pyttsx3.init()
            return True
        except Exception as e:
            print(f"[Pyttsx3Provider] Initialization failed: {e}")
            return False

    def get_available_voices(self) -> List[Dict[str, Any]]:
        if not self.engine:
            return []
            
        voices_list = []
        try:
            voices = self.engine.getProperty('voices')
            for v in voices:
                # Attempt to determine gender (often unreliable in pyttsx3, so we check name/id)
                gender = "female" if "Zira" in v.name or "female" in v.name.lower() or "Hazel" in v.name else "unknown"
                if "David" in v.name or "male" in v.name.lower():
                    gender = "male"
                    
                voices_list.append({
                    "id": v.id,
                    "name": v.name,
                    "language": getattr(v, "languages", ["unknown"])[0] if hasattr(v, "languages") and v.languages else "unknown",
                    "gender": gender
                })
        except Exception as e:
            print(f"[Pyttsx3Provider] Failed to get voices: {e}")
            
        return voices_list

    def speak(self, text: str, voice_id: str, rate: int = 150, volume: float = 1.0) -> bool:
        with self._lock:
            if not self.engine:
                return False
                
            self._is_speaking = True
            try:
                # Pyttsx3 comtypes can crash if manipulated heavily across threads, 
                # but we'll try to re-init if it's dead, or just use the existing engine safely.
                if voice_id:
                    self.engine.setProperty('voice', voice_id)
                self.engine.setProperty('rate', rate)
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
                
                self.engine.say(text)
                self.engine.runAndWait()
                return True
            except Exception as e:
                print(f"[Pyttsx3Provider] Speech failed: {e}")
                return False
            finally:
                self._is_speaking = False

    def stop(self) -> None:
        if self.engine and self._is_speaking:
            try:
                self.engine.stop()
            except Exception:
                pass

    def is_available(self) -> bool:
        return self.engine is not None
