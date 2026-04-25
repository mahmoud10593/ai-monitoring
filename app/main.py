from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.ai_agent import analyze_with_openclaw
from app.monitor import check_website   
from app.database import engine, SessionLocal
from app.models import Base, Website

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ إنشاء الجداول
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "AI Monitoring System Running 🚀"}


# ➕ إضافة موقع
@app.get("/add")
def add_website(url: str):
    db = SessionLocal()

    if not url.startswith("http"):
        url = "https://" + url

    existing = db.query(Website).filter(Website.url == url).first()
    if existing:
        return {"message": "Website already exists"}

    site = Website(url=url)
    db.add(site)
    db.commit()

    return {"message": "Website added"}


# 📋 عرض المواقع
@app.get("/websites")
def get_websites():
    db = SessionLocal()
    return db.query(Website).all()


@app.get("/clear")
def clear_db():
    db = SessionLocal()
    db.query(Website).delete()
    db.commit()
    return {"message": "Database cleared"}

# 🔍 check موقع واحد (ده اللي كان ناقص!)
@app.get("/check")
def check(url: str):
    if not url.startswith("http"):
        url = "https://" + url

    result = check_website(url)

    ai = analyze_with_openclaw(result)

    return {
        "monitoring": result,
        "ai": ai
    }

# 🔄 check كل المواقع
@app.get("/check-all")
def check_all():
    db = SessionLocal()

    websites = db.query(Website).all()
    results = []

    for site in websites:
        result = check_website(site.url)

        results.append({
            "url": site.url,
            "status": result.get("status"),
            "response_time": result.get("response_time"),
            "ssl_valid": result.get("ssl_valid")
        })

    return results