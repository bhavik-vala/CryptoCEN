"""Get LinkedIn access token interactively."""
import requests
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "profile,openid,w_member_social"

def get_authorization_url():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }
    url = "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(params)
    return url

def exchange_code_for_token(code):
    """Exchange authorization code for access token."""
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("ERROR: LINKEDIN_CLIENT_ID or LINKEDIN_CLIENT_SECRET not set in .env")
        return
    
    print("LinkedIn Access Token Generator")
    print("=" * 50)
    print("\n1. Opening LinkedIn authorization page...")
    auth_url = get_authorization_url()
    print(f"\nAuthorization URL:\n{auth_url}")
    
    try:
        webbrowser.open(auth_url)
        print("\nBrowser opened. Allow access, then copy the code from the URL.")
    except:
        print("\nPlease visit the URL above in your browser.")
    
    code = input("\nEnter the authorization code from the redirect URL: ").strip()
    if not code:
        print("No code provided. Exiting.")
        return
    
    print("\nExchanging code for access token...")
    token_response = exchange_code_for_token(code)
    
    if token_response:
        access_token = token_response.get("access_token")
        expires_in = token_response.get("expires_in", 3600)
        print(f"\nSUCCESS!")
        print(f"Access Token: {access_token}")
        print(f"Expires in: {expires_in} seconds (~{expires_in//3600} hours)")
        print(f"\nAdd to .env:\nLINKEDIN_ACCESS_TOKEN={access_token}")
    else:
        print("Failed to get access token.")

if __name__ == "__main__":
    main()
