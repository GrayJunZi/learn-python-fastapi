from datetime import datetime
from random import randint
from pydantic import BaseModel, Field

from app.database.models import ShipmentStatus

def random_destination():
    return randint(11000,11999)

# 定义基类（将重复声明的字段抽象出来）
class BaseShipment(BaseModel):
    content: str
    weight: float=Field(le=25)
    destination: int

# 继承基类
class ShipmentRead(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime

# 继承基类
class ShipmentCreate(BaseShipment):
    pass

# 继承基类
class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)