"""
FastAPI app entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api import project_analytics, auth

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="REST APIs for Project Analytics Dashboard",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_analytics.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "auth_required": settings.ENVIRONMENT.lower() == "prod",
        "docs": "/docs" if settings.DEBUG else "disabled"
    }

if __name__ == "__main__":
    import uvicorn
    print(f"Starting {settings.APP_NAME}...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Auth: {'Required' if settings.ENVIRONMENT.lower() == 'prod' else 'Disabled'}")
    print(f"Docs: http://localhost:{settings.PORT}/docs")
    
    if settings.DEBUG:
        uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
    else:
        uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=False)
