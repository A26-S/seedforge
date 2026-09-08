# SeedForge 项目架构

## 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    前端 (React + TypeScript)                      │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Dashboard   │  │  种子库      │  │  规则编辑    │  ┌──────┐ │
│  │              │  │              │  │              │  │ 分析 │ │
│  │ • 当前任务   │  │ • 导入       │  │ • 规则链     │  │ 统计 │ │
│  │ • 预计数量   │  │ • 分类       │  │ • 预览       │  │      │ │
│  │ • 最近任务   │  │ • 编辑       │  │ • 预设库     │  └──────┘ │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                        HTTP/WebSocket
                           │
┌──────────────────────────┴───────────────────────────────────────┐
│                    后端 (FastAPI + Python)                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                      API 层                                 │ │
│  │  /seeds  /rules  /tasks  /export  /analysis                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                           │                                       │
│  ┌────────────┬───────────┼───────────┬──────────────┐           │
│  ▼            ▼           ▼           ▼              ▼           │
│┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────────┐ ┌────────┐ │
││ Seed库   │ │规则引擎  │ │ 变形   │ │ 任务系统  │ │ 导出   │ │
││          │ │          │ │处理    │ │           │ │        │ │
││ Manager  │ │ Parser   │ │├─ 字符 │ │├─ 队列    │ │├─格式  │ │
││ Loader   │ │ Engine   │ │├─拼音 │ │├─ 执行    │ │├─排序  │ │
││ Generator│ │ Executor │ │├─数字 │ │├─ 进度    │ │├─分割  │ │
││          │ │          │ │├─符号 │ │└─ 历史    │ │└─压缩  │ │
││          │ │          │ │└─组合 │ │           │ │        │ │
│└──────────┘ └──────────┘ └────────┘ └────────────┘ └────────┘ │
│                           │                                       │
│  ┌────────────────────────┴────────────────────────┐            │
│  ▼                                                 ▼            │
│┌──────────────────────────┐  ┌──────────────────────────────┐  │
││    本地存储                │  │    缓存 & 队列               │  │
││  ├─ SQLite DB             │  │  ├─ Redis (缓存)           │  │
││  ├─ 种子文件              │  │  ├─ RabbitMQ (任务队列)    │  │
││  └─ 生成缓存              │  │  └─ 进度通道               │  │
│└──────────────────────────┘  └──────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## 核心模块设计

### 1. Seed 库管理

```python
Seed
├── id: UUID
├── value: str           # "张三"
├── category: str        # "姓名"
├── source: str          # "builtin" | "imported"
├── tags: List[str]      # ["常见", "2字"]
├── enabled: bool
└── metadata: dict       # 额外信息

SeedLibrary
├── list_categories()    # 获取所有分类
├── add_seed()          # 添加种子
├── import_from_file()  # 从文件导入
├── auto_classify()     # 自动分类
└── search()            # 搜索
```

### 2. 规则引擎

```python
RuleTemplate
├── {name}{year}             # 基础组合
├── {name}@{year}{symbol}    # 复杂组合
├── IF year > 2015:          # 条件规则
│   {name}{year}{symbol}
├── FOR digit in [6,8,88]:   # 循环规则
│   {name}{digit}
└── {name}[0-9]{2,4}         # 正则规则

RuleEngine
├── parse()              # 解析模板
├── validate()           # 验证规则
├── execute()            # 执行生成
├── get_presets()        # 获取预设
└── preview()            # 实时预览
```

### 3. 变形处理

```python
TransformPipeline
├── Case Transform
│   ├── lowercase
│   ├── UPPERCASE
│   ├── Capitalize
│   └── MixedCase
├── Pinyin Transform
│   ├── full_pinyin
│   ├── first_letter
│   └── tone_marks
├── Number Transform
│   ├── digit_replace
│   ├── homophone
│   └── lucky_numbers
├── Symbol Processing
│   ├── prefix_add
│   ├── suffix_add
│   └── middle_insert
├── Combine Rules
│   ├── cartesian_product
│   ├── permutation
│   └── custom_template
└── Filter
    ├── length_range
    ├── char_type
    ├── entropy
    ├── dedup
    └── pattern_match
```

