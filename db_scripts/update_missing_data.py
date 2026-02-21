import os
import sys
import requests
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    sys.exit(1)

REST_URL = f"{url}/rest/v1"
HEADERS = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def update_data():
    print("Updating missing data based on web search...")

    # 1. Reliance Footwear - Mark as Closed
    print("Updating Reliance Footwear...")
    slug = "reliance-footwear"
    
    # Check if exists
    resp = requests.get(f"{REST_URL}/businesses?slug=eq.{slug}", headers=HEADERS)
    if resp.json():
        business_id = resp.json()[0]['id']
        update_payload = {
            "working_hours_raw": "Permanently Closed",
            "description": "Reliance Footwear (Closed Down) - Former shoe store in Vaniyambadi."
        }
        res = requests.patch(f"{REST_URL}/businesses?id=eq.{business_id}", headers=HEADERS, json=update_payload)
        if res.status_code in [200, 204]:
            print("  -> Marked as Closed.")
        else:
            print(f"  -> Failed to update: {res.text}")
    else:
        print("  -> Reliance Footwear not found in DB.")

    # 2. Manual Updates for others if found (Placeholder for future)
    # Most searched businesses (Aatif, Mohib, Happy Heels) had no public digital footprint.
    print("No reliable online data found for Aatif, Mohib, or Happy Heels.")

if __name__ == "__main__":
    update_data()
