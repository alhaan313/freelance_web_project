import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    sys.exit(1)

# Supabase REST API endpoint
REST_URL = f"{url}/rest/v1"
HEADERS = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def seed_data():
    print("Seeding data via REST API...")

    # 1. Clinic: City Dental Care
    clinic_data = {
        "slug": "city-dental-care",
        "name": "City Dental Care",
        "category": "clinic",
        "description": "Premium dental care services in Vaniyambadi.",
        "address": "123 Main Bazaar, Vaniyambadi",
        "phone": "9876543210",
        "email": "contact@citydental.com",
        "working_hours_raw": "Mon-Sat: 10AM - 8PM",
        "whatsapp": "919876543210"
    }

    print(f"Inserting {clinic_data['name']}...")
    resp = requests.post(f"{REST_URL}/businesses", headers=HEADERS, json=clinic_data)
    
    if resp.status_code == 201:
        clinic_id = resp.json()[0]['id']
        requests.post(f"{REST_URL}/clinic_details", headers=HEADERS, json={
            "business_id": clinic_id,
            "doctor_name": "Suresh Kumar",
            "specialization": "Dentist",
            "qualification": "BDS, MDS"
        })
    elif resp.status_code == 409:
        print("Business already exists, skipping.")
    else:
        print(f"Error inserting business: {resp.text}")


    # 2. Shoe Store: Step Style
    shoe_data = {
        "slug": "step-style-shoes",
        "name": "Step Style Shoes",
        "category": "shoe_store",
        "description": "Latest collection of formal and casual footwear.",
        "address": "45 New Town Road, Vaniyambadi",
        "phone": "9988776655",
        "working_hours_raw": "Everyday: 9AM - 10PM",
        "whatsapp": "919988776655"
    }

    print(f"Inserting {shoe_data['name']}...")
    resp = requests.post(f"{REST_URL}/businesses", headers=HEADERS, json=shoe_data)
    
    if resp.status_code == 201:
        shoe_id = resp.json()[0]['id']
        requests.post(f"{REST_URL}/shoe_store_details", headers=HEADERS, json={
            "business_id": shoe_id,
            "store_type": "retail",
            "primary_brand_focus": "Nike, Adidas, Woodland"
        })
    elif resp.status_code == 409:
         print("Business already exists, skipping.")
    else:
        print(f"Error inserting business: {resp.text}")


    # 3. Leather Company: VNB Exports
    leather_data = {
        "slug": "vnb-exports",
        "name": "VNB Leather Exports",
        "category": "leather_company",
        "description": "High quality finished leather for international markets.",
        "address": "Industrial Estate, Vaniyambadi",
        "phone": "8877665544",
        "working_hours_raw": "Mon-Fri: 9AM - 6PM",
        "whatsapp": "918877665544"
    }

    print(f"Inserting {leather_data['name']}...")
    resp = requests.post(f"{REST_URL}/businesses", headers=HEADERS, json=leather_data)

    if resp.status_code == 201:
        leather_id = resp.json()[0]['id']
        requests.post(f"{REST_URL}/leather_company_details", headers=HEADERS, json={
            "business_id": leather_id,
            "export_status": True,
            "certifications": ["ISO 9001", "LWG Gold"],
            "year_established": 1995
        })
    elif resp.status_code == 409:
         print("Business already exists, skipping.")
    else:
        print(f"Error inserting business: {resp.text}")

    print("Data seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
