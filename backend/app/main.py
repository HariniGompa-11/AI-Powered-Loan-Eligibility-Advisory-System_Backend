import os
import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Import your application modules
from app.core.config import settings
from app.db.init_db import init_db
from app.api.routes import auth, predict, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Loan Eligibility API",
    version="1.0.0",
    description="API for loan eligibility prediction and management",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# Request validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Custom HTTP exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": app.version,
        "environment": settings.ENVIRONMENT
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Loan Eligibility API is running",
        "version": app.version,
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }

# Include API routers
app.include_router(
    auth.router,
    prefix=settings.API_V1_STR + "/auth",
    tags=["Authentication"]
)

app.include_router(
    predict.router,
    prefix=settings.API_V1_STR + "/predict",
    tags=["Predictions"]
)

app.include_router(
    admin.router,
    prefix=settings.API_V1_STR + "/admin",
    tags=["Admin"],
    dependencies=[]
)

# Startup Event — run initialization
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting application initialization...")
        await init_db()
        logger.info("Application startup complete")
    except Exception as e:
        logger.critical(f"Failed to initialize application: {e}")
        # Re-raise to prevent the application from starting in a bad state
        raise

# For local development
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
