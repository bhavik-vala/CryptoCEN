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
            "audience": "Crypto traders, developers, institutional clients, product teams in fintech and blockchain",
            "value_prop": "Educational content on crypto trading, blockchain technology, and infrastructure for traders and builders",
        },
        "content_themes": [
            "Spot trading mechanics and order types",
            "Futures and perpetuals trading mechanics",
            "Options trading: Greeks, pricing, strategies",
            "Blockchain trilemma: scalability, security, decentralization",
            "PoW vs PoS: technical differences and validator economics",
            "Layer 1, Layer 2, Layer 0: scaling solutions deep dive",
            "Bitcoin halving: technical mechanics and historical effects",
            "Custody solutions: self-custody vs custodial wallets",
            "Fireblocks and MPC wallets: institutional custody tech",
            "Smart contracts and EVM-compatible chains",
            "Tokenomics and token launch strategies",
            "KYC/AML technical implementation in exchanges",
            "DeFi protocols: liquidity pools, AMMs, market making",
            "Matching engines and order book mechanics",
            "Liquidation engines and risk management",
            "MEV, sandwich attacks, and front-running mitigation",
            "Market making bots and liquidity provision",
            "Blockchain interoperability and bridges",
            "Staking mechanisms and yield economics",
            "Privacy coins and privacy technologies",
            "Cold storage vs hot wallets trade-offs",
            "Technical analysis for traders",
            "Blockchain nodes and infrastructure",
            "Mining economics and block rewards",
            "Stock-to-flow model and price prediction",
            "Oracle networks: Chainlink and price feeds",
            "BIP standards, SegWit, and transaction optimization",
            "NFTs, tokenization, and smart contracts",
            "Governance tokens and DAO mechanics",
            "Proof of Reserve and transparency",
            "Regulatory landscape and FIU requirements",
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
