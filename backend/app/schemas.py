from enum import Enum
from random import randint
from pydantic import BaseModel, Field

def random_destination():
    return randint(11000,11999)

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

# 定义基类（将重复声明的字段抽象出来）
class BaseShipment(BaseModel):
    content: str
    weight: float=Field(le=25)

# 继承基类
class ShipmentRead(BaseShipment):
    status: ShipmentStatus

# 继承基类
class ShipmentCreate(BaseShipment):
    pass

# 继承基类
class ShipmentUpdate(BaseModel):
    status: ShipmentStatus