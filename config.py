"""Configuration and brand information for ValtriLabs LinkedIn automation."""
from typing import List, Dict

PROFILES = {
    "valtrilabs": {
        "company_info": {
            "name": "ValtriLabs",
            "services": "Virtual assistant services: admin support, calendar management, lead qualification, research, and operations",
            "audience": "Founders, solopreneurs, small business owners, and busy executives",
            "value_prop": "Reliable, skilled virtual assistants that let leaders focus on growth while we handle the day-to-day",
        },
        "content_themes": [
            "VA benefits",
            "productivity tips",
            "case studies",
            "client wins",
            "tooling & automation",
            "pricing transparency",
        ],
        "hashtags": [
            "#VirtualAssistant",
            "#Productivity",
            "#SmallBusiness",
            "#Founders",
            "#RemoteWork",
        ],
    },
    "arab_global_crypto": {
        "company_info": {
            "name": "Arab Global Crypto Exchange",
            "services": "Centralized exchange: Crypto trading, custody, KYC, liquidity, and institutional-grade security (Fireblocks)",
            "audience": "Crypto traders, exchanges, institutional clients, product teams in fintech",
            "value_prop": "Secure, compliant, and high-performance centralized exchange across India & UAE",
        },
        "content_themes": [
            "Crypto product updates",
            "Blockchain & decentralization",
            "DeFi vs CeFi",
            "KYC & compliance",
            "Exchange security and Fireblocks",
            "NFT & marketplace trends",
        ],
        "hashtags": [
            "#Crypto",
            "#Blockchain",
            "#NFT",
            "#DeFi",
            "#CeFi",
            "#Fireblocks",
        ],
    },
}

POST_FORMATS: List[str] = [
    "educational",
    "question",
    "story",
    "list",
    "myth-busting",
]

BRAND_VOICE: Dict[str, str] = {
    "tone": "Professional, approachable, and helpful",
    "dos": "Short paragraphs, actionable tips, clear CTAs, human examples",
    "donts": "Overly salesy language, long dense paragraphs, vague claims",
}

LINKEDIN_BEST_PRACTICES: Dict[str, int] = {
    "min_length": 150,
    "max_length": 300,
}

DEFAULT_SCHEDULE = {"hour": 11, "minute": 0}

# Default profile key to use. Can be overridden by env var CONTENT_PROFILE
DEFAULT_PROFILE = "valtrilabs"


DEFAULT_SCHEDULE = {"hour": 11, "minute": 0}
