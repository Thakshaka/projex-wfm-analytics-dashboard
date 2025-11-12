"""
Auth endpoints for the frontend service
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import timedelta
from core.config import settings, REQUIRE_AUTH
from core.security import create_access_token
from api.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class FrontendAuthRequest(BaseModel):
    api_key: str
    api_secret: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

@router.post("/login", response_model=TokenResponse)
async def frontend_login(auth: FrontendAuthRequest):
    """Authenticate the frontend service and return a JWT"""
    if REQUIRE_AUTH:
        if not (settings.FRONTEND_API_KEY and settings.FRONTEND_API_SECRET):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Frontend API credentials missing in config."
            )
        if (
            auth.api_key != settings.FRONTEND_API_KEY
            or auth.api_secret != settings.FRONTEND_API_SECRET
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API credentials."
            )

    token_data = {"sub": "frontend_service", "type": "service_token"}
    token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return info about the current authenticated user"""
    return {
        "user": current_user,
        "auth_mode": "prod" if REQUIRE_AUTH else "dev"
    }
