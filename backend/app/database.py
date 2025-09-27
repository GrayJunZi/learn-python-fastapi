import sqlite3
from contextlib import contextmanager

from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any

class Database:
    def connect(self):
        # 连接SQLite数据库
        self.connection = sqlite3.connect('sqlite.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_table(self):
        # 1. 创建表
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            weight REAL,
            status TEXT
        )
        ''')

    def create(self, shipment: ShipmentCreate) -> int:
        # 2. 添加 shipment 数据
        self.cursor.execute('''
        INSERT INTO shipment (content, weight, status) VALUES (:content, :weight, :status)
        ''', {
            **shipment.model_dump(),
            "status": "placed"
        })

        # 提交
        self.connection.commit()

        return self.cursor.lastrowid

    def get(self, id: int) -> dict[str, int] | None:
        # 3. 读取 shipment 数据
        self.cursor.execute('''
            SELECT * FROM shipment
            WHERE id = :id
        ''', {
            "id": id
        })

        # 获取前一条数据
        row = self.cursor.fetchone()

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3],
        } if row else None

    def update(self,id: int,  shipment: ShipmentUpdate) -> dict[str, Any]:
        # 4. 更新 shipment 数据
        self.cursor.execute('''
                       UPDATE shipment
                       SET status = :status
                       WHERE id = :id
                       ''', {
            "id": id,
            "status": "in_transit"
        })
        self.connection.commit()

        return self.get(id)

    def delete(self, id: int):
        self.cursor.execute('''
        DELETE FROM shipment WHERE id = :id
                            ''', {
            "id": id,
        })
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

@contextmanager
def managed_db():
    db = Database()
    print('Database Setup Success!')

    db.connect()
    print('Database Connected!')

    db.create_table()
    print('Database Table Created!')

    yield db

    # 释放数据库连接
    db.close()
    print('Database Table Closed!')

with managed_db() as db:
    print(db.get(id=1))
    pass