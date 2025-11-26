from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import auth, predict, admin

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # Include API routes
    application.include_router(
        auth.router,
        prefix=f"{settings.API_V1_STR}/auth",
        tags=["auth"]
    )
    
    application.include_router(
        predict.router,
        prefix=f"{settings.API_V1_STR}/predict",
        tags=["predictions"]
    )
    
    application.include_router(
        admin.router,
        prefix=f"{settings.API_V1_STR}/admin",
        tags=["admin"]
    )
    
    return application

app = create_application()

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    from app.db.init_db import init_db
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    init_db(db)
