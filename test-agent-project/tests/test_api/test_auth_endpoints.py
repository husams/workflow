"""
Test cases for authentication endpoints.
Testing the complete login API with rate limiting.
"""

import asyncio
from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app and endpoints
from test_agent_project.api.auth_endpoints import app, fake_users_db


class TestLoginEndpoint:
    """Test cases for the login endpoint."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        # Clear rate limit storage before each test
        from test_agent_project.api.auth_endpoints import rate_limit_storage
        rate_limit_storage.clear()
        return TestClient(app)
    
    def test_login_success(self, client):
        """Test successful login with valid credentials."""
        response = client.post(
            "/auth/login",
            json={
                "username": "test@example.com",
                "password": "TestPassword123!"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "Bearer"
        assert data["expires_in"] == 1800  # 30 minutes
    
    def test_login_invalid_username(self, client):
        """Test login with non-existent username."""
        response = client.post(
            "/auth/login",
            json={
                "username": "nonexistent@example.com",
                "password": "TestPassword123!"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_invalid_password(self, client):
        """Test login with wrong password."""
        response = client.post(
            "/auth/login",
            json={
                "username": "test@example.com",
                "password": "WrongPassword456!"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_disabled_account(self, client):
        """Test login with disabled account."""
        response = client.post(
            "/auth/login",
            json={
                "username": "disabled@example.com",
                "password": "TestPassword123!"
            }
        )
        
        assert response.status_code == 403
        assert "Account disabled" in response.json()["detail"]
    
    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format."""
        response = client.post(
            "/auth/login",
            json={
                "username": "not-an-email",
                "password": "TestPassword123!"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_login_weak_password(self, client):
        """Test login with weak password (validation)."""
        response = client.post(
            "/auth/login",
            json={
                "username": "test@example.com",
                "password": "weak"
            }
        )
        
        assert response.status_code == 422  # Validation error


class TestRateLimiting:
    """Test cases for rate limiting functionality."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        # Clear rate limit storage before each test
        from test_agent_project.api.auth_endpoints import rate_limit_storage
        rate_limit_storage.clear()
        return TestClient(app)
    
    def test_rate_limit_normal_usage(self, client):
        """Test that normal usage is not rate limited."""
        # Make 3 requests (under limit)
        for i in range(3):
            response = client.post(
                "/auth/login",
                json={
                    "username": f"user{i}@example.com",
                    "password": "WrongPassword123!"
                }
            )
            assert response.status_code in [401, 403]  # Not rate limited
    
    def test_rate_limit_exceeded(self, client):
        """Test that excessive requests are rate limited."""
        # Make 6 requests rapidly (over limit of 5)
        for i in range(6):
            response = client.post(
                "/auth/login",
                json={
                    "username": "test@example.com",
                    "password": "WrongPassword123!"
                },
                headers={"X-Forwarded-For": "192.168.1.100"}
            )
            
            if i < 5:
                assert response.status_code in [401, 403]
            else:
                # 6th request should be rate limited
                assert response.status_code == 429
                assert "Too many requests" in response.json()["detail"]
    
    def test_rate_limit_different_ips(self, client):
        """Test that rate limiting is per IP address."""
        # Make requests from different IPs
        for i in range(6):
            response = client.post(
                "/auth/login",
                json={
                    "username": "test@example.com",
                    "password": "WrongPassword123!"
                },
                headers={"X-Forwarded-For": f"192.168.1.{i}"}
            )
            # All should succeed (different IPs)
            assert response.status_code in [401, 403]


class TestRefreshToken:
    """Test cases for refresh token functionality."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        # Clear rate limit storage before each test
        from test_agent_project.api.auth_endpoints import rate_limit_storage
        rate_limit_storage.clear()
        return TestClient(app)
    
    @pytest.fixture
    def auth_tokens(self, client):
        """Get valid auth tokens."""
        response = client.post(
            "/auth/login",
            json={
                "username": "test@example.com",
                "password": "TestPassword123!"
            }
        )
        return response.json()
    
    def test_refresh_token_success(self, client, auth_tokens):
        """Test successful token refresh."""
        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": auth_tokens["refresh_token"]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["expires_in"] == 1800
        # New access token should be different
        assert data["access_token"] != auth_tokens["access_token"]
    
    def test_refresh_token_invalid(self, client):
        """Test refresh with invalid token."""
        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": "invalid.refresh.token"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]
    
    def test_refresh_token_expired(self, client):
        """Test refresh with expired token."""
        from test_agent_project.auth.jwt_handler import create_refresh_token
        
        # Create an expired refresh token
        expired_token = create_refresh_token(
            {"sub": "test@example.com"},
            expires_delta=timedelta(seconds=-1)
        )
        
        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": expired_token
            }
        )
        
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]


class TestSecurityHeaders:
    """Test cases for security headers and CORS."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        # Clear rate limit storage before each test
        from test_agent_project.api.auth_endpoints import rate_limit_storage
        rate_limit_storage.clear()
        return TestClient(app)
    
    def test_cors_headers(self, client):
        """Test that CORS headers are properly set."""
        response = client.options(
            "/auth/login",
            headers={
                "Origin": "https://example.com",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
    
    def test_security_headers(self, client):
        """Test that security headers are present."""
        response = client.post(
            "/auth/login",
            json={
                "username": "test@example.com",
                "password": "TestPassword123!"
            }
        )
        
        # Check for security headers
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"
        assert "x-frame-options" in response.headers
        assert response.headers["x-frame-options"] == "DENY"