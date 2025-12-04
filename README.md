# GovinfoCheckSystem（舆情分析系统）

一个基于 B/S 架构的政企智能舆情分析报告生成智能体应用系统，前端采用 `Layui v2.13.2`，后端采用 `Python3 + Flask + SQLite`，支持用户登录、权限管理、系统设置以及新闻数据采集预览。

## 技术栈

- 前端：`Layui v2.13.2`（已拷贝到 `static/layui`）
- 后端：`Flask 3`、`Flask-Login`、`Flask-SQLAlchemy`
- 数据库：`SQLite`
- 采集：`requests` + `beautifulsoup4`

## 目录结构

- `app/` 应用核心
  - `__init__.py` 应用工厂、初始化数据库与默认数据
  - `config.py` 配置（数据库、密钥）
  - `models.py` 模型（用户、角色、系统设置）
  - `routes.py` 路由（登录/退出、首页、后台管理、采集API）
  - `services/` 业务模块
    - `crawler.py` 采集模块，按关键字抓取百度新闻
- `templates/` 页面模板
  - `base.html` 基础布局（响应式、权限菜单）
  - `login.html` 登录页（暗色风格）
  - `index.html` 首页示例
  - `admin/` 后台页面（用户管理、角色管理、系统设置、数据采集预览）
- `static/` 静态资源（含 `layui`）
- `requirements/` 依赖文件（`base.txt`）
- `run.py` 启动入口

## 环境准备

```bash
python -m venv venv
./venv/Scripts/activate  # Windows
pip install -r requirements/base.txt
```

## 快速启动

```bash
# Windows PowerShell
python -m venv venv
./venv/Scripts/Activate.ps1
python -m pip install -r requirements/base.txt

# 使用 Flask CLI（与参考项目一致）
python -m flask --app app:create_app run --port 5000 --debug
# 访问：http://127.0.0.1:5000/
```

首次启动会自动创建默认数据：
- 角色：`Administrator`、`User`
- 管理员账号：用户名 `admin`，密码 `admin123`
- 系统设置：应用名称为“舆情分析系统”

## 功能模块

- 登录/退出（`Flask-Login`）
- 权限菜单（管理员可见：后台管理、系统设置、数据采集预览）
- 数据采集预览（后台页面 `admin/crawl.html`）
- 采集接口：
  - `GET /api/collect?q=关键词&limit=20&pn=0`
    - 返回字段：`title`, `cover`, `url`, `source`
  - `GET /api/collect/xinhua?limit=20`（示例实现，返回同结构）

## 采集说明

- 数据来源：按关键字访问百度新闻页并解析结构化字段
- 兼容多种页面结构选择器，提升解析鲁棒性
- 可扩展：入库、去重、定时任务、多来源聚合

## 开发说明

- 使用虚拟环境 `venv` 进行开发，避免影响系统环境
- 可在 `templates/admin/settings.html` 修改应用名称（动态展示）
- 静态框架资源位于 `static/layui`，可根据官网文档进行组件扩展

## 部署建议

- 生产环境请使用 WSGI（如 `gunicorn` 或 `waitress`）部署，并配置反向代理（Nginx/IIS）
- 配置环境变量 `SECRET_KEY` 与数据库路径，避免硬编码

## 许可证

此项目用于内部演示与原型开发，实际使用请根据组织规范设置许可证与版权信息。
