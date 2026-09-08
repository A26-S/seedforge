"""Backend main application entry point"""

import uvicorn
from app.core.config import settings
from app.core.app import create_app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
