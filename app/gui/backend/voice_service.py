from PySide6.QtCore import QObject, Slot, Signal, Property
import threading

class VoiceService(QObject):
    """Exposes VoiceManager capabilities to the QML GUI safely."""
    
    statusChanged = Signal()
    voicesLoaded = Signal(list)
    
    def __init__(self, voice_manager):
        super().__init__()
        self.manager = voice_manager
        
    @Slot(result=list)
    def get_available_voices(self):
        return self.manager.get_available_voices()
        
    @Slot(result=dict)
    def get_config(self):
        return self.manager.config
        
    @Slot(str)
    def preview_voice(self, text):
        # Spoken via the queue to avoid freezing PySide6
        self.manager.speak(text)
        
    @Slot(str, float)
    def update_setting(self, key, value):
        self.manager.config[key] = value
        self.manager.save_config()
        self.statusChanged.emit()
        
    @Slot()
    def stop_speaking(self):
        self.manager.stop_speaking()
        self.statusChanged.emit()
        
    @Slot(result=dict)
    def get_status(self):
        return self.manager.get_status()
