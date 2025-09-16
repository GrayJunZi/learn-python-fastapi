# learn-python-fastapi

## 一、介绍 (Introduction)

### 001. 课程概览

01. 介绍
02. 开始
03. 路径参数
04. 查询参数
05. 增删改查操作
06. Pydantic模型
07. SQL数据库
08. SQL模型
09. 异步IO
10. PostgreSQL
11. 注册用户
12. OAuth 2
13. 登出用户
14. SQL关系
15. Alembic
16. Delivery Partner
17. Shipment Event
18. 发送邮件
19. 自定义响应
20. 邮件确认
21. 密码重置
22. SMS
23. 回顾
24. Celery
25. 多对多
26. 错误处理
27. 中间件
28. API文档
29. API测试
30. ReactJS
31. Docker
32. 部署
33. Tips & Tricks

### 002. 什么是 REST APIs？

API允许程序通过代码直接向另一服务器请求数据，无需浏览器或用户界面。这种交互被称为 API 或 应用程序接口(Application Programming Interface)。

REST 代表 表述性状态传递(REpresentational State Transfer)，是构建API的流行方法，它为API的设计和功能提供了规范与规则。

当程序需要与REST API 通信时，它会向服务器特定地址发送请求，这个地址被称为端点(Endpoint)，技术上是一个URI(统一资源标识符, Uniform Resource Identifier)。

发送API请求的程序称为客户端(Client)，每个请求都是特定的HTTP方法。
- GET - 用于读取数据
- POST - 用于创建新数据
- PUT - 用于更新现有数据
- DELETE - 用于删除数据

HTTP方法用于向服务器告知客户端希望在端点资源上执行的操作。

此外请求时还可以携带，请求头(Header)、请求体(Body)。

请求响应会提供响应码，与响应体。

- 2** - 成功
- 3** - 重定向
- 4** - 客户端错误
- 5** - 服务端错误

### 003. 什么是 FastAPI？

FastAPI 是一个用于构建API和Python的极速Web框架，由 `Sebastian Remirez` 开发，并迅速变得流行。

FastAPI 还可以使用数据验证、自动生成API文档、使用OpenAPI标准、依赖注入和异步代码来构建稳健且可扩展的API。

FastAPI 依赖以下关键库：
- Starlette - 作为底层Web服务器。
- Pydantic - 用于处理数据验证。

### 004. 为什么选择 FastAPI？

| | django | FastAPI | Flask |
| -- | -- | -- | -- |
| 开始 | 需初始设置与项目结构配置 | 开箱即用 | 开箱即用 |
| 工具 | 内置 | 第三方库 | 第三方库 |
| 安全 | 内置 | OAuth 2 | 手动 |
| 扩展 | 困难 | 易于扩展，模块化 | 易于扩展，模块化 |
| 性能 | 较差 | 性能极高，支持异步操作 | 较差 |
| 数据验证 | 使用ORM | 优异，使用标准Python类型提示 | 手动 |
| OpenAPI | 不支持 | 支持 | 不支持 |

- Flask适合构建简单API（当你希望最小化结构时）。
- Django适合全栈应用，内置功能可节省开发时间，尽管学习曲线陡峭。
- FastAPI 在高性能和强大功能中达到最佳平衡。

## 二、开始 (Getting Started)

### 005. 安装与设置

#### 下载 Python

