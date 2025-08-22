'''
Data transformation file to initialize 
transformation from supabase data
'''

import os, sys

from src.logging.logging import logging
from src.exception.exception import CustomException

from dataclasses import dataclass
from typing import List, Dict, Any, Protocol
from datetime import date

# Define data transformation protocols
class IDataTransformation(Protocol):
  pass