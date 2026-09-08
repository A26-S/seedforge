"""API routes for tasks"""

from fastapi import APIRouter, HTTPException, WebSocket
from typing import List
from uuid import UUID

from app.services.tasks.manager import task_manager, TaskStatus

router = APIRouter()

@router.post("/create")
async def create_task(name: str, seed_ids: List[str], rule_ids: List[str], config: dict):
    """Create a new task"""
    try:
        seed_uuids = [UUID(sid) for sid in seed_ids]
        rule_uuids = [UUID(rid) for rid in rule_ids]
        
        task = task_manager.create_task(name, seed_uuids, rule_uuids, config)
        return {
            "success": True,
            "task": task.to_dict()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}")
async def get_task(task_id: str):
    """Get task details"""
    try:
        tid = UUID(task_id)
        task = task_manager.get_task(tid)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task.to_dict()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID")

@router.post("/{task_id}/start")
async def start_task(task_id: str):
    """Start a task"""
    try:
        tid = UUID(task_id)
        if task_manager.start_task(tid):
            return {"success": True, "status": "running"}
        raise HTTPException(status_code=400, detail="Cannot start task")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID")

@router.post("/{task_id}/pause")
async def pause_task(task_id: str):
    """Pause a task"""
    try:
        tid = UUID(task_id)
        if task_manager.pause_task(tid):
            return {"success": True, "status": "paused"}
        raise HTTPException(status_code=400, detail="Cannot pause task")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID")

@router.post("/{task_id}/resume")
async def resume_task(task_id: str):
    """Resume a paused task"""
    try:
        tid = UUID(task_id)
        if task_manager.resume_task(tid):
            return {"success": True, "status": "running"}
        raise HTTPException(status_code=400, detail="Cannot resume task")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID")

@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    """Cancel a task"""
    try:
        tid = UUID(task_id)
        if task_manager.cancel_task(tid):
            return {"success": True, "status": "cancelled"}
        raise HTTPException(status_code=400, detail="Cannot cancel task")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID")

@router.get("/history")
async def list_tasks():
    """List task history"""
    tasks = task_manager.list_tasks()
    return {
        "count": len(tasks),
        "tasks": [t.to_dict() for t in tasks]
    }

@router.post("/compare")
async def compare_tasks(task_id1: str, task_id2: str):
    """Compare two tasks"""
    try:
        tid1 = UUID(task_id1)
        tid2 = UUID(task_id2)
        comparison = task_manager.compare_tasks(tid1, tid2)
        if not comparison:
            raise HTTPException(status_code=404, detail="One or both tasks not found")
        return comparison
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID")
