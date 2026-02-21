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

def check_missing():
    print("Checking for missing data...")
    
    # Fetch all businesses
    resp = requests.get(f"{REST_URL}/businesses?select=id,name,phone,working_hours_raw,category", headers=HEADERS)
    if resp.status_code != 200:
        print(f"Error: {resp.text}")
        return

    businesses = resp.json()
    missing_phone = []
    missing_hours = []

    for b in businesses:
        contact = b.get('phone')
        hours = b.get('working_hours_raw')
        
        # Check for empty or placeholder values
        if not contact or contact.strip() == "" or contact == "None" or contact == "-":
            missing_phone.append(b)
        
        if not hours or hours.strip() == "" or hours == "None" or hours == "-" or "Not listed" in hours:
            missing_hours.append(b)

    print(f"Total Businesses: {len(businesses)}")
    print(f"Missing Phone: {len(missing_phone)}")
    print(f"Missing Hours: {len(missing_hours)}")
    
    print("\n--- Missing Phone (First 5) ---")
    for b in missing_phone[:5]:
        print(f"- {b['name']} ({b['category']})")

    print("\n--- Missing Hours (First 5) ---")
    for b in missing_hours[:5]:
        print(f"- {b['name']} ({b['category']})")

if __name__ == "__main__":
    check_missing()
