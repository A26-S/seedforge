# SeedForge - 快速开始指南

## ⚡ 30 秒快速启动

### 前置要求
- Python 3.11+
- Node.js 18+

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/A26-S/seedforge.git
cd seedforge

# 2. 后端 (新终端)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
# 后端运行在 http://localhost:8000

# 3. 前端 (新终端)
cd frontend
npm install
npm run dev
# 前端运行在 http://localhost:5173
```

✅ 完成！访问 http://localhost:5173

---

## 🎯 项目状态

### ✅ 已完成 (V0.1)
- 📁 完整的项目结构
- 🔧 后端框架 (FastAPI)
- ⚛️ 前端框架 (React + TypeScript)
- 🌱 种子库管理系统
- ⚙️ 规则引擎
- 🔄 变形处理模块
- 📋 任务管理系统
- 📚 完整文档
- 🐳 Docker 配置

### 🚀 进行中 (V0.2)
- 🖥️ UI 组件开发
- 📡 WebSocket 实时通讯
- 🎨 样式优化
- 🧪 单元测试

### 📋 计划中 (V0.3)
- 📊 数据可视化
- 🔐 用户认证
- ⚡ 性能优化
- 🌐 多语言支持

---

## 📖 主要文档

- [架构设计](docs/architecture.md) - 系统整体架构
- [API 文档](docs/api.md) - 所有 API 端点说明
- [开发指南](docs/development.md) - 详细开发教程
- [用户指南](docs/user-guide.md) - 如何使用

---

## 🏗️ 项目结构

```
seedforge/
├── backend/              # FastAPI 后端
├── frontend/             # React 前端
├── docs/                 # 文档
├── data/                 # 数据文件
├── output/               # 输出目录
├── docker-compose.yml    # Docker 配置
└── README.md
```

---

## 🔗 快速链接

- 🌐 前端: http://localhost:5173
- 📚 API: http://localhost:8000/docs
- 🏥 健康检查: http://localhost:8000/health

---

## 🤔 常见问题

### Q: 后端无法启动？
A: 检查 Python 版本 (需要 3.11+)
```bash
python --version
```

### Q: 前端显示 CORS 错误？
A: 确保后端正在运行且在 http://localhost:8000

### Q: 如何开发新功能？
A: 查看 [开发指南](docs/development.md)

---

## 📝 许可证

MIT License

---

## 🎉 开始使用

1. 📖 阅读 [开发指南](docs/development.md)
2. 🔍 浏览 [API 文档](docs/api.md)
3. 💻 修改代码并测试
4. 🚀 提交 PR

祝你开发愉快！🚀
