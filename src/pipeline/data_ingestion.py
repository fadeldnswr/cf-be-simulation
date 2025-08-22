'''
Data ingestion file to initialize
data extraction from supabase.
'''

import sys
import pandas as pd

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
  def convert_data_to_dataframe(self) -> pd.DataFrame:
    ...

# Define data ingestion class
class DataIngestion:
  def __init__(self):
    self.supabase: Client = connect_to_supabase()
    self.data = None
  
  def fetch_data_from_supabase(self, user_id: str, start_date: date, end_date: date) -> List[Dict[str, Any]]:
    try:
      # Define supabase response
      response = self.supabase.table("daily_expenses").select("*").eq("user_id", user_id) \
        .gte("date", start_date.isoformat()).lte("date", end_date.isoformat()).execute()
      # Create response data
      self.data = response.data
      # Check if not data available
      if not self.data:
        logging.warning(f"No data found for user {user_id} between {start_date} to {end_date}")
        return []
      return self.data
    except Exception as e:
      raise CustomException(e, sys)
  
  def convert_data_to_dataframe(self) -> pd.DataFrame:
    try:
      df = pd.DataFrame(self.data)
      if df.empty:
        logging.warning("No data to convert to DataFrame format")
        return pd.DataFrame()
      return df
    except Exception as e:
      raise CustomException(e, sys)