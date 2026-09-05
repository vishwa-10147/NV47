import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot

class GUIController(QObject):
    def __init__(self, kernel):
        super().__init__()
        self.kernel = kernel

    @Slot(result=str)
    def get_system_status(self):
        return "NV001 Kernel Online (PySide6 Connected)"

def start_gui():
    # We must import kernel inside to avoid circular issues
    from app.core.kernel import NV001Kernel
    
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Initialize Core System
    kernel = NV001Kernel()
    
    # Initialize Voice Manager
    from app.voice.voice_manager import VoiceManager
    voice_manager = VoiceManager()
    voice_manager.start_worker()
    
    kernel.start()
    
    # Setup Controllers
    from app.gui.backend.voice_service import VoiceService
    controller = GUIController(kernel)
    voice_service = VoiceService(voice_manager)
    
    engine.rootContext().setContextProperty("backend", controller)
    engine.rootContext().setContextProperty("voiceBackend", voice_service)
    
    # Load QML
    qml_file = Path(__file__).parent / "qml" / "Main.qml"
    engine.load(qml_file)
    
    if not engine.rootObjects():
        sys.exit(-1)
        
    ret = app.exec()
    kernel.stop()
    voice_manager.stop_worker()
    sys.exit(ret)

if __name__ == "__main__":
    start_gui()
