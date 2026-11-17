from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import models

from services.image_detector import analyze_image

app = FastAPI(title="DeepGaurd")

# --- CORS SETUP ---
# Jab tak admin panel (HTML/CSS/JS) backend se alag port/file se khula hai,
# browser bina CORS ke requests block kar dega. Development ke liye "*"
# theek hai, lekin production mein yahan apna asli frontend URL likhna.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "DeepGaurd AI Backend is running"}

from fastapi import UploadFile, File

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_path=f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    image_info=analyze_image(file_path)

    return{
        "filename":file.filename,
        "message":"File uploaded successfully",
        "path":file_path,
        "image_info":image_info
    }

@app.get("/admin/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):

    total_users = db.query(models.User).count()
    total_analyses = db.query(models.Analysis).count()

    real_count = db.query(models.Analysis).filter(
        models.Analysis.result == "Real"
    ).count()

    fake_count = db.query(models.Analysis).filter(
        models.Analysis.result == "Fake"
    ).count()

    return {
        "total_users": total_users,
        "total_analyses": total_analyses,
        "real_count": real_count,
        "fake_count": fake_count
    }

@app.get("/admin/dashboard/recent-analyses")
def recent_analyses(db: Session = Depends(get_db)):

    analyses = db.query(models.Analysis).order_by(
        models.Analysis.created_at.desc()
    ).limit(10).all()

    return [
        {
            "id": analysis.id,
            "file_name": analysis.file_name,
            "file_type": analysis.file_type,
            "result": analysis.result,
            "confidence": analysis.confidence,
            "created_at": analysis.created_at
        }
        for analysis in analyses
    ]

@app.get("/admin/dashboard/recent-users")
def recent_users(db: Session = Depends(get_db)):

    users = db.query(models.User).order_by(
        models.User.created_at.desc()
    ).limit(10).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "status": user.status,
            "created_at": user.created_at
        }
        for user in users
    ]

@app.get("/admin/dashboard/file-types")
def file_type_distribution(db: Session = Depends(get_db)):

    image_count = db.query(models.Analysis).filter(
        models.Analysis.file_type == "image"
    ).count()

    video_count = db.query(models.Analysis).filter(
        models.Analysis.file_type == "video"
    ).count()

    audio_count = db.query(models.Analysis).filter(
        models.Analysis.file_type == "audio"
    ).count()

    return {
        "image": image_count,
        "video": video_count,
        "audio": audio_count
    }