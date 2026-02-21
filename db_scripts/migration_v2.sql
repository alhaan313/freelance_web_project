-- Migration V2: Add columns and relax constraints for Excel data support

-- 1. Update businesses table
ALTER TABLE businesses ADD COLUMN IF NOT EXISTS area text;

ALTER TABLE businesses ADD COLUMN IF NOT EXISTS source text;

-- 2. Update clinic_details
ALTER TABLE clinic_details
ADD COLUMN IF NOT EXISTS services_raw text;

-- 3. Update leather_company_details
ALTER TABLE leather_company_details
ADD COLUMN IF NOT EXISTS product_type_raw text;

-- 4. Relax Constraints (to allow varied Excel data)
-- Remove check constraint on shoe_store_details.store_type if it exists
DO $$ 
BEGIN 
    IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'shoe_store_details_store_type_check') THEN 
        ALTER TABLE shoe_store_details DROP CONSTRAINT shoe_store_details_store_type_check; 
    END IF; 
END $$;

-- Remove check constraint on leather_company_details (if any explicit checks existed besides type)
-- (The export_status is boolean, so we just handle conversion in python)