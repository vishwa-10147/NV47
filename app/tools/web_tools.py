from app.knowledge.engine import KnowledgeEngine

knowledge_engine = KnowledgeEngine()

def search_and_learn(query: str = "") -> dict:
    """Uses the KnowledgeEngine to search for a query and extract facts."""
    if not query:
        return {"success": False, "error": "Query cannot be empty."}
        
    return knowledge_engine.acquire_knowledge(query)
