from __future__ import annotations

import json
from decimal import Decimal
from typing import Any


LOCAL_IMAGE = {
    "clinic": {
        "hero": "images/hero_clinic.jpg",
        "about": "images/about_clinic.jpg",
        "gallery": ["images/clinic_seq_1.jpg", "images/clinic_seq_2.jpg", "images/clinic_seq_3.jpg"],
        "services": ["images/service_clinic_1.jpg", "images/service_clinic_2.jpg", "images/service_clinic_3.jpg"],
    },
    "shoe_store": {
        "hero": "images/hero_shoe.jpg",
        "about": "images/about_shoe.jpg",
        "gallery": ["images/shoe_seq_1.jpg", "images/shoe_seq_2.jpg", "images/shoe_seq_3.jpg"],
        "services": ["images/service_shoe_1.jpg", "images/service_shoe_2.jpg", "images/service_shoe_3.jpg"],
    },
    "leather_company": {
        "hero": "images/hero_leather.jpg",
        "about": "images/about_leather.jpg",
        "gallery": ["images/leather_seq_1.jpg", "images/craft.jpg", "images/leather_seq_3.jpg"],
        "services": ["images/service_leather_1.jpg", "images/service_leather_2.jpg", "images/service_leather_3.jpg"],
    },
}


VERTICALS = {
    "clinic": {
        "category": "clinic",
        "label": "Clinic website demo",
        "eyebrow": "Healthcare demo ready for launch",
        "primary_cta": "Book Appointment",
        "secondary_cta": "Call Clinic",
        "whatsapp_cta": "WhatsApp Clinic",
        "lead_context": "appointment_request",
        "nav": [
            ("Doctor", "#doctor"),
            ("Treatments", "#services"),
            ("Timings", "#visit"),
            ("Contact", "#contact"),
        ],
        "hero_intro": "A calm, trust-first healthcare website demo for patients looking for clear care, timings, and a fast appointment path.",
        "offering_label": "Treatments",
        "offering_heading": "Care options patients can understand quickly",
        "gallery_label": "Clinic environment",
        "trust_heading": "Patient trust signals",
        "contact_heading": "Request an appointment",
        "form_prompt": "Share the concern, preferred timing, or treatment you want to ask about.",
        "fallback_offerings": [
            ("General Consultation", "Clear diagnosis guidance and next-step treatment advice."),
            ("Dental Procedures", "Routine and specialist dental care with appointment-led visits."),
            ("Preventive Care", "Checkups, hygiene guidance, and early issue detection."),
        ],
        "fallback_reviews": [
            ("Clear explanation and careful treatment made the visit easy to trust.", "Patient family"),
            ("The appointment process was simple and the clinic timing was convenient.", "Local patient"),
        ],
        "fallback_faqs": [
            ("Do I need an appointment?", "Appointments are recommended so the clinic can plan your visit and reduce waiting time."),
            ("Can I call for urgent dental pain?", "Yes. Call the clinic directly so the team can guide you on the next available slot."),
            ("What should I bring?", "Bring previous prescriptions, reports, or dental records if you have them."),
        ],
        "trust_blocks": [
            ("Appointment clarity", "Patients see timings, location, and call paths without searching."),
            ("Specialist profile", "Doctor, qualification, and specialization are shown up front."),
            ("Local confidence", "The page is shaped around the actual clinic, not a generic hospital template."),
        ],
        "marquee": ["Appointments", "Doctor profile", "Treatments", "Timings", "Location", "Patient calls"],
    },
    "shoe_store": {
        "category": "shoe_store",
        "label": "Retail website demo",
        "eyebrow": "Footwear storefront demo",
        "primary_cta": "Order on WhatsApp",
        "secondary_cta": "Visit Store",
        "whatsapp_cta": "WhatsApp Order",
        "lead_context": "product_order",
        "nav": [
            ("Collection", "#services"),
            ("Styles", "#styles"),
            ("Visit", "#visit"),
            ("Contact", "#contact"),
        ],
        "hero_intro": "A retail-ready footwear demo that makes the collection, prices, WhatsApp ordering, and store visit path obvious.",
        "offering_label": "Featured collection",
        "offering_heading": "Styles customers can ask for today",
        "gallery_label": "Store and collection",
        "trust_heading": "Shopping confidence",
        "contact_heading": "Ask for size, price, or availability",
        "form_prompt": "Mention the style, size, color, or occasion you are shopping for.",
        "fallback_offerings": [
            ("Formal Shoes", "Office and occasion-ready footwear with polished finishes."),
            ("Casual Sneakers", "Everyday styles for college, travel, and weekend wear."),
            ("Sandals and Daily Wear", "Comfort-first options for regular use and quick replacement."),
        ],
        "fallback_reviews": [
            ("Good collection and the staff helped me choose the right size.", "Store customer"),
            ("Easy to check availability on WhatsApp before visiting the shop.", "Local shopper"),
        ],
        "fallback_faqs": [
            ("Can I check size availability on WhatsApp?", "Yes. Send the style and size you need, and the store can confirm availability."),
            ("Do you have formal and casual footwear?", "The demo supports multiple collections including formal, casual, sports, and daily wear."),
            ("Can I visit the store?", "Yes. Use the map or call button to plan a store visit."),
        ],
        "trust_blocks": [
            ("Size-first ordering", "Customers are prompted to ask for size, color, and occasion."),
            ("Store visit ready", "Address, timings, and call actions stay visible across the page."),
            ("Collection clarity", "Products are grouped so buyers can browse without a full ecommerce setup."),
        ],
        "marquee": ["New styles", "WhatsApp orders", "Size checks", "Store visit", "Daily wear", "Formal shoes"],
    },
    "leather_company": {
        "category": "leather_company",
        "label": "B2B manufacturing demo",
        "eyebrow": "Leather export and procurement demo",
        "primary_cta": "Request Quote",
        "secondary_cta": "Call Sales",
        "whatsapp_cta": "Discuss Requirement",
        "lead_context": "quote_request",
        "nav": [
            ("Capabilities", "#capabilities"),
            ("Products", "#services"),
            ("Trust", "#trust"),
            ("Quote", "#contact"),
        ],
        "hero_intro": "A procurement-focused website demo for buyers who need capabilities, product types, certifications, export readiness, and a clear quote path.",
        "offering_label": "Product capabilities",
        "offering_heading": "Leather categories buyers can source",
        "gallery_label": "Facility and craftsmanship",
        "trust_heading": "Procurement confidence",
        "contact_heading": "Send a sourcing requirement",
        "form_prompt": "Share product type, quantity, destination, specification, or certification requirement.",
        "fallback_offerings": [
            ("Finished Leather", "Buyer-ready finished leather for footwear and leather goods production."),
            ("Shoe Uppers", "Component production support for footwear manufacturers and sourcing teams."),
            ("Leather Goods", "Manufacturing capability for bags, wallets, belts, and custom programs."),
        ],
        "fallback_reviews": [
            ("The page quickly communicates capability, export readiness, and how to request a quote.", "Procurement lead"),
            ("Certifications and product categories are clear without forcing a long sales conversation.", "B2B buyer"),
        ],
        "fallback_faqs": [
            ("Can buyers request a custom quote?", "Yes. The form is structured for sourcing details, product type, quantity, and certification needs."),
            ("Do you support export inquiries?", "Export status and certifications are shown when available in the business data."),
            ("Can product categories be customized?", "Yes. Product capabilities can come from offerings, detail fields, or demo content records."),
        ],
        "trust_blocks": [
            ("Capability-led layout", "Buyers see product types and manufacturing strengths before marketing copy."),
            ("Certification space", "ISO, LWG, and other credentials are displayed when supplied."),
            ("Quote conversion", "The contact form asks for procurement context instead of a generic message."),
        ],
        "marquee": ["Capabilities", "Certifications", "Export ready", "Quote request", "Product types", "Manufacturing"],
    },
}


