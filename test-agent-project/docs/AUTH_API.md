# Authentication API Documentation

## Overview

Secure REST API for user authentication with JWT tokens, rate limiting, and comprehensive security measures.

## Security Features

- **Password Security**: Bcrypt hashing with salt, minimum 8 characters with complexity requirements
- **JWT Tokens**: HS256 algorithm with configurable expiration
- **Rate Limiting**: 5 requests per minute per IP address
- **CORS Support**: Configurable cross-origin resource sharing
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- **Correlation IDs**: Request tracking for debugging and audit trails
- **Input Validation**: Email format and password strength validation via Pydantic

## API Endpoints

### 1. Login
**POST** `/auth/login`

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account disabled
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded

### 2. Refresh Token
**POST** `/auth/refresh`

Exchange refresh token for new access token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 1800
}
```

### 3. Get Current User
**GET** `/auth/me`

Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "username": "user@example.com",
  "user_id": "user_001"
}
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)

## Rate Limiting

- **Limit**: 5 requests per minute
- **Window**: 60 seconds sliding window
- **Scope**: Per IP address
- **Header**: X-Forwarded-For supported for proxy configurations

## Security Considerations

1. **Token Storage**: Store tokens securely (httpOnly cookies or secure storage)
2. **HTTPS Only**: Always use HTTPS in production
3. **Token Rotation**: Regularly refresh access tokens using refresh tokens
4. **Environment Variables**: Use proper secret management for JWT_SECRET_KEY
5. **CORS Configuration**: Configure allowed origins appropriately for production
6. **Logging**: Sensitive data is never logged

## Configuration

Environment variables:
- `JWT_SECRET_KEY`: Secret key for JWT signing (required for production)
- Default expiration times can be modified in `jwt_handler.py`:
  - Access token: 30 minutes
  - Refresh token: 7 days

## Testing

Run tests with coverage:
```bash
export PYTHONPATH=src
pytest tests/ --cov=test_agent_project --cov-report=term-missing
```

Current test coverage: 92%

## Development

Start the development server:
```bash
uvicorn test_agent_project.api.auth_endpoints:app --reload
```

Access API documentation at: `http://localhost:8000/docs`