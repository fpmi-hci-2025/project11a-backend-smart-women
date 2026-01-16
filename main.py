from fastapi import FastAPI, HTTPException, Query, Depends, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="Onlearn API",
    description="Educational web platform API",
    version="1.0.0"
)

# CORS middleware
# Для продакшена добавьте URL вашего фронтенда через переменную окружения
import os
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

# SQLAlchemy ORM Models
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=False)
    image = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    price = Column(String, nullable=True)
    level = Column(String, nullable=True)

class EnrollmentModel(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    progress_percent = Column(Integer, default=0)

class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(String, nullable=False)  # ISO format string

# Pydantic Models
class User(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user: User
    message: str = "Login successful"

class Course(BaseModel):
    id: int
    title: str
    description: str
    teacher_id: int
    is_published: bool
    image: Optional[str] = None
    rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    price: Optional[str] = None
    level: Optional[str] = None

class Enrollment(BaseModel):
    id: int
    user_id: int
    course_id: int
    progress_percent: int = Field(ge=0, le=100)

class EnrollRequest(BaseModel):
    course_id: int

class ProgressUpdateRequest(BaseModel):
    progress_percent: int = Field(ge=0, le=100)

class EnrollmentWithCourse(BaseModel):
    enrollment_id: int
    course: Course
    progress_percent: int

class Comment(BaseModel):
    id: int
    user_id: int
    course_id: int
    text: str
    created_at: str
    user_name: Optional[str] = None

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Cookie-based authentication
def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserModel:
    # Для отладки в продакшене (можно убрать после проверки)
    import os
    is_production = os.getenv("RENDER") is not None or os.getenv("ENVIRONMENT") == "production"
    
    user_id = request.cookies.get("session_user_id")
    
    # Логируем для отладки в продакшене
    if is_production:
        print(f"[AUTH DEBUG] Cookie received: {user_id}")
        print(f"[AUTH DEBUG] All cookies: {request.cookies}")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# Seed initial data
def seed_data(db: Session):
    if db.query(UserModel).first() is not None:
        return
    
    users = [
        UserModel(id=1, name="Alice Johnson", email="alice@example.com", role=UserRole.STUDENT.value, hashed_password=get_password_hash("password123")),
        UserModel(id=2, name="Bob Smith", email="bob@example.com", role=UserRole.STUDENT.value, hashed_password=get_password_hash("password123")),
        UserModel(id=3, name="Dr. Sarah Williams", email="sarah@example.com", role=UserRole.TEACHER.value, hashed_password=get_password_hash("password123")),
        UserModel(id=4, name="Prof. Michael Brown", email="michael@example.com", role=UserRole.TEACHER.value, hashed_password=get_password_hash("password123")),
        UserModel(id=5, name="Admin User", email="admin@example.com", role=UserRole.ADMIN.value, hashed_password=get_password_hash("password123")),
    ]
    db.add_all(users)
    
    courses = [
        CourseModel(id=1, title="Веб-разработка для начинающих: HTML, CSS, JavaScript", description="Этот курс предназначен для тех, кто хочет начать карьеру в веб-разработке с нуля.", teacher_id=3, is_published=True, image="/src/assets/course-web.jpg", rating=4.8, review_count=1234, price="4 990 ₽", level="Начальный"),
        CourseModel(id=2, title="Основы UI/UX дизайна: от идеи до прототипа", description="Изучите основы дизайна пользовательских интерфейсов и создайте свой первый прототип.", teacher_id=3, is_published=True, image="/src/assets/course-design.jpg", rating=4.9, review_count=987, price="5 490 ₽", level="Начальный"),
        CourseModel(id=3, title="Python для анализа данных: pandas, numpy, matplotlib", description="Мастер-класс по работе с данными в Python.", teacher_id=4, is_published=True, image="/src/assets/course-data.jpg", rating=4.9, review_count=1456, price="7 490 ₽", level="Средний"),
        CourseModel(id=4, title="Machine Learning: введение в искусственный интеллект", description="Введение в машинное обучение и искусственный интеллект.", teacher_id=4, is_published=True, image="/src/assets/course-data.jpg", rating=4.9, review_count=1789, price="9 990 ₽", level="Продвинутый"),
    ]
    db.add_all(courses)
    
    enrollments = [
        EnrollmentModel(id=1, user_id=1, course_id=1, progress_percent=45),
        EnrollmentModel(id=2, user_id=1, course_id=2, progress_percent=20),
        EnrollmentModel(id=3, user_id=2, course_id=1, progress_percent=80),
        EnrollmentModel(id=4, user_id=2, course_id=3, progress_percent=100),
    ]
    db.add_all(enrollments)
    
    # Примеры комментариев
    from datetime import datetime
    comments = [
        CommentModel(id=1, user_id=1, course_id=1, text="Отличный курс! Очень понятно объясняется материал.", created_at=datetime.now().isoformat()),
        CommentModel(id=2, user_id=2, course_id=1, text="Спасибо за курс, много полезной информации!", created_at=datetime.now().isoformat()),
    ]
    db.add_all(comments)
    db.commit()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

# Endpoints
@app.get("/")
async def root():
    return "Onlearn API - VERSION 2.0"

@app.get("/test")
async def test():
    return {"status": "ok", "message": "Backend работает!"}

@app.post("/login")
async def login(request: Request, response: Response, db: Session = Depends(get_db)):
    # Максимально простое чтение JSON
    import json
    body_bytes = await request.body()
    body = json.loads(body_bytes.decode())
    
    email = body.get("email") or ""
    password = body.get("password") or ""
    
    if not email or not password:
        raise HTTPException(status_code=422, detail="Email and password required")
    
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Определяем secure и samesite для cookies
    import os
    is_production = os.getenv("RENDER") is not None or os.getenv("ENVIRONMENT") == "production"
    
    # Для продакшена (кросс-доменные запросы): SameSite=None требует Secure=True
    # Для локальной разработки: SameSite=Lax, Secure=False
    if is_production:
        secure_cookie = True
        samesite_value = "none"  # Для кросс-доменных запросов
    else:
        secure_cookie = False
        samesite_value = "lax"   # Для локальной разработки
    
    # Логирование для отладки
    print(f"[LOGIN] Setting cookie: user_id={user.id}, secure={secure_cookie}, samesite={samesite_value}, is_production={is_production}")
    
    response.set_cookie(
        key="session_user_id",
        value=str(user.id),
        httponly=True,
        samesite=samesite_value,
        secure=secure_cookie,
        max_age=86400 * 7,
        path="/"
    )
    
    # Дополнительная проверка для отладки
    print(f"[LOGIN] Cookie should be set in response headers")
    
    return {
        "success": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        },
        "message": "Login successful"
    }

@app.post("/logout")
async def logout(response: Response):
    # Используем те же настройки, что и при установке cookie
    import os
    is_production = os.getenv("RENDER") is not None or os.getenv("ENVIRONMENT") == "production"
    
    if is_production:
        secure_cookie = True
        samesite_value = "none"
    else:
        secure_cookie = False
        samesite_value = "lax"
    
    response.delete_cookie(
        key="session_user_id",
        path="/",
        samesite=samesite_value,
        secure=secure_cookie
    )
    return {"success": True, "message": "Logged out"}

@app.get("/me", response_model=User)
async def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    return User(id=current_user.id, name=current_user.name, email=current_user.email, role=UserRole(current_user.role))

@app.get("/courses", response_model=List[Course])
async def list_courses(published_only: Optional[bool] = Query(None), db: Session = Depends(get_db)):
    query = db.query(CourseModel)
    if published_only is not None:
        query = query.filter(CourseModel.is_published == published_only)
    db_courses = query.all()
    return [Course(id=c.id, title=c.title, description=c.description, teacher_id=c.teacher_id, is_published=c.is_published, image=c.image, rating=c.rating, review_count=c.review_count, price=c.price, level=c.level) for c in db_courses]

@app.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return Course(id=db_course.id, title=db_course.title, description=db_course.description, teacher_id=db_course.teacher_id, is_published=db_course.is_published, image=db_course.image, rating=db_course.rating, review_count=db_course.review_count, price=db_course.price, level=db_course.level)

@app.post("/enroll", response_model=Enrollment, status_code=201)
async def enroll_user(enroll_request: EnrollRequest, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_course = db.query(CourseModel).filter(CourseModel.id == enroll_request.course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    existing = db.query(EnrollmentModel).filter(EnrollmentModel.user_id == current_user.id, EnrollmentModel.course_id == enroll_request.course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")
    db_enrollment = EnrollmentModel(user_id=current_user.id, course_id=enroll_request.course_id, progress_percent=0)
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return Enrollment(id=db_enrollment.id, user_id=db_enrollment.user_id, course_id=db_enrollment.course_id, progress_percent=db_enrollment.progress_percent)

@app.get("/my-courses", response_model=List[EnrollmentWithCourse])
async def get_my_courses(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_enrollments = db.query(EnrollmentModel).filter(EnrollmentModel.user_id == current_user.id).all()
    result = []
    for db_enrollment in db_enrollments:
        db_course = db.query(CourseModel).filter(CourseModel.id == db_enrollment.course_id).first()
        if db_course:
            result.append(EnrollmentWithCourse(
                enrollment_id=db_enrollment.id,
                course=Course(id=db_course.id, title=db_course.title, description=db_course.description, teacher_id=db_course.teacher_id, is_published=db_course.is_published, image=db_course.image, rating=db_course.rating, review_count=db_course.review_count, price=db_course.price, level=db_course.level),
                progress_percent=db_enrollment.progress_percent
            ))
    return result

@app.patch("/enrollments/{enrollment_id}/progress", response_model=Enrollment)
async def update_progress(enrollment_id: int, request: ProgressUpdateRequest, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_enrollment = db.query(EnrollmentModel).filter(EnrollmentModel.id == enrollment_id).first()
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if db_enrollment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db_enrollment.progress_percent = request.progress_percent
    db.commit()
    db.refresh(db_enrollment)
    return Enrollment(id=db_enrollment.id, user_id=db_enrollment.user_id, course_id=db_enrollment.course_id, progress_percent=db_enrollment.progress_percent)

@app.get("/courses/{course_id}/comments", response_model=List[Comment])
async def get_course_comments(course_id: int, db: Session = Depends(get_db)):
    """Получить все комментарии к курсу"""
    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_comments = db.query(CommentModel).filter(CommentModel.course_id == course_id).order_by(CommentModel.id.desc()).all()
    result = []
    for db_comment in db_comments:
        user = db.query(UserModel).filter(UserModel.id == db_comment.user_id).first()
        result.append(Comment(
            id=db_comment.id,
            user_id=db_comment.user_id,
            course_id=db_comment.course_id,
            text=db_comment.text,
            created_at=db_comment.created_at,
            user_name=user.name if user else None
        ))
    return result

@app.post("/courses/{course_id}/comments", response_model=Comment, status_code=201)
async def create_comment(course_id: int, request: Request, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    """Создать комментарий к курсу"""
    db_course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Читаем JSON напрямую
    import json
    from datetime import datetime
    body_bytes = await request.body()
    body = json.loads(body_bytes.decode())
    text = body.get("text") or ""
    
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=422, detail="Comment text is required")
    
    db_comment = CommentModel(
        user_id=current_user.id,
        course_id=course_id,
        text=text.strip(),
        created_at=datetime.now().isoformat()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    return Comment(
        id=db_comment.id,
        user_id=db_comment.user_id,
        course_id=db_comment.course_id,
        text=db_comment.text,
        created_at=db_comment.created_at,
        user_name=current_user.name
    )

@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    """Удалить свой комментарий"""
    db_comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")
    db.delete(db_comment)
    db.commit()
    return {"success": True, "message": "Comment deleted"}
