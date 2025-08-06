from fastapi import FastAPI
from src.app.api.endpoint import router as disaster_router

app = FastAPI()
app.include_router(disaster_router, prefix="/api")

# uvicorn src.app.main:app --reload
