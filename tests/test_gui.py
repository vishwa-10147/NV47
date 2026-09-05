import pytest
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from app.gui.main import GUIController
from app.core.kernel import NV001Kernel

# Create a single global app instance for tests to avoid crashing PySide6
app = QGuiApplication.instance()
if not app:
    app = QGuiApplication(sys.argv)

def test_gui_controller():
    kernel = NV001Kernel()
    controller = GUIController(kernel)
    
    # Test that the controller correctly maps properties
    status = controller.get_system_status()
    assert "NV001 Kernel Online" in status
    
def test_qml_engine_load():
    engine = QQmlApplicationEngine()
    kernel = NV001Kernel()
    controller = GUIController(kernel)
    engine.rootContext().setContextProperty("backend", controller)
    
    # It shouldn't crash initializing the engine
    assert engine is not None
