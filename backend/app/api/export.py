"""API routes for export"""

from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.post("/txt")
async def export_txt(passwords: List[str], filename: str = "dictionary.txt"):
    """Export as TXT"""
    return {
        "success": True,
        "format": "txt",
        "count": len(passwords),
        "filename": filename
    }

@router.post("/csv")
async def export_csv(passwords: List[str], filename: str = "dictionary.csv"):
    """Export as CSV"""
    return {
        "success": True,
        "format": "csv",
        "count": len(passwords),
        "filename": filename
    }

@router.post("/json")
async def export_json(passwords: List[str], filename: str = "dictionary.json"):
    """Export as JSON"""
    return {
        "success": True,
        "format": "json",
        "count": len(passwords),
        "filename": filename
    }
