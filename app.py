from flask import Flask, render_template, abort, request, jsonify
import os
from dotenv import load_dotenv

# Load env before imports that might check os.environ
load_dotenv()

from db_client import create_lead as save_lead
from db_client import get_all_businesses, get_business_by_slug

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
        data = request.get_json(silent=True) or {}
        
        business_id = str(data.get('business_id') or '').strip()
        customer_name = str(data.get('customer_name') or '').strip()
        phone = str(data.get('phone') or '').strip()
        inquiry_text = str(data.get('inquiry_text') or '').strip()
        lead_source = str(data.get('lead_source') or 'demo_page').strip()[:80]
        lead_context = str(data.get('lead_context') or '').strip()[:120]

        if not business_id:
            return jsonify({"error": "business_id is required"}), 400
        if not customer_name:
            return jsonify({"error": "customer_name is required"}), 400
        if not phone:
            return jsonify({"error": "phone is required"}), 400
        
        lead_payload = {
            "business_id": business_id,
            "customer_name": customer_name[:120],
            "phone": phone[:40],
            "inquiry_text": inquiry_text[:1200],
            "lead_source": lead_source,
            "lead_context": lead_context,
        }

        ok, saved = save_lead(lead_payload)
        if ok:
            return jsonify({"message": "Lead captured successfully", "lead": saved}), 201
        return jsonify({"error": "Failed to save lead"}), 500
            
    except Exception as e:
        print(f"Lead capture error: {e}")
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
