"""Tests for password validation following TDD approach.

These tests are written BEFORE implementation to follow TDD Red-Green-Refactor cycle.
The developer agent should implement the code to make these tests pass.
"""

import pytest
from test_agent_project.auth.validators import validate_password, ValidationResult


class TestPasswordValidation:
    """Test suite for password validation rules."""

    def test_password_minimum_length(self):
        """Password must be at least 8 characters."""
        result = validate_password("short")
        assert not result.is_valid
        assert "at least 8 characters" in result.error_message

    def test_password_accepts_minimum_length(self):
        """Password with exactly 8 characters should be checked for other criteria."""
        # This will fail on length but we're testing the length check works
        result = validate_password("12345678")
        # It might fail on other criteria, but not length
        if not result.is_valid and "at least 8 characters" in result.error_message:
            pytest.fail("Should not fail on length for 8 character password")

    def test_password_requires_uppercase(self):
        """Password must contain at least one uppercase letter."""
        result = validate_password("password123!")
        assert not result.is_valid
        assert "uppercase letter" in result.error_message.lower()

    def test_password_requires_lowercase(self):
        """Password must contain at least one lowercase letter."""
        result = validate_password("PASSWORD123!")
        assert not result.is_valid
        assert "lowercase letter" in result.error_message.lower()

    def test_password_requires_number(self):
        """Password must contain at least one number."""
        result = validate_password("Password!")
        assert not result.is_valid
        assert "number" in result.error_message.lower() or "digit" in result.error_message.lower()

    def test_password_requires_special_character(self):
        """Password must contain at least one special character."""
        result = validate_password("Password123")
        assert not result.is_valid
        assert "special character" in result.error_message.lower()

    def test_valid_password_passes_all_checks(self):
        """A password meeting all criteria should be valid."""
        result = validate_password("MyP@ssw0rd!")
        assert result.is_valid
        assert result.error_message == ""

    def test_password_cannot_be_none(self):
        """Password cannot be None."""
        result = validate_password(None)
        assert not result.is_valid
        assert "required" in result.error_message.lower() or "cannot be empty" in result.error_message.lower()

    def test_password_cannot_be_empty(self):
        """Password cannot be an empty string."""
        result = validate_password("")
        assert not result.is_valid
        assert "required" in result.error_message.lower() or "cannot be empty" in result.error_message.lower()

    def test_common_password_rejected(self):
        """Common passwords should be rejected even if they meet other criteria."""
        # This would meet all criteria but is too common
        result = validate_password("Password123!")
        assert not result.is_valid
        assert "common password" in result.error_message.lower() or "too common" in result.error_message.lower()

    def test_password_with_username_rejected(self):
        """Password containing the username should be rejected."""
        result = validate_password("JohnDoe123!", username="johndoe")
        assert not result.is_valid
        assert "username" in result.error_message.lower()

    def test_password_with_email_rejected(self):
        """Password containing the email should be rejected."""
        result = validate_password("john@example123!", email="john@example.com")
        assert not result.is_valid
        assert "email" in result.error_message.lower()

    def test_multiple_validation_errors_reported(self):
        """Multiple validation errors should all be reported."""
        result = validate_password("abc")  # Too short, no uppercase, no number, no special char
        assert not result.is_valid
        # Check that multiple issues are mentioned
        error_lower = result.error_message.lower()
        error_indicators = [
            "at least 8" in error_lower or "length" in error_lower,
            "uppercase" in error_lower,
            "number" in error_lower or "digit" in error_lower,
            "special" in error_lower
        ]
        assert sum(error_indicators) >= 2, "Should report multiple validation failures"


class TestValidationResult:
    """Test the ValidationResult data class."""

    def test_validation_result_success(self):
        """ValidationResult can represent success."""
        result = ValidationResult(is_valid=True, error_message="")
        assert result.is_valid
        assert result.error_message == ""

    def test_validation_result_failure(self):
        """ValidationResult can represent failure with message."""
        result = ValidationResult(is_valid=False, error_message="Password too short")
        assert not result.is_valid
        assert result.error_message == "Password too short"

    def test_validation_result_string_representation(self):
        """ValidationResult should have useful string representation."""
        result = ValidationResult(is_valid=False, error_message="Test error")
        str_repr = str(result)
        assert "False" in str_repr or "invalid" in str_repr.lower()
        assert "Test error" in str_repr