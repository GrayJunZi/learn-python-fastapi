a
    weight = data["weight"]

    if weight > 25:
        raise HTTPException {
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25kgs"
        }

    id = max(shipments.keys()) + 1
    shipments[id] = {
        "content": content,
        "weight": weight,
    }
    
    return {
        "id": id,
    }
```

### 017. 路径参数和查询字符串

```py
@app.get("/shipment/{field}")
def get_shipment_field(field: str, id: int) -> Any:
    return shipments[id][field]
```

## 五、增删改查操作

### 018. PUT 方法

`PUT` 一般用于处理更新数据的请求。

```py
@app.put("/shipment")
def shipment_update(id: int, content: str, weight: float, status: str) -> dict[str, Any]:
    shipments[id] = {
        "content": content,
        "weight": weight,
        "status": status,
    }

    return shipments[id]
```

### 019. PATCH 方法

`PATCH` 用于更新部分字段。

> `PUT` 和 `PATCH` 都可以用来更新数据，但两者之间存在的区别是，我们使用`PUT`替换所有字段，而`PATCH`用于替换部分字段。（但这些并非强制要求）

```py
@app.patch("/shipment")
def patch_shipment(
    id: int, 
    content: str | None = None, 
    weight: float | None = None, 
    status: str | None = None
):
    shipment = shipments[id]

    if content:
        shipment["content"] = content
    if weight:
        shipment["weight] = weight
    if status:
        shipment["status"] = status

    shipments[id] = shipment
    return shipment
```

或者采用字典的方式来更新

```py
@app.patch("/shipment")
def patch_shipment(
    id: int, 
    body: dict[str, Any]
):
    shipment = shipments[id]
    shipment.update(body)
    return shipment
```

### 020. DELETE 方法

```py
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    shipments.pop(id)
    return { "detail", "Shipment with id #{id} is deleted!" }
```

## 六、Pydantic模型

### 021. 为什么使用Pydantic

Pydantic将会验证请求的参数。

```py
from pydantic import BaseModel

class Shipment(BaseModel):
    content: str
    weight: float
    destination: int

@app.post("/shipment")
def submit_shipment(shipment: Shipment) -> Shipment:
    if shipment.weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Maximum weight limit is 25 kgs",
        )

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": shipment.content,
        "weight": shipment.weight,
        "status": "placed",
    }

    return { "id": new_id }
```

### 022. 模型字段

将模型类移到 `schemas.py` 文件单独存储。

```py
from random import randint
from pydantic import BaseModel, Field

def random_destination():
    return randint(11000,11999)

class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int | None = Field(default_factory=random_destination),

```

- `Field(max_length)` - 字符串长度小于等于30。
- `Field(lt=25)` - 验证值必须小于25。
- `Field(le=25, ge=1)` - 验证值必须小于等于25，并且大于等于1。
- `Field(default=None)` - 默认为None。
- `Field(default_factory=random_destination)` - 创建时被调用并赋值返回值。

### 023. 枚举

定义枚举

```py
class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
```

### 024. 响应模型

第一种可以通过定义返回的模型类。

```py
@app.get("/shipment")
def get_shipment(id: int) -> Shipment:
    shipment = shipments[id]
    return Shipment(
        # 使用 ** 解包字典中的内容
        **shipment
    )
```

第二种方式可以在路由上标记响应的模型。

```py
@app.get("/shipment", response_model=Shipment)
def get_shipment(id: int):
    return shipments[id]
```

### 025. 不同的模型

可以为不同的接口创建独立的模型，使接口只接收和返回需要的内容。

```py
# 定义基类（将重复声明的字段抽象出来）
class BaseShipment(BaseModel):
    content: str
    weight: float=Field(le=25)
    destination: int

# 继承基类
class ShipmentRead(BaseShipment):
    status: ShipmentStatus

# 继承基类
class ShipmentCreate(BaseShipment):
    pass

# 继承基类
class ShipmentUpdate(BaseModel):
    status: ShipmentStatus
```

### 026. 技巧和提示 (Tips & Tricks)

1. 可以通过在路由中将`response_model`设为`None`，这在`FastAPI`中表示跳过此用例的验证。
```py
@app.post("/shipment", response_model=None)
```

2. 使用模型转储方法。
```py
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        **shipment.model_dump(),
        "status": "placed",
    }
```

3. 为字段添加默认值
```py
class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=None, le=25)
    destination: int | None = Field(default=None)
    status: ShipmentStatus()
