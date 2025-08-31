"""Password validation module.

This module validates passwords against security requirements following
industry best practices for password strength and security.

The validator checks for:
- Minimum length requirements
- Character diversity (uppercase, lowercase, numbers, special characters)
- Common password patterns
- Username/email inclusion
"""

import re
from dataclasses import dataclass
from typing import Optional

# Password validation patterns
UPPERCASE_PATTERN = r'[A-Z]'
LOWERCASE_PATTERN = r'[a-z]'
NUMBER_PATTERN = r'[0-9]'
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*(),.?":{}|<>]'

# Password requirements
MIN_PASSWORD_LENGTH = 8

# Common passwords that should be rejected
# In production, this would typically be a larger database or service call
COMMON_PASSWORDS = [
    'Password123!', 
    'password123', 
    'Welcome123!', 
    'Qwerty123!'
]


@dataclass
class ValidationResult:
    """Result of a validation check."""
    is_valid: bool
    error_message: str
    
    def __str__(self) -> str:
        """String representation of validation result."""
        if self.is_valid:
            return "Valid"
        return f"Invalid: {self.error_message}"


def validate_password(
    password: Optional[str], 
    username: Optional[str] = None,
    email: Optional[str] = None
) -> ValidationResult:
    """Validate a password against security requirements.
    
    Performs comprehensive password validation including:
    - Length validation (minimum 8 characters)
    - Character complexity requirements
    - Common password detection
    - Context-based validation (username/email exclusion)
    
    Args:
        password: The password to validate
        username: Optional username to check password doesn't contain
        email: Optional email to check password doesn't contain
        
    Returns:
        ValidationResult with is_valid and error_message.
        If validation fails, error_message contains all validation failures
        concatenated with '. ' separator.
    """
    # Check for None or empty password - this is critical and fails immediately
    if password is None or password == "":
        return ValidationResult(
            is_valid=False,
            error_message="Password is required and cannot be empty"
        )
    
    # Accumulate all validation errors
    errors = []
    
    # Check minimum length
    if len(password) < MIN_PASSWORD_LENGTH:
        errors.append(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long")
    
    # Check for uppercase letter
    if not re.search(UPPERCASE_PATTERN, password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase letter
    if not re.search(LOWERCASE_PATTERN, password):
        errors.append("Password must contain at least one lowercase letter")
    
    # Check for number
    if not re.search(NUMBER_PATTERN, password):
        errors.append("Password must contain at least one number")
    
    # Check for special character
    if not re.search(SPECIAL_CHAR_PATTERN, password):
        errors.append("Password must contain at least one special character")
    
    # Check against common passwords
    if password in COMMON_PASSWORDS:
        errors.append("This is a common password and cannot be used")
    
    # Check if password contains username
    if username and username.lower() in password.lower():
        errors.append("Password cannot contain the username")
    
    # Check if password contains parts of email
    if email:
        email_parts = email.split('@')
        if email_parts[0].lower() in password.lower():
            errors.append("Password cannot contain parts of the email address")
    
    # Return result based on accumulated errors
    if errors:
        return ValidationResult(
            is_valid=False,
            error_message=". ".join(errors)
        )
    else:
        return ValidationResult(
            is_valid=True,
            error_message=""
        )