'''
Route for Telegram API integration.
This module handles all interactions with the Telegram API, including sending and receiving messages.
'''
import os

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import date
from typing import Dict, Any
from dotenv import load_dotenv
from src.api.controller.telegram_controller import parse_text, fingerprint
from src.api.db.supabase_config import insert_data_to_supabase

# Load environment variables
load_dotenv()
ALLOWED_CHAT_IDS = {cid.strip() for cid in os.getenv("ALLOWED_CHAT_IDS").split(",") if cid.strip()}

# Define router instance
router = APIRouter()

# Define health router
router.get("/health")
async def health() -> Dict[str, Any]:
  return {
    "ok": True
  }

# Define endpoint to insert telegram message to Supabase
@router.post("/webhook", status_code=200)
async def telegram_webhook(request: Request) -> JSONResponse:
  '''
  Telegram webhook function to send expenses inputted from telegram to Supabase table
  params:
  - request: Request format from Request class
  return:
  - Returns JSON response according to the reply
  '''
  try:
    # Get message payload
    payload = await request.json()
    
    # Check if the message payload is valid
    message = payload.get("message", {}) or payload.get("edited_message", {})
    if not message:
      return JSONResponse({
        "ok": True
      })
    
    # Get chat_id, text, and data
    chat_id = str(message["chat"]["id"])
    text= message["text"].strip()
    if ALLOWED_CHAT_IDS and chat_id not in ALLOWED_CHAT_IDS:
      return JSONResponse({
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": "Access denied!"
      })
    
    # Parse data and error using parse_text function
    data, error = parse_text(text)
    if error:
      return JSONResponse({
        "method":"sendMessage",
        "chat_id": chat_id,
        "text": error
      })
    
    # Create date 
    dt = date.today().isoformat()
    fp = fingerprint(chat_id, dt, data["amount"], data["category"], data["mode"], data["note"])
    
    # Define row dictionary
    row = {
      "user_id": chat_id,
      "date": dt,
      "amount_idr": data["amount"],
      "category": data["category"],
      "mode": data["mode"],
      "note": data["note"],
      "source": "telegram",
      "fingerprint": fp
    }
    
    # Insert row and create response if its succeed or not
    code, body = await insert_data_to_supabase(row)
    if code in (201, 204):
      reply = f"OK: {data['amount']:,} · {data['category']} · {data['mode']} · {dt}"
    else:
      reply = f"Insert error: {code} {body}"
    
    # Reply via telegram using webhook response style
    return JSONResponse({
      "method": "sendMessage",
      "chat_id": chat_id,
      "text": reply
    })
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))