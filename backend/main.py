
from fastapi import FastAPI

app = FastAPI(title="DeepGaurd")

@app.get("/")
def home():
    return {"message": "DeepGaurd AI Backend is running"}

from fastapi import UploadFile, File

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_path=f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return{
        "filename":file.filename,
        "message":"File uploaded successfully",
        "path":file_path
    }