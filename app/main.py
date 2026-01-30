from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime

from db import SessionLocal, engine, Base
from models import Task, User

# DB初期化
Base.metadata.create_all(bind=engine)

# パスワードハッシング設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydanticモデル
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

app = FastAPI()

# CORS設定（開発用 - すべてのオリジンを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DBセッション
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Authentication Utilities
# =========================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# =========================
# API Endpoints
# =========================

@app.get("/api")
def read_root():
    return {"message": "Schedule Management API"}

# 登録エンドポイント
@app.post("/api/auth/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # メールアドレスが既に登録されているか確認
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="このメールアドレスは既に登録されています")
    
    # 新規ユーザーを作成
    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "id": new_user.id,
        "email": new_user.email,
        "message": "ユーザー登録が完了しました"
    }

# ログインエンドポイント
@app.post("/api/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="メールアドレスまたはパスワードが正しくありません")
    
    return {
        "id": user.id,
        "email": user.email,
        "message": "ログインしました"
    }

# タスク作成
@app.post("/api/tasks/")
def create_task(
    user_id: str,
    title: str,
    priority: int = 3,
    deadline: str = None,
    db: Session = Depends(get_db)
):
    deadline_dt = None
    if deadline:
        try:
            deadline_dt = datetime.fromisoformat(deadline)
        except:
            pass
    
    task = Task(user_id=user_id, title=title, priority=priority, deadline=deadline_dt)
    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "user_id": task.user_id,
        "title": task.title,
        "priority": task.priority,
        "deadline": task.deadline.isoformat() if task.deadline else None
    }

# タスク一覧取得
@app.get("/api/tasks/")
def read_tasks(user_id: str, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return [
        {
            "id": t.id,
            "user_id": t.user_id,
            "title": t.title,
            "priority": t.priority,
            "deadline": t.deadline.isoformat() if t.deadline else None
        }
        for t in tasks
    ]

# タスク削除
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

# =========================
# Frontend (React build)
# =========================

app.mount(
    "/",
    StaticFiles(directory="../frontend/build", html=True),
    name="frontend"
)