# SeedForge API 文档

## 基础信息

- **基础 URL**: `http://localhost:8000/api`
- **内容类型**: `application/json`
- **认证**: 暂无（可选添加）

## 状态码

- `200` - 成功
- `201` - 创建成功
- `400` - 请求错误
- `404` - 资源不存在
- `500` - 服务器错误

---

## Seed 管理 API

### 1. 获取所有种子类别

**请求**
```
GET /seeds/categories
```

**响应**
```json
{
  "categories": ["name", "date", "place", "animal", "website", "slang", "meme", "keyboard", "lucky_number", "homophone", "hobby", "brand", "custom"]
}
```

### 2. 列出种子

**请求**
```
GET /seeds/list/{category}
```

**参数**
- `category`: 种子类别 (path)

**响应**
```json
{
  "category": "name",
  "count": 150,
  "seeds": [
    {
      "id": "uuid",
      "value": "张三",
      "category": "name",
      "source": "builtin",
      "tags": ["common"],
      "enabled": true
    }
  ]
}
```

### 3. 搜索种子

**请求**
```
GET /seeds/search?q=query&category=name
```

**参数**
- `q`: 搜索词 (query)
- `category`: 种子类别 (query, optional)

**响应**
```json
{
  "query": "张",
  "count": 5,
  "seeds": [...]
}
```

### 4. 添加种子

**请求**
```
POST /seeds/add
Content-Type: application/json

{
  "value": "新种子",
  "category": "name",
  "tags": ["custom"]
}
```

**响应**
```json
{
  "success": true,
  "seed": {
    "id": "uuid",
    "value": "新种子",
    "category": "name",
    "source": "imported",
    "tags": ["custom"],
    "enabled": true
  }
}
```

### 5. 导入种子文件

**请求**
```
POST /seeds/import?category=name
Content-Type: multipart/form-data

file: <file>
```

**参数**
- `category`: 种子类别 (query)
- `file`: 上传的文件 (form)

**响应**
```json
{
  "success": true,
  "imported": 100
}
```

### 6. 获取统计信息

**请求**
```
GET /seeds/statistics
```

**响应**
```json
{
  "total": 500,
  "name": 100,
  "date": 50,
  "place": 75,
  "animal": 30,
  "website": 40,
  "slang": 60,
  "meme": 45,
  "keyboard": 25,
  "lucky_number": 20,
  "homophone": 15,
  "hobby": 35,
  "brand": 40,
  "custom": 20
}
```

---

## 规则管理 API

### 1. 获取预设列表

**请求**
```
GET /rules/presets
```

**响应**
```json
{
  "presets": [
    {
      "name": "company",
      "title": "Company Pattern",
      "description": "Company-style passwords"
    },
    {
      "name": "personal",
      "title": "Personal Pattern",
      "description": "Personal-style passwords"
    }
  ]
}
```

### 2. 获取预设详情

**请求**
```
GET /rules/presets/{preset_name}
```

**响应**
```json
{
  "name": "Company Pattern",
  "description": "Company-style passwords",
  "templates": [
    "{company}{year}",
    "{company_abbr}{number}",
    "{department}{emp_id}"
  ]
}
```

### 3. 预览规则结果

**请求**
```
POST /rules/preview
Content-Type: application/json

{
  "seeds": ["zhang", "li", "wang"],
  "rules": {
    "case": "capitalize",
    "number": "year",
    "symbol": "@"
  }
}
```

**响应**
```json
{
  "preview": ["Zhang2024@", "Zhang2025@", "Li2024@"],
  "estimated_total": 12000
}
```

### 4. 验证规则

**请求**
```
POST /rules/validate
Content-Type: application/json

{
  "type": "case",
  "config": {"format": "capitalize"}
}
```

**响应**
```json
{
  "valid": true,
  "errors": []
}
```

---

## 任务管理 API

### 1. 创建任务

