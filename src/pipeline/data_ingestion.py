'''
Data ingestion file to initialize
data extraction from supabase.
'''

import os, sys, httpx

from typing import List, Dict, Any, Protocol
from dataclasses import dataclass
from supabase import Client
from datetime import date

from src.exception.exception import CustomException
from src.logging.logging import logging
from src.api.db.supabase_config import connect_to_supabase

# Define data ingestion protocol with method
@dataclass
class IDataIngestion(Protocol):
  def fetch_data_from_supabase(self, user_id: str, start_date: date, end_date: date) -> List[Dict[str, Any]]:
    ...

# Define data ingestion class
class DataIngestion:
  def __init__(self):
    self.supabase: Client = connect_to_supabase()
  
  def fetch_data_from_supabase(self, user_id: str, start_date: date, end_date: date) -> List[Dict[str, Any]]:
    try:
      # Define supabase response
      response = self.supabase.table("daily_expenses").select("*").eq("user_id", user_id) \
        .gte("date", start_date.isoformat()).lte("date", end_date.isoformat()).execute()
      # Create response data
      data = response.data
      # Check if not data available
      if not data:
        logging.warning(f"No data found for user {user_id} between {start_date} to {end_date}")
        return []
      return data
    except Exception as e:
      raise CustomException(e, sys)