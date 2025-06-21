# API Key Wallet - REST API Implementation Plan

## Overview

This document outlines the technical implementation plan for adding a REST API layer to the existing Flask application, preparing it for SaaS deployment.

---

## API Architecture

### Design Principles
- RESTful design patterns
- JWT-based authentication
- Versioned endpoints (v1)
- Consistent error handling
- Rate limiting from day one
- Comprehensive logging

### Base URL Structure
```
https://api.apikeywallet.com/v1/
```

---

## Authentication Implementation

### JWT Configuration
```python
# config.py
class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
```

### Auth Endpoints
```python
# api/auth.py
@api_bp.route('/v1/auth/register', methods=['POST'])
def api_register():
    """
    Register new user
    Request: {
        "email": "user@example.com",
        "password": "securepass123"
    }
    Response: {
        "message": "User created successfully",
        "user_id": "usr_123abc"
    }
    """

@api_bp.route('/v1/auth/login', methods=['POST'])
def api_login():
    """
    Login user
    Response: {
        "access_token": "eyJ0...",
        "refresh_token": "eyJ1...",
        "expires_in": 3600
    }
    """

@api_bp.route('/v1/auth/refresh', methods=['POST'])
def api_refresh():
    """Refresh access token using refresh token"""

@api_bp.route('/v1/auth/logout', methods=['POST'])
@jwt_required()
def api_logout():
    """Invalidate refresh token"""
```

---

## API Endpoints Specification

### Keys Management

#### List Keys
```
GET /v1/keys
Authorization: Bearer {token}

Query Parameters:
- category_id (optional): Filter by category
- page (default: 1)
- per_page (default: 50)
- search (optional): Search in key names

Response:
{
    "keys": [
        {
            "id": "key_123abc",
            "name": "OpenAI Production",
            "category": {
                "id": "cat_456def",
                "name": "AI Services"
            },
            "created_at": "2025-01-20T10:00:00Z",
            "updated_at": "2025-01-20T10:00:00Z",
            "last_accessed": "2025-01-21T15:30:00Z",
            "metadata": {
                "environment": "production",
                "service": "openai"
            }
        }
    ],
    "pagination": {
        "page": 1,
        "per_page": 50,
        "total": 150,
        "pages": 3
    }
}
```

#### Create Key
```
POST /v1/keys
Authorization: Bearer {token}

Request:
{
    "name": "Stripe Production",
    "key": "sk_live_...",
    "category_id": "cat_789ghi",
    "metadata": {
        "environment": "production",
        "expires_at": "2025-12-31T23:59:59Z"
    }
}

Response:
{
    "id": "key_newkey123",
    "name": "Stripe Production",
    "category": {...},
    "created_at": "2025-01-21T16:00:00Z"
}
```

#### Get Key
```
GET /v1/keys/{key_id}
Authorization: Bearer {token}

Response:
{
    "id": "key_123abc",
    "name": "OpenAI Production",
    "key": "sk-...", // Decrypted
    "category": {...},
    "metadata": {...},
    "access_log": [
        {
            "accessed_at": "2025-01-21T15:30:00Z",
            "ip": "192.168.1.1",
            "user_agent": "Mozilla/5.0..."
        }
    ]
}
```

#### Update Key
```
PATCH /v1/keys/{key_id}
Authorization: Bearer {token}

Request:
{
    "name": "OpenAI Production v2",
    "category_id": "cat_newcat",
    "metadata": {
        "version": "2"
    }
}
```

#### Delete Key
```
DELETE /v1/keys/{key_id}
Authorization: Bearer {token}

Response: 204 No Content
```

### Categories Management

#### List Categories
```
GET /v1/categories
Authorization: Bearer {token}

Response:
{
    "categories": [
        {
            "id": "cat_123",
            "name": "Databases",
            "key_count": 5,
            "created_at": "2025-01-01T00:00:00Z"
        }
    ]
}
```

#### Create Category
```
POST /v1/categories
Authorization: Bearer {token}

Request:
{
    "name": "Payment Processors"
}
```

### User Management

#### Get Profile
```
GET /v1/user/profile
Authorization: Bearer {token}

Response:
{
    "id": "usr_123",
    "email": "user@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "subscription": {
        "plan": "pro",
        "status": "active",
        "expires_at": "2025-01-01T00:00:00Z"
    },
    "usage": {
        "keys_count": 45,
        "keys_limit": 100,
        "api_calls_this_month": 1523
    }
}
```

#### Update Profile
```
PATCH /v1/user/profile
Authorization: Bearer {token}

Request:
{
    "notifications": {
        "key_expiry": true,
        "security_alerts": true
    }
}
```

---

## Implementation Details

### Error Handling
```python
# api/errors.py
class APIError(Exception):
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = {
            'message': self.message,
            'code': self.status_code
        }
        return rv

@api_bp.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
```

### Rate Limiting
```python
# api/middleware.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Applied to endpoints:
@limiter.limit("5 per minute")
@api_bp.route('/v1/keys', methods=['POST'])
def create_key():
    pass
```

