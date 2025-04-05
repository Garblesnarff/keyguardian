# KeyGuardian Technical Documentation

---
created: 2025-03-15
project: KeyGuardian
type: technical_documentation
status: in_progress
tags: [documentation, technical, architecture]
---

## 1. System Architecture Overview

KeyGuardian is a secure personal API key management application built with Flask, providing encrypted storage and organization for API keys. The architecture is designed with security as the primary focus, while maintaining an intuitive user experience.

### Core Components

- **Web Application Layer**: Flask application with Jinja2 templates
- **Authentication Layer**: User authentication and session management
- **Encryption Layer**: Secure key encryption and decryption
- **Data Access Layer**: Database models and operations
- **Integration Layer**: OAuth2 implementation for external access

### High-Level Architecture Diagram

```
┌───────────────┐     ┌─────────────────────┐     ┌───────────────────┐
│               │     │                     │     │                   │
│    Browser    │────▶│  Flask Application  │────▶│     Database      │
│               │     │                     │     │                   │
└───────────────┘     └─────────────────────┘     └───────────────────┘
                               │   ▲
                               │   │
                               ▼   │
                      ┌──────────────────────┐
                      │                      │
                      │  Encryption Service  │
                      │                      │
                      └──────────────────────┘
                               │   ▲
                               │   │
                               ▼   │
                      ┌──────────────────────┐
                      │                      │
                      │   OAuth2 Provider    │
                      │                      │
                      └──────────────────────┘
                               │   ▲
                               │   │
                               ▼   │
                      ┌──────────────────────┐
                      │                      │
                      │  Client Applications │
                      │ (e.g. Story Generator)│
                      │                      │
                      └──────────────────────┘
```

## 2. Component Details

### Authentication System

The authentication system manages user accounts, login sessions, and access control.

**Technologies:**
- Flask-Login: Session management and authentication
- Werkzeug: Password hashing
- Flask-WTF: Form validation and CSRF protection

**Key Files:**
- `models.py`: User model definition
- `routes/auth.py`: Authentication routes
- `forms.py`: Login and registration forms
- `templates/auth/`: Authentication templates

**Authentication Flow:**
1. User registers with email and password
2. Password is hashed using Werkzeug's `generate_password_hash`
3. User logs in with credentials
4. Flask-Login creates and manages user session
5. Authentication status is checked for protected routes

### Encryption Service

The encryption service handles secure storage and retrieval of API keys.

**Technologies:**
- cryptography.fernet: Symmetric encryption
- os.urandom: Secure random generation
- base64: Encoding for storage

**Key Files:**
- `utils.py`: Encryption utility functions
- `services/encryption_service.py`: Core encryption logic

**Encryption Process:**
1. Application generates a master encryption key at initialization
2. Each API key is encrypted using Fernet symmetric encryption
3. Encrypted keys are stored in the database
4. Keys are decrypted only when needed and never stored unencrypted

**Key Management:**
- Master encryption key stored as environment variable
- Key is never stored in code or database
- Memory-safe handling of decrypted API keys

### Data Models

The application uses SQLAlchemy ORM with the following primary models:

**User Model:**
```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    api_keys = db.relationship('APIKey', backref='owner', lazy='dynamic')
    categories = db.relationship('Category', backref='owner', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

**API Key Model:**
```python
class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    encrypted_key = db.Column(db.Text, nullable=False)
    service_url = db.Column(db.String(256))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Category Model:**
