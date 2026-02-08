"""Extract LinkedIn Person ID from access token."""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_linkedin_person_id():
    """Fetch LinkedIn person ID from access token."""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not set in .env")
        return None
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    
    try:
        # Get user info
        response = requests.get("https://api.linkedin.com/v2/me", headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract person ID from the URN: urn:li:person:XXXXXXXXX
        person_urn = data.get("id")
        if person_urn:
            person_id = person_urn.split(":")[-1]
            print(f"SUCCESS! Your LinkedIn Person ID is: {person_id}")
            print(f"\nFull URN: {person_urn}")
            print(f"\nAdd this to your .env file:")
            print(f"LINKEDIN_PERSON_ID={person_id}")
            return person_id
        else:
            print("ERROR: Could not extract person ID from response")
            return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("ERROR: Access token is invalid or expired (401 Unauthorized)")
        elif e.response.status_code == 403:
            print("ERROR: Access token does not have required scopes (403 Forbidden)")
            print("Required scopes: w_member_social, profile, openid")
        else:
            print(f"ERROR: HTTP {e.response.status_code}: {e.response.text}")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

if __name__ == "__main__":
    person_id = get_linkedin_person_id()
    if person_id:
        print("\nNext: Update your .env file and restart the system.")
