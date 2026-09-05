import os
from datetime import datetime
from uuid import uuid4

class SemanticMemory:
    """Manages Vector-based RAG Memory using ChromaDB for advanced retrieval."""
    
    def __init__(self, persist_dir: str = "app/memory/chroma_db"):
        self.persist_dir = persist_dir
        self.collection = None
        self._setup()
        
    def _setup(self):
        try:
            import chromadb
            os.makedirs(self.persist_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.client.get_or_create_collection(name="nv001_semantic_memory")
            print("[Semantic Memory] ChromaDB initialized successfully.")
        except ImportError:
            print("[Semantic Memory] Warning: chromadb not installed. Semantic memory disabled.")
        except Exception as e:
            print(f"[Semantic Memory] Error initializing ChromaDB: {e}")

    def store_memory(self, text: str, metadata: dict = None) -> str:
        if not self.collection:
            return None
            
        doc_id = str(uuid4())
        meta = metadata or {}
        meta["timestamp"] = datetime.now().isoformat()
        
        try:
            self.collection.add(
                documents=[text],
                metadatas=[meta],
                ids=[doc_id]
            )
            return doc_id
        except Exception as e:
            print(f"[Semantic Memory] Failed to store memory: {e}")
            return None
            
    def search_memory(self, query: str, n_results: int = 3) -> list:
        if not self.collection:
            return []
            
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results into a clean list of dictionaries
            formatted_results = []
            if results and results.get("documents"):
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if "distances" in results else None
                    })
            return formatted_results
        except Exception as e:
            print(f"[Semantic Memory] Search failed: {e}")
            return []
