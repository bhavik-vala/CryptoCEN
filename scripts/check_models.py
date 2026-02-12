#!/usr/bin/env python
"""Check available Google Gemini models and verify API access."""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not set in .env")
    sys.exit(1)

try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    print("✓ Google GenAI configured successfully")
    
    # Attempt to list models
    try:
        models = genai.list_models()
        print("\n✓ Available models:")
        for m in models:
            print(f"  - {m.name}")
            if hasattr(m, 'supported_generation_methods'):
                print(f"    Methods: {m.supported_generation_methods}")
    except Exception as e:
        print(f"⚠ Could not list models: {e}")
        print("  (This is okay—API key works but list_models may be restricted)")
    
    # Try a test generation with gemini-2.5-flash
    print("\n✓ Testing generation with gemini-2.5-flash...")
    from google.generativeai import GenerativeModel
    model = GenerativeModel("gemini-2.5-flash")
    resp = model.generate_content("Say 'Hello' in one word")
    if resp and resp.text:
        print(f"  Response: {resp.text[:100]}")
        print("✓ Generation successful!")
    else:
        print("⚠ No response text (but call succeeded)")
    
except ImportError:
    print("ERROR: google-generativeai not installed")
    print("Run: pip install google-generativeai")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
