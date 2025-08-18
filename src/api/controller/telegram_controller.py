'''
Telegram controller for handling Telegram bot interactions.
Consists several functions for processing incoming messages, sending replies, and managing user sessions.
'''
import os, sys, hashlib
from dotenv import load_dotenv
from typing import Dict, Any
from src.exception.exception import CustomException

# Load telegram bot token
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("CASH_SIM_BOT")

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