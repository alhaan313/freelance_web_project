import importlib
import os
import unittest
from unittest.mock import Mock, patch


os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "test-key")


class VerticalEngineTests(unittest.TestCase):
    def test_clinic_context_uses_details_offerings_and_safe_fallbacks(self):
        from verticals import build_landing_context

        business = {
            "id": "clinic-1",
            "slug": "city-dental-care",
            "name": "City Dental Care",
            "category": "clinic",
            "description": "Premium dental care services in Vaniyambadi.",
            "phone": "9876543210",
            "whatsapp": "919876543210",
            "doctor_name": "Dr. Suresh Kumar",
            "qualification": "BDS, MDS",
            "specialization": "Dental Surgeon",
            "services_raw": "Root canal, Smile design, Dental implants",
            "working_hours_raw": "Mon-Sat: 10AM - 8PM",
        }

        context = build_landing_context(
            business,
            offerings=[{"name": "Root Canal", "type": "service", "description": "Pain-managed dental treatment"}],
            media=[],
            page_content=[],
        )

        self.assertEqual(context["vertical"]["category"], "clinic")
        self.assertEqual(context["hero"]["headline"], "City Dental Care")
        self.assertIn("Appointment", context["hero"]["primary_cta"])
        self.assertIn("Dr. Suresh Kumar", context["credibility"][0]["value"])
        self.assertEqual(context["offerings"][0]["name"], "Root Canal")
        self.assertGreaterEqual(len(context["faqs"]), 3)

    def test_leather_context_prioritizes_procurement_and_certifications(self):
        from verticals import build_landing_context

        business = {
            "id": "leather-1",
            "slug": "vnb-exports",
            "name": "VNB Leather Exports",
            "category": "leather_company",
            "description": "Finished leather for international buyers.",
            "export_status": True,
            "certifications": ["ISO 9001", "LWG Gold"],
            "year_established": 1995,
            "product_type_raw": "Finished leather, Shoe uppers, Leather goods",
        }

        context = build_landing_context(business, offerings=[], media=[], page_content=[])

        self.assertIn("quote", context["hero"]["primary_cta"].lower())
        self.assertIn("Procurement", context["sections"]["trust_heading"])
        self.assertTrue(any(item["value"] == "Export ready" for item in context["credibility"]))
        self.assertTrue(any("LWG Gold" in item["value"] for item in context["trust_blocks"]))


class LeadCaptureTests(unittest.TestCase):
    def setUp(self):
        import app

        self.app_module = importlib.reload(app)
        self.client = self.app_module.app.test_client()

    def test_lead_requires_business_name_and_phone(self):
        response = self.client.post(
            "/api/lead",
            json={"business_id": "biz-1", "customer_name": "Afnan", "phone": "  "},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.get_json()["error"].lower())

    @patch("requests.post")
    def test_lead_posts_valid_payload_with_context(self, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: [{"id": "lead-1"}])

        response = self.client.post(
            "/api/lead",
            json={
                "business_id": "biz-1",
                "customer_name": "Afnan",
                "phone": "8610866049",
                "inquiry_text": "Need a website demo",
                "lead_source": "demo_page",
                "lead_context": "hero_cta",
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = mock_post.call_args.kwargs["json"]
        self.assertEqual(payload["lead_source"], "demo_page")
        self.assertEqual(payload["lead_context"], "hero_cta")
        self.assertEqual(payload["phone"], "8610866049")


if __name__ == "__main__":
    unittest.main()
