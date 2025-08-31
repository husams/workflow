"""
Test cases for authentication Pydantic models.
Following TDD approach - tests written before implementation.
"""

import pytest
from pydantic import ValidationError

# These imports will fail initially - that's expected in TDD
from test_agent_project.api.auth_endpoints import (
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    UserCredentials,
)


class TestLoginRequest:
    """Test cases for LoginRequest model validation."""

    def test_valid_login_request(self):
        """Test that valid login request data passes validation."""
        request = LoginRequest(
            username="testuser@example.com",
            password="SecurePass123!",
        )
        assert request.username == "testuser@example.com"
        assert request.password == "SecurePass123!"
    
    def test_login_request_empty_username(self):
        """Test that empty username raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(username="", password="password123")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("username",) for error in errors)
    
    def test_login_request_empty_password(self):
        """Test that empty password raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(username="user@example.com", password="")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("password",) for error in errors)
    
    def test_login_request_invalid_email(self):
        """Test that invalid email format raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(username="not-an-email", password="password123")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("username",) for error in errors)
    
    def test_login_request_weak_password(self):
        """Test that weak password raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            LoginRequest(username="user@example.com", password="weak")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("password",) for error in errors)


class TestLoginResponse:
    """Test cases for LoginResponse model."""
    
    def test_valid_login_response(self):
        """Test that valid login response data passes validation."""
        response = LoginResponse(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            refresh_token="refresh_token_string",
            token_type="Bearer",
            expires_in=3600,
        )
        assert response.access_token.startswith("eyJ")
        assert response.token_type == "Bearer"
        assert response.expires_in == 3600
        assert response.refresh_token == "refresh_token_string"
    
    def test_login_response_without_refresh_token(self):
        """Test that login response works without refresh token."""
        response = LoginResponse(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            token_type="Bearer",
            expires_in=3600,
        )
        assert response.refresh_token is None
    
    def test_login_response_invalid_token_type(self):
        """Test that invalid token type raises validation error."""
        with pytest.raises(ValidationError):
            LoginResponse(
                access_token="token",
                token_type="InvalidType",
                expires_in=3600,
            )


class TestTokenRefreshRequest:
    """Test cases for TokenRefreshRequest model."""
    
    def test_valid_refresh_request(self):
        """Test that valid refresh request passes validation."""
        request = TokenRefreshRequest(
            refresh_token="valid_refresh_token_string"
        )
        assert request.refresh_token == "valid_refresh_token_string"
    
    def test_refresh_request_empty_token(self):
        """Test that empty refresh token raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            TokenRefreshRequest(refresh_token="")
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("refresh_token",) for error in errors)


class TestTokenRefreshResponse:
    """Test cases for TokenRefreshResponse model."""
    
    def test_valid_refresh_response(self):
        """Test that valid refresh response passes validation."""
        response = TokenRefreshResponse(
            access_token="new_access_token",
            expires_in=3600,
        )
        assert response.access_token == "new_access_token"
        assert response.expires_in == 3600


class TestUserCredentials:
    """Test cases for UserCredentials internal model."""
    
    def test_valid_user_credentials(self):
        """Test that valid user credentials pass validation."""
        creds = UserCredentials(
            username="user@example.com",
            hashed_password="$2b$12$hashed_password_here",
            user_id="user_123",
        )
        assert creds.username == "user@example.com"
        assert creds.hashed_password.startswith("$2b$")
        assert creds.user_id == "user_123"
    
    def test_user_credentials_with_disabled_flag(self):
        """Test user credentials with disabled flag."""
        creds = UserCredentials(
            username="user@example.com",
            hashed_password="$2b$12$hashed_password_here",
            user_id="user_123",
            disabled=True,
        )
        assert creds.disabled is True