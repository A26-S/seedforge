# 🌱 SeedForge

**专业的本地种子字典生成工具** | Professional seed-based dictionary generator for security auditing

一个面向授权安全测试、密码审计和实验室环境的高效能种子字典生成平台。

## ✨ 核心特性

### 🎯 产品定位
- ✅ 授权安全测试专用
- ✅ 本地运行，零网络依赖
- ✅ 高性能多核并行处理
- ✅ 专业级密码生成质量
- ✅ 完整的任务管理系统

### 🌱 种子库管理
- **10+内置种子类型** - 姓名、日期、地理、网站等
- **智能日期生成器** - 自动推导相对日期、纪念日、时令节日
- **灵活导入系统** - TXT/CSV/JSON/Excel/剪贴板支持
- **自动分类识别** - AI智能识别种子类型
- **数据清洗** - 自动去重、去空、编码转换

### ⚙️ 规则引擎
- **规则链系统** - 可视化规则组合与排序
- **高级模板语法** - 支持条件、循环、正则表达式
- **预设模式库** - 内置密码模式（公司型、个人型、混合型等）
- **实时预览** - 修改规则即时反馈效果
- **规则快照** - 保存和复用规则配置

### 🔄 变形处理
- **字符变形** - 大小写、首字母、混合等
- **拼音变形** - 全拼、首字母、音调等
- **数字变形** - 数字替换、编码、谐音等
- **符号处理** - 前缀、后缀、中间插入
- **组合规则** - 复杂的种子组合与排列

### 📊 生成与输出
- **实时进度显示** - 速度、ETA、进度百分比
- **任务管理** - 暂停/继续/取消/历史记录
- **多格式导出** - TXT/CSV/JSON/MD5/压缩包
- **智能排序** - 字典序、熵值、强度、长度等
- **高级过滤** - 长度、字符类型、强度等级

### 📈 分析对比
- **熵值评分** - 密码复杂度实时计算
- **强度分布** - 弱/中/强比例分析
- **A/B对比** - 不同任务的结果对比分析
- **质量分析** - 重叠率、独有率、相似度等

## 🛠️ 技术栈

### 前端
- **React 18** - UI框架
- **TypeScript** - 类型安全
- **Vite** - 现代构建工具
- **TailwindCSS** - 样式系统
- **Zustand** - 状态管理
- **TanStack Query** - 数据获取
- **Recharts** - 数据可视化

### 后端
- **FastAPI** - 高性能Web框架
- **Python 3.11+** - 开发语言
- **SQLAlchemy** - ORM
- **Pydantic** - 数据验证
- **Redis** - 缓存/消息队列
- **Celery** - 异步任务处理

### 基础设施
- **SQLite** - 本地数据库（开发）
- **PostgreSQL** - 数据库（可选）
- **Docker** - 容器化
- **Nginx** - 反向代理

## 📦 项目结构

```
seedforge/
├── frontend/                      # React 前端应用
│   ├── src/
│   │   ├── components/           # UI组件
│   │   ├── pages/                # 页面
│   │   ├── layouts/              # 布局
│   │   ├── stores/               # Zustand状态
│   │   ├── hooks/                # 自定义hooks
│   │   ├── services/             # API服务
│   │   ├── types/                # TypeScript类型
│   │   ├── utils/                # 工具函数
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                       # FastAPI 后端
│   ├── app/
│   │   ├── api/                  # API路由
│   │   ├── core/                 # 核心配置
│   │   ├── models/               # 数据模型
│   │   ├── schemas/              # Pydantic模式
│   │   ├── services/             # 业务逻辑
│   │   │
│   │   ├── seed/                 # 种子管理
│   │   │   ├── loader.py         # 加载器
│   │   │   ├── manager.py        # 管理器
│   │   │   └── generator.py      # 生成器
│   │   │
│   │   ├── rules/                # 规则引擎
│   │   │   ├── engine.py         # 规则引擎
│   │   │   ├── parser.py         # 模板解析
│   │   │   ├── preset.py         # 预设库
│   │   │   └── executor.py       # 规则执行
│   │   │
│   │   ├── transform/            # 变形处理
│   │   │   ├── case.py           # 大小写变形
│   │   │   ├── pinyin.py         # 拼音变形
│   │   │   ├── number.py         # 数字变形
│   │   │   ├── symbol.py         # 符号处理
│   │   │   ├── combine.py        # 组合规则
│   │   │   └── filter.py         # 过滤处理
│   │   │
│   │   ├── tasks/                # 任务系统
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   └── worker.py
│   │   │
│   │   ├── export/               # 导出功能
│   │   │   ├── formatter.py
│   │   │   ├── sorter.py
│   │   │   └── compressor.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── data/                         # 数据文件
│   ├── seeds/                    # 种子库
│   │   ├── builtin/              # 内置种子
│   │   └── imported/             # 导入种子
│   └── patterns/                 # 密码模式库
│
├── docs/                         # 文档
│   ├── architecture.md
│   ├── api.md
│   ├── user-guide.md
│   └── development.md
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🚀 快速开始

### 前置要求
- Python 3.11+
- Node.js 18+
- Docker (可选)

### 安装

```bash
# 克隆项目
git clone https://github.com/A26-S/seedforge.git
cd seedforge

# 后端
cd backend
pip install -r requirements.txt
python main.py

# 前端 (新终端)
cd frontend
npm install
npm run dev
```

### 访问
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📖 使用示例

### 完整流程

```
STEP 01: 选择种子
├─ 姓名 (12,382条)
├─ 年份 (自动生成)
├─ 宠物 (891条)
└─ 吉祥数 (自动生成)

STEP 02: 配置规则
├─ 大小写变形
├─ 年份前缀
├─ 符号后缀
├─ 长度过滤 (6-16)
└─ 去重

STEP 03: 预览效果
└─ 预计生成: 1,823,921条

STEP 04: 启动生成
└─ 进度: ████████████████ 85% (1.2M/s)

STEP 05: 导出结果
└─ dictionary.txt (45.2 MB)
```

## 🎯 开发路线

### V0.1 (MVP - 2周)
- [x] 基础种子库
- [x] 核心变形规则
- [x] TXT导出
- [x] 基础任务系统

### V0.2 (增强 - 2周)
- [ ] 规则链系统
- [ ] 实时预览
- [ ] 高级模板语法
- [ ] 密码模式库
- [ ] 日期生成器

### V0.3 (完善 - 2周)
- [ ] A/B对比
- [ ] 熵值分析
- [ ] 高级导入
- [ ] 规则快照
- [ ] 性能优化

## 📊 性能指标

- ⚡ 生成速度: 100万条/分钟 (单核)
- 💾 内存占用: <500MB (处理1000万条)
- 🔍 去重性能: 毫秒级 (布隆过滤)
- 📈 最大规模: 1GB+ 种子库支持

## 🔐 安全性

- ✅ 本地运行，零网络上传
- ✅ 敏感数据加密存储
- ✅ 完整的审计日志
- ✅ 访问权限控制
- ✅ 支持导出时混淆

## 📝 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

- 📖 [文档](docs/)
- 🐛 [Issue Tracker](https://github.com/A26-S/seedforge/issues)
- 💬 [讨论](https://github.com/A26-S/seedforge/discussions)

---

**开发中 🚧** | 所有核心模块正在构建中