```python
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    api_keys = db.relationship('APIKey', backref='category', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Routes and Blueprints

The application uses Flask blueprints to organize routes logically:

**Auth Blueprint (`blueprints/auth.py`):**
- `/login`: User login
- `/register`: User registration
- `/logout`: User logout
- `/reset-password`: Password reset functionality

**API Keys Blueprint (`blueprints/keys.py`):**
- `/keys`: List all API keys
- `/keys/add`: Add new API key
- `/keys/<id>`: View single API key
- `/keys/<id>/edit`: Edit API key
- `/keys/<id>/delete`: Delete API key
- `/keys/<id>/copy`: Copy API key to clipboard

**Categories Blueprint (`blueprints/categories.py`):**
- `/categories`: List all categories
- `/categories/add`: Add new category
- `/categories/<id>/edit`: Edit category
- `/categories/<id>/delete`: Delete category

**Main Blueprint (`blueprints/main.py`):**
- `/`: Dashboard/home page
- `/profile`: User profile
- `/settings`: Application settings

**OAuth Blueprint (`blueprints/oauth.py`):**
- `/oauth/authorize`: OAuth2 authorization endpoint
- `/oauth/token`: OAuth2 token endpoint
- `/oauth/revoke`: OAuth2 token revocation

## 3. OAuth2 Implementation

KeyGuardian implements OAuth2 to securely provide API key access to authorized applications like Story Generator.

### OAuth2 Provider Implementation

The OAuth2 provider is implemented using Flask-OAuthlib:

**Key Components:**
- `oauth.py`: OAuth2 provider setup
- `models.py`: OAuth2 client and token models
- `routes/oauth.py`: OAuth2 endpoints

**OAuth2 Models:**
```python
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), unique=True, nullable=False)
    client_secret = db.Column(db.String(55), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)
    
    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []
        
    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []
```

```python
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'), nullable=False)
    client = db.relationship('Client')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    scopes = db.Column(db.Text)
```

### OAuth2 Workflow

1. **Registration of OAuth2 Client**
   - Story Generator (or other client) is registered in KeyGuardian
   - Client receives client_id and client_secret
   - Redirect URIs and scopes are defined

2. **Authorization Flow**
   - Client redirects user to `/oauth/authorize` with appropriate parameters
   - User authenticates and grants permissions
   - KeyGuardian redirects back to client with authorization code
   - Client exchanges authorization code for access token
   - Client uses access token to access API keys

3. **API Key Access via OAuth2**
   - Client makes authenticated request to `/api/keys`
   - KeyGuardian validates token and scopes
   - KeyGuardian returns authorized API keys
   - Decryption occurs only on KeyGuardian server

### Scopes Definition

- `read:keys`: Permission to read API keys
- `read:categories`: Permission to read categories
- `write:keys`: Permission to add or update API keys
- `delete:keys`: Permission to delete API keys
- `write:categories`: Permission to manage categories

## 4. API Endpoints

### Internal API

**API Keys Endpoints:**
```
GET /api/keys
Response: List of API keys with metadata (no actual keys)

GET /api/keys/<id>
Response: Single API key with metadata (no actual key)

POST /api/keys/decrypt/<id>
Request: {"reason": "Reason for access"}
Response: {"key": "Decrypted API key"}
Security: Only accessible via authenticated session or valid OAuth2 token with appropriate scope

POST /api/keys
Request: {"name": "Key name", "key": "API key", "category_id": 1, "description": "Description"}
Response: {"id": 1, "name": "Key name", "success": true}

PUT /api/keys/<id>
Request: {"name": "Updated name", "category_id": 2, "description": "Updated description"}
Response: {"success": true}

DELETE /api/keys/<id>
Response: {"success": true}
```

**Categories Endpoints:**
```
GET /api/categories
Response: List of categories

GET /api/categories/<id>
Response: Single category with associated API keys (metadata only)

POST /api/categories
Request: {"name": "Category name", "description": "Description"}
Response: {"id": 1, "name": "Category name", "success": true}

PUT /api/categories/<id>
Request: {"name": "Updated name", "description": "Updated description"}
Response: {"success": true}

DELETE /api/categories/<id>
Response: {"success": true}
```

### OAuth2 API

```
GET /oauth/api/keys
Header: Authorization: Bearer <token>
Query Parameters: category_id (optional)
Response: List of accessible API keys based on OAuth2 scopes

GET /oauth/api/keys/<id>
Header: Authorization: Bearer <token>
Response: Single API key if authorized

