import os
import json
import threading
import queue
from pathlib import Path
from typing import Dict, Any, List

from app.voice.providers.pyttsx3_provider import Pyttsx3Provider

class VoiceManager:
    """Manages TTS configuration, routing, and a background speech queue."""
    
    def __init__(self, config_path: str = "app/config/voice.json"):
        self.config_path = Path(config_path)
        self.config = {
            "enabled": True,
            "provider": "system",
            "voice_id": "",
            "profile": "default",
            "language": "en",
            "rate": 150,
            "volume": 0.9,
            "startup_greeting": True,
            "task_notifications": True,
            "warning_notifications": True
        }
        
        self.providers = {}
        self.active_provider = None
        
        self.speech_queue = queue.Queue(maxsize=10)
        self._stop_event = threading.Event()
        self._worker_thread = None
        self._currently_speaking = False
        
        self._load_config()
        self._init_providers()
        
    def _load_config(self) -> None:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"[VoiceManager] Failed to load config: {e}")
        else:
            self.save_config()

    def save_config(self) -> None:
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"[VoiceManager] Failed to save config: {e}")

    def _init_providers(self):
        # Register Pyttsx3 as the system provider
        sys_provider = Pyttsx3Provider()
        if sys_provider.initialize():
            self.providers["system"] = sys_provider
        
        self.active_provider = self.providers.get(self.config["provider"])
        
        # Auto-select best female voice if none is configured
        if self.active_provider and not self.config.get("voice_id"):
            voices = self.active_provider.get_available_voices()
            female_voices = [v for v in voices if v["gender"] == "female"]
            if female_voices:
                # Pick Zira or first female
                zira = next((v for v in female_voices if "Zira" in v["name"]), None)
                self.config["voice_id"] = zira["id"] if zira else female_voices[0]["id"]
                self.save_config()
                
    def start_worker(self):
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._stop_event.clear()
            self._worker_thread = threading.Thread(target=self._queue_worker, daemon=True)
            self._worker_thread.start()

    def stop_worker(self):
        self._stop_event.set()
        self.stop_speaking()
        if self._worker_thread:
            self._worker_thread.join(timeout=2)
            
    def _queue_worker(self):
        while not self._stop_event.is_set():
            try:
                text = self.speech_queue.get(timeout=0.5)
            except queue.Empty:
                continue
                
            if not self.config.get("enabled", True):
                self.speech_queue.task_done()
                continue
                
            if not self.active_provider:
                self.speech_queue.task_done()
                continue
                
            self._currently_speaking = True
            try:
                # Sanitize text slightly
                clean_text = self._sanitize_text(text)
                if clean_text:
                    self.active_provider.speak(
                        text=clean_text,
                        voice_id=self.config.get("voice_id", ""),
                        rate=self.config.get("rate", 150),
                        volume=self.config.get("volume", 0.9)
                    )
            finally:
                self._currently_speaking = False
                self.speech_queue.task_done()

    def _sanitize_text(self, text: str) -> str:
        # Prevent speaking long secrets or massive text
        if len(text) > 500:
            return text[:497] + "..."
        return text

    def speak(self, text: str, priority: int = 1):
        if not self.config.get("enabled", True):
            return
            
        try:
            self.speech_queue.put_nowait(text)
        except queue.Full:
            print("[VoiceManager] Speech queue full, dropping message.")
            
    def stop_speaking(self):
        # Empty queue
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
                self.speech_queue.task_done()
            except queue.Empty:
                break
                
        # Stop current speech
        if self.active_provider:
            self.active_provider.stop()
            
    def get_available_voices(self) -> List[Dict[str, Any]]:
        if self.active_provider:
            return self.active_provider.get_available_voices()
        return []
        
    def get_status(self) -> Dict[str, Any]:
        return {
            "enabled": self.config.get("enabled", True),
            "speaking": self._currently_speaking,
            "queue_size": self.speech_queue.qsize(),
            "provider": self.config.get("provider", "unknown")
        }