**请求**
```
POST /tasks/create
Content-Type: application/json

{
  "name": "公司审计",
  "seed_ids": ["uuid1", "uuid2"],
  "rule_ids": ["uuid3", "uuid4"],
  "config": {
    "min_length": 8,
    "max_length": 16
  }
}
```

**响应**
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "name": "公司审计",
    "status": "pending",
    "progress": {"current": 0, "total": 0, "speed": 0, "eta": 0},
    "results": {"generated": 0, "deduplicated": 0, "filtered": 0}
  }
}
```

### 2. 获取任务详情

**请求**
```
GET /tasks/{task_id}
```

**响应**
```json
{
  "id": "uuid",
  "name": "公司审计",
  "status": "running",
  "progress": {
    "current": 50000,
    "total": 100000,
    "speed": 10000,
    "eta": 5
  },
  "results": {
    "generated": 50000,
    "deduplicated": 48000,
    "filtered": 45000
  },
  "created_at": "2024-09-08T10:00:00"
}
```

### 3. 启动任务

**请求**
```
POST /tasks/{task_id}/start
```

**响应**
```json
{
  "success": true,
  "status": "running"
}
```

### 4. 暂停任务

**请求**
```
POST /tasks/{task_id}/pause
```

### 5. 继续任务

**请求**
```
POST /tasks/{task_id}/resume
```

### 6. 取消任务

**请求**
```
POST /tasks/{task_id}/cancel
```

### 7. 获取任务历史

**请求**
```
GET /tasks/history
```

**响应**
```json
{
  "count": 5,
  "tasks": [...]
}
```

### 8. 对比任务

**请求**
```
POST /tasks/compare
Content-Type: application/json

{
  "task_id1": "uuid1",
  "task_id2": "uuid2"
}
```

**响应**
```json
{
  "task1": {...},
  "task2": {...},
  "comparison": {
    "seed_diff": 5,
    "rule_diff": 2,
    "result_diff": 15000
  }
}
```

---

## 导出 API

### 1. 导出为 TXT

**请求**
```
POST /export/txt
Content-Type: application/json

{
  "passwords": ["pass1", "pass2"],
  "filename": "dictionary.txt"
}
```

### 2. 导出为 CSV

**请求**
```
POST /export/csv
Content-Type: application/json

{
  "passwords": ["pass1", "pass2"],
  "filename": "dictionary.csv"
}
```

### 3. 导出为 JSON

**请求**
```
POST /export/json
Content-Type: application/json

{
  "passwords": ["pass1", "pass2"],
  "filename": "dictionary.json"
}
```

---

## 分析 API

### 1. 分析熵值

**请求**
```
POST /analysis/entropy
Content-Type: application/json

{
  "passwords": ["password123", "P@ssw0rd"]
}
```

**响应**
```json
{
  "count": 2,
  "analysis": [
    {
      "password": "password123",
      "entropy": 42.5,
      "strength": "medium"
    },
    {
      "password": "P@ssw0rd",
      "entropy": 58.3,
      "strength": "strong"
    }
  ]
}
```

### 2. 分析字符分布

**请求**
```
POST /analysis/distribution
Content-Type: application/json

{
  "passwords": ["password123", "P@ssw0rd"]
}
```

**响应**
```json
{
  "count": 2,
  "distribution": {
    "lowercase": 26,
    "uppercase": 26,
    "digits": 10,
    "symbols": 32
  }
}
```

---

## 错误处理

所有错误响应格式为：

```json
{
  "detail": "错误描述信息"
}
```

**常见错误**:

- `400 Bad Request` - 请求参数无效
- `404 Not Found` - 资源不存在
- `500 Internal Server Error` - 服务器错误

---

## WebSocket 事件 (即将推出)

用于实时进度更新：

```
WS ws://localhost:8000/ws/tasks/{task_id}
```

**事件类型**:
- `progress` - 进度更新
- `sample` - 样本数据
- `complete` - 任务完成
- `error` - 错误信息
