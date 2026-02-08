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
        prompt = (
            f"You are a professional content writer for {company_name}."
            f" Use brand voice: {brand_tone}.\n"
            f"Theme: {theme}. Format: {fmt}.\n"
            "Requirements: Create a LinkedIn post between 150-300 words. Strong hook in first 2 lines, short paragraphs, clear CTA, and 3-5 hashtags. Not salesy. Actionable.\n"
            "Context: Use the following extracted context to ground factual statements:\n"
            f"{ctx_text}\n"
            "Produce the post only (no metadata). At the end include a line of hashtags separated by spaces."
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
