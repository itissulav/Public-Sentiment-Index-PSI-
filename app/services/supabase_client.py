import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY or not SUPABASE_SERVICE_KEY:
    raise RuntimeError("Supabase environment variables not loaded")

public_supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
)

admin_supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)