```

4. 更新时使用模型转储方法排除默认值字段
```py
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    shipments[id].update(body.model_dump(exclude_none=True)
    return shipments[id]
```

## 七、SQL数据库

> 如何使用SQL数据库持久化数据

### 027. JSON

> JSON 文件可以包含与字典相同的结构，我们可以将数据保存到JSON文件中。

读取json文件
```py
import json

shipments = {}

with open("shipments.json") as json_file:
    data = json.load(json_file)

    for value in data:
        shipments[value["id"]] = value

print(shipments)
```

### 028. 什么是SQL

SQL即结构化查询语言(Structured Query Language)，SQL数据库以固定列存储表和数据，并允许与数据交互，比如创建数据、读取数据等，使用SQL操作数据。

### 029. SQLite 数据库

引入 `sqlite3` 来操作连接Sqlite

```py
import sqlite3

# 连接SQLite数据库
connection = sqlite3.connect('sqlite.db')

cursor = connection.cursor()

# 1. 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS shipment (
    id INTEGER,
    content TEXT,
    weight REAL,
    status TEXT
)
''')

# 关闭数据库连接
connection.close()
```

### 030. 添加数据

执行插入SQL并提交

```py
# 添加数据
cursor.execute('''
INSERT INTO shipment (id, content, weight, status) VALUES (1, 'palm trees', 8.5, 'placed')
''')

# 提交
connection.commit()
```

### 031. 获取数据

编写SQL的Where条件来筛选数据。

```py
data =cursor.execute('''
SELECT * FROM shipment
WHERE id = 1
''').fetchall()
```

获取所有数据可使用 `fetchall()`
```py
cursor.fetchall()
```

获取指定几条数据可使用 `fetchmany()`
```py
cursor.fetchman(2)
```

获取一条数据可使用 `fetchone`
```py
cursor.fetchone()
```

### 032. 主键

删除数据

```py
cursor.excecute('''
DELETE FROM shipment 
''')
connection.commit()
```

删除数据库
```py
cursor.excecute('''
DROP TABLE shipment 
''')
connection.commit()
```

### 033. 更新数据

```py
cursor.execute('''
UPDATE shipment SET status = 'in_transit'
WHERE id = 1
''')
connection.commit()
```

### 034. SQL查询参数

如果SQL查询时直接将参数拼接到SQL字符串中将会造成SQL注入的问题，所以需要将其进行参数化。

可以使用 `?` 的形式作为占位符，实际执行时将元组参数替换进来。

```py
status = 'placed'
cursor.execute('''
UPDATE shipment SET status = ?
WHERE id = 1
''', (status, ))
connection.commit()

```

或者采用 `:` 为占位符命名，然后将参数以字典的形式传入进去。

```py
id = 0,
status = 'in_transit'
cursor.execute('''
UPDATE shipment SET status = :status
WHERE id = :id
''', {'status':status,'id':id})
connection.commit()
```

### 035. 数据库

封装数据库操作类

```py
import sqlite3

from .schemas import ShipmentCreate, ShipmentUpdate
from typing import Any

class Database:
    def __init__(self):
        # 连接SQLite数据库
        self.connection = sqlite3.connect('sqlite.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_table('shipment')

    def create_table(self, name: str):
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
        ''', (id,))

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
```

### 036. API使用

在接口层调用封装好的数据库类的方法。

```py
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic.v1 import NoneStr
from scalar_fastapi import get_scalar_api_reference

from .database import Database
from .schemas import ShipmentRead, ShipmentCreate, ShipmentUpdate

app = FastAPI()

db = Database()


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment


@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    id = db.create(shipment)
    return {"id": id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment: ShipmentUpdate):
    shipment = db.update(id, shipment)
    return shipment


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)

    return {"detail": f"Shipment id #{id} was deleted"}


@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )
```

## 八、SQL模型

### 037. 上下文管理

没有上下文管理时，我们将需要自己在类中写 `__enter__` 和 `__exit__` 函数来管理数据库的连接与释放。

```py
import sqlite3

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
        ''', (id,))

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

    def __enter__(self):
        self.connect()
        self.create_table()
        return self

    def __exit__(self, *args):
        self.close()

# 自动调用 `__enter__` 函数，执行完成后自动执行 `__exit__`
with Database() as db:
    db.get(1)
    pass
```

使用上文管理时无需使用额外的函数来管理，直接在我们的函数中标记 `@contextmanager` 。

```py
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
        ''', (id,))

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
    db.get(1)
    pass
```

使用以下命令来执行。
```py
python -m app.database
```

### 038. SQL模型

我们可以使用SQL模型通过Python类生成数据库表。

安装 `sqlmodel`
```bash
pip install sqlmodel
```

定义SQL模型，默认继承了`SQLModel`的类名会转换为小写作为表名，也可以指定`__tablename__`作为自定义表名。

```py
import datetime
from enum import Enum