### Request/Response Middleware
```python
# api/middleware.py
@api_bp.before_request
def before_request():
    # Log request
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")
    
    # Validate content type
    if request.method in ['POST', 'PATCH', 'PUT']:
        if not request.is_json:
            raise APIError("Content-Type must be application/json", 400)

@api_bp.after_request
def after_request(response):
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # CORS headers (configure as needed)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE'
    
    return response
```

### Input Validation
```python
# api/validators.py
from marshmallow import Schema, fields, validate

class CreateKeySchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    key = fields.Str(required=True, validate=validate.Length(min=1))
    category_id = fields.Str(required=False)
    metadata = fields.Dict(required=False)

# Usage in endpoint:
@api_bp.route('/v1/keys', methods=['POST'])
@jwt_required()
def create_key():
    schema = CreateKeySchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        raise APIError("Invalid input", 400, err.messages)
```

---

## Database Schema Updates

### New Tables/Columns
```sql
-- API Access Logs
CREATE TABLE api_access_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    key_id INTEGER REFERENCES api_keys(id),
    action VARCHAR(50),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API Tokens (for refresh tokens)
CREATE TABLE api_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    token_hash VARCHAR(256) UNIQUE,
    expires_at TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add columns to existing tables
ALTER TABLE api_keys ADD COLUMN metadata JSONB DEFAULT '{}';
ALTER TABLE api_keys ADD COLUMN expires_at TIMESTAMP;
ALTER TABLE api_keys ADD COLUMN last_accessed TIMESTAMP;

ALTER TABLE users ADD COLUMN api_key_limit INTEGER DEFAULT 10;
ALTER TABLE users ADD COLUMN subscription_tier VARCHAR(20) DEFAULT 'free';
```

---

## SDK Development

### Python SDK Example
```python
# apikeywallet-python/src/apikeywallet/client.py
import requests
from typing import Optional, Dict, List

class APIKeyWallet:
    def __init__(self, api_key: str, base_url: str = "https://api.apikeywallet.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def list_keys(self, category: Optional[str] = None) -> List[Dict]:
        params = {}
        if category:
            params["category_id"] = category
        
        response = self.session.get(f"{self.base_url}/v1/keys", params=params)
        response.raise_for_status()
        return response.json()["keys"]
    
    def create_key(self, name: str, key: str, **kwargs) -> Dict:
        data = {"name": name, "key": key, **kwargs}
        response = self.session.post(f"{self.base_url}/v1/keys", json=data)
        response.raise_for_status()
        return response.json()
    
    def get_key(self, key_id: str) -> str:
        response = self.session.get(f"{self.base_url}/v1/keys/{key_id}")
        response.raise_for_status()
        return response.json()["key"]
```

---

## Testing Strategy

### Unit Tests
```python
# tests/test_api_keys.py
import pytest
from app import app
from models import User, APIKey

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client):
    # Create test user and get token
    response = client.post('/v1/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    response = client.post('/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_create_key(client, auth_headers):
    response = client.post('/v1/keys', 
        headers=auth_headers,
        json={
            'name': 'Test Key',
            'key': 'test_secret_key_123'
        }
    )
    
    assert response.status_code == 201
    assert response.json['name'] == 'Test Key'
    assert 'id' in response.json
```

---

## Migration Path

### Phase 1: API Foundation (Week 1-2)
1. Set up API blueprint structure
2. Implement JWT authentication
3. Add error handling and logging
4. Create first endpoints (auth + keys list)

### Phase 2: Full CRUD (Week 3)
1. Complete all CRUD endpoints
2. Add input validation
3. Implement rate limiting
4. Add API access logging

### Phase 3: Advanced Features (Week 4)
1. Add search functionality
2. Implement metadata support
3. Add key expiration
4. Create usage analytics

### Phase 4: Production Ready (Week 5-6)
1. Comprehensive testing
2. API documentation (OpenAPI)
3. SDK development
4. Performance optimization

---

## Security Considerations

1. **API Key Security**
   - Use separate API keys from stored keys
   - Implement key rotation
   - Add IP whitelisting option

2. **Rate Limiting**
   - Per-endpoint limits
   - User-based quotas
   - DDoS protection

3. **Audit Trail**
   - Log all API access
   - Track key usage
   - Monitor suspicious activity

4. **Data Encryption**
   - Encrypt API keys in database
   - Use TLS for all connections
   - Implement field-level encryption

---

## Deployment Considerations

1. **Infrastructure**
   - Use AWS/GCP load balancers
   - Implement auto-scaling
   - Set up Redis for caching
   - Use CDN for static assets

2. **Monitoring**
   - APM with DataDog/NewRelic
   - Custom metrics dashboard
   - Alert on anomalies
   - Track API performance

3. **Documentation**
   - Interactive API docs (Swagger UI)
   - Code examples
   - Postman collection
   - Video tutorials

This implementation plan provides a solid foundation for transforming API Key Wallet into a production-ready SaaS platform.