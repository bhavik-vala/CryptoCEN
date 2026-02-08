# Troubleshooting

- If PDF extraction returns empty: ensure PDFs are text-based, not image-scans. Use OCR externally if needed.
- If ChromaDB fails to start: verify `chromadb` installed and Python version matches requirements.
- If AI provider errors: confirm keys in `.env` and selected `AI_PROVIDER`.
- If LinkedIn posting fails: check access token scopes and `LINKEDIN_PERSON_ID` format.
- Logs: see `valtrilabs.log` for details.
