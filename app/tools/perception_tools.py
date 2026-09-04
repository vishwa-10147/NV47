import ctypes

def get_active_window() -> dict:
    """Returns the title of the currently active (foreground) window."""
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if not hwnd:
            return {"success": True, "active_window": "None (No active window)"}
            
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
        return {"success": True, "active_window": buf.value}
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_visible_windows() -> dict:
    """Returns a list of all visible window titles."""
    try:
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        titles = []
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buf, length + 1)
                    if buf.value:
                        titles.append(buf.value)
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)
        return {"success": True, "windows": titles}
    except Exception as e:
        return {"success": False, "error": str(e)}