### 4. 任务系统

```python
Task
├── id: UUID
├── name: str
├── seed_ids: List[UUID]     # 选中的种子
├── rule_ids: List[UUID]     # 应用的规则
├── config: TaskConfig
├── status: TaskStatus       # pending/running/completed/failed
├── progress: ProgressInfo
│   ├── current: int
│   ├── total: int
│   ├── speed: int           # items/sec
│   └── eta: int             # 秒
├── results: ResultInfo
│   ├── generated: int       # 生成数
│   ├── deduplicated: int    # 去重后
│   ├── filtered: int        # 过滤后
│   └── file_path: str
├── created_at: datetime
├── completed_at: datetime
└── metadata: dict

TaskManager
├── create_task()
├── start_task()
├── pause_task()
├── resume_task()
├── cancel_task()
├── get_progress()
├── list_history()
└── compare_tasks()
```

### 5. 预设模式库

```python
PasswordPattern
├── 公司型
│   ├── {company}{year}
│   ├── {company_abbr}{number}
│   └── {department}{emp_id}
├── 个人型
│   ├── {name}{birthday}
│   ├── {nickname}{year}
│   └── {hobby}{number}
├── 混合型
│   ├── {name}{place}{date}
│   ├── {brand}{number}{symbol}
│   └── {keyword}{year}{emoji}
└── 键盘型
    ├── qwerty_trace
    ├── number_row_trace
    └── numpad_trace

PatternLibrary
├── get_patterns()
├── get_pattern_by_category()
├── get_recommended_rules()
└── apply_pattern()
```

## 数据流

```
用户输入
    ↓
[前端] 构建请求
    ↓
[API] 验证请求
    ↓
[种子库] 获取种子
    ↓
[规则引擎] 解析规则
    ↓
[变形处理] 应用变形
    ├─ Case Transform
    ├─ Pinyin Transform
    ├─ Number Transform
    ├─ Symbol Processing
    └─ Combine Rules
    ↓
[过滤] 长度/字符/强度
    ↓
[去重] 布隆过滤器
    ↓
[排序] 字典序/熵值/长度
    ↓
[导出] TXT/CSV/JSON
    ↓
结果文件
```

## 任务处理流程

```
UI 发起生成请求
    ↓
[TaskManager] 创建Task
    ↓
[Redis] 存储任务配置
    ↓
[Celery] 加入队列
    ↓
[Worker] 提取任务
    ├─ 加载种子
    ├─ 解析规则
    ├─ 流式生成 (分批)
    ├─ 实时更新进度 (WebSocket)
    └─ 结果写入文件
    ↓
[Redis] 缓存结果统计
    ↓
[UI] 实时反馈 (WebSocket)
    ├─ 进度条更新
    ├─ 速度显示
    ├─ ETA计算
    └─ 完成通知
```

## 扩展点

### 添加新的变形规则
```python
# 在 transform/ 下新建模块
class CustomTransform(BaseTransform):
    def transform(self, seed: str) -> List[str]:
        # 实现变形逻辑
        pass
```

### 添加新的预设模式
```python
# 在 patterns/ 下定义
NEW_PATTERN = {
    "name": "自定义模式",
    "template": "{seed1}_{seed2}",
    "rules": [...]
}
```

### 集成新的种子源
```python
# 在 seed/loader.py 中注册
LOADERS = {
    "api": APILoader,
    "database": DatabaseLoader,
    "new_source": NewSourceLoader
}
```

## 性能优化

1. **流式处理** - 不加载全部到内存
2. **多核并行** - Celery分布式任务
3. **缓存策略** - Redis缓存热数据
4. **批量操作** - 数据库批量插入
5. **布隆过滤** - O(1)去重
6. **增量计算** - 支持断点续传

## 安全设计

1. **本地优先** - 数据不上网
2. **加密存储** - 敏感数据加密
3. **审计日志** - 完整操作记录
4. **权限控制** - 多用户隔离
5. **输出混淆** - 导出时可混淆
