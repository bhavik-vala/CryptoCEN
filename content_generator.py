"""Generate LinkedIn posts using RAG retrieval and AI providers."""
from typing import List, Dict, Any
import os
import logging
from datetime import datetime
import json
from rag_system import RAGStore
from ai_provider import AIProvider
import config

logger = logging.getLogger("valtrilabs.content_generator")


class ContentGenerator:
    def __init__(self, rag: RAGStore, ai: AIProvider, save_path: str = "data/posts.json"):
        self.rag = rag
        self.ai = ai
        self.save_path = save_path
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        except Exception:
            pass

    def build_prompt(self, theme: str, fmt: str, context_docs: List[dict]) -> str:
        # Compose prompt with retrieved context and brand info
        ctx_text = "\n---\n".join([d.get("document", "") for d in context_docs[:4]])
        # determine profile info
        profile_key = os.getenv("CONTENT_PROFILE", config.DEFAULT_PROFILE)
        profile = config.PROFILES.get(profile_key, config.PROFILES[config.DEFAULT_PROFILE])
        company_name = profile["company_info"]["name"]
        brand_tone = config.BRAND_VOICE.get("tone", "Professional")
        
        # Enhanced prompt for technical, educational content
        prompt = (
            f"You are a technical educator and thought leader in crypto and blockchain.\n"
            f"Brand voice: {brand_tone}, authoritative, insightful, teach-first.\n"
            f"Theme: {theme}. Format: {fmt}.\n"
            f"\n"
            f"CRITICAL INSTRUCTIONS:\n"
            f"1. LEAD with a concrete technical insight (first line). Not a question, not generic.\n"
            f"2. EDUCATE: Explain the concept clearly. Use data-backed insights.\n"
            f"3. GROUND claims in the provided context/data (actual mechanics, standards).\n"
            f"4. PROVIDE VALUE: Why traders/builders/users should care about this.\n"
            f"5. END with a thoughtful CTA: Invite discussion on implications or deeper aspects.\n"
            f"6. TONE: Expert, educational, not salesy. Assume readers are traders/developers.\n"
            f"\n"
            f"Length: 200-400 words. Structure: Hook → Technical explanation → Why it matters → CTA\n"
            f"Hashtags: 4-6 technical/specific tags (e.g., #BlockchainTech, #FuturesTrading, #Custody)\n"
            f"\n"
            f"CONTEXT DATA (ground claims here):\n"
            f"{ctx_text}\n"
            f"\n"
            f"Output: Plain text post with hook, body, CTA, and hashtags (space-separated)."
        )
        return prompt

    def generate_post(self, theme: str, fmt: str, query: str) -> Dict[str, Any]:
        docs = self.rag.similarity_search(query, k=4)
        prompt = self.build_prompt(theme, fmt, docs)
        logger.debug("Prompt length: %d", len(prompt))
        resp = self.ai.generate(prompt, max_tokens=600, temperature=0.2)
        text = resp.get("text", "").strip()
        # basic trimming and hashtags extraction
        hashtags = [p for p in text.splitlines()[-1].split() if p.startswith("#")] if text else []
        post = {
            "theme": theme,
            "format": fmt,
            "query": query,
            "content": text,
            "hashtags": hashtags,
            "provider": resp.get("provider"),
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        self._save_post(post)
        return post

    def _save_post(self, post: Dict[str, Any]) -> None:
        try:
            data = []
            if os.path.exists(self.save_path):
                with open(self.save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            data.append(post)
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved post to %s", self.save_path)
        except Exception:
            logger.exception("Failed to save post")


if __name__ == "__main__":
    import dotenv, logging
    dotenv.load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    rag = RAGStore()
    ai = AIProvider()
    cg = ContentGenerator(rag, ai)
    post = cg.generate_post(theme="productivity tips", fmt="list", query="how virtual assistants improve productivity")
    print(post.get("content", ""))
