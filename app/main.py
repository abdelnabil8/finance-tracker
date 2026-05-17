from fastapi import FastAPI
from app.routes import router
from app.database import engine, Base

app = FastAPI()

# This creates the tables in PostgreSQL automatically
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api/transactions", tags=["transactions"])

@app.get("/")
def root():
    return {"message": "Finance Tracker API running!"}