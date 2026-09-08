# 🌱 SeedForge - 完整开发指南

## 📋 项目概述

SeedForge 是一个专业的本地种子字典生成工具，面向授权安全测试、密码审计和实验室环境。

## 🚀 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- Git

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/A26-S/seedforge.git
cd seedforge
```

#### 2. 后端设置

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp .env.example .env

# 运行后端
python main.py
```

后端将运行在 http://localhost:8000

#### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在 http://localhost:5173

### 验证安装

- 访问 http://localhost:5173 查看前端
- 访问 http://localhost:8000/docs 查看 API 文档
- 访问 http://localhost:8000/health 检查后端状态

## 🏗️ 项目结构

### 后端结构

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   ├── seeds.py      # 种子管理
│   │   ├── rules.py      # 规则管理
│   │   ├── tasks.py      # 任务管理
│   │   ├── export.py     # 导出功能
│   │   └── analysis.py   # 分析功能
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   └── app.py        # FastAPI 应用
│   ├── services/         # 业务逻辑
│   │   ├── seed/         # 种子服务
│   │   ├── rules/        # 规则引擎
│   │   ├── transform/    # 变形处理
│   │   ├── tasks/        # 任务管理
│   │   └── export/       # 导出服务
│   └── models/           # 数据模型（后续添加）
├── main.py               # 应用入口
└── requirements.txt      # 依赖列表
```

### 前端结构

```
frontend/
├── src/
│   ├── components/       # 可复用组件
│   ├── pages/            # 页面组件
│   ├── stores/           # Zustand 状态
│   ├── services/         # API 服务
│   ├── hooks/            # 自定义 hooks
│   ├── types/            # TypeScript 类型
│   ├── styles/           # 全局样式
│   ├── App.tsx           # 主应用
│   └── main.tsx          # 入口文件
├── index.html            # HTML 模板
├── vite.config.ts        # Vite 配置
├── tsconfig.json         # TypeScript 配置
└── package.json          # 依赖管理
```

## 📚 核心模块说明

### 1. Seed 库管理

**文件**: `backend/app/services/seed/manager.py`

- 管理种子数据
- 支持多个种子类别
- 导入/导出功能
- 搜索和过滤

**使用示例**:
```python
from app.services.seed.manager import seed_manager, SeedCategory, SeedSource

# 添加种子
seed = seed_manager.add_seed(
    value="张三",
    category=SeedCategory.NAME,
    source=SeedSource.IMPORTED,
    tags=["common", "2char"]
)

# 列出种子
seeds = seed_manager.list_seeds(SeedCategory.NAME)

# 搜索种子
results = seed_manager.search_seeds("张")
```

### 2. 规则引擎

**文件**: `backend/app/services/rules/engine.py`

- 规则解析和执行
- 模板系统支持
- 预设模式库

**使用示例**:
```python
from app.services.rules.engine import rule_engine, PresetLibrary

# 获取预设
presets = PresetLibrary.list_presets()
company_preset = PresetLibrary.get_preset("company")

# 注册变量
rule_engine.parser.register_variable("name", ["zhang", "li"])
rule_engine.parser.register_variable("year", ["2024", "2025"])

# 解析模板
results = rule_engine.parser.parse_template("{name}{year}")
# 结果: ["zhang2024", "zhang2025", "li2024", "li2025"]
```

### 3. 变形处理

**文件**: `backend/app/services/transform/processor.py`

- 大小写变形
- 数字替换
- 符号处理
- 过滤和去重

**使用示例**:
```python
from app.services.transform.processor import (
    CaseTransform, NumberTransform, FilterProcessor, DeduplicateProcessor
)

# 大小写变形
case_transform = CaseTransform()
variants = case_transform.apply("password")
# 结果: ["password", "PASSWORD", "Password", ...]

# 过滤
filter_proc = FilterProcessor(min_length=6, max_length=32)
filtered = filter_proc.filter_by_length(["pwd", "password", "p@ssw0rd"])
# 结果: ["password", "p@ssw0rd"]

# 去重
dedup = DeduplicateProcessor()
dedup.add("password1")
has_duplicate = dedup.contains("password1")  # True
```

### 4. 任务管理

**文件**: `backend/app/services/tasks/manager.py`

- 创建和管理任务
- 进度跟踪
- 任务历史
- 任务对比

**使用示例**:
```python
from app.services.tasks.manager import task_manager, ResultInfo
from uuid import UUID

# 创建任务
task = task_manager.create_task(
    name="Company Audit",
    seed_ids=[UUID("..."), UUID("...")],
    rule_ids=[UUID("...")],
    config={"filter": {"min_length": 8}}
)

# 启动任务
task_manager.start_task(task.id)

