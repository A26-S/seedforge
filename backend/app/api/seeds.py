"""API routes for seed management"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from uuid import UUID

from app.services.seed.manager import seed_manager, Seed, SeedCategory, SeedSource

router = APIRouter()

@router.get("/categories")
async def list_categories():
    """List all seed categories"""
    return {
        "categories": [cat.value for cat in SeedCategory]
    }

@router.get("/list/{category}")
async def list_seeds(category: str):
    """List seeds by category"""
    try:
        cat = SeedCategory(category)
        seeds = seed_manager.list_seeds(cat)
        return {
            "category": category,
            "count": len(seeds),
            "seeds": [s.to_dict() for s in seeds]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category")

@router.get("/search")
async def search_seeds(q: str, category: Optional[str] = None):
    """Search seeds"""
    try:
        cat = SeedCategory(category) if category else None
        seeds = seed_manager.search_seeds(q, cat)
        return {
            "query": q,
            "count": len(seeds),
            "seeds": [s.to_dict() for s in seeds]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category")

@router.post("/add")
async def add_seed(value: str, category: str, tags: List[str] = None):
    """Add a seed"""
    try:
        cat = SeedCategory(category)
        seed = seed_manager.add_seed(value, cat, SeedSource.IMPORTED, tags)
        return {
            "success": True,
            "seed": seed.to_dict()
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category")

@router.post("/import")
async def import_seeds(category: str, file: UploadFile = File(...)):
    """Import seeds from file"""
    try:
        cat = SeedCategory(category)
        # Handle file upload
        contents = await file.read()
        
        # Save temporarily and import
        count = 0
        for line in contents.decode('utf-8').splitlines():
            value = line.strip()
            if value:
                seed_manager.add_seed(value, cat, SeedSource.IMPORTED)
                count += 1
        
        return {
            "success": True,
            "imported": count
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category")

@router.get("/statistics")
async def get_statistics():
    """Get seed statistics"""
    return seed_manager.get_statistics()
