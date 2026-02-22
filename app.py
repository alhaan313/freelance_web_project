from flask import Flask, render_template, abort, request, jsonify
import os
from dotenv import load_dotenv

# Load env before imports that might check os.environ
load_dotenv()

from db_client import get_business_by_slug, get_all_businesses

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/d9x3k7')
def directory():
    # Fetch all businesses for the directory
    businesses = get_all_businesses()
    return render_template('index.html', businesses=businesses)

@app.route('/<slug>')
def business_landing(slug):
    # Fetch business data from Supabase
    business_data = get_business_by_slug(slug)
    
    if not business_data:
        abort(404)
        
    return render_template('landing.html', **business_data)

@app.route('/api/lead', methods=['POST'])
def create_lead():
    """Capture lead inquiries from the contact form."""
    try:
        import requests as req
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        lead_payload = {
            "business_id": data.get('business_id'),
            "customer_name": data.get('customer_name', ''),
            "phone": data.get('phone', ''),
            "inquiry_text": data.get('inquiry_text', '')
        }
        
        # Post to Supabase
        REST_URL = os.environ.get("SUPABASE_URL") + "/rest/v1"
        KEY = os.environ.get("SUPABASE_KEY")
        headers = {
            "apikey": KEY,
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        resp = req.post(f"{REST_URL}/leads", headers=headers, json=lead_payload)
        
        if resp.status_code == 201:
            return jsonify({"message": "Lead captured successfully"}), 201
        else:
            return jsonify({"error": "Failed to save lead"}), 500
            
    except Exception as e:
        print(f"Lead capture error: {e}")
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
