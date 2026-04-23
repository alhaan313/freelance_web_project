import os
import requests
from dotenv import load_dotenv

from verticals import build_landing_context

load_dotenv()

# Initialize API Config
URL: str = os.environ.get("SUPABASE_URL")
KEY: str = os.environ.get("SUPABASE_KEY")

REST_URL = f"{URL}/rest/v1" if URL and KEY else None
HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

LOCAL_DEMO_BUSINESSES = [
    {
        "id": "local-city-dental-care",
        "slug": "city-dental-care",
        "name": "City Dental Care",
        "category": "clinic",
        "description": "Premium dental care services in Vaniyambadi.",
        "address": "123 Main Bazaar, Vaniyambadi",
        "phone": "9876543210",
        "email": "contact@citydental.com",
        "working_hours_raw": "Mon-Sat: 10AM - 8PM",
        "whatsapp": "919876543210",
        "doctor_name": "Dr. Suresh Kumar",
        "specialization": "Dentist",
        "qualification": "BDS, MDS",
        "services_raw": "Root canal, Smile design, Dental implants",
    },
    {
        "id": "local-step-style-shoes",
        "slug": "step-style-shoes",
        "name": "Step Style Shoes",
        "category": "shoe_store",
        "description": "Latest collection of formal and casual footwear.",
        "address": "45 New Town Road, Vaniyambadi",
        "phone": "9988776655",
        "working_hours_raw": "Everyday: 9AM - 10PM",
        "whatsapp": "919988776655",
        "store_type": "retail",
        "primary_brand_focus": "Formal, casual, and daily wear",
    },
    {
        "id": "local-vnb-exports",
        "slug": "vnb-exports",
        "name": "VNB Leather Exports",
        "category": "leather_company",
        "description": "High quality finished leather for international markets.",
        "address": "Industrial Estate, Vaniyambadi",
        "phone": "8877665544",
        "working_hours_raw": "Mon-Fri: 9AM - 6PM",
        "whatsapp": "918877665544",
        "export_status": True,
        "certifications": ["ISO 9001", "LWG Gold"],
        "year_established": 1995,
        "product_type_raw": "Finished leather, Shoe uppers, Leather goods",
    },
]

def _is_configured():
    if REST_URL and KEY:
        return True
    print("Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY to load live data.")
    return False

def get_all_businesses():
    """Fetches all businesses for the directory."""
    try:
        if not _is_configured():
            return LOCAL_DEMO_BUSINESSES
        resp = requests.get(f"{REST_URL}/businesses?select=*&order=name.asc", headers=HEADERS)
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        print(f"Error fetching all businesses: {e}")
        return []

def _get_rows(table, query):
    """Fetch rows from Supabase REST. Missing optional tables fail closed."""
    try:
        if not _is_configured():
            return []
        resp = requests.get(f"{REST_URL}/{table}?{query}", headers=HEADERS)
        if resp.status_code == 200:
            return resp.json()
        print(f"Supabase fetch skipped for {table}: {resp.status_code}")
        return []
    except Exception as e:
        print(f"Error fetching {table}: {e}")
        return []

def get_business_by_slug(slug):
    """
    Fetches business metadata and related details based on slug.
    Performs joins with extension tables based on category.
    """
    try:
        if not _is_configured():
            business = next((item for item in LOCAL_DEMO_BUSINESSES if item["slug"] == slug), None)
            return build_landing_context(dict(business), offerings=[], media=[], page_content=[]) if business else None
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

        offerings = _get_rows(
            "offerings",
            f"business_id=eq.{business_id}&select=*&order=created_at.asc",
        )
        media = _get_rows(
            "media",
            f"business_id=eq.{business_id}&select=*&order=created_at.asc",
        )
        page_content = _get_rows(
            "demo_page_content",
            f"business_id=eq.{business_id}&select=*&order=sort_order.asc",
        )

        return build_landing_context(
            business,
            offerings=offerings,
            media=media,
            page_content=page_content,
        )
        
    except Exception as e:
        print(f"Error fetching business: {e}")
        return None

def create_lead(payload):
    """Persist a validated lead payload to Supabase."""
    try:
        if not _is_configured():
            return False, []
        resp = requests.post(f"{REST_URL}/leads", headers=HEADERS, json=payload)
        if resp.status_code in (200, 201):
            return True, resp.json() if resp.text else []
        if resp.status_code in (400, 404) and ("lead_source" in payload or "lead_context" in payload):
            legacy_payload = dict(payload)
            legacy_payload.pop("lead_source", None)
            legacy_payload.pop("lead_context", None)
            legacy_resp = requests.post(f"{REST_URL}/leads", headers=HEADERS, json=legacy_payload)
            if legacy_resp.status_code in (200, 201):
                return True, legacy_resp.json() if legacy_resp.text else []
        print(f"Lead capture failed: {resp.status_code} {resp.text}")
        return False, []
    except Exception as e:
        print(f"Lead capture error: {e}")
        return False, []
