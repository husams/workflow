"""
Test cases for password hashing and security functions.
Following TDD approach - tests written before implementation.
"""

import time
import pytest

# These imports will fail initially - that's expected in TDD
from test_agent_project.auth.security import (
    hash_password,
    verify_password,
    is_password_hash_valid,
    constant_time_compare,
)


class TestPasswordHashing:
    """Test cases for password hashing functionality."""
    
    def test_hash_password_returns_hash(self):
        """Test that hash_password returns a bcrypt hash."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        # Bcrypt hashes start with $2b$
        assert hashed.startswith("$2b$")
        # Should be different from original
        assert hashed != password
        # Should be a reasonable length
        assert len(hashed) > 50
    
    def test_hash_password_different_salts(self):
        """Test that same password produces different hashes (salting)."""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Same password should produce different hashes due to salt
        assert hash1 != hash2
    
    def test_hash_password_empty_string(self):
        """Test that empty password raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            hash_password("")
        assert "empty" in str(exc_info.value).lower()
    
    def test_hash_password_none(self):
        """Test that None password raises TypeError."""
        with pytest.raises(TypeError):
            hash_password(None)


class TestPasswordVerification:
    """Test cases for password verification."""
    
    def test_verify_password_correct(self):
        """Test that correct password verifies successfully."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test that incorrect password fails verification."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        # Different case should fail
        assert verify_password("testpassword123!", hashed) is False
        assert verify_password("TESTPASSWORD123!", hashed) is False
    
    def test_verify_password_timing_resistant(self):
        """Test that verification time is consistent (timing attack resistance)."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        # Measure correct password timing
        start = time.perf_counter()
        for _ in range(10):
            verify_password(password, hashed)
        correct_time = time.perf_counter() - start
        
        # Measure incorrect password timing
        start = time.perf_counter()
        for _ in range(10):
            verify_password("WrongPassword", hashed)
        incorrect_time = time.perf_counter() - start
        
        # Times should be similar (within 20% variance)
        ratio = max(correct_time, incorrect_time) / min(correct_time, incorrect_time)
        assert ratio < 1.2, "Password verification may be vulnerable to timing attacks"
    
    def test_verify_password_invalid_hash(self):
        """Test that invalid hash format raises ValueError."""
        with pytest.raises(ValueError):
            verify_password("password", "not-a-valid-hash")
    
    def test_verify_password_empty_inputs(self):
        """Test that empty inputs are handled properly."""
        hashed = hash_password("TestPassword123!")
        
        # Empty password should fail
        assert verify_password("", hashed) is False
        
        # Empty hash should raise error
        with pytest.raises(ValueError):
            verify_password("password", "")


class TestHashValidation:
    """Test cases for hash validation."""
    
    def test_is_password_hash_valid_bcrypt(self):
        """Test that valid bcrypt hash is recognized."""
        valid_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY.pjQYRYRPjqUi"
        assert is_password_hash_valid(valid_hash) is True
    
    def test_is_password_hash_valid_invalid_format(self):
        """Test that invalid hash format is rejected."""
        invalid_hashes = [
            "not-a-hash",
            "$1$invalid",
            "2b$12$tooshort",
            "",
            None,
        ]
        
        for invalid_hash in invalid_hashes:
            assert is_password_hash_valid(invalid_hash) is False


class TestConstantTimeComparison:
    """Test cases for constant-time string comparison."""
    
    def test_constant_time_compare_equal(self):
        """Test that equal strings return True."""
        assert constant_time_compare("test123", "test123") is True
        assert constant_time_compare("", "") is True
    
    def test_constant_time_compare_not_equal(self):
        """Test that different strings return False."""
        assert constant_time_compare("test123", "test456") is False
        assert constant_time_compare("test", "testing") is False
        assert constant_time_compare("", "test") is False
    
    def test_constant_time_compare_timing(self):
        """Test that comparison time is constant regardless of match position."""
        # String that differs at beginning
        s1 = "a" * 1000
        s2 = "b" + "a" * 999
        
        start = time.perf_counter()
        for _ in range(100):
            constant_time_compare(s1, s2)
        early_diff_time = time.perf_counter() - start
        
        # String that differs at end
        s3 = "a" * 999 + "b"
        
        start = time.perf_counter()
        for _ in range(100):
            constant_time_compare(s1, s3)
        late_diff_time = time.perf_counter() - start
        
        # Times should be similar (within 20% variance)
        ratio = max(early_diff_time, late_diff_time) / min(early_diff_time, late_diff_time)
        assert ratio < 1.2, "String comparison may leak timing information"