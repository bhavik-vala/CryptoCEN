# LinkedIn Automation — ValtriLabs / Arab Global Crypto

This repository generates RAG-backed LinkedIn posts using multiple AI providers and can post automatically to your personal LinkedIn profile.

Quick start

1. Copy `.env.example` to `.env` and fill secrets.

2. Install dependencies (locally):
```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Build knowledge base (optional):
```bash
python main.py
# choose option 1 to build from PDFs in data/pdfs
```

4. Run a preview post locally:
```bash
# ensure TEST_MODE=true in .env
python main.py
# choose option 2 (Run now - preview)
```

Switch content profile to crypto

- Set `CONTENT_PROFILE=arab_global_crypto` in `.env` or in GitHub Secrets to switch to crypto/Exchange-related content.
- Ensure `LINKEDIN_PERSON_ID` is your personal URN (e.g. `urn:li:person:vvQE2g2rkz`) if you want posts on your personal account.

Deploying on GitHub Actions (free)

1. Push this repo to GitHub.
2. Go to Settings → Secrets and create the following repository secrets:
	- `LINKEDIN_ACCESS_TOKEN` (must include `w_member_social` scope)
	- `LINKEDIN_PERSON_ID` (your personal URN)
	- `AI_PROVIDER`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY` as needed
3. The workflow `.github/workflows/scheduled_post.yml` runs daily at 11:00 IST and invokes `python main.py` to post.

Notes & limitations

- LinkedIn UGC API only supports posting to personal profiles via this endpoint. Company page posting via API is restricted.
- LinkedIn access tokens may expire; you'll need to re-run the OAuth flow periodically to refresh the token.
- To post on the company page, either reshare the personal post manually or use LinkedIn's native page scheduler.

Adding domain-specific PDFs

- To improve factual grounding, add your crypto/Exchange PDFs to `data/pdfs/` and choose option 1 in the CLI to rebuild the knowledge base.

If you want, I can:
- Add an automated token refresh flow (requires refresh token)
- Configure deployment on Render or Railway (both have free tiers)