POST /oauth/api/keys/decrypt/<id>
Header: Authorization: Bearer <token>
Request: {"reason": "Reason for access"}
Response: {"key": "Decrypted API key"}
Security: Only accessible with valid OAuth2 token with 'read:keys' scope
```

## 5. Security Considerations

### Authentication Security

- Passwords are hashed using Werkzeug's secure hashing algorithm
- Session cookies are secure and HTTP-only
- CSRF protection enabled for all forms
- Rate limiting on login attempts
- Automatic session timeout after inactivity

### Encryption Security

- API keys encrypted using Fernet symmetric encryption
- Encryption key stored securely as environment variable
- Keys decrypted only when needed and never stored in session
- Memory security practices to avoid leaving decrypted keys in memory

### Application Security

- Input validation on all forms
- Parameterized database queries to prevent SQL injection
- XSS protection via content security policy and proper escaping
- Secure headers configuration
- Regular security updates for dependencies

### OAuth2 Security

- Client secrets properly secured
- Token expiration and refresh mechanism
- Scope-based access control
- PKCE (Proof Key for Code Exchange) for public clients
- State parameter validation to prevent CSRF attacks

## 6. Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    description TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- API Keys table
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    encrypted_key TEXT NOT NULL,
    service_url VARCHAR(256),
    description TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OAuth2 Clients table
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(40) UNIQUE NOT NULL,
    client_secret VARCHAR(55) UNIQUE NOT NULL,
    name VARCHAR(64) NOT NULL,
    description TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    _redirect_uris TEXT,
    _default_scopes TEXT
);

-- OAuth2 Tokens table
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(40) NOT NULL REFERENCES clients(client_id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token_type VARCHAR(40),
    access_token VARCHAR(255) UNIQUE,
    refresh_token VARCHAR(255) UNIQUE,
    expires TIMESTAMP,
    scopes TEXT
);
```

## 7. Frontend Implementation

### UI Framework

- Bootstrap 5 for responsive design
- Custom CSS for branding and specific components
- JavaScript for dynamic interactions

### Key UI Components

1. **Dashboard**
   - Overview of API keys by category
   - Quick access to frequently used keys
   - Recent activity log

2. **API Key Management**
   - List view with filtering and sorting
   - Add/Edit forms
   - Copy to clipboard functionality
   - Secure view key option

3. **Category Management**
   - List/grid view of categories
   - Add/Edit forms
   - Category assignment for keys

4. **Authentication Pages**
   - Login form
   - Registration form
   - Password reset workflow

5. **OAuth Authorization**
   - Permission grant screen
   - Application details display
   - Scope explanation

### Responsive Design Considerations

- Mobile-first approach using Bootstrap breakpoints
- Progressive enhancement for better desktop experiences
- Touch-friendly UI elements for mobile users
- Readable typography and accessible color scheme

## 8. Deployment Considerations

### Development Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL=postgresql://username:password@localhost/keyguardian
export SECRET_KEY=your-secret-key
export ENCRYPTION_KEY=your-encryption-key

# Initialize database
flask db init
flask db migrate
flask db upgrade

# Run development server
flask run
```

### Production Deployment

- **WSGI Server**: Gunicorn for production deployment
- **Database**: PostgreSQL for production data storage
- **Reverse Proxy**: Nginx for handling client connections
- **SSL/TLS**: Required for all production deployments
- **Environment**: Production variables securely managed

### Containerization (Optional)

- Docker container for application
- Docker Compose for local development
- Container orchestration for scaling (Kubernetes, ECS)

### Monitoring and Logging

- Application logging with different log levels
- Error tracking and alerting
- Performance monitoring
- Security event logging

## 9. Testing Strategy

### Unit Testing

- Test encryption/decryption functions
- Test model methods and validations
- Test utility functions
- Mock external dependencies

### Integration Testing

- Test API endpoints
- Test OAuth2 flows
- Test database operations
- Test form submissions

### Security Testing

- Authentication bypass attempts
- Input validation testing
- Encryption verification
- OAuth2 implementation testing

### UI Testing

- Basic user flow testing
- Form validation testing
- Responsive design testing
- Accessibility testing

## 10. Integration with Story Generator

### Integration Architecture

The integration with Story Generator is implemented using OAuth2:

1. **Story Generator Configuration**:
   - Register as OAuth2 client in KeyGuardian
   - Store client credentials securely
   - Implement OAuth2 client flow

2. **User Flow**:
   - User initiates API key access from Story Generator
   - Story Generator redirects to KeyGuardian authorization endpoint
   - User authenticates and grants access
   - KeyGuardian redirects back to Story Generator with authorization code
   - Story Generator exchanges code for access token
   - Story Generator uses token to access API keys

3. **Technical Implementation**:
   - OAuth2 client library in Story Generator
   - Token management and refresh
   - API requests with token authentication
   - Error handling for authentication failures

### API Usage Example

```python
# Story Generator code example
import requests

