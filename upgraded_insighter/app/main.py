from fastapi import FastAPI
from app.api.ingest_api import router as ingest_router
from app.db.models import Base
from app.db.session import engine

app = FastAPI()
app.include_router(ingest_router)

@app.get("/")
def root():
    return {"message": "InsightSniffer API is running. Visit /docs to upload data."}


# Create tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    
