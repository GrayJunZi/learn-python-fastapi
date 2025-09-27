from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from .models import Shipment

engine = create_engine(
    # 创建数据库连接
    url='sqlite:///sqlite.db',
    # 查看执行的SQL语句
    echo=True,
    # 同时运行SQLite数据库和FastAPI服务器，需要使用不同的线程
    connect_args={
        'check_same_thread': False
    }
)

# 创建数据库表
def create_db_tables():
    # 创建所有的表
    SQLModel.metadata.create_all(bind=engine)

# 获取会话
def get_session():
    with Session(bind=engine) as session:
        yield session

SessionDependency = Annotated[Session, Depends(get_session)]