进入 [Python](https://python.org/downloads/) 官网进行下载。

 #### 虚拟环境(virtual env)

 默认情况下安装任何包都会全局安装并且全局可用的，我们将创建虚拟环境并进行包的安装，这样可以隔离项目。

创建虚拟环境
```bash
python -m venv ./venv
```

激活虚拟环境
```bash
.\venv\Scripts\activate
```

安装 `fastapi`
```bash
pip install fastapi[all]
```

#### 安装 VSCode 扩展

- Python
- Ruff
- error lens

### 006. API Endpoint

启动服务
```bash
fastapi dev
```

访问接口地址：http://127.0.0.1:8000/

### 007. API 文档

访问API文档地址：http://127.0.0.1:8000/docs


另一种自动生成文档，通过Redoc访问，它是 Swagger UI 轻量版：http://127.0.0.1:8000/redoc

安装 `scalar`，它使用`OpenAPI`协议。
```bash
pip install scalar_fastapi
```

访问 Scalar 文档地址：http://127.0.0.1:8000/scalar/

## 三、路径参数

### 008. 数据类型提示 (Type Hinting)

通过为变量指定数据类型，来实现对应类型的函数提示，当赋值为不同类型的值时编辑器也会进行提示，但不是强制的。

```py
text: str = "value"
pert: int = 90
temp: float = 37.5
```

在函数中可以通过 `->` 方式来声明方法的类型。
```py
def root(num: int) -> float:
    return pow(num, .5)

root_25 = root(25)
```

可以通过管道运算符`|` 来同时声明多种类型。

```py
number: int | float = 12

def root(num: int | float) -> float:
    return pow(num, .5)
```

使用管道操作符还可以使变量变得可选。
```py
optional: str | None

def root(num: int | float, exp: float | None) -> float:
    return pow(num, .5 if exp is None else exp)
```

可以在函数中为参数添加默认值。
```py
def root(num: int | float, exp: float | None = .5) -> float:
    return pow(num, exp)
```

定义更多类型声明：
```py
from typing import Any
digitis: list[int] = [1, 2, 3, 4, 5]

tuples: tuple[int, ...] = (5, 10, 15, 20, 25)

cities: tuple[str, float] = ("City", 20.5)

shipment: dict[str, Any] = {
    "id": 1234,
    "weight": 1.2,
    "content": "wooden table",
    "status": "in transit",
}

class City:
    def __init__(self, name, location):
        self.name = name
        self.location = location

hampshire = City("hamspshire", 2048593)
city: tuple[City, float] = (hampshire, 20.5)
```

### 009. 函数装饰器 (Function Decorator)

定义一个装饰器函数，需要接收一个函数参数并且返回一个闭包函数，当其他函数想要应用该装饰器函数时，需在函数上增加`@+函数名`来使用。

```py
def fence(func):

    def wrapper():
        print("+" * 10)
        func()
        print("+" * 10)
    
    return wrapper

@fence
def log():
    print("decorated?")

log()
```

可以在装饰器函数中接收其他参数。

```py
def custom_fence(fence: str = "+")

    def add_fence(func):

        def wrapper(text: str):
            print(fence * len(text))
            func(text)
            print(fence * len(text))

        return wrapper

    return add_fence

@custom_fence("-")
def log(text: str)
    print(text)
```

可以为装饰器函数增加类型提示。

```py
from typing import Callable, Any

def decorator( func: Callable[ [Any], Any ] ):
    pass
```

通过函数装饰器来模拟一个 `FastAPI` 的路由模式。

```py
from typing import Any, Callable

routes: dict[str, Callable[[Any], Any]] = {}

def route(path: str)
    def register_route(func):
        routes[path] = func
        return func
    return register_route

@route("/shipment")
def get_shipment():
    return "Shipment<1001, in transit>"

request: str = ""

while request != "quit":
    request = input(">    ")

    if request in routes:
        response = routes[request]()
        print(response, end="\n\n")
    else:
        print("Not found")
```

### 010. 路径参数 (Path Parameter)

```py
# /shipment/12345
@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, str | int | float]:
    return {
        "id": id,
        "weight": 1.2,
        "content": "wooden table",
        "status": "in transit"
    }
```

### 011. 路由顺序

当路由相同时，注册路由的顺序会对请求结果产生影响，如下定义中当请求路由 `/shipment/latest` 将会报错，因为它会先匹配 `/shipment/{id}` 路由并接收参数。如果将两个路由的顺序进行调换将不会报错。 

```py
@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:
    return {
        "id": id,
        "weight": 1.2,
        "content": "wooden table",
        "status": "in transit"
    }
    
@app.get("/shipment/latest")
def get_shipment_latest():
    return {
        "id": 1234,
        "weight": .6,
        "content": "wooden table",
        "status": "in transit"
    }
```

### 012. 简易数据库

```py
shipments = {
    1: {
        "weight": .6,
        "content": "wooden table",
        "status": "in transit"  
    },
    2: {
        "weight": .8,
        "content": "books",
        "status": "shipped"  
    },
}

@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]

@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:

    if id not in shipments:
        return {"default": "Given id doesn't exist!"}

    return shipments[id]
```

## 四、查询字符串参数

### 013. 查询字符串参数介绍

默认情况下，`GET` 请求中在函数中定义的参数会被映射为查询字符串，即 `/shipment?id=` 的形式。

```py
@app.get("/shipment")
def get_shipment(id: int) -> dict[str, Any]:

    if id not in shipments:
        return {"default": "Given id doesn't exist!"}

    return shipments[id]
```

当想要为接口设置可选参数时可通过将值设置为 `None` 的形式实现。

```py
@app.get("/shipment")
def get_shipment(id: int | None = None) -> dict[str, Any]:
    ...
```

### 014. HTTP 异常

每个路由的响应默认的状态码为 `200`。

```py
from typing improt Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    ...
}

@app.get("/shipment")
def get_shipment(id: int) -> dict[str, Any]:

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment[id]
```

### 015. POST 方法

```py
@app.post("/shipment")
def submit_shipment(content: str, weight: float) -> dict[str, Any]:
    
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

### 016. 请求体

```py
@app.post("/shipment")
def submit_shipment(data: dict:[str, Any]) -> dict[str, Any]:
    content = data["content"]
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