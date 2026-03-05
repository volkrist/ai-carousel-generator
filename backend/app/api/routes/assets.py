from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.storage_service import upload_file

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/upload")
async def upload_asset(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    data = await file.read()

    result = upload_file(
        file_bytes=data,
        filename=file.filename,
        content_type=file.content_type,
    )

    return result
