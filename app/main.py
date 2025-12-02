from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from .db import engine, Base, get_db
from .api.offers import router as offers_router

app = FastAPI(title="Offer Service")

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "error", "db": str(e)}


@app.get("/")
def root():
    return {"message": "Offer Service is running"}


app.include_router(offers_router)