# 更新进度
task_manager.update_progress(
    task.id,
    current=50000,
    total=100000,
    speed=10000,
    eta=5
)

# 完成任务
results = ResultInfo(
    generated=100000,
    deduplicated=95000,
    filtered=85000,
    file_path="/output/dictionary.txt"
)
task_manager.complete_task(task.id, results)
```

## 🔌 API 端点

### Seed 管理

- `GET /api/seeds/categories` - 获取所有种子类别
- `GET /api/seeds/list/{category}` - 列出指定类别的种子
- `GET /api/seeds/search?q=...` - 搜索种子
- `POST /api/seeds/add` - 添加种子
- `POST /api/seeds/import` - 导入种子文件
- `GET /api/seeds/statistics` - 获取统计信息

### 规则管理

- `GET /api/rules/presets` - 列出预设模式
- `GET /api/rules/presets/{name}` - 获取预设详情
- `POST /api/rules/preview` - 预览规则结果
- `POST /api/rules/validate` - 验证规则

### 任务管理

- `POST /api/tasks/create` - 创建任务
- `GET /api/tasks/{task_id}` - 获取任务详情
- `POST /api/tasks/{task_id}/start` - 启动任务
- `POST /api/tasks/{task_id}/pause` - 暂停任务
- `POST /api/tasks/{task_id}/resume` - 继续任务
- `POST /api/tasks/{task_id}/cancel` - 取消任务
- `GET /api/tasks/history` - 获取任务历史
- `POST /api/tasks/compare` - 对比任务

### 导出功能

- `POST /api/export/txt` - 导出为 TXT
- `POST /api/export/csv` - 导出为 CSV
- `POST /api/export/json` - 导出为 JSON

### 分析功能

- `POST /api/analysis/entropy` - 分析熵值
- `POST /api/analysis/distribution` - 分析字符分布

## 🛠️ 开发工作流

### 后端开发

1. **修改 services 中的业务逻辑**
2. **在 api 路由中暴露接口**
3. **测试 API**：使用 http://localhost:8000/docs
4. **推送更改**

### 前端开发

1. **创建新的页面组件** (在 `src/pages/`)
2. **创建对应的 hooks** (在 `src/hooks/`)
3. **调用 API 服务** (在 `src/services/`)
4. **管理状态** (在 `src/stores/`)
5. **热更新测试**：修改文件后自动刷新

### 添加新功能的步骤

1. **后端**:
   - 在 `backend/app/services/` 创建新模块
   - 在 `backend/app/api/` 创建新路由
   - 在 `backend/app/core/config.py` 添加配置

2. **前端**:
   - 在 `frontend/src/services/api.ts` 添加 API 调用
   - 在 `frontend/src/hooks/` 创建 React Query hooks
   - 在 `frontend/src/pages/` 创建页面组件
   - 在 `frontend/src/stores/` 管理全局状态

## 📝 编码规范

### Python (后端)

- 遵循 PEP 8
- 使用类型注解
- 添加文档字符串
- 使用 black 格式化

```bash
# 格式化代码
black backend/app

# 检查类型
mypy backend/app
```

### TypeScript (前端)

- 严格的类型检查
- 遵循 ESLint 规则
- 组件使用 FC 类型
- 使用自定义 hooks

```bash
# 检查类型
npm run type-check

# 检查代码
npm run lint
```

## 🧪 测试

### 后端测试

```bash
cd backend
pytest tests/
pytest --cov=app tests/  # 覆盖率报告
```

### 前端测试

```bash
cd frontend
npm run test
```

## 📦 部署

### 生产构建

**后端**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.core.app:create_app --host 0.0.0.0 --port 8000
```

**前端**:
```bash
cd frontend
npm run build
# 部署 dist 文件夹内容到 Web 服务器
```

### Docker 部署

```bash
# 使用 docker-compose (需要 Docker 配置)
docker-compose up -d
```

## 🐛 常见问题

### 后端无法启动

```bash
# 检查 Python 版本
python --version  # 需要 3.11+

# 重新安装依赖
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 前端无法连接到后端

- 检查 `vite.config.ts` 中的 proxy 配置
- 确保后端运行在 http://localhost:8000
- 检查浏览器控制台的网络错误

### CORS 错误

- 检查 `backend/app/core/config.py` 中的 CORS_ORIGINS
- 添加前端地址到允许列表

## 📚 进一步阅读

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [React 文档](https://react.dev/)
- [Zustand 文档](https://github.com/pmndrs/zustand)
- [Tailwind CSS 文档](https://tailwindcss.com/)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📞 支持

- 📧 Email: support@seedforge.dev
- 🐛 [Issue Tracker](https://github.com/A26-S/seedforge/issues)
- 💬 [Discussions](https://github.com/A26-S/seedforge/discussions)