def get_api_key(key_name, token):
    # Get API key metadata
    response = requests.get(
        'https://keyguardian.example.com/oauth/api/keys',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to get API keys: {response.text}")
    
    # Find the specific key by name
    keys = response.json()
    key_id = None
    for key in keys:
        if key['name'] == key_name:
            key_id = key['id']
            break
    
    if not key_id:
        raise Exception(f"API key '{key_name}' not found")
    
    # Request decryption of the specific key
    decrypt_response = requests.post(
        f'https://keyguardian.example.com/oauth/api/keys/decrypt/{key_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'reason': 'Story generation API access'}
    )
    
    if decrypt_response.status_code != 200:
        raise Exception(f"Failed to decrypt API key: {decrypt_response.text}")
    
    return decrypt_response.json()['key']
```

## 11. Error Handling

### Client-Side Error Handling

- Form validation with immediate feedback
- Error messages for failed operations
- Graceful degradation for JavaScript failures
- Loading indicators for asynchronous operations

### Server-Side Error Handling

- Structured error responses
- Appropriate HTTP status codes
- Detailed error logging
- User-friendly error messages

### Common Error Scenarios

1. **Authentication Failures**
   - Invalid credentials
   - Session timeout
   - Account lockout

2. **Permission Errors**
   - Unauthorized API key access
   - Invalid OAuth2 scopes
   - Cross-user access attempts

3. **Data Validation Errors**
   - Invalid form submissions
   - Duplicate key names
   - Invalid API key formats

4. **System Errors**
   - Database connection issues
   - Encryption failures
   - External service unavailability

## 12. Future Enhancements

### Technical Enhancements

- Automated key rotation
- Multi-factor authentication
- Advanced encryption options
- Audit logging
- Performance optimizations

### Feature Enhancements

- API key usage tracking
- Team sharing and collaboration
- Browser extension for easy access
- Mobile application for on-the-go access
- Advanced search and filtering

### Integration Enhancements

- More granular OAuth2 scopes
- Webhook notifications
- Direct API integration
- CI/CD pipeline integration

## 13. Appendix

### Technology Stack

- **Backend**: Python 3.9+, Flask 2.2+
- **Database**: PostgreSQL 13+, SQLAlchemy 2.0+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login, Werkzeug
- **Forms**: Flask-WTF, WTForms
- **Encryption**: cryptography.fernet
- **OAuth2**: Flask-OAuthlib
- **Testing**: Pytest, Coverage

### Dependency List

```
Flask==2.2.3
Flask-Login==0.6.2
Flask-Migrate==4.0.4
Flask-SQLAlchemy==3.0.3
Flask-WTF==1.1.1
cryptography==39.0.2
psycopg2-binary==2.9.5
SQLAlchemy==2.0.5.post1
Flask-OAuthlib==0.9.6
pytest==7.3.1
coverage==7.2.5
gunicorn==20.1.0
```

### API Reference Documentation

Full API documentation is available at `/docs` within the application or as a downloadable Swagger/OpenAPI specification.

### Security Best Practices

For maintainers and developers, please follow these security best practices:

1. Never commit API keys or secrets to version control
2. Always use environment variables for sensitive configuration
3. Keep dependencies updated
4. Follow the principle of least privilege
5. Conduct regular security reviews
6. Implement proper logging and monitoring

This documentation provides a comprehensive overview of the KeyGuardian application architecture, components, and implementation. It serves as a guide for development, maintenance, and integration with other systems.
