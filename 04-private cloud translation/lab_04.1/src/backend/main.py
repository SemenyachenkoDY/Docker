from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

# ──────────────────────────────────────────────
# Подключение к PostgreSQL через переменные окружения
# ──────────────────────────────────────────────
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "courses_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ──────────────────────────────────────────────
# Модель таблицы «Курсы»
# ──────────────────────────────────────────────
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)          # Название курса
    duration = Column(Float)                    # Длительность (часы)
    author = Column(String)                     # Автор
    rating = Column(Float)                      # Рейтинг (1-5)

# ──────────────────────────────────────────────
# Ожидание готовности БД (с повторными попытками)
# ──────────────────────────────────────────────
MAX_RETRIES = 30
for attempt in range(MAX_RETRIES):
    try:
        Base.metadata.create_all(bind=engine)
        print(f"✅ БД подключена (попытка {attempt + 1})")
        break
    except Exception as e:
        print(f"⏳ Ожидание БД... попытка {attempt + 1}/{MAX_RETRIES}: {e}")
        time.sleep(2)
else:
    raise RuntimeError("❌ Не удалось подключиться к БД после 30 попыток")

# ──────────────────────────────────────────────
# FastAPI приложение
# ──────────────────────────────────────────────
app = FastAPI(title="Learning Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────
# Pydantic-схема для валидации входных данных
# ──────────────────────────────────────────────
class CourseModel(BaseModel):
    name: str
    duration: float = Field(gt=0, description="Длительность в часах")
    author: str
    rating: float = Field(ge=1, le=5, description="Рейтинг от 1 до 5")

# ──────────────────────────────────────────────
# CRUD-эндпоинты
# ──────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Learning Platform API is running"}

@app.get("/courses")
def get_courses():
    """Получить список всех курсов."""
    db = SessionLocal()
    courses = db.query(Course).all()
    db.close()
    return [
        {"id": c.id, "name": c.name, "duration": c.duration, "author": c.author, "rating": c.rating}
        for c in courses
    ]

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    """Получить курс по ID."""
    db = SessionLocal()
    course = db.query(Course).filter(Course.id == course_id).first()
    db.close()
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    return {"id": course.id, "name": course.name, "duration": course.duration, "author": course.author, "rating": course.rating}

@app.post("/courses")
def add_course(course: CourseModel):
    """Добавить новый курс."""
    db = SessionLocal()
    new_course = Course(
        name=course.name,
        duration=course.duration,
        author=course.author,
        rating=course.rating,
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    db.close()
    return {"id": new_course.id, "name": new_course.name, "duration": new_course.duration, "author": new_course.author, "rating": new_course.rating}

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    """Удалить курс по ID."""
    db = SessionLocal()
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        db.close()
        raise HTTPException(status_code=404, detail="Курс не найден")
    db.delete(course)
    db.commit()
    db.close()
    return {"detail": f"Курс {course_id} удален"}
