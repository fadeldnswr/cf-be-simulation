'''
Twin model file to create rule based digital twin model
for monthly cashflow analysis. This fill include the
equation for simulation.
'''
import calendar
import statistics
import datetime as dt
import random

from __future__ import annotations
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Define digital twin configuration class
@dataclass
class TwinConfig:
  year: int
  month: int
  budget_idr: int = 2_000_000
  office_probability: float = 0.1

# Define data source class abstraction
class DataSource:
  pass

# Define scheduler class
class Scheduler:
  pass

# Define digital twin model
class DigitalTwinModel:
  pass