from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, CHAR
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

app = FastAPI() #ベース。空箱を作る

# .envファイルの内容をロード
load_dotenv()

# CORS設定 (NEXT.jsからのリクエストを許可する)
origins = [
    "http://localhost:3000",  # NEXT.jsのデフォルトポート
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベースの設定 (MySQLとの接続)
DATABASE_URL = os.getenv("DATABASE_URL") # 環境変数からDATABASE_URLを取得 # 自分の環境に合わせて設定
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# モデルの定義 (例として商品モデル)
class ItemModel(Base):
    __tablename__ = "商品マスタ"
    prd_id = Column(Integer, primary_key=True)
    code = Column(CHAR(13), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)


@app.get("/")
def home():
    return {"message": "FastAPIで作成"}

@app.get("/check")
async def check():
    return {"message": "確認しました"}


# エンドポイントの追加
@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).all()
    return items