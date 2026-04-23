-- Migration V3: vertical demo engine content and lead attribution

ALTER TABLE leads
ADD COLUMN IF NOT EXISTS lead_source text DEFAULT 'demo_page',
ADD COLUMN IF NOT EXISTS lead_context text;

ALTER TABLE media
ADD COLUMN IF NOT EXISTS caption text,
ADD COLUMN IF NOT EXISTS alt_text text,
ADD COLUMN IF NOT EXISTS sort_order int DEFAULT 0;

ALTER TABLE offerings
ADD COLUMN IF NOT EXISTS sort_order int DEFAULT 0,
ADD COLUMN IF NOT EXISTS cta_label text;

CREATE TABLE IF NOT EXISTS demo_page_content (
  id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
  business_id uuid REFERENCES businesses(id) ON DELETE CASCADE NOT NULL,
  section_type text NOT NULL CHECK (section_type IN ('hero', 'trust', 'review', 'faq', 'article')),
  title text,
  body text,
  author text,
  eyebrow text,
  image_url text,
  primary_cta text,
  sort_order int DEFAULT 0,
  is_active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_demo_page_content_business_section
ON demo_page_content (business_id, section_type, sort_order);
