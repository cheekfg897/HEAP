from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

url = os.environ.get("https://culnykmmgfetgpuglvrt.supabase.co")
key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN1bG55a21tZ2ZldGdwdWdsdnJ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2NTgwMzcsImV4cCI6MjA2NTIzNDAzN30.q2eGpMlEkhAj32na-U7No_7ffNGv_HgECLpn1GCLyR0")

supabase = create_client(url, key)

data = supabase.table("Attendees").select("*").execute()
print(data)