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

def clean_data():
    print("Cleaning up data...")
    
    # 1. Remove businesses with no name (invalid imports)
    print("Removing invalid rows...")
    requests.delete(f"{REST_URL}/businesses?name=is.null", headers=HEADERS)
    requests.delete(f"{REST_URL}/businesses?slug=is.null", headers=HEADERS)

    # 2. Fix "None", "-", "Not mentioned" in text fields
    # We'll fetch all and update locally for simplicity in this script, 
    # though SQL update would be more efficient for large datasets.
    resp = requests.get(f"{REST_URL}/businesses?select=*", headers=HEADERS)
    businesses = resp.json()
    
    for b in businesses:
        updates = {}
        for k, v in b.items():
            if isinstance(v, str):
                lower_v = v.lower().strip()
                if lower_v in ['none', '-', 'not mentioned', 'not listed', 'null']:
                    updates[k] = None # Set to null
        
        if updates:
            print(f"Cleaning business {b.get('name')}...")
            requests.patch(f"{REST_URL}/businesses?id=eq.{b['id']}", headers=HEADERS, json=updates)

    # 3. Clean Clinic Details
    resp = requests.get(f"{REST_URL}/clinic_details?select=*", headers=HEADERS)
    clinics = resp.json()
    for c in clinics:
        updates = {}
        # distinct cleanup for doctor names
        if c.get('doctor_name') and c.get('doctor_name').strip() in ['-', 'None', '']:
             updates['doctor_name'] = None
        
        if updates:
            print(f"Cleaning clinic details for {c.get('business_id')}...")
            requests.patch(f"{REST_URL}/clinic_details?business_id=eq.{c['business_id']}", headers=HEADERS, json=updates)

    print("Cleanup completed.")

if __name__ == "__main__":
    clean_data()
