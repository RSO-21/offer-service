from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from prometheus_fastapi_instrumentator import Instrumentator

from .db import get_db, Base, engine
from .api.offers import router as offers_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Offer Service")


Instrumentator().instrument(app).expose(app)


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
