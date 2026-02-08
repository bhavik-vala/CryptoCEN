# Quickstart (5-minute)

1. Install Python 3.10+ and create a virtualenv.

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Copy `.env.template` to `.env` and fill API keys.

3. Add your PDFs to `data/pdfs/`.

4. Build knowledge base and preview a post:

```bash
python main.py
# choose option 1 to build KB, option 2 to run preview
```

5. To enable live posting, set `TEST_MODE=false` in `.env` and set `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_ID`.
