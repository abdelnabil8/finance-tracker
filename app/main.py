from fastapi import FastAPI
from app.routes import router

app = FastAPI()

app.include_router(router, prefix="/api/transactions", tags=["transactions"])

@app.get("/")
def root():
    return {"message": "Finance Tracker API running!"}