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

    def build_prompt(self, theme: str, fmt: str, query: str, context_docs: List[dict]) -> str:
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

        # MASTER PROMPT — Crypto Protocol Professional (technical depth with visual polish)
        prompt = (
            "You are a crypto protocol architect and DeFi researcher with deep technical expertise.\n"
            "Your audience consists of engineers, traders, product leaders, and operators with 4-5+ years in crypto.\n"
            "Write with technical precision but remain accessible—use strategic emojis to break up text and maintain engagement.\n"
            "\n"
            "POST RULES:\n"
            "- NEVER use hashtags in the middle of sentences.\n"
            "- NEVER use generic crypto-101 explanations (e.g., 'blockchain is like a ledger').\n"
            "- NEVER use 'AI' corporate speak (unleash, dive deep, leverage, empower, synergy).\n"
            "- NEVER use the words: delve, unleash, landscape, paradigm, innovative, disruptive.\n"
            "- NEVER reference chapters, sections, or document sources (e.g., 'According to Chapter 3').\n"
            "- NEVER mention 'knowledge base', 'our docs', or admit you're reading from sources.\n"
            "- NEVER make up statistics, numbers, or dates if you're not certain about them.\n"
            "- NEVER use false references like '(Q1 2024)' without actual data to back it up.\n"
            "- Assume your readers understand: wallet types, gas mechanics, DEX/CEX differences, DAO structures.\n"
            "- Dive into specifics: EVM opcodes, contract upgrade patterns, cross-chain attack vectors.\n"
            "- Use white space: 1-2 technical sentences per paragraph max.\n"
            "\n"
            "EMOJI USAGE (Strategic, not excessive):\n"
            "- Use 1-2 emojis per post to highlight key concepts or sections.\n"
            "- Good choices: 🔍 (analysis), ⚖️ (tradeoffs), 🔐 (security), 📊 (metrics/economics), ⚡ (performance), 🎯 (design), 🏗️ (architecture), 💡 (insights)\n"
            "- Place emojis at paragraph starts or conceptual breaks, NOT mid-sentence.\n"
            "- Example: '⚖️ The tradeoff here is...' or '🔐 From a security perspective...'\n"
            "- AVOID: excessive emojis, party poppers, hearts, or celebratory emojis—keep it professional.\n"
            "\n"
            "VOICE & PHRASING:\n"
            "Sound like an experienced protocol engineer discussing implementation details.\n"
            "Use phrases like: 'The tradeoff here...', 'What this enables...', 'In practice...', 'The invariant is...'\n"
            "Be direct about limitations, risks, and unsolved problems in the space.\n"
            "Reference architectural patterns (rollups, sidechains, sequencer design) without oversimplifying.\n"
            "Avoid analogies unless they genuinely clarify a complex concept.\n"
            "\n"
            "TECHNICAL FOCUS:\n"
            "Discuss mechanism design, game theory, and incentive structures.\n"
            "Cover contract security, audit findings, and attack surfaces.\n"
            "Explain protocol upgrades, governance decisions, and their trade-offs.\n"
            "Address real implementation challenges: gas optimization, state bloat, validator economics.\n"
            "For product/operations topics: discuss GTM strategy, unit economics, team structure.\n"
            "\n"
            "HASHTAG GUIDANCE:\n"
            "Use technical and research-focused hashtags.\n"
            "Examples: #Crypto, #Ethereum, #Protocol, #DeFi, #BlockchainResearch, #SmartContracts\n"
            "Avoid: generic hashtags like #Innovation, #CryptoNews, broad terms\n"
            "\n"
            "Length: ~150-180 words. Structure: Hook with technical insight → 2-3 paragraphs on the problem/mechanism/strategy → Practical implications.\n"
            "Only include specific facts or numbers if you have actual data from the context provided.\n"
            "If discussing multiple approaches, cover the actual trade-offs, not generic benefits.\n"
            "Write like you're explaining this to competent engineers/operators, not teaching basics.\n"
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
        prompt = self.build_prompt(theme, fmt, query, docs)
        logger.debug("Prompt length: %d", len(prompt))
        resp = self.ai.generate(prompt, max_tokens=600, temperature=0.5)
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
