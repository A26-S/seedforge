"""Task management service"""

from typing import List, Dict, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict
import json

class TaskStatus(str, Enum):
    """Task status"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ProgressInfo:
    """Progress information"""
    current: int = 0
    total: int = 0
    speed: int = 0  # items/sec
    eta: int = 0    # seconds
    
    def to_dict(self):
        return asdict(self)

@dataclass
class ResultInfo:
    """Result information"""
    generated: int = 0
    deduplicated: int = 0
    filtered: int = 0
    file_path: Optional[str] = None
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Task:
    """Task definition"""
    id: UUID
    name: str
    seed_ids: List[UUID] = field(default_factory=list)
    rule_ids: List[UUID] = field(default_factory=list)
    config: Dict = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    progress: ProgressInfo = field(default_factory=ProgressInfo)
    results: ResultInfo = field(default_factory=ResultInfo)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self):
        data = asdict(self)
        data['id'] = str(self.id)
        data['seed_ids'] = [str(sid) for sid in self.seed_ids]
        data['rule_ids'] = [str(rid) for rid in self.rule_ids]
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['started_at'] = self.started_at.isoformat() if self.started_at else None
        data['completed_at'] = self.completed_at.isoformat() if self.completed_at else None
        data['progress'] = self.progress.to_dict()
        data['results'] = self.results.to_dict()
        return data

class TaskManager:
    """Task management"""
    
    def __init__(self):
        self.tasks: Dict[UUID, Task] = {}
        self.history: List[UUID] = []  # Task ID history
    
    def create_task(self, name: str, seed_ids: List[UUID], 
                   rule_ids: List[UUID], config: Dict = None) -> Task:
        """Create a new task"""
        task_id = uuid4()
        task = Task(
            id=task_id,
            name=name,
            seed_ids=seed_ids,
            rule_ids=rule_ids,
            config=config or {}
        )
        self.tasks[task_id] = task
        self.history.append(task_id)
        return task
    
    def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def start_task(self, task_id: UUID) -> bool:
        """Start a task"""
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            return True
        return False
    
    def update_progress(self, task_id: UUID, current: int, total: int, 
                       speed: int = 0, eta: int = 0):
        """Update task progress"""
        task = self.get_task(task_id)
        if task:
            task.progress.current = current
            task.progress.total = total
            task.progress.speed = speed
            task.progress.eta = eta
    
    def complete_task(self, task_id: UUID, results: ResultInfo):
        """Complete a task"""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.results = results
            task.completed_at = datetime.now()
    
    def fail_task(self, task_id: UUID, error_message: str):
        """Mark task as failed"""
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.error_message = error_message
            task.completed_at = datetime.now()
    
    def pause_task(self, task_id: UUID) -> bool:
        """Pause a task"""
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.RUNNING:
            task.status = TaskStatus.PAUSED
            return True
        return False
    
    def resume_task(self, task_id: UUID) -> bool:
        """Resume a paused task"""
        task = self.get_task(task_id)
        if task and task.status == TaskStatus.PAUSED:
            task.status = TaskStatus.RUNNING
            return True
        return False
    
    def cancel_task(self, task_id: UUID) -> bool:
        """Cancel a task"""
        task = self.get_task(task_id)
        if task and task.status in [TaskStatus.PENDING, TaskStatus.RUNNING, TaskStatus.PAUSED]:
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now()
            return True
        return False
    
    def list_tasks(self, limit: int = 50) -> List[Task]:
        """List recent tasks"""
        recent_ids = self.history[-limit:]
        return [self.tasks[tid] for tid in recent_ids if tid in self.tasks]
    
    def compare_tasks(self, task_id1: UUID, task_id2: UUID) -> Dict:
        """Compare two tasks"""
        task1 = self.get_task(task_id1)
        task2 = self.get_task(task_id2)
        
        if not task1 or not task2:
            return {}
        
        return {
            "task1": task1.to_dict(),
            "task2": task2.to_dict(),
            "comparison": {
                "seed_diff": len(set(task1.seed_ids) - set(task2.seed_ids)),
                "rule_diff": len(set(task1.rule_ids) - set(task2.rule_ids)),
                "result_diff": abs(task1.results.generated - task2.results.generated)
            }
        }

# Global task manager instance
task_manager = TaskManager()
