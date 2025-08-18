'''
Telegram controller for handling Telegram bot interactions.
Consists several functions for processing incoming messages, sending replies, and managing user sessions.
'''
import os, sys, hashlib, httpx
from dotenv import load_dotenv
from typing import Dict, Any
from src.exception.exception import CustomException
from datetime import date

# Load telegram bot token
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("CASH_SIM_BOT")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")

# Define categories and modes
CATS = {"transport","food","misc","bill"}
MODES = {"motorcycle","car","none"}

# Define parse text function to parse text from telegram bot
def parse_text(text: str) -> Dict[str, Any]:
  '''
  Parse text from telegram bot message.
  params:
  - text: The text to parse.
  return:
  - A dictionary containing the parsed data.
  '''
  # Split the text
  parts = text.strip().split()
  # Check if the command is valid
  if len(parts) < 4 or parts[0].lower() != "/add":
    return None, "Use: /add <amount> <category> <mode> [note]"
  try:
    amount = int(parts[1])
  except:
    return None, "Invalid amount. Please enter a valid number."
  
  # Extract category, mode, and note
  category, mode = parts[2].lower(), parts[3].lower()
  # Extract note
  note = " ".join(parts[4:]) if len(parts) > 4 else ""
  
  # Check if amount and category is valid
  if amount < 0 or category not in CATS or mode not in MODES:
    return None, "Invalid input. Please check the amount, category, and mode."

  # Return parsed data
  return {
    "amount": amount,
    "category": category,
    "mode": mode,
    "note": note
  }, None

# Define function to add fingerprint
def fingerprint(
  user_id:str, dt:str, amount:int,
  category:str, mode:str, note:str | None) -> str:
  try:
    s = f"{user_id}|{dt}|{amount}|{category}|{mode}|{note or ' '}"
    return hashlib.sha256(s.encode()).hexdigest()
  except Exception as e:
    raise CustomException(e, sys)

# Define function to sum todays spend
async def todays_spend(chat_id:str) -> Dict[str, Any]:
  try:
    headers = {
      "apiKey": SUPABASE_SERVICE_ROLE,
      "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE}",
      "Prefer": "resolution=ignore-duplicate,return=minimal",
      "Content-Type": "application/json",
    }
    dt = date
    url = f"{SUPABASE_URL}/rest/v1/daily_expenses"
    q = f"?user_id=eq.{chat_id}&date=eq.{dt.today():%Y-%m-%d}&select=amount_idr"
    async with httpx.AsyncClient() as client:
      response = await client.get(url+q, headers=headers); response.raise_for_status()
    total = sum(amount["amount_idr"] for amount in response.json())
    return {
      "today_spend": total
    }
  except Exception as e:
    raise CustomException(e, sys)