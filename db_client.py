import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Initialize API Config
URL: str = os.environ.get("SUPABASE_URL")
KEY: str = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

REST_URL = f"{URL}/rest/v1"
HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_all_businesses():
    """Fetches all businesses for the directory."""
    try:
        resp = requests.get(f"{REST_URL}/businesses?select=*&order=name.asc", headers=HEADERS)
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        print(f"Error fetching all businesses: {e}")
        return []

def get_business_by_slug(slug):
    """
    Fetches business metadata and related details based on slug.
    Performs joins with extension tables based on category.
    """
    try:
        # 1. Fetch core business data
        resp = requests.get(f"{REST_URL}/businesses?slug=eq.{slug}&select=*", headers=HEADERS)
        
        if resp.status_code != 200 or not resp.json():
            return None
            
        business = resp.json()[0]
        business_id = business['id']
        category = business['category']
        
        # 2. Fetch category-specific details
        details = {}
        table_map = {
            'clinic': 'clinic_details',
            'shoe_store': 'shoe_store_details',
            'leather_company': 'leather_company_details'
        }
        
        if category in table_map:
            table = table_map[category]
            det_resp = requests.get(f"{REST_URL}/{table}?business_id=eq.{business_id}&select=*", headers=HEADERS)
            if det_resp.status_code == 200 and det_resp.json():
                details = det_resp.json()[0]

        # Merge details into business object
        business.update(details)
        
        return business
        
    except Exception as e:
        print(f"Error fetching business: {e}")
        return None
