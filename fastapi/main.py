from fastapi import HTTPException,Depends,FastAPI
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal,engine
from fastapi.middleware.cors import CORSMiddleware
import models

app = FastAPI()

origins = ["localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str


class TransactionModel(TransactionBase):
    id: int

    class Config:
        orm_mode=True


def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()



db_dependency = Annotated[Session,Depends(get_db)]
models.Base.metadata.create_all(bind=engine)

@app.post("/transactions/",response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase,db: db_dependency):
    db_transaction = models.Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

