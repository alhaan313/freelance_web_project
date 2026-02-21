-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- 1. Businesses Table (Core Tenant)
create table businesses (
  id uuid default uuid_generate_v4() primary key,
  slug text unique not null,
  name text not null,
  category text not null check (category in ('clinic', 'shoe_store', 'leather_company')),
  description text,
  address text,
  phone text,
  email text,
  whatsapp text,
  gmap_link text,
  working_hours_raw text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Extension: Clinic Details
create table clinic_details (
    business_id uuid references businesses (id) on delete cascade primary key,
    doctor_name text,
    specialization text,
    qualification text
);

-- 3. Extension: Shoe Store Details
create table shoe_store_details (
    business_id uuid references businesses (id) on delete cascade primary key,
    store_type text check (
        store_type in (
            'retail',
            'wholesale',
            'manufacturer'
        )
    ),
    primary_brand_focus text
);

-- 4. Extension: Leather Company Details
create table leather_company_details (
    business_id uuid references businesses (id) on delete cascade primary key,
    export_status boolean default false,
    certifications jsonb, -- e.g. ["ISO 9001", "LWG"]
    year_established int
);

-- 5. Offerings (Products & Services)
create table offerings (
  id uuid default uuid_generate_v4() primary key,
  business_id uuid references businesses(id) on delete cascade not null,
  name text not null,
  description text,
  price decimal(10,2),
  image_url text,
  type text check (type in ('service', 'product')),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 6. Leads (Inquiries)
create table leads (
  id uuid default uuid_generate_v4() primary key,
  business_id uuid references businesses(id) on delete cascade not null,
  customer_name text not null,
  phone text not null,
  inquiry_text text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 7. Media (Optional for now, but good to have)
create table media (
  id uuid default uuid_generate_v4() primary key,
  business_id uuid references businesses(id) on delete cascade not null,
  url text not null,
  type text check (type in ('image', 'document')),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);