import os
from datetime import datetime

def take_screenshot() -> dict:
    """Takes a screenshot of the main monitor and saves it to memory."""
    try:
        import pyautogui
        save_dir = "app/memory/vision"
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(save_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return {"success": True, "path": filename, "message": f"Screenshot saved to {filename}"}
    except ImportError:
        return {"success": False, "error": "pyautogui or Pillow is not installed."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def mouse_click(x: int, y: int) -> dict:
    """Simulates a mouse click at the specified coordinates."""
    try:
        import pyautogui
        pyautogui.click(x=int(x), y=int(y))
        return {"success": True, "message": f"Clicked at ({x}, {y})"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def keyboard_type(text: str) -> dict:
    """Simulates typing text on the keyboard."""
    try:
        import pyautogui
        pyautogui.write(text, interval=0.05)
        return {"success": True, "message": f"Typed text length: {len(text)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
