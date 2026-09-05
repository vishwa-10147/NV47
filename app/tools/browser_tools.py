import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def scrape_website(url: str) -> dict:
    """Scrapes raw text from a given URL without needing a heavy browser binary."""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) NV001 Agent'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
            
        # Parse text from HTML
        from html.parser import HTMLParser
        class TextParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.ignore = False
            def handle_starttag(self, tag, attrs):
                if tag in ("script", "style", "meta", "link", "noscript"):
                    self.ignore = True
            def handle_endtag(self, tag):
                if tag in ("script", "style", "meta", "link", "noscript"):
                    self.ignore = False
            def handle_data(self, data):
                if not self.ignore and data.strip():
                    self.text.append(data.strip())
                    
        parser = TextParser()
        parser.feed(html)
        content = " ".join(parser.text)
        
        # Truncate to avoid exploding context windows
        return {"success": True, "url": url, "content": content[:4000] + "..."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def play_voice(text: str) -> dict:
    """Mock text-to-speech entrypoint."""
    # In a full system, this would use pyttsx3 or whisper
    print(f"\n[Voice Output] {text}")
    return {"success": True, "message": "Voice played."}
