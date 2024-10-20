from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, CHAR, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
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

# Pydanticモデル
class CodeRequest(BaseModel):
    code: str

# 取引マスタモデル
class TransactionModel(Base):
    __tablename__ = "取引マスタ"
    TRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    EMP_CD = Column(CHAR(10), nullable=False)
    STORE_CD = Column(CHAR(5), nullable=False) 
    POS_NO = Column(CHAR(3), nullable=False)
    TOTAL_AMT = Column(Integer, nullable=False)

# Pydanticモデルにstore_cdを追加
class PurchaseRequest(BaseModel):
    items: list
    emp_cd: str
    store_cd: str  # store_cdを追加
    pos_no: str
    total_amt: int

# 取引明細モデル
class TransactionDetailModel(Base):
    __tablename__ = "取引明細"
    TRD_ID = Column(Integer, primary_key=True)
    DTL_ID = Column(Integer, primary_key=True)
    PRD_ID = Column(Integer, nullable=False)
    PRD_CODE = Column(CHAR(13), nullable=False)
    PRD_NAME = Column(String(50), nullable=False)
    PRD_PRICE = Column(Integer, nullable=False)

# 商品を取得するエンドポイント
@app.post("/items/")
def get_item_by_code(request: CodeRequest, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.code == request.code).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"prd_id": item.prd_id, "name": item.name, "price": item.price}

# 購入リクエストを処理するエンドポイント
@app.post("/purchase")
def process_purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    # 合計金額を計算
    total_amount = sum(item['price'] for item in request.items)

    transaction = TransactionModel(
        EMP_CD=request.emp_cd,
        STORE_CD=request.store_cd,  # STORE_CDを追加
        POS_NO=request.pos_no,
        TOTAL_AMT=total_amount,
    )
    db.add(transaction)
    db.commit()

    # 生成されたTRD_IDを取得
    trd_id = transaction.TRD_ID

    # 取引明細に購入リストを追加
    for index, item in enumerate(request.items):
        detail = TransactionDetailModel(
            TRD_ID=trd_id,
            DTL_ID=index + 1,  # 各商品の枝番を生成
            PRD_ID=item['prd_id'],
            PRD_CODE=item['code'],
            PRD_NAME=item['name'],
            PRD_PRICE=item['price'],
        )
        db.add(detail)

    # すべての取引明細をデータベースに保存
    db.commit()

    return {"message": "Purchase processed successfully", "transaction_id": trd_id}

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "FastAPIで作成"}

@app.get("/check")
async def check():
    return {"message": "確認しました"}


