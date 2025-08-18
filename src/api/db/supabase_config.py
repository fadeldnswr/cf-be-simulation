'''
Supabase configuration for database access.
'''
import httpx, os, sys
from src.exception.exception import CustomException
from dotenv import load_dotenv
from typing import Tuple

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")

# Define function to insert data to Supabase table
async def insert_data_to_supabase(data: dict) -> Tuple[int, str]:
  '''
  Insert data into Supabase table
  params:
  - data : The data to insert into the table
  '''
  try:
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?on_conflict=fingerprint"
    headers = {
      "apiKey": SUPABASE_SERVICE_ROLE,
      "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE}",
      "Prefer": "resolution=ignore-duplicate,return=minimal",
      "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=10) as client:
      response = await client.post(url, headers=headers, json=data)
      return response.status_code, response.text
  except Exception as e:
    raise CustomException(e, sys)