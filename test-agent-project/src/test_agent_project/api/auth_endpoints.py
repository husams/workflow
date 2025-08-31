"""
Authentication endpoints with Pydantic models for request/response validation.
Implements secure REST API for user authentication with JWT tokens.

Security features:
- Strong password validation (minimum 8 chars, mixed case, digits)
- Email format validation for usernames
- JWT token-based authentication
- Support for refresh tokens
- Bcrypt password hashing (hashed passwords only in storage)
- Rate limiting to prevent brute force attacks
- CORS headers for API security
- Correlation IDs for request tracking
"""

import re
import uuid
import logging
from datetime import datetime, timedelta
from typing import Optional, Literal, Dict, Any
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr, field_validator

from test_agent_project.auth.security import hash_password, verify_password
from test_agent_project.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoginRequest(BaseModel):
    """Request model for user login."""
    
    username: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password meets minimum security requirements.
        
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter  
        - At least one digit
        
        Raises:
            ValueError: If password doesn't meet requirements
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        
        return v


class LoginResponse(BaseModel):
    """Response model for successful login."""
    
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    token_type: Literal["Bearer"] = Field("Bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenRefreshRequest(BaseModel):
    """Request model for token refresh."""
    
    refresh_token: str = Field(..., min_length=1, description="Valid refresh token")


class TokenRefreshResponse(BaseModel):
    """Response model for token refresh."""
    
    access_token: str = Field(..., description="New JWT access token")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class UserCredentials(BaseModel):
    """Internal model for user credentials storage."""
    
    username: EmailStr = Field(..., description="User email address")
    hashed_password: str = Field(..., description="Bcrypt hashed password")
    user_id: str = Field(..., description="Unique user identifier")
    disabled: bool = Field(False, description="Account disabled flag")


# Initialize FastAPI app
app = FastAPI(title="Auth API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting storage
rate_limit_storage: Dict[str, list] = defaultdict(list)
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW = 60  # seconds

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    response = await call_next(request)
    
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    return response


# Fake users database for testing
fake_users_db = {
    "test@example.com": {
        "username": "test@example.com",
        "hashed_password": hash_password("TestPassword123!"),
        "user_id": "user_001",
        "disabled": False,
    },
    "disabled@example.com": {
        "username": "disabled@example.com",
        "hashed_password": hash_password("TestPassword123!"),
        "user_id": "user_002",
        "disabled": True,
    },
}


def check_rate_limit(request: Request) -> bool:
    """
    Check if request exceeds rate limit.
    
    Args:
        request: FastAPI request object
        
    Returns:
        True if rate limit exceeded, False otherwise
    """
    # Get client IP
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)
    
    # Get current time
    now = datetime.now()
    
    # Clean old entries
    rate_limit_storage[client_ip] = [
        timestamp for timestamp in rate_limit_storage[client_ip]
        if (now - timestamp).total_seconds() < RATE_LIMIT_WINDOW
    ]
    
    # Check limit
    if len(rate_limit_storage[client_ip]) >= RATE_LIMIT_REQUESTS:
        return True
    
    # Add current request
    rate_limit_storage[client_ip].append(now)
    return False


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Get current user from JWT token.
    
    Args:
        credentials: Bearer token from request
        
    Returns:
        User information from token
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    
    if not verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_token(token)
    return payload


@app.post("/auth/login", response_model=LoginResponse)
async def login(request: Request, login_data: LoginRequest):
    """
    Authenticate user and return JWT tokens.
    
    Args:
        request: FastAPI request object
        login_data: Login credentials
        
    Returns:
        LoginResponse with access and refresh tokens
        
    Raises:
        HTTPException: For various authentication failures
    """
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    
    # Check rate limiting
    if check_rate_limit(request):
        logger.warning(
            f"Rate limit exceeded for login attempt",
            extra={"correlation_id": correlation_id, "username": login_data.username}
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )
    
    # Log login attempt
    logger.info(
        f"Login attempt for user: {login_data.username}",
        extra={"correlation_id": correlation_id}
    )
    
    # Get user from database
    user = fake_users_db.get(login_data.username)
    
    if not user:
        logger.warning(
            f"Login failed - user not found: {login_data.username}",
            extra={"correlation_id": correlation_id}
        )
        # Use generic error to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Verify password
    if not verify_password(login_data.password, user["hashed_password"]):
        logger.warning(
            f"Login failed - invalid password for: {login_data.username}",
            extra={"correlation_id": correlation_id}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Check if account is disabled
    if user["disabled"]:
        logger.warning(
            f"Login failed - account disabled: {login_data.username}",
            extra={"correlation_id": correlation_id}
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disabled",
        )
    
    # Create tokens
    token_data = {
        "sub": user["username"],
        "user_id": user["user_id"],
        "correlation_id": correlation_id,
    }
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    logger.info(
        f"Login successful for user: {login_data.username}",
        extra={"correlation_id": correlation_id}
    )
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=1800,  # 30 minutes
    )


@app.post("/auth/refresh", response_model=TokenRefreshResponse)
async def refresh_token(request: Request, refresh_data: TokenRefreshRequest):
    """
    Refresh access token using refresh token.
    
    Args:
        request: FastAPI request object
        refresh_data: Refresh token request
        
    Returns:
        TokenRefreshResponse with new access token
        
    Raises:
        HTTPException: If refresh token is invalid
    """
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    
    # Verify refresh token
    if not verify_token(refresh_data.refresh_token):
        logger.warning(
            f"Invalid refresh token attempted",
            extra={"correlation_id": correlation_id}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Decode refresh token
    payload = decode_token(refresh_data.refresh_token)
    
    if not payload or payload.get("token_type") != "refresh":
        logger.warning(
            f"Invalid refresh token type",
            extra={"correlation_id": correlation_id}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Create new access token
    token_data = {
        "sub": payload["sub"],
        "user_id": payload.get("user_id"),
        "correlation_id": correlation_id,
    }
    
    new_access_token = create_access_token(token_data)
    
    logger.info(
        f"Token refreshed for user: {payload['sub']}",
        extra={"correlation_id": correlation_id}
    )
    
    return TokenRefreshResponse(
        access_token=new_access_token,
        expires_in=1800,  # 30 minutes
    )


@app.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user information from token.
    
    Args:
        current_user: User info from JWT token
        
    Returns:
        Current user information
    """
    return {
        "username": current_user.get("sub"),
        "user_id": current_user.get("user_id"),
    }