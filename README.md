# learn-python-fastapi

## 一、介绍 (Introduction)

### 课程概览

01. 介绍
02. 开始
03. 路径参数
04. 查询字符串参数
05. 增删改查操作
06. Pydantic模型验证
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

### 什么是 REST APIs？

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

### 什么是 FastAPI？

FastAPI 是一个用于构建API和Python的极速Web框架，由 `Sebastian Remirez` 开发，并迅速变得流行。

FastAPI 还可以使用数据验证、自动生成API文档、使用OpenAPI标准、依赖注入和异步代码来构建稳健且可扩展的API。

FastAPI 依赖以下关键库：
- Starlette - 作为底层Web服务器。
- Pydantic - 用于处理数据验证。

### 为什么选择 FastAPI？

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