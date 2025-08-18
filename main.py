'''
Main application entry point.
Creates the FastAPI application and includes all necessary routes and middleware.
'''

from fastapi import FastAPI
from src.api.router.telegram_api import router as telegram_route

# Define app instance
app = FastAPI(
  title="Cashflow Simulation Analysis",
  description="API for analyzing cashflow simulations",
  version="0.1.0"
)

# Define router for telegram API
app.include_router(telegram_route, prefix="/telegram", tags=["Telegram"])

# Define home routes
@app.get("/")
def read_root():
  return {
    "message": "Welcome to the Cashflow Simulation Analysis API"
  }