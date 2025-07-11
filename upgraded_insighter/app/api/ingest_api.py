from fastapi import APIRouter, UploadFile
from app.ingest.mixpanel_loader import load_mixpanel_json

router = APIRouter()

@router.post("/upload-mixpanel")
async def upload_json(file: UploadFile):
    with open("temp.json", "wb") as f:
        content = await file.read()
        f.write(content)

    load_mixpanel_json("temp.json")
    return {"message": "Data ingested successfully"}
