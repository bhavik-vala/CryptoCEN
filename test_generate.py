from dotenv import load_dotenv
load_dotenv()
from rag_system import RAGStore
from ai_provider import AIProvider
from content_generator import ContentGenerator

rag = RAGStore(persist_dir="data/chroma_db")
ai = AIProvider()    # uses AI_PROVIDER from .env
cg = ContentGenerator(rag, ai)

post = cg.generate_post(
    theme="Derivatives & Perps",
    fmt="paragraph",
    query="funding rates funding arbitrage recent"
)
print("-----POST PREVIEW-----")
print(post["content"])
print("\n-----HASHTAGS-----\n", post["hashtags"])