"""API routes for rules"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.services.rules.engine import rule_engine, RuleParser, PresetLibrary

router = APIRouter()

@router.get("/presets")
async def list_presets():
    """List password pattern presets"""
    return {
        "presets": PresetLibrary.list_presets()
    }

@router.get("/presets/{preset_name}")
async def get_preset(preset_name: str):
    """Get preset details"""
    preset = PresetLibrary.get_preset(preset_name)
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return preset

@router.post("/preview")
async def preview_rules(seeds: List[str], rules: Dict[str, Any]):
    """Preview rule results"""
    # Validate and preview
    preview_results = rule_engine.preview(seeds[:5])  # Limit to 5 for preview
    
    return {
        "preview": preview_results[:20],  # Show first 20
        "estimated_total": len(preview_results) * 4  # Rough estimate
    }

@router.post("/validate")
async def validate_rule(rule: Dict[str, Any]):
    """Validate a rule"""
    # Validate rule structure
    if "type" not in rule:
        raise HTTPException(status_code=400, detail="Missing rule type")
    
    return {
        "valid": True,
        "errors": []
    }
