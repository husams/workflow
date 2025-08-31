"""
Security functions for password hashing and verification.
Implements secure password handling with bcrypt and timing attack resistance.
"""

import hmac
import bcrypt
from typing import Union


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with automatic salt generation.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Bcrypt hash string
        
    Raises:
        ValueError: If password is empty
        TypeError: If password is not a string
    """
    if password is None:
        raise TypeError("Password cannot be None")
    
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Convert to bytes and generate salt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    
    # Hash the password
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    Uses constant-time comparison to prevent timing attacks.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to verify against
        
    Returns:
        True if password matches, False otherwise
        
    Raises:
        ValueError: If hashed_password is invalid format
    """
    if not hashed_password:
        raise ValueError("Hashed password cannot be empty")
    
    if not is_password_hash_valid(hashed_password):
        raise ValueError("Invalid hash format")
    
    if not plain_password:
        return False
    
    try:
        # Convert to bytes
        password_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        
        # Use bcrypt's built-in verification (already timing-safe)
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception:
        return False


def is_password_hash_valid(password_hash: Union[str, None]) -> bool:
    """
    Check if a string is a valid bcrypt hash.
    
    Args:
        password_hash: String to validate
        
    Returns:
        True if valid bcrypt hash, False otherwise
    """
    if password_hash is None:
        return False
    
    if not isinstance(password_hash, str):
        return False
    
    # Bcrypt hashes have specific format: $2b$[cost]$[22 char salt][31 char hash]
    # Total length is typically 60 characters
    if len(password_hash) < 59:
        return False
    
    # Must start with $2b$ (or $2a$, $2y$ for older versions)
    if not password_hash.startswith(('$2b$', '$2a$', '$2y$')):
        return False
    
    # Check structure
    parts = password_hash.split('$')
    if len(parts) != 4:
        return False
    
    # Check cost parameter (should be 2 digits)
    if len(parts[2]) != 2 or not parts[2].isdigit():
        return False
    
    return True


def constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to prevent timing attacks.
    
    Args:
        val1: First string to compare
        val2: Second string to compare
        
    Returns:
        True if strings are equal, False otherwise
    """
    # Use hmac.compare_digest for constant-time comparison
    return hmac.compare_digest(val1, val2)