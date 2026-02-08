"""Run a local OAuth flow to obtain a LinkedIn access token and person id.

Usage: python oauth_local_server.py

This script will:
- Read `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET` from `.env`.
- Open the authorization URL in your default browser.
- Start a local HTTP server on port 8000 to capture the redirect with the code.
- Exchange the code for an access token and update `.env` with `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_ID`.

Keep your secrets private. This is for local testing only.
"""
import http.server
import socketserver
import threading
import webbrowser
import requests
import os
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv, set_key
from pathlib import Path

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "profile,openid,w_member_social"
ENV_PATH = Path(__file__).with_name('.env')

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: Please set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in .env before running this script.")
    raise SystemExit(1)


class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path == '/callback' and 'code' in qs:
            code = qs['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Authorization received. You can close this window.</h2></body></html>")
            # Exchange code for token in a separate thread to avoid blocking
            threading.Thread(target=exchange_code_and_save, args=(code,)).start()
        else:
            self.send_response(404)
            self.end_headers()


def exchange_code_and_save(code: str):
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    try:
        r = requests.post(token_url, data=data, timeout=10)
        r.raise_for_status()
        token_data = r.json()
        access_token = token_data.get('access_token')
        if not access_token:
            print('Failed to obtain access token:', token_data)
            return
        # Save to .env
        set_key(str(ENV_PATH), 'LINKEDIN_ACCESS_TOKEN', access_token)
        print('\nSaved LINKEDIN_ACCESS_TOKEN to .env')

        # Fetch person id
        headers = {'Authorization': f'Bearer {access_token}', 'X-Restli-Protocol-Version': '2.0.0'}
        r2 = requests.get('https://api.linkedin.com/v2/me', headers=headers, timeout=10)
        r2.raise_for_status()
        me = r2.json()
        person_id = me.get('id')
        if person_id:
            set_key(str(ENV_PATH), 'LINKEDIN_PERSON_ID', person_id)
            print(f'Saved LINKEDIN_PERSON_ID={person_id} to .env')
        else:
            print('Could not extract person id from response:', me)
        print('\nDone. Restart your automation (python main.py) and set TEST_MODE=false when ready to post live.')
    except Exception as e:
        print('Error exchanging code:', e)


def open_auth_url():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
    }
    from urllib.parse import urlencode
    url = 'https://www.linkedin.com/oauth/v2/authorization?' + urlencode(params)
    print('Opening browser for LinkedIn authorization...')
    webbrowser.open(url)


def run_server():
    PORT = 8000
    with socketserver.TCPServer(('localhost', PORT), OAuthHandler) as httpd:
        print(f'Serving local callback on http://localhost:{PORT}/callback')
        httpd.serve_forever()


def main():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    open_auth_url()
    print('Waiting for authorization... (check the browser)')
    try:
        while t.is_alive():
            t.join(1)
    except KeyboardInterrupt:
        print('\nServer stopped')


if __name__ == '__main__':
    main()