def build_landing_context(
    business: dict[str, Any],
    offerings: list[dict[str, Any]] | None = None,
    media: list[dict[str, Any]] | None = None,
    page_content: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    category = business.get("category") or "business"
    vertical = VERTICALS.get(category, _generic_vertical(category))
    content = _group_content(page_content or [])
    images = LOCAL_IMAGE.get(category, LOCAL_IMAGE["shoe_store"])

    merged = dict(business)
    merged.update(
        {
            "vertical": vertical,
            "hero": _hero(merged, vertical, content, images),
            "credibility": _credibility(merged, vertical),
            "offerings": _offerings(merged, vertical, offerings or [], images),
            "gallery": _gallery(media or [], images, vertical),
            "reviews": content.get("review") or _review_fallbacks(vertical),
            "faqs": content.get("faq") or _faq_fallbacks(vertical),
            "trust_blocks": _trust_blocks(merged, vertical, content),
            "sections": {
                "offering_label": vertical["offering_label"],
                "offering_heading": vertical["offering_heading"],
                "gallery_label": vertical["gallery_label"],
                "trust_heading": vertical["trust_heading"],
                "contact_heading": vertical["contact_heading"],
                "form_prompt": vertical["form_prompt"],
            },
            "marquee_items": vertical["marquee"],
            "contact_actions": _contact_actions(merged, vertical),
        }
    )
    return merged


def _hero(business: dict[str, Any], vertical: dict[str, Any], content: dict[str, list[dict[str, Any]]], images: dict[str, Any]) -> dict[str, Any]:
    hero_records = content.get("hero") or []
    configured = hero_records[0] if hero_records else {}
    return {
        "eyebrow": configured.get("eyebrow") or vertical["eyebrow"],
        "headline": configured.get("title") or business.get("name") or "Business demo",
        "intro": configured.get("body") or business.get("description") or vertical["hero_intro"],
        "primary_cta": configured.get("primary_cta") or vertical["primary_cta"],
        "secondary_cta": vertical["secondary_cta"],
        "image": configured.get("image_url") or images["hero"],
    }


def _credibility(business: dict[str, Any], vertical: dict[str, Any]) -> list[dict[str, str]]:
    category = vertical["category"]
    if category == "clinic":
        doctor = _join_present([business.get("doctor_name"), business.get("qualification")])
        return [
            {"label": "Doctor", "value": doctor or "Specialist profile available"},
            {"label": "Specialization", "value": business.get("specialization") or "General care"},
            {"label": "Timings", "value": business.get("working_hours_raw") or "Call for appointment timing"},
        ]
    if category == "shoe_store":
        return [
            {"label": "Store type", "value": business.get("store_type") or "Retail footwear store"},
            {"label": "Focus", "value": business.get("primary_brand_focus") or "Formal, casual, and daily wear"},
            {"label": "Location", "value": business.get("area") or "Vaniyambadi"},
        ]
    if category == "leather_company":
        established = str(business.get("year_established")) if business.get("year_established") else "Established manufacturer"
        export = "Export ready" if business.get("export_status") else "Domestic and B2B enquiries"
        products = business.get("product_type_raw") or "Finished leather and leather goods"
        return [
            {"label": "Export status", "value": export},
            {"label": "Established", "value": established},
            {"label": "Product types", "value": products},
        ]
    return [{"label": "Category", "value": category.replace("_", " ").title()}]


def _offerings(business: dict[str, Any], vertical: dict[str, Any], offerings: list[dict[str, Any]], images: dict[str, Any]) -> list[dict[str, Any]]:
    normalized = []
    for index, item in enumerate(offerings[:6]):
        normalized.append(
            {
                "name": item.get("name") or "Offering",
                "description": item.get("description") or _offering_hint(vertical),
                "price": _format_price(item.get("price")),
                "type": item.get("type") or ("service" if vertical["category"] == "clinic" else "product"),
                "image": item.get("image_url") or _cycle(images["services"], index),
            }
        )
    if normalized:
        return normalized

    raw_field = "services_raw" if vertical["category"] == "clinic" else "product_type_raw"
    raw_names = _split_raw(business.get(raw_field))
    fallback = raw_names or [item[0] for item in vertical["fallback_offerings"]]
    fallback_desc = {name: desc for name, desc in vertical["fallback_offerings"]}
    return [
        {
            "name": name,
            "description": fallback_desc.get(name) or _offering_hint(vertical),
            "price": None,
            "type": "service" if vertical["category"] == "clinic" else "product",
            "image": _cycle(images["services"], index),
        }
        for index, name in enumerate(fallback[:6])
    ]


def _gallery(media: list[dict[str, Any]], images: dict[str, Any], vertical: dict[str, Any]) -> list[dict[str, str]]:
    gallery = [
        {
            "url": item.get("url"),
            "caption": item.get("caption") or item.get("alt_text") or vertical["gallery_label"],
        }
        for item in media
        if item.get("url") and (item.get("type") in (None, "image"))
    ]
    if gallery:
        return gallery[:6]
    return [{"url": url, "caption": caption} for url, caption in zip(images["gallery"], _gallery_captions(vertical))]


def _trust_blocks(business: dict[str, Any], vertical: dict[str, Any], content: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    blocks = content.get("trust")
    if blocks:
        return blocks
    configured = [{"title": title, "value": body} for title, body in vertical["trust_blocks"]]
    if vertical["category"] == "leather_company":
        certs = _parse_certs(business.get("certifications"))
        if certs:
            configured.insert(0, {"title": "Certifications", "value": ", ".join(certs)})
    return configured[:4]


def _contact_actions(business: dict[str, Any], vertical: dict[str, Any]) -> list[dict[str, str]]:
    actions = []
    if business.get("phone"):
        actions.append({"label": vertical["secondary_cta"], "href": f"tel:{business['phone']}", "kind": "phone"})
    if business.get("whatsapp"):
        actions.append({"label": vertical["whatsapp_cta"], "href": f"https://wa.me/{business['whatsapp']}", "kind": "whatsapp"})
    if business.get("gmap_link"):
        actions.append({"label": "Open Maps", "href": business["gmap_link"], "kind": "map"})
    return actions


def _group_content(records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        kind = record.get("section_type") or record.get("type")
        if not kind:
            continue
        normalized = {
            "title": record.get("title") or record.get("question") or record.get("name"),
            "body": record.get("body") or record.get("answer") or record.get("description"),
            "value": record.get("body") or record.get("answer") or record.get("description"),
            "author": record.get("author") or record.get("subtitle"),
            "eyebrow": record.get("eyebrow"),
            "image_url": record.get("image_url"),
            "primary_cta": record.get("primary_cta"),
        }
        grouped.setdefault(kind, []).append({k: v for k, v in normalized.items() if v})
    return grouped


def _review_fallbacks(vertical: dict[str, Any]) -> list[dict[str, str]]:
    return [{"body": text, "author": author} for text, author in vertical["fallback_reviews"]]


def _faq_fallbacks(vertical: dict[str, Any]) -> list[dict[str, str]]:
    return [{"title": question, "body": answer} for question, answer in vertical["fallback_faqs"]]


def _gallery_captions(vertical: dict[str, Any]) -> list[str]:
    if vertical["category"] == "clinic":
        return ["Clinic frontage", "Care environment", "Patient-ready setup"]
    if vertical["category"] == "shoe_store":
        return ["Featured styles", "Daily wear collection", "Store-ready catalog"]
    if vertical["category"] == "leather_company":
        return ["Material capability", "Craftsmanship detail", "Production confidence"]
    return ["Business showcase", "Work detail", "Customer experience"]


def _generic_vertical(category: str) -> dict[str, Any]:
    return {
        **VERTICALS["shoe_store"],
        "category": category,
        "label": "Business website demo",
        "eyebrow": "Ready-to-launch business demo",
        "primary_cta": "Contact Business",
        "secondary_cta": "Call Now",
        "whatsapp_cta": "WhatsApp",
    }


def _split_raw(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [part.strip() for part in str(value).replace("\n", ",").split(",") if part.strip()]


def _parse_certs(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(item) for item in parsed if item]
        except json.JSONDecodeError:
            return _split_raw(value)
    return []


def _format_price(value: Any) -> str | None:
    if value in (None, ""):
        return None
    try:
        amount = Decimal(str(value))
    except Exception:
        return str(value)
    if amount == amount.to_integral():
        return f"Rs. {int(amount):,}"
    return f"Rs. {amount:,.2f}"


def _offering_hint(vertical: dict[str, Any]) -> str:
    if vertical["category"] == "clinic":
        return "Structured treatment information that helps patients know what to ask for."
    if vertical["category"] == "leather_company":
        return "Procurement-ready capability detail for buyers and sourcing teams."
    return "A collection item customers can ask about by size, style, or availability."


def _join_present(values: list[Any]) -> str:
    return ", ".join([str(value) for value in values if value])


def _cycle(values: list[str], index: int) -> str:
    return values[index % len(values)]