from sqlmodel import SQLModel, Field

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel):
    # 自定义表名
    __tablename__ = 'shipments'

    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estinated_delivery: datetime
```

### 039. 数据库引擎

我们可以创建一个 `session.py` 文件，用于管理我们的数据库连接。

```py
from sqlalchemy import create_engine
from sqlmodel import SQLModel

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

# 创建所有的表
SQLModel.metadata.create_all(bind=engine)
```

要想自动创建表，需要在模型类的定义上增加一个`table=True`的参数。
```py

class Shipment(SQLModel, table=True):
    # 自定义表名
    __tablename__ = 'shipments'

    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estinated_delivery: datetime
```

### 040. 服务生命周期 (Server Lifespan)

定义一个生命周期处理器函数，并且标记一个异步上下文管理，它可以在服务启动和关闭时处理一些事情。

```py
from contextlib import asynccontextmanager
from rich import panel

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server Started ...", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("Server Stopped ...", border_style="red"))

app = FastAPI(lifespan=lifespan_handler)
```

### 041. 依赖注入

在 `session.py` 文件中定义获取会话的函数。

```py
# 获取会话
def get_session():
    with Session(bind=engine) as session:
        yield session
```

然后在接口上增加参数 `Depends(get_session)` 将 `Session` 对象注入进来。

```py
from fastapi.params import Depends

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: Session = Depends(get_session)):
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment
```

anShipmentUpdate):
    shipment = db.update(id, shipment)
    return shipment


@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)

    return {"detail": f"Shipment id #{id} was deleted"}


@app.get("/scalar")
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API"
    )
```

## 八、SQL模型

### 037. 上下文管理

没有上下文管理时，我们将需要自己在类中写 `__enter__` 和 `__exit__` 函数来管理数据库的连接与释放。

```py
import sqlite3

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
        ''', (id,))

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

    def __enter__(self):
        self.connect()
        self.create_table()
        return self

    def __exit__(self, *args):
        self.close()

# 自动调用 `__enter__` 函数，执行完成后自动执行 `__exit__`
with Database() as db:
    db.get(1)
    pass
```

使用上文管理时无需使用额外的函数来管理，直接在我们的函数中标记 `@contextmanager` 。

```py
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
        ''', (id,))

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
    db.get(1)
    pass
```

使用以下命令来执行。
```py
python -m app.database
```

### 038. SQL模型

我们可以使用SQL模型通过Python类生成数据库表。

安装 `sqlmodel`
```bash
pip install sqlmodel
```

定义SQL模型，默认继承了`SQLModel`的类名会转换为小写作为表名，也可以指定`__tablename__`作为自定义表名。

```py
import datetime
from enum import Enum

from sqlmodel import SQLModel, Field

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel):
    # 自定义表名
    __tablename__ = 'shipments'

    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estinated_delivery: datetime
```

### 039. 数据库引擎

我们可以创建一个 `session.py` 文件，用于管理我们的数据库连接。

```py
from sqlalchemy import create_engine
from sqlmodel import SQLModel

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

# 创建所有的表
SQLModel.metadata.create_all(bind=engine)
```

要想自动创建表，需要在模型类的定义上增加一个`table=True`的参数。
```py

class Shipment(SQLModel, table=True):
    # 自定义表名
    __tablename__ = 'shipments'

    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estinated_delivery: datetime
```

### 040. 服务生命周期 (Server Lifespan)

定义一个生命周期处理器函数，并且标记一个异步上下文管理，它可以在服务启动和关闭时处理一些事情。

```py
from contextlib import asynccontextmanager
from rich import panel

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("Server Started ...", border_style="green"))
    create_db_tables()
    yield
    print(panel.Panel("Server Stopped ...", border_style="red"))

app = FastAPI(lifespan=lifespan_handler)
```

### 041. 依赖注入

在 `session.py` 文件中定义获取会话的函数。

```py
# 获取会话
def get_session():
    with Session(bind=engine) as session:
        yield session
```

然后在接口上增加参数 `Depends(get_session)` 将 `Session` 对象注入进来。

```py
from fastapi.params import Depends

@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: Session = Depends(get_session)):
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment
```

### 042. 会话依赖

定义 `Annotated` 类型

```py
from typing import Annotated
SessionDependency = Annotated[Session, Depends(get_session)]
```

将 `Session` 对象声明为该类型即可。

```py
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDependency):
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment
```