import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

class KnowledgeStore:
    def __init__(self, knowledge_dir: str = "app/knowledge/data"):
        self.knowledge_dir = Path(knowledge_dir)
        self.db_file = self.knowledge_dir / "facts.jsonl"
        self._setup()

    def _setup(self) -> None:
        try:
            self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Failed to create knowledge directory: {e}")

    def store_fact(self, topic: str, claim: str, source: str, confidence: float) -> None:
        try:
            record = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "topic": topic,
                "claim": claim,
                "source": source,
                "confidence": confidence,
                "verified": False
            }
            log_line = json.dumps(record, default=str)
            with open(self.db_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
        except Exception as e:
            print(f"Failed to store knowledge: {e}")

class KnowledgeEngine:
    """Manages web search, reading, and extraction of facts."""
    def __init__(self) -> None:
        self.store = KnowledgeStore()
        
    def search_web(self, query: str) -> List[Dict[str, str]]:
        import urllib.request
        import urllib.parse
        import json
        
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&utf8=&format=json"
        req = urllib.request.Request(url, headers={'User-Agent': 'NV001 Knowledge Engine'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                results = []
                # Get the top 3 results
                for item in data.get("query", {}).get("search", [])[:3]:
                    # Clean up basic HTML highlighting returned by Wikipedia
                    snippet = item["snippet"].replace('<span class="searchmatch">', '').replace('</span>', '')
                    snippet = snippet.replace('&quot;', '"').replace('&#039;', "'")
                    
                    results.append({
                        "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(item['title'].replace(' ', '_'))}", 
                        "snippet": snippet.strip()
                    })
                return results
        except Exception as e:
            print(f"[KnowledgeEngine] Web search failed: {e}")
            return []
        
    def acquire_knowledge(self, topic: str) -> dict:
        results = self.search_web(topic)
        facts_extracted = 0
        
        for res in results:
            claim = res["snippet"]
            source = res["url"]
            self.store.store_fact(topic=topic, claim=claim, source=source, confidence=0.75)
            facts_extracted += 1
            
        return {
            "success": True,
            "message": f"Acquired {facts_extracted} facts about '{topic}'.",
            "data": {
                "topic": topic, 
                "facts_extracted": facts_extracted,
                "facts": results
            }
        }
