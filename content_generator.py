"""Generate LinkedIn posts using RAG retrieval and AI providers."""
from typing import List, Dict, Any
import os
import logging
from datetime import datetime
import json
import re
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

        # Optionally fetch a short market snapshot (CoinGecko) to ground recent prices
        # But only if the query seems to be about trading/prices/market
        market_snippet = ""
        try:
            if os.getenv("ENABLE_MARKET_GROUNDING", "false").lower() in ("1", "true"):
                # Only add market data if query/theme relates to trading, prices, or market metrics
                market_related_keywords = ["price", "trading", "market", "volatility", "pump", "dump", "bull", "bear", "liquidity", "volume"]
                query_lower = (query + " " + theme).lower()
                include_market = any(kw in query_lower for kw in market_related_keywords)
                
                if include_market:
                    import requests
                    ids = os.getenv("GROUND_TOKENS", "bitcoin,ethereum")
                    r = requests.get(
                        f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true",
                        timeout=10,
                    )
                    if r.ok:
                        data = r.json()
                        parts = []
                        for tk in ids.split(","):
                            if tk in data:
                                p = data[tk]
                                parts.append(f"{tk.upper()}: ${p.get('usd'):,} ({p.get('usd_24h_change'):+.2f}% 24h)")
                        if parts:
                            market_snippet = "Recent market snapshot: " + "; ".join(parts) + "."
        except Exception:
            logger.exception("Market grounding fetch failed")

        # MASTER PROMPT — Crypto Industry Expert persona (authoritative, data-driven, technical)
        prompt = (
            "You are a respected technical expert and thought leader in crypto and blockchain infrastructure.\n"
            "Your voice is rational, slightly contrarian, and technical. You write from deep industry experience.\n"
            "\n"
            "POST RULES:\n"
            "- NEVER use hashtags in the middle of sentences.\n"
            "- NEVER use 'AI' corporate speak (unleash, dive deep, comprehensive).\n"
            "- NEVER use the words: delve, unleash, landscape.\n"
            "- NEVER reference chapters, sections, or document sources (e.g., 'Chapter 7', 'Section 5').\n"
            "- NEVER mention 'knowledge base', 'our docs', or quote text that reads like textbook excerpts.\n"
            "- NEVER use hashtags like #ProductStrategy, #ProductLeadership, or company-specific tags.\n"
            "- NEVER say 'our exchange', 'my exchange', or any company-specific language. Use general industry language.\n"
            "- START with a hook that challenges common wisdom or presents a shocking stat.\n"
            "- END with a strategic takeaway for builders/operators in the industry.\n"
            "- Use white space: 1-2 sentences per paragraph max.\n"
            "\n"
            "VOICE & PHRASING:\n"
            "Write as an independent industry observer with hands-on crypto/blockchain experience.\n"
            "Use phrases like: 'We've seen...', 'In practice...', 'Teams often...', 'The reality is...', 'What works...'\n"
            "Paraphrase knowledge base content as industry trends and battle-tested practices.\n"
            "Ground claims in the provided context but express as general industry insights, not company-specific.\n"
            "Focus on technical realities, trade-offs, and what actually works in production crypto systems.\n"
            "\n"
            "HASHTAG GUIDANCE:\n"
            "Use technical, infrastructure, and blockchain-focused hashtags.\n"
            "Examples: #Crypto, #Blockchain, #DeFi, #Bitcoin, #Ethereum, #CryptoTech, #Layer2, #Finality, #Custody\n"
            "Avoid: #ProductStrategy, #ProductLeadership, #Innovation, #Disruption, industry/company-specific tags\n"
            "\n"
            "Length: ~150 words. Structure: Hook → 1-2 short paragraphs with data/technical focus → Strategic takeaway.\n"
            "Include at least one specific real-world event or price metric from the last 24-48 hours and mark its source/year in parentheses.\n"
            "IMPORTANT: Only mention token prices or market metrics if the topic is about trading, price discovery, market data, or liquidity.\n"
            "Do NOT force prices into posts about custody, security, architecture, or other non-trading topics.\n"
            "Do NOT use phrases that identify the writer as an AI. Sound like an experienced crypto operator/builder.\n"
            "Avoid marketing language; focus on measurable realities and technical implications for the industry.\n"
            "\n"
            "CONTEXT — Background Knowledge (paraphrase naturally, never cite chapters):\n"
            f"{ctx_text}\n"
            f"{market_snippet}\n"
            "\n"
            "Output: Plain LinkedIn post text only — hook, body, 1-line strategic takeaway, and final hashtags on their own line."
        )
        return prompt

    def generate_post(self, theme: str, fmt: str, query: str) -> Dict[str, Any]:
        docs = self.rag.similarity_search(query, k=4)
        prompt = self.build_prompt(theme, fmt, docs)
        logger.debug("Prompt length: %d", len(prompt))
        resp = self.ai.generate(prompt, max_tokens=600, temperature=0.2)
        text = resp.get("text", "").strip()
        # Post-process to remove stray markdown/asterisks and clean formatting
        try:
            # remove runs of asterisks inside text
            text = re.sub(r"\*{2,}", "", text)
            # strip leading/trailing asterisks/spaces on each line and remove empty lines
            lines = text.splitlines()
            cleaned = []
            for ln in lines:
                ln2 = re.sub(r"^[\s\*]+|[\s\*]+$", "", ln)
                if ln2:
                    cleaned.append(ln2)
            text = "\n".join(cleaned)
        except Exception:
            logger.exception("Post-processing cleanup failed")

        # improved hashtag extraction (find all hashtags anywhere in the text)
        hashtags = re.findall(r"#[-_A-Za-z0-9]+", text) if text else []
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
