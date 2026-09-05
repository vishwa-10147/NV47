def speak_text(text: str) -> dict:
    """Speaks the given text out loud using the local system Text-to-Speech engine."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Configure voice settings for a futuristic AI feel
        engine.setProperty('rate', 175)    # Slightly faster than average
        engine.setProperty('volume', 0.9)  # 90% volume
        
        # Try to find a female/AI sounding voice if on Windows
        voices = engine.getProperty('voices')
        for voice in voices:
            if "Zira" in voice.name or "Female" in voice.name:
                engine.setProperty('voice', voice.id)
                break
                
        print(f"\n[Voice Output] {text}")
        engine.say(text)
        engine.runAndWait()
        return {"success": True, "message": f"Successfully spoke text length: {len(text)}"}
    except ImportError:
        return {"success": False, "error": "pyttsx3 not installed. Cannot use voice."}
    except Exception as e:
        return {"success": False, "error": str(e)}
