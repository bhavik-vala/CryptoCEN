"""Unified AI provider interface for Claude, OpenAI, and Google Gemini."""
from typing import Optional, Dict
import os
import logging
import time

logger = logging.getLogger("valtrilabs.ai_provider")


class AIProvider:
    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("AI_PROVIDER", "google")).lower()
        logger.info("AI provider set to: %s (env=%s, param=%s)", self.provider, os.getenv("AI_PROVIDER", "NOT_SET"), provider)
        # lazy imports
        self._client = None

    def _init_anthropic(self):
        try:
            from anthropic import Anthropic
        except Exception:
            logger.exception("anthropic SDK not installed")
            raise
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        self._client = Anthropic(api_key=key)

    def _init_openai(self):
        try:
            from openai import OpenAI
        except Exception:
            logger.exception("openai SDK not installed")
            raise
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self._client = OpenAI(api_key=key)

    def _init_google(self):
        try:
            import google.generativeai as gai
        except Exception:
            logger.exception("google generative SDK not installed")
            raise
        key = os.getenv("GOOGLE_API_KEY")
        if not key:
            raise RuntimeError("GOOGLE_API_KEY not set")
        gai.configure(api_key=key)
        from google.generativeai import GenerativeModel
        self._client = gai

    def _ensure_client(self):
        if self._client:
            return
        try:
            if self.provider == "claude":
                self._init_anthropic()
            elif self.provider == "openai":
                self._init_openai()
            elif self.provider in ("google", "gemini"):
                self._init_google()
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logger.warning("Failed to init %s provider: %s. Falling back to Google.", self.provider, e)
            # Fall back to Google
            self.provider = "google"
            self._init_google()

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, str]:
        """Generate text from selected provider; returns dict with 'text' and metadata."""
        self._ensure_client()
        try:
            if self.provider == "claude":
                # Use Messages API (new)
                resp = self._client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                )
                text = resp.content[0].text
                return {"text": text, "provider": "claude"}
            elif self.provider == "openai":
                resp = self._client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                text = resp.choices[0].message.content
                return {"text": text, "provider": "openai"}
            else:
                # Google Gemini - use GenerativeModel
                from google.generativeai import GenerativeModel
                model = GenerativeModel("gemini-2.0-flash-exp")
                resp = model.generate_content(contents=prompt)
                text = resp.text if resp and resp.text else ""
                return {"text": text, "provider": "google"}
        except Exception:
            logger.exception("AI generation failed for provider %s", self.provider)
            raise


if __name__ == "__main__":
    import dotenv, logging
    dotenv.load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    api = AIProvider()
    try:
        out = api.generate("Write a short LinkedIn post about virtual assistants.")
        print(out.get("text", ""))
    except Exception as e:
        print("Generation failed:", e)
