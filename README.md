# Vaniyambadi Business Platform

## Project Setup

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**
    Ensure `.env` file exists with:
    ```
    SUPABASE_URL=...
    SUPABASE_KEY=...
    ```

3.  **Database Setup**
    - Run the SQL queries in `db_scripts/schema.sql` in your Supabase SQL Editor.
    - Run the seed script to populate data:
      ```bash
      python db_scripts/seed_data.py
      ```

## Running Locally

```bash
python app.py
```

Visit:
- Clinic: `http://localhost:5000/city-dental-care`
- Shoe Store: `http://localhost:5000/step-style-shoes`
- Leather: `http://localhost:5000/vnb-exports`

## Deployment

Deploy to Vercel:
```bash
vercel
```
