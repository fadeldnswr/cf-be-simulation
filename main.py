'''
Main application entry point.
Creates the FastAPI application and includes all necessary routes and middleware.
'''

from fastapi import FastAPI

# Define app instance
app = FastAPI(
  title="Cashflow Simulation Analysis",
  description="API for analyzing cashflow simulations",
  version="0.1.0"
)

# Define home routes
@app.get("/")
def read_root():
  return {
    "message": "Welcome to the Cashflow Simulation Analysis API"
  }