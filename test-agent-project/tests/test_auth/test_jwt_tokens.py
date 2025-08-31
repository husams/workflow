"""
Test cases for JWT token generation and validation.
Following TDD approach - tests written before implementation.
"""

import time
from datetime import datetime, timedelta, timezone
import pytest

# These imports will fail initially - that's expected in TDD
from test_agent_project.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
    get_token_expiry,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class TestAccessTokenGeneration:
    """Test cases for access token generation."""
    
    def test_create_access_token_structure(self):
        """Test that access token has correct JWT structure."""
        user_data = {"sub": "user@example.com", "user_id": "123"}
        token = create_access_token(user_data)
        
        # JWT has three parts separated by dots
        parts = token.split(".")
        assert len(parts) == 3
        
        # Can be decoded
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "user@example.com"
        assert decoded["user_id"] == "123"
    
    def test_create_access_token_expiry(self):
        """Test that access token has correct expiry time."""
        user_data = {"sub": "user@example.com"}
        token = create_access_token(user_data)
        
        decoded = decode_token(token)
        assert decoded is not None
        
        # Check expiry is set
        assert "exp" in decoded
        
        # Check expiry is approximately correct (within 1 minute tolerance)
        expected_exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        diff = abs((expected_exp - actual_exp).total_seconds())
        assert diff < 60  # Within 1 minute
    
    def test_create_access_token_custom_expiry(self):
        """Test creating access token with custom expiry."""
        user_data = {"sub": "user@example.com"}
        custom_expiry = timedelta(hours=2)
        token = create_access_token(user_data, expires_delta=custom_expiry)
        
        decoded = decode_token(token)
        assert decoded is not None
        
        expected_exp = datetime.now(timezone.utc) + custom_expiry
        actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        diff = abs((expected_exp - actual_exp).total_seconds())
        assert diff < 60  # Within 1 minute
    
    def test_create_access_token_additional_claims(self):
        """Test that additional claims are included in token."""
        user_data = {
            "sub": "user@example.com",
            "user_id": "123",
            "roles": ["user", "admin"],
            "correlation_id": "abc-123"
        }
        token = create_access_token(user_data)
        
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["roles"] == ["user", "admin"]
        assert decoded["correlation_id"] == "abc-123"


class TestRefreshTokenGeneration:
    """Test cases for refresh token generation."""
    
    def test_create_refresh_token_structure(self):
        """Test that refresh token has correct structure."""
        user_data = {"sub": "user@example.com", "user_id": "123"}
        token = create_refresh_token(user_data)
        
        # JWT structure
        parts = token.split(".")
        assert len(parts) == 3
        
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "user@example.com"
        assert decoded["token_type"] == "refresh"
    
    def test_create_refresh_token_longer_expiry(self):
        """Test that refresh token has longer expiry than access token."""
        user_data = {"sub": "user@example.com"}
        refresh_token = create_refresh_token(user_data)
        
        decoded = decode_token(refresh_token)
        assert decoded is not None
        
        # Check expiry is approximately correct (within 1 hour tolerance)
        expected_exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        actual_exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        diff = abs((expected_exp - actual_exp).total_seconds())
        assert diff < 3600  # Within 1 hour


class TestTokenVerification:
    """Test cases for token verification."""
    
    def test_verify_valid_token(self):
        """Test that valid token verifies successfully."""
        user_data = {"sub": "user@example.com"}
        token = create_access_token(user_data)
        
        result = verify_token(token)
        assert result is True
    
    def test_verify_expired_token(self):
        """Test that expired token fails verification."""
        user_data = {"sub": "user@example.com"}
        # Create token that expires immediately
        token = create_access_token(user_data, expires_delta=timedelta(seconds=-1))
        
        result = verify_token(token)
        assert result is False
    
    def test_verify_invalid_signature(self):
        """Test that token with invalid signature fails."""
        user_data = {"sub": "user@example.com"}
        token = create_access_token(user_data)
        
        # Tamper with the token
        parts = token.split(".")
        tampered_token = f"{parts[0]}.{parts[1]}.invalid_signature"
        
        result = verify_token(tampered_token)
        assert result is False
    
    def test_verify_malformed_token(self):
        """Test that malformed token fails verification."""
        invalid_tokens = [
            "not.a.token",
            "only.two",
            "",
            "completely-invalid",
        ]
        
        for invalid_token in invalid_tokens:
            assert verify_token(invalid_token) is False


class TestTokenDecoding:
    """Test cases for token decoding."""
    
    def test_decode_valid_token(self):
        """Test decoding a valid token returns payload."""
        user_data = {"sub": "user@example.com", "user_id": "123"}
        token = create_access_token(user_data)
        
        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "user@example.com"
        assert decoded["user_id"] == "123"
    
    def test_decode_expired_token(self):
        """Test that expired token returns None."""
        user_data = {"sub": "user@example.com"}
        token = create_access_token(user_data, expires_delta=timedelta(seconds=-1))
        
        decoded = decode_token(token)
        assert decoded is None
    
    def test_decode_invalid_token(self):
        """Test that invalid token returns None."""
        decoded = decode_token("invalid.token.here")
        assert decoded is None


class TestTokenExpiry:
    """Test cases for token expiry extraction."""
    
    def test_get_token_expiry_valid(self):
        """Test extracting expiry from valid token."""
        user_data = {"sub": "user@example.com"}
        token = create_access_token(user_data)
        
        expiry = get_token_expiry(token)
        assert expiry is not None
        assert isinstance(expiry, datetime)
        assert expiry > datetime.now(timezone.utc).replace(tzinfo=None)
    
    def test_get_token_expiry_invalid(self):
        """Test that invalid token returns None for expiry."""
        expiry = get_token_expiry("invalid.token")
        assert expiry is None