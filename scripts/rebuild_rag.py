#!/usr/bin/env python
"""Rebuild RAG embeddings from PDFs/DOCX in data/pdfs."""
import os
import sys
import logging
from dotenv import load_dotenv

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from pdf_processor import load_pdfs, chunk_text
    from rag_system import RAGStore
    
    logger.info("Loading PDFs/DOCX from data/pdfs...")
    docs = load_pdfs("data/pdfs")
    
    if not docs:
        logger.warning("No PDFs/DOCX found in data/pdfs")
        sys.exit(0)
    
    logger.info(f"Loaded {len(docs)} documents")
    
    # Delete old chroma db to force rebuild
    import shutil
    db_path = "data/chroma_db"
    if os.path.exists(db_path):
        logger.info(f"Removing old {db_path}...")
        shutil.rmtree(db_path)
    
    # Build new RAG
    logger.info("Building RAG embeddings...")
    rag = RAGStore(persist_dir=db_path)
    rag.build_from_documents(docs)
    rag.persist()
    
    logger.info("✓ RAG rebuilt successfully")
    
except Exception as e:
    logger.exception(f"Failed to rebuild RAG: {e}")
    sys.exit(1)
