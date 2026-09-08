"""FastAPI application factory"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api import seeds, rules, tasks, export, analysis

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="SeedForge API",
        description="Professional seed-based dictionary generator",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(seeds.router, prefix="/api/seeds", tags=["Seeds"])
    app.include_router(rules.router, prefix="/api/rules", tags=["Rules"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
    app.include_router(export.router, prefix="/api/export", tags=["Export"])
    app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "ok", "version": "0.1.0"}
    
    return app
