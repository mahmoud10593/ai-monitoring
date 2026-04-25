from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from app.database import Base

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CheckResult(Base):
    __tablename__ = "checks"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    status = Column(Integer)
    response_time = Column(Float)
    ssl_valid = Column(Boolean)
    risk = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)