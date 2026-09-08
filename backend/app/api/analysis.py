"""API routes for analysis"""

from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

@router.post("/entropy")
async def analyze_entropy(passwords: List[str]):
    """Analyze password entropy"""
    return {
        "count": len(passwords),
        "analysis": [
            {
                "password": pwd,
                "entropy": 50.0,
                "strength": "medium"
            } for pwd in passwords[:10]
        ]
    }

@router.post("/distribution")
async def analyze_distribution(passwords: List[str]):
    """Analyze character distribution"""
    return {
        "count": len(passwords),
        "distribution": {
            "lowercase": 26,
            "uppercase": 26,
            "digits": 10,
            "symbols": 32
        }
    }
