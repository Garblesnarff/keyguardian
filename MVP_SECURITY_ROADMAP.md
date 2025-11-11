# KeyGuardian API Key Wallet - Secure MVP Roadmap

**Document Version:** 1.0
**Created:** 2025-11-11
**Target Completion:** 6-8 weeks
**Current Status:** Functional Prototype → Secure MVP

---

## 🚨 **CRITICAL SECURITY ALERT**

**STATUS: IMMEDIATE ACTION REQUIRED**

Your `.env` file containing:
- Database password: `Ld7au7ld7au7!`
- Encryption key: `1-hhfn0oML76BI5vV_RfizBN11Kg5srq6PthetLde1U=`

Has been committed to git and is in your repository history. This is a **CRITICAL SECURITY BREACH**.

---

## **Phase 0: EMERGENCY SECURITY TRIAGE** ⚠️
**Priority:** CRITICAL
**Timeline:** DO NOW (30 minutes)
**Cannot proceed to other phases until complete**

### Task 0.1: Assess Exposure Scope
- [ ] **0.1.1** Check if repository is public on GitHub
  ```bash
  git -C /home/user/keyguardian remote -v
  curl -s https://api.github.com/repos/Garblesnarff/apikeywallet | jq '.private'
  ```
- [ ] **0.1.2** Document exposure timeline (when was .env first committed?)
  ```bash
  git log --all --full-history --diff-filter=A -- "apikeywallet-main/.env"
  ```
- [ ] **0.1.3** Check if encryption key or database credentials appear in any other files
  ```bash
  cd /home/user/keyguardian
  grep -r "1-hhfn0oML76BI5vV_RfizBN11Kg5srq6PthetLde1U=" . --exclude-dir=venv
  grep -r "Ld7au7ld7au7" . --exclude-dir=venv
  ```

### Task 0.2: Immediate Containment
- [ ] **0.2.1** Create `.gitignore` file at repository root
  ```bash
  # Create /home/user/keyguardian/.gitignore with:
  .env
  *.env
  .env.*
  apikeywallet-main/.env
  venv/
  .venv/
  __pycache__/
  *.pyc
  *.pyo
  *.pyd
  .Python
  instance/
  .pytest_cache/
  .coverage
  htmlcov/
  dist/
  build/
  *.egg-info/
  *.db
  *.sqlite
  *.sqlite3
  .DS_Store
  .idea/
  .vscode/
  ```
- [ ] **0.2.2** Remove `.env` from git tracking (keep local file)
  ```bash
  git rm --cached apikeywallet-main/.env
  git commit -m "security: Remove .env from tracking"
  ```
- [ ] **0.2.3** If repo is public: Make it private immediately via GitHub settings

### Task 0.3: Credential Rotation
- [ ] **0.3.1** Generate new encryption key
  ```python
  from cryptography.fernet import Fernet
  new_key = Fernet.generate_key()
  print(new_key.decode())
  ```
- [ ] **0.3.2** Change database password
  ```sql
  ALTER USER wonky WITH PASSWORD 'NEW_STRONG_PASSWORD_HERE';
  ```
- [ ] **0.3.3** Generate new Flask SECRET_KEY
  ```python
  import secrets
  print(secrets.token_hex(32))
  ```
- [ ] **0.3.4** Update `.env` file with new credentials
- [ ] **0.3.5** **CRITICAL:** Re-encrypt all existing API keys with new encryption key
  - Create migration script
  - Decrypt with old key
  - Encrypt with new key
  - Update database

### Task 0.4: Git History Cleanup
- [ ] **0.4.1** Install git-filter-repo
  ```bash
  pip install git-filter-repo
  ```
- [ ] **0.4.2** Remove `.env` from entire git history
  ```bash
  cd /home/user/keyguardian
  git filter-repo --path apikeywallet-main/.env --invert-paths
  ```
- [ ] **0.4.3** Force push to remote (ONLY after making repo private)
  ```bash
  git push origin --force --all
  git push origin --force --tags
  ```
- [ ] **0.4.4** Notify all collaborators to re-clone repository

### Task 0.5: Create Environment Template
- [ ] **0.5.1** Create `.env.example` file (safe to commit)
  ```bash
  DATABASE_URL=postgresql://username:password@localhost:5432/dbname
  ENCRYPTION_KEY=generate_with_fernet_generate_key
  SECRET_KEY=generate_with_secrets_token_hex_32
  FLASK_ENV=development
  FLASK_DEBUG=False
  ```
- [ ] **0.5.2** Add setup instructions to README.md
- [ ] **0.5.3** Commit `.env.example` and `.gitignore`

**CHECKPOINT:** Do not proceed until Phase 0 is complete and credentials are rotated.

---

## **Phase 1: IMMEDIATE SECURITY FIXES** 🔐
**Priority:** HIGH
**Timeline:** Week 1 (5-7 days)
**Goal:** Fix critical vulnerabilities that expose users to immediate risk

### Task 1.1: Delete Duplicate Code
**Rationale:** `routes.py` is a 360-line duplicate causing maintenance issues

- [ ] **1.1.1** Verify `routes.py` is not imported anywhere
  ```bash
  grep -r "from routes import" apikeywallet-main/
  grep -r "import routes" apikeywallet-main/
  ```
- [ ] **1.1.2** Back up file (just in case)
  ```bash
  cp apikeywallet-main/routes.py apikeywallet-main/routes.py.backup
  ```
- [ ] **1.1.3** Delete file
  ```bash
  git rm apikeywallet-main/routes.py
  ```
- [ ] **1.1.4** Test application still works
  ```bash
  cd apikeywallet-main && python app.py
  # Visit http://localhost:5000 and test login/add key
  ```
- [ ] **1.1.5** Commit deletion
  ```bash
  git commit -m "refactor: Remove duplicate routes.py file"
  ```

### Task 1.2: Implement Rate Limiting
**Rationale:** Prevent brute force attacks on login endpoint

- [ ] **1.2.1** Add Flask-Limiter to dependencies
  ```bash
  # Add to pyproject.toml dependencies:
  "flask-limiter>=3.5.0"
  ```
- [ ] **1.2.2** Install dependency
  ```bash
  cd apikeywallet-main && pip install flask-limiter
  ```
- [ ] **1.2.3** Create `apikeywallet-main/extensions.py`
  ```python
  from flask_limiter import Limiter
  from flask_limiter.util import get_remote_address

  limiter = Limiter(
      key_func=get_remote_address,
      default_limits=["200 per day", "50 per hour"],
      storage_uri="memory://"
  )
  ```
- [ ] **1.2.4** Initialize limiter in `app.py`
  ```python
  # Add after line 53 (after db, migrate, login_manager)
  from extensions import limiter
  limiter.init_app(app)
  ```
- [ ] **1.2.5** Apply strict limits to auth routes
  ```python
  # In auth_routes.py, add decorator:
  @auth.route('/login', methods=['GET', 'POST'])
  @limiter.limit("5 per minute")  # Max 5 attempts per minute
  def login():
      ...

  @auth.route('/register', methods=['GET', 'POST'])
  @limiter.limit("3 per hour")  # Max 3 registrations per hour per IP
  def register():
      ...
  ```
- [ ] **1.2.6** Apply limits to sensitive key operations
  ```python
  # In wallet_routes.py:
  @main.route('/copy_key/<int:key_id>', methods=['POST'])
  @login_required
  @limiter.limit("30 per minute")  # Prevent rapid key exfiltration
  def copy_key(key_id):
      ...
  ```
- [ ] **1.2.7** Test rate limiting works
  - Make 6 login attempts quickly → should block 6th
  - Wait 60 seconds → should allow again
- [ ] **1.2.8** Add user-friendly error messages
  ```python
  @app.errorhandler(429)
  def ratelimit_handler(e):
      return jsonify({
          'error': 'Rate limit exceeded. Please try again later.',
          'retry_after': e.description
      }), 429
  ```
- [ ] **1.2.9** Document rate limits in API documentation

### Task 1.3: Disable Debug Mode
**Rationale:** Debug logs expose sensitive data (SQL queries, decrypted keys)

- [ ] **1.3.1** Create `apikeywallet-main/config.py`
  ```python
  import os
  from urllib.parse import urlparse

  class Config:
      SECRET_KEY = os.environ.get('SECRET_KEY')
      SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
      SQLALCHEMY_TRACK_MODIFICATIONS = False
      SQLALCHEMY_ECHO = False  # Disable SQL logging

  class DevelopmentConfig(Config):
      DEBUG = True
      SQLALCHEMY_ECHO = True  # Only in dev

  class TestingConfig(Config):
      TESTING = True
      SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
      WTF_CSRF_ENABLED = False

  class ProductionConfig(Config):
      DEBUG = False
      SQLALCHEMY_ECHO = False
      SESSION_COOKIE_SECURE = True
      SESSION_COOKIE_HTTPONLY = True
      SESSION_COOKIE_SAMESITE = 'Lax'
      PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

  config = {
      'development': DevelopmentConfig,
      'testing': TestingConfig,
      'production': ProductionConfig,
      'default': DevelopmentConfig
  }
  ```
- [ ] **1.3.2** Update `app.py` to use config classes
  ```python
  # Replace lines 58-62 with:
  from config import config

  config_name = os.environ.get('FLASK_ENV', 'development')
  app.config.from_object(config[config_name])
  ```
- [ ] **1.3.3** Update logging configuration in `app.py`
  ```python
  # Replace line 45 with:
  log_level = logging.INFO if config_name == 'production' else logging.DEBUG
  logging.basicConfig(level=log_level)
  ```
- [ ] **1.3.4** Remove debug logging from `utils.py` (lines 73-76)
  ```python
  # Replace logging.debug() calls with:
  logger.info(f'Decrypting key for user')  # No actual key data
  ```
- [ ] **1.3.5** Add `FLASK_ENV=production` to production `.env`
- [ ] **1.3.6** Test in production mode
  ```bash
  export FLASK_ENV=production
  python app.py
  # Verify no SQL queries logged
  ```

### Task 1.4: Fix Session Management
**Rationale:** Sessions never expire; SECRET_KEY changes on restart

- [ ] **1.4.1** Remove `os.urandom(24)` fallback from `app.py:59`
  ```python
  # Change from:
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
  # To:
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
  if not app.config['SECRET_KEY']:
      raise ValueError("SECRET_KEY environment variable is required")
  ```
- [ ] **1.4.2** Configure session timeout in `ProductionConfig`
  ```python
  PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
  SESSION_REFRESH_EACH_REQUEST = True
  ```
- [ ] **1.4.3** Mark sessions as permanent on login
  ```python
  # In auth_routes.py login() after line 105:
  from flask import session
  session.permanent = True
  login_user(user)
  ```
- [ ] **1.4.4** Add session security headers in `ProductionConfig`
  ```python
  SESSION_COOKIE_SECURE = True  # HTTPS only
  SESSION_COOKIE_HTTPONLY = True  # No JS access
  SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
  ```
- [ ] **1.4.5** Test session timeout
  - Login
  - Wait 31 minutes
  - Try to access /wallet → should redirect to login

### Task 1.5: Strengthen Password Policy
**Rationale:** Current policy only requires 8 characters

- [ ] **1.5.1** Create password validator in `utils.py`
  ```python
  import re

  def validate_password_strength(password):
      """
      Validate password meets security requirements.

      Requirements:
      - At least 12 characters
      - At least one uppercase letter
      - At least one lowercase letter
      - At least one digit
      - At least one special character

      Returns:
          tuple: (is_valid, error_message)
      """
      if len(password) < 12:
          return False, "Password must be at least 12 characters long"
      if not re.search(r'[A-Z]', password):
          return False, "Password must contain at least one uppercase letter"
      if not re.search(r'[a-z]', password):
          return False, "Password must contain at least one lowercase letter"
      if not re.search(r'\d', password):
          return False, "Password must contain at least one digit"
      if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
          return False, "Password must contain at least one special character"
      return True, None
  ```
- [ ] **1.5.2** Create custom WTForms validator in `forms.py`
  ```python
  from wtforms import ValidationError
  from utils import validate_password_strength

  def password_complexity(form, field):
      is_valid, error_msg = validate_password_strength(field.data)
      if not is_valid:
          raise ValidationError(error_msg)
  ```
- [ ] **1.5.3** Update `RegistrationForm` in `forms.py`
  ```python
  # Change line 34:
  password = PasswordField('Password', validators=[
      DataRequired(),
      Length(min=12, max=128),
      password_complexity
  ])
  ```
- [ ] **1.5.4** Add password strength indicator to registration template
  ```html
  <!-- In templates/register.html, add after password field: -->
  <div id="password-strength" class="password-strength">
      <div class="strength-meter"></div>
      <div class="strength-text">Password strength: <span></span></div>
  </div>
  ```
- [ ] **1.5.5** Add JavaScript password strength checker
  ```javascript
  // In static/js/main.js (create if doesn't exist)
  function checkPasswordStrength(password) {
      let strength = 0;
      if (password.length >= 12) strength++;
      if (/[a-z]/.test(password)) strength++;
      if (/[A-Z]/.test(password)) strength++;
      if (/[0-9]/.test(password)) strength++;
      if (/[^a-zA-Z0-9]/.test(password)) strength++;

      const levels = ['Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
      return { score: strength, level: levels[Math.min(strength, 4)] };
  }
  ```
- [ ] **1.5.6** Update user-facing documentation with new requirements

### Task 1.6: Add Audit Logging
**Rationale:** Need to track who accessed which keys when

- [ ] **1.6.1** Create audit log model in `models.py`
  ```python
  class AuditLog(db.Model):
      """
      Audit log for tracking sensitive operations.

      Attributes:
          id (int): Primary key
          user_id (int): User who performed action
          action (str): Action type (e.g., 'KEY_ACCESSED', 'KEY_CREATED')
          resource_type (str): Type of resource (e.g., 'APIKey', 'Category')
          resource_id (int): ID of affected resource
          ip_address (str): IP address of request
          user_agent (str): Browser user agent
          timestamp (datetime): When action occurred
          details (str): Additional JSON details
      """
      id = db.Column(db.Integer, primary_key=True)
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
      action = db.Column(db.String(50), nullable=False)
      resource_type = db.Column(db.String(50), nullable=False)
      resource_id = db.Column(db.Integer, nullable=True)
      ip_address = db.Column(db.String(45), nullable=True)
      user_agent = db.Column(db.String(256), nullable=True)
      timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
      details = db.Column(db.Text, nullable=True)

      def __repr__(self):
          return f'<AuditLog {self.action} by User {self.user_id}>'
  ```
- [ ] **1.6.2** Create audit logging utility in `utils.py`
  ```python
  from flask import request
  import json

  def log_audit_event(user_id, action, resource_type, resource_id=None, details=None):
      """
      Log an audit event.

      Args:
          user_id (int): User ID
          action (str): Action type
          resource_type (str): Resource type
          resource_id (int, optional): Resource ID
          details (dict, optional): Additional details
      """
      from models import AuditLog
      from app import db

      audit_entry = AuditLog(
          user_id=user_id,
          action=action,
          resource_type=resource_type,
          resource_id=resource_id,
          ip_address=request.remote_addr,
          user_agent=request.headers.get('User-Agent'),
          details=json.dumps(details) if details else None
      )
      db.session.add(audit_entry)
      db.session.commit()
  ```
- [ ] **1.6.3** Add audit logging to sensitive operations
  ```python
  # In wallet_routes.py copy_key():
  from utils import log_audit_event

  @main.route('/copy_key/<int:key_id>', methods=['POST'])
  @login_required
  def copy_key(key_id):
      api_key = APIKey.query.filter_by(id=key_id, user_id=current_user.id).first()
      if not api_key:
          return jsonify({'error': 'API key not found'}), 403

      # Add audit log BEFORE decrypting
      log_audit_event(
          user_id=current_user.id,
          action='KEY_ACCESSED',
          resource_type='APIKey',
          resource_id=key_id,
          details={'key_name': api_key.key_name}
      )

      decrypted_key = decrypt_key(api_key.encrypted_key)
      return jsonify({'key': decrypted_key})
  ```
- [ ] **1.6.4** Add audit logging to other operations
  - `add_key()` → 'KEY_CREATED'
  - `delete_key()` → 'KEY_DELETED'
  - `edit_key()` → 'KEY_MODIFIED'
  - `login()` → 'USER_LOGIN'
  - `logout()` → 'USER_LOGOUT'
  - `register()` → 'USER_REGISTERED'
- [ ] **1.6.5** Create database migration
  ```bash
  cd apikeywallet-main
  flask db migrate -m "Add audit log table"
  flask db upgrade
  ```
- [ ] **1.6.6** Create audit log viewing route (admin only)
  ```python
  # In wallet_routes.py:
  @main.route('/audit_logs')
  @login_required
  def view_audit_logs():
      if not current_user.is_admin:
          flash('Unauthorized', 'danger')
          return redirect(url_for('main.wallet'))

      logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
      return render_template('audit_logs.html', logs=logs)
  ```
- [ ] **1.6.7** Create audit log template (basic table view)

---

## **Phase 2: TESTING INFRASTRUCTURE** 🧪
**Priority:** HIGH
**Timeline:** Week 2 (5-7 days)
**Goal:** Establish automated testing to prevent regressions

### Task 2.1: Set Up Testing Framework
- [ ] **2.1.1** Create test directory structure
  ```bash
  mkdir -p apikeywallet-main/tests/{unit,integration,security}
  touch apikeywallet-main/tests/__init__.py
  touch apikeywallet-main/tests/conftest.py
  ```
- [ ] **2.1.2** Add testing dependencies to `pyproject.toml`
  ```python
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  python_classes = ["Test*"]
  python_functions = ["test_*"]
  addopts = "-v --cov=. --cov-report=html --cov-report=term"

  # Add to dependencies:
  "pytest>=8.0.0",
  "pytest-cov>=4.1.0",
  "pytest-flask>=1.3.0",
  ```
- [ ] **2.1.3** Install testing dependencies
  ```bash
  cd apikeywallet-main && pip install pytest pytest-cov pytest-flask
  ```
- [ ] **2.1.4** Create pytest configuration in `conftest.py`
  ```python
  import pytest
  from app import app as flask_app, db
  from models import User, APIKey, Category
  from config import config

  @pytest.fixture
  def app():
      """Create application for testing."""
      flask_app.config.from_object(config['testing'])

      with flask_app.app_context():
          db.create_all()
          yield flask_app
          db.session.remove()
          db.drop_all()

  @pytest.fixture
  def client(app):
      """Create test client."""
      return app.test_client()

  @pytest.fixture
  def runner(app):
      """Create CLI test runner."""
      return app.test_cli_runner()

  @pytest.fixture
  def auth_client(client):
      """Create authenticated test client."""
      # Register and login test user
      client.post('/register', data={
          'email': 'test@example.com',
          'password': 'TestPassword123!',
          'confirm_password': 'TestPassword123!'
      })
      client.post('/login', data={
          'email': 'test@example.com',
          'password': 'TestPassword123!'
      })
      return client
  ```

### Task 2.2: Write Unit Tests
- [ ] **2.2.1** Create `tests/unit/test_models.py`
  ```python
  def test_user_password_hashing(app):
      """Test password hashing works correctly."""
      with app.app_context():
          user = User(email='test@example.com')
          user.set_password('SecurePass123!')

          assert user.password_hash is not None
          assert user.password_hash != 'SecurePass123!'
          assert user.check_password('SecurePass123!')
          assert not user.check_password('WrongPassword')

  def test_apikey_creation(app):
      """Test API key can be created with encryption."""
      with app.app_context():
          user = User(email='test@example.com')
          user.set_password('Password123!')
          db.session.add(user)
          db.session.commit()

          from utils import encrypt_key
          encrypted = encrypt_key('sk-test-key-12345')

          api_key = APIKey(
              user_id=user.id,
              key_name='Test Key',
              encrypted_key=encrypted
          )
          db.session.add(api_key)
          db.session.commit()

          assert api_key.id is not None
          assert api_key.key_name == 'Test Key'
  ```
- [ ] **2.2.2** Create `tests/unit/test_utils.py`
  ```python
  from utils import encrypt_key, decrypt_key, validate_password_strength

  def test_encryption_decryption():
      """Test encryption and decryption work correctly."""
      original = "sk-test-api-key-12345"
      encrypted = encrypt_key(original)
      decrypted = decrypt_key(encrypted)

      assert encrypted != original
      assert decrypted == original

  def test_password_strength_validator():
      """Test password strength validation."""
      # Should fail
      assert not validate_password_strength('short')[0]
      assert not validate_password_strength('nocapitals123!')[0]
      assert not validate_password_strength('NOLOWERCASE123!')[0]
      assert not validate_password_strength('NoNumbers!')[0]
      assert not validate_password_strength('NoSpecials123')[0]

      # Should pass
      assert validate_password_strength('SecurePass123!')[0]
  ```
- [ ] **2.2.3** Create `tests/unit/test_forms.py`
  ```python
  from forms import RegistrationForm, LoginForm, AddAPIKeyForm

  def test_registration_form_validation(app):
      """Test registration form validates correctly."""
      with app.app_context():
          # Valid form
          form = RegistrationForm(data={
              'email': 'test@example.com',
              'password': 'SecurePass123!',
              'confirm_password': 'SecurePass123!'
          })
          assert form.validate()

          # Invalid email
          form = RegistrationForm(data={
              'email': 'invalid-email',
              'password': 'SecurePass123!',
              'confirm_password': 'SecurePass123!'
          })
          assert not form.validate()

          # Password mismatch
          form = RegistrationForm(data={
              'email': 'test@example.com',
              'password': 'SecurePass123!',
              'confirm_password': 'DifferentPass123!'
          })
          assert not form.validate()
  ```

### Task 2.3: Write Integration Tests
- [ ] **2.3.1** Create `tests/integration/test_auth.py`
  ```python
  def test_registration_flow(client):
      """Test user registration flow."""
      response = client.post('/register', data={
          'email': 'newuser@example.com',
          'password': 'SecurePass123!',
          'confirm_password': 'SecurePass123!'
      }, follow_redirects=True)

      assert response.status_code == 200
      assert b'Registration successful' in response.data

  def test_login_logout_flow(client):
      """Test login and logout flow."""
      # Register user
      client.post('/register', data={
          'email': 'user@example.com',
          'password': 'SecurePass123!',
          'confirm_password': 'SecurePass123!'
      })

      # Login
      response = client.post('/login', data={
          'email': 'user@example.com',
          'password': 'SecurePass123!'
      }, follow_redirects=True)
      assert response.status_code == 200

      # Logout
      response = client.get('/logout', follow_redirects=True)
      assert b'logged out' in response.data.lower()

  def test_login_rate_limiting(client):
      """Test rate limiting on login endpoint."""
      # Register user
      client.post('/register', data={
          'email': 'user@example.com',
          'password': 'SecurePass123!',
          'confirm_password': 'SecurePass123!'
      })

      # Make 6 rapid login attempts
      for i in range(6):
          response = client.post('/login', data={
              'email': 'user@example.com',
              'password': 'WrongPassword'
          })

          if i < 5:
              assert response.status_code != 429
          else:
              assert response.status_code == 429  # Rate limited
  ```
- [ ] **2.3.2** Create `tests/integration/test_wallet.py`
  ```python
  def test_add_key_flow(auth_client):
      """Test adding an API key."""
      response = auth_client.post('/add_key', data={
          'key_name': 'OpenAI',
          'api_key': 'sk-test-key-12345',
          'category': 0
      }, follow_redirects=True)

      assert response.status_code == 200
      assert b'OpenAI' in response.data

  def test_copy_key_requires_auth(client):
      """Test copying key requires authentication."""
      response = client.post('/copy_key/1')
      assert response.status_code == 302  # Redirect to login

  def test_copy_key_authorization(auth_client, app):
      """Test users can only copy their own keys."""
      with app.app_context():
          # Add key for auth_client user
          auth_client.post('/add_key', data={
              'key_name': 'My Key',
              'api_key': 'sk-my-key',
              'category': 0
          })

          # Create another user and their key
          from models import User, APIKey
          from utils import encrypt_key
          other_user = User(email='other@example.com')
          other_user.set_password('Pass123!')
          db.session.add(other_user)
          db.session.commit()

          other_key = APIKey(
              user_id=other_user.id,
              key_name='Other Key',
              encrypted_key=encrypt_key('sk-other-key')
          )
          db.session.add(other_key)
          db.session.commit()

          # Try to access other user's key
          response = auth_client.post(f'/copy_key/{other_key.id}')
          assert response.status_code == 403
  ```
- [ ] **2.3.3** Create `tests/integration/test_categories.py`
  ```python
  def test_category_crud(auth_client):
      """Test category create, read, update, delete."""
      # Create
      response = auth_client.post('/add_category', data={
          'name': 'AI Services'
      }, follow_redirects=True)
      assert b'AI Services' in response.data

      # Read (via manage_categories)
      response = auth_client.get('/manage_categories')
      assert b'AI Services' in response.data

      # Update
      response = auth_client.post('/edit_category/1', data={
          'name': 'ML Services'
      }, follow_redirects=True)
      assert b'ML Services' in response.data

      # Delete
      response = auth_client.post('/delete_category/1', follow_redirects=True)
      assert b'ML Services' not in response.data
  ```

### Task 2.4: Write Security Tests
- [ ] **2.4.1** Create `tests/security/test_vulnerabilities.py`
  ```python
  def test_sql_injection_prevention(auth_client):
      """Test SQL injection is prevented."""
      # Try SQL injection in key_name
      response = auth_client.post('/add_key', data={
          'key_name': "'; DROP TABLE api_key; --",
          'api_key': 'sk-test-key',
          'category': 0
      })
      # Should not crash, key name should be escaped
      assert response.status_code in [200, 302]

  def test_xss_prevention(auth_client):
      """Test XSS is prevented in user inputs."""
      # Try XSS in key_name
      response = auth_client.post('/add_key', data={
          'key_name': '<script>alert("XSS")</script>',
          'api_key': 'sk-test-key',
          'category': 0
      }, follow_redirects=True)

      # Script should be escaped in output
      assert b'&lt;script&gt;' in response.data or b'<script>' not in response.data

  def test_csrf_protection(client):
      """Test CSRF protection is enabled."""
      # Register and login
      client.post('/register', data={
          'email': 'test@example.com',
          'password': 'SecurePass123!',
          'confirm_password': 'SecurePass123!'
      })
      client.post('/login', data={
          'email': 'test@example.com',
          'password': 'SecurePass123!'
      })

      # Try to add key without CSRF token
      with client.session_transaction() as sess:
          # Remove CSRF token from session
          if 'csrf_token' in sess:
              del sess['csrf_token']

      response = client.post('/add_key', data={
          'key_name': 'Test',
          'api_key': 'sk-test',
          'category': 0
      })
      # Should fail without CSRF token
      assert response.status_code == 400 or b'CSRF' in response.data

  def test_encryption_key_isolation(app):
      """Test encrypted keys cannot be decrypted without proper key."""
      from cryptography.fernet import Fernet, InvalidToken
      from utils import decrypt_key, encrypt_key

      # Encrypt with correct key
      encrypted = encrypt_key('sk-test-key')

      # Try to decrypt with wrong key
      wrong_fernet = Fernet(Fernet.generate_key())
      with pytest.raises(InvalidToken):
          wrong_fernet.decrypt(encrypted.encode())
  ```
- [ ] **2.4.2** Create `tests/security/test_authentication.py`
  ```python
  def test_unauthorized_access_blocked(client):
      """Test unauthorized users cannot access protected routes."""
      protected_routes = [
          '/wallet',
          '/add_key',
          '/manage_categories',
          '/audit_logs'
      ]

      for route in protected_routes:
          response = client.get(route)
          assert response.status_code == 302  # Redirect to login

  def test_session_timeout(auth_client, app):
      """Test sessions expire after inactivity."""
      # This test requires time manipulation
      # Implementation depends on testing strategy
      pass  # TODO: Implement with freezegun or similar
  ```

### Task 2.5: Set Up Coverage Reporting
- [ ] **2.5.1** Run tests with coverage
  ```bash
  cd apikeywallet-main
  pytest --cov=. --cov-report=html --cov-report=term
  ```
- [ ] **2.5.2** Review coverage report
  ```bash
  open htmlcov/index.html
  ```
- [ ] **2.5.3** Add coverage badge to README
- [ ] **2.5.4** Set minimum coverage threshold in `.coveragerc`
  ```ini
  [run]
  omit =
      */tests/*
      */venv/*
      */migrations/*

  [report]
  fail_under = 70
  ```
- [ ] **2.5.5** Add pre-commit hook to run tests
  ```bash
  # Create .git/hooks/pre-commit
  #!/bin/bash
  cd apikeywallet-main
  pytest --cov=. --cov-report=term --cov-fail-under=70
  ```

---

## **Phase 3: PRODUCTION HARDENING** 🛡️
**Priority:** MEDIUM-HIGH
**Timeline:** Week 3-4 (10-14 days)
**Goal:** Make application production-ready

### Task 3.1: HTTPS Enforcement
- [ ] **3.1.1** Add Flask-Talisman for security headers
  ```bash
  pip install flask-talisman
  ```
- [ ] **3.1.2** Initialize Talisman in `app.py`
  ```python
  from flask_talisman import Talisman

  # After app creation, before routes:
  if not app.config.get('TESTING'):
      Talisman(app,
          force_https=True,
          strict_transport_security=True,
          strict_transport_security_max_age=31536000,
          content_security_policy={
              'default-src': "'self'",
              'script-src': "'self' 'unsafe-inline'",
              'style-src': "'self' 'unsafe-inline'"
          }
      )
  ```
- [ ] **3.1.3** Configure reverse proxy (nginx/Apache) for SSL termination
  ```nginx
  # nginx.conf example
  server {
      listen 80;
      server_name keyguardian.yourdomain.com;
      return 301 https://$server_name$request_uri;
  }

  server {
      listen 443 ssl http2;
      server_name keyguardian.yourdomain.com;

      ssl_certificate /etc/letsencrypt/live/keyguardian.yourdomain.com/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/keyguardian.yourdomain.com/privkey.pem;

      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers HIGH:!aNULL:!MD5;

      location / {
          proxy_pass http://127.0.0.1:5000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }
  ```
- [ ] **3.1.4** Obtain SSL certificate (Let's Encrypt)
  ```bash
  sudo certbot --nginx -d keyguardian.yourdomain.com
  ```
- [ ] **3.1.5** Test HTTPS configuration
  - Visit https://www.ssllabs.com/ssltest/
  - Run: `curl -I https://keyguardian.yourdomain.com`

### Task 3.2: Database Security
- [ ] **3.2.1** Enable PostgreSQL SSL connections
  ```python
  # In config.py:
  class ProductionConfig(Config):
      SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') + '?sslmode=require'
  ```
- [ ] **3.2.2** Create dedicated database user with minimal permissions
  ```sql
  -- As postgres superuser:
  CREATE USER keyguardian_app WITH PASSWORD 'strong_random_password';
  GRANT CONNECT ON DATABASE keyguardian TO keyguardian_app;
  GRANT USAGE ON SCHEMA public TO keyguardian_app;
  GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO keyguardian_app;
  GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO keyguardian_app;
  ```
- [ ] **3.2.3** Implement connection pooling
  ```python
  # In app.py:
  app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
      'pool_size': 10,
      'pool_recycle': 3600,
      'pool_pre_ping': True
  }
  ```
- [ ] **3.2.4** Set up automated database backups
  ```bash
  # Create backup script: /usr/local/bin/backup_keyguardian.sh
  #!/bin/bash
  BACKUP_DIR="/var/backups/keyguardian"
  DATE=$(date +%Y%m%d_%H%M%S)
  BACKUP_FILE="$BACKUP_DIR/keyguardian_$DATE.sql.gz"

  mkdir -p $BACKUP_DIR
  pg_dump -U keyguardian_app keyguardian | gzip > $BACKUP_FILE

  # Keep only last 30 days
  find $BACKUP_DIR -name "keyguardian_*.sql.gz" -mtime +30 -delete

  # Encrypt backup
  gpg --encrypt --recipient admin@yourdomain.com $BACKUP_FILE
  rm $BACKUP_FILE
  ```
- [ ] **3.2.5** Add backup script to crontab
  ```bash
  # Run daily at 2 AM
  0 2 * * * /usr/local/bin/backup_keyguardian.sh
  ```
- [ ] **3.2.6** Test backup restoration process

### Task 3.3: Secrets Management
- [ ] **3.3.1** Evaluate secrets management solutions
  - Option A: AWS Secrets Manager
  - Option B: HashiCorp Vault
  - Option C: Azure Key Vault
  - Option D: Environment variables + encrypted config
- [ ] **3.3.2** Implement chosen solution (example: AWS Secrets Manager)
  ```python
  # Create secrets_manager.py
  import boto3
  import json
  from botocore.exceptions import ClientError

  def get_secret(secret_name):
      """Retrieve secret from AWS Secrets Manager."""
      session = boto3.session.Session()
      client = session.client(
          service_name='secretsmanager',
          region_name='us-east-1'
      )

      try:
          response = client.get_secret_value(SecretId=secret_name)
          return json.loads(response['SecretString'])
      except ClientError as e:
          raise Exception(f"Failed to retrieve secret: {e}")
  ```
- [ ] **3.3.3** Update config to use secrets manager
  ```python
  # In config.py:
  if os.environ.get('USE_SECRETS_MANAGER') == 'true':
      from secrets_manager import get_secret
      secrets = get_secret('keyguardian/production')
      SECRET_KEY = secrets['SECRET_KEY']
      DATABASE_URL = secrets['DATABASE_URL']
      ENCRYPTION_KEY = secrets['ENCRYPTION_KEY']
  else:
      SECRET_KEY = os.environ.get('SECRET_KEY')
      DATABASE_URL = os.environ.get('DATABASE_URL')
      ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
  ```
- [ ] **3.3.4** Store secrets in AWS Secrets Manager
  ```bash
  aws secretsmanager create-secret \
      --name keyguardian/production \
      --description "KeyGuardian production secrets" \
      --secret-string '{
          "SECRET_KEY": "your-secret-key-here",
          "DATABASE_URL": "postgresql://...",
          "ENCRYPTION_KEY": "your-fernet-key-here"
      }'
  ```
- [ ] **3.3.5** Update deployment to use secrets manager
- [ ] **3.3.6** Document secrets rotation procedure

### Task 3.4: Error Handling and Monitoring
- [ ] **3.4.1** Set up error tracking (Sentry)
  ```bash
  pip install sentry-sdk[flask]
  ```
- [ ] **3.4.2** Initialize Sentry in `app.py`
  ```python
  import sentry_sdk
  from sentry_sdk.integrations.flask import FlaskIntegration

  if config_name == 'production':
      sentry_sdk.init(
          dsn=os.environ.get('SENTRY_DSN'),
          integrations=[FlaskIntegration()],
          traces_sample_rate=0.1,
          environment='production'
      )
  ```
- [ ] **3.4.3** Create custom error pages
  ```python
  # In app.py:
  @app.errorhandler(404)
  def not_found(error):
      return render_template('errors/404.html'), 404

  @app.errorhandler(500)
  def internal_error(error):
      db.session.rollback()
      return render_template('errors/500.html'), 500

  @app.errorhandler(403)
  def forbidden(error):
      return render_template('errors/403.html'), 403
  ```
- [ ] **3.4.4** Create error templates in `templates/errors/`
- [ ] **3.4.5** Set up application monitoring (New Relic/DataDog)
- [ ] **3.4.6** Configure alerts for:
  - Error rate spike (>10 errors/minute)
  - High response time (>2 seconds p95)
  - Database connection failures
  - Failed login attempts (>50/minute)

### Task 3.5: Logging Infrastructure
- [ ] **3.5.1** Configure structured logging
  ```python
  # Create logging_config.py
  import logging
  import json
  from datetime import datetime

  class JSONFormatter(logging.Formatter):
      """Format logs as JSON for easier parsing."""
      def format(self, record):
          log_data = {
              'timestamp': datetime.utcnow().isoformat(),
              'level': record.levelname,
              'message': record.getMessage(),
              'module': record.module,
              'function': record.funcName,
              'line': record.lineno
          }

          if hasattr(record, 'user_id'):
              log_data['user_id'] = record.user_id
          if hasattr(record, 'request_id'):
              log_data['request_id'] = record.request_id

          return json.dumps(log_data)

  def setup_logging(app):
      """Configure application logging."""
      handler = logging.StreamHandler()
      handler.setFormatter(JSONFormatter())

      app.logger.addHandler(handler)
      app.logger.setLevel(logging.INFO)
  ```
- [ ] **3.5.2** Add request ID tracking
  ```python
  # In app.py:
  import uuid

  @app.before_request
  def before_request():
      g.request_id = str(uuid.uuid4())

  @app.after_request
  def after_request(response):
      logger.info('Request completed', extra={
          'request_id': g.request_id,
          'method': request.method,
          'path': request.path,
          'status': response.status_code,
          'user_id': current_user.id if current_user.is_authenticated else None
      })
      return response
  ```
- [ ] **3.5.3** Set up log aggregation (ELK Stack/CloudWatch Logs)
- [ ] **3.5.4** Create log retention policy (90 days)

### Task 3.6: Performance Optimization
- [ ] **3.6.1** Add database indexes
  ```python
  # In models.py:
  class APIKey(db.Model):
      # Add indexes for common queries
      __table_args__ = (
          db.Index('idx_apikey_user_category', 'user_id', 'category_id'),
          db.Index('idx_apikey_user_name', 'user_id', 'key_name'),
      )

  class AuditLog(db.Model):
      __table_args__ = (
          db.Index('idx_audit_user_timestamp', 'user_id', 'timestamp'),
          db.Index('idx_audit_action_timestamp', 'action', 'timestamp'),
      )
  ```
- [ ] **3.6.2** Create migration for indexes
  ```bash
  flask db migrate -m "Add performance indexes"
  flask db upgrade
  ```
- [ ] **3.6.3** Implement query result caching (Flask-Caching)
  ```bash
  pip install Flask-Caching
  ```
  ```python
  from flask_caching import Cache

  cache = Cache(app, config={
      'CACHE_TYPE': 'redis',
      'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
  })

  @main.route('/wallet')
  @login_required
  @cache.memoize(timeout=60)  # Cache for 60 seconds
  def wallet(category_id=None):
      # ... existing code
  ```
- [ ] **3.6.4** Optimize API key decryption (only when needed)
  - Remove decrypt_key() from list views
  - Only decrypt on explicit copy/view action
- [ ] **3.6.5** Add response compression
  ```python
  from flask_compress import Compress
  Compress(app)
  ```
- [ ] **3.6.6** Run load testing
  ```bash
  pip install locust

  # Create locustfile.py for load testing
  from locust import HttpUser, task, between

  class KeyGuardianUser(HttpUser):
      wait_time = between(1, 3)

      def on_start(self):
          """Login before tests."""
          self.client.post("/login", {
              "email": "test@example.com",
              "password": "TestPassword123!"
          })

      @task(3)
      def view_wallet(self):
          self.client.get("/wallet")

      @task(1)
      def add_key(self):
          self.client.post("/add_key", {
              "key_name": "Test Key",
              "api_key": "sk-test-key",
              "category": 0
          })
  ```
- [ ] **3.6.7** Run load test and optimize bottlenecks
  ```bash
  locust -f locustfile.py --host=http://localhost:5000
  ```

---

## **Phase 4: ADDITIONAL SECURITY FEATURES** 🔒
**Priority:** MEDIUM
**Timeline:** Week 5-6 (10-14 days)
**Goal:** Add nice-to-have security enhancements

### Task 4.1: Multi-Factor Authentication (MFA)
- [ ] **4.1.1** Add pyotp for TOTP generation
  ```bash
  pip install pyotp qrcode[pil]
  ```
- [ ] **4.1.2** Add MFA fields to User model
  ```python
  # In models.py:
  class User(UserMixin, db.Model):
      # Add after line 55:
      mfa_enabled = db.Column(db.Boolean, default=False, nullable=False)
      mfa_secret = db.Column(db.String(32), nullable=True)
      backup_codes = db.Column(db.Text, nullable=True)  # JSON array
  ```
- [ ] **4.1.3** Create migration for MFA columns
- [ ] **4.1.4** Create MFA setup route
  ```python
  @auth.route('/setup_mfa', methods=['GET', 'POST'])
  @login_required
  def setup_mfa():
      if request.method == 'GET':
          # Generate secret
          secret = pyotp.random_base32()
          current_user.mfa_secret = secret
          db.session.commit()

          # Generate QR code
          totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
              name=current_user.email,
              issuer_name='KeyGuardian'
          )

          import qrcode
          from io import BytesIO
          import base64

          qr = qrcode.make(totp_uri)
          buffer = BytesIO()
          qr.save(buffer, format='PNG')
          qr_code = base64.b64encode(buffer.getvalue()).decode()

          return render_template('setup_mfa.html', qr_code=qr_code, secret=secret)

      # POST: Verify setup
      code = request.form.get('code')
      totp = pyotp.TOTP(current_user.mfa_secret)

      if totp.verify(code, valid_window=1):
          current_user.mfa_enabled = True

          # Generate backup codes
          backup_codes = [secrets.token_hex(4) for _ in range(10)]
          current_user.backup_codes = json.dumps(backup_codes)
          db.session.commit()

          flash('MFA enabled successfully. Save your backup codes!', 'success')
          return render_template('mfa_backup_codes.html', codes=backup_codes)
      else:
          flash('Invalid code. Please try again.', 'danger')
          return redirect(url_for('auth.setup_mfa'))
  ```
- [ ] **4.1.5** Update login flow to check MFA
  ```python
  # In auth_routes.py login():
  if user and user.check_password(password):
      if user.mfa_enabled:
          # Store user ID in session temporarily
          session['mfa_user_id'] = user.id
          return redirect(url_for('auth.verify_mfa'))
      else:
          login_user(user)
          return redirect(url_for('main.wallet'))
  ```
- [ ] **4.1.6** Create MFA verification route
  ```python
  @auth.route('/verify_mfa', methods=['GET', 'POST'])
  def verify_mfa():
      user_id = session.get('mfa_user_id')
      if not user_id:
          return redirect(url_for('auth.login'))

      user = User.query.get(user_id)

      if request.method == 'POST':
          code = request.form.get('code')
          totp = pyotp.TOTP(user.mfa_secret)

          if totp.verify(code, valid_window=1):
              login_user(user)
              session.pop('mfa_user_id', None)
              return redirect(url_for('main.wallet'))
          else:
              # Check backup codes
              backup_codes = json.loads(user.backup_codes or '[]')
              if code in backup_codes:
                  backup_codes.remove(code)
                  user.backup_codes = json.dumps(backup_codes)
                  db.session.commit()

                  login_user(user)
                  session.pop('mfa_user_id', None)
                  flash('Backup code used. Please generate new codes.', 'warning')
                  return redirect(url_for('main.wallet'))

              flash('Invalid code.', 'danger')

      return render_template('verify_mfa.html')
  ```
- [ ] **4.1.7** Create MFA templates
- [ ] **4.1.8** Add "Disable MFA" functionality
- [ ] **4.1.9** Add MFA tests

### Task 4.2: Key Rotation Support
- [ ] **4.2.1** Create key rotation utility
  ```python
  # In utils.py:
  def rotate_encryption_key(old_key_str, new_key_str):
      """
      Rotate encryption key for all API keys.

      Args:
          old_key_str: Old Fernet key
          new_key_str: New Fernet key

      Returns:
          tuple: (success_count, failure_count)
      """
      from models import APIKey
      from app import db
      from cryptography.fernet import Fernet

      old_fernet = Fernet(old_key_str.encode())
      new_fernet = Fernet(new_key_str.encode())

      api_keys = APIKey.query.all()
      success = 0
      failure = 0

      for key in api_keys:
          try:
              # Decrypt with old key
              decrypted = old_fernet.decrypt(key.encrypted_key.encode())

              # Encrypt with new key
              key.encrypted_key = new_fernet.encrypt(decrypted).decode()
              success += 1
          except Exception as e:
              logger.error(f"Failed to rotate key {key.id}: {e}")
              failure += 1

      db.session.commit()
      return success, failure
  ```
- [ ] **4.2.2** Create CLI command for rotation
  ```python
  # In app.py:
  @app.cli.command()
  @click.option('--old-key', required=True, help='Old encryption key')
  @click.option('--new-key', required=True, help='New encryption key')
  def rotate_keys(old_key, new_key):
      """Rotate encryption keys for all API keys."""
      from utils import rotate_encryption_key

      click.echo('Starting key rotation...')
      success, failure = rotate_encryption_key(old_key, new_key)

      click.echo(f'Rotation complete: {success} succeeded, {failure} failed')

      if failure == 0:
          click.echo('Update ENCRYPTION_KEY in your .env file to:')
          click.echo(new_key)
      else:
          click.echo('WARNING: Some keys failed to rotate. Do not update .env yet!')
  ```
- [ ] **4.2.3** Document rotation procedure
- [ ] **4.2.4** Create rotation schedule (every 90 days)
- [ ] **4.2.5** Add automated reminders for rotation

### Task 4.3: Account Security Features
- [ ] **4.3.1** Add password change functionality
  ```python
  @auth.route('/change_password', methods=['GET', 'POST'])
  @login_required
  def change_password():
      form = ChangePasswordForm()
      if form.validate_on_submit():
          if not current_user.check_password(form.current_password.data):
              flash('Current password is incorrect.', 'danger')
              return render_template('change_password.html', form=form)

          current_user.set_password(form.new_password.data)
          db.session.commit()

          # Log audit event
          log_audit_event(
              user_id=current_user.id,
              action='PASSWORD_CHANGED',
              resource_type='User',
              resource_id=current_user.id
          )

          flash('Password changed successfully.', 'success')
          return redirect(url_for('main.wallet'))

      return render_template('change_password.html', form=form)
  ```
- [ ] **4.3.2** Add email verification on registration
  ```python
  # Add to User model:
  email_verified = db.Column(db.Boolean, default=False)
  email_verification_token = db.Column(db.String(100), nullable=True)

  # Add route:
  @auth.route('/verify_email/<token>')
  def verify_email(token):
      user = User.query.filter_by(email_verification_token=token).first()
      if user:
          user.email_verified = True
          user.email_verification_token = None
          db.session.commit()
          flash('Email verified successfully!', 'success')
      else:
          flash('Invalid verification token.', 'danger')
      return redirect(url_for('auth.login'))
  ```
- [ ] **4.3.3** Add password reset functionality
  ```python
  from itsdangerous import URLSafeTimedSerializer

  @auth.route('/forgot_password', methods=['GET', 'POST'])
  def forgot_password():
      if request.method == 'POST':
          email = request.form.get('email')
          user = User.query.filter_by(email=email).first()

          if user:
              # Generate reset token
              s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
              token = s.dumps(user.email, salt='password-reset')

              # Send email (implement email sending)
              send_password_reset_email(user.email, token)

          # Always show success (don't leak user existence)
          flash('If that email exists, a reset link has been sent.', 'info')
          return redirect(url_for('auth.login'))

      return render_template('forgot_password.html')

  @auth.route('/reset_password/<token>', methods=['GET', 'POST'])
  def reset_password(token):
      try:
          s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
          email = s.loads(token, salt='password-reset', max_age=3600)  # 1 hour
      except:
          flash('Invalid or expired reset link.', 'danger')
          return redirect(url_for('auth.login'))

      user = User.query.filter_by(email=email).first()

      if request.method == 'POST':
          password = request.form.get('password')
          user.set_password(password)
          db.session.commit()

          flash('Password reset successfully.', 'success')
          return redirect(url_for('auth.login'))

      return render_template('reset_password.html')
  ```
- [ ] **4.3.4** Add account deletion
  ```python
  @auth.route('/delete_account', methods=['POST'])
  @login_required
  def delete_account():
      password = request.form.get('password')

      if not current_user.check_password(password):
          flash('Incorrect password.', 'danger')
          return redirect(url_for('main.settings'))

      # Delete user data
      APIKey.query.filter_by(user_id=current_user.id).delete()
      Category.query.filter_by(user_id=current_user.id).delete()
      AuditLog.query.filter_by(user_id=current_user.id).delete()

      user_id = current_user.id
      logout_user()

      User.query.filter_by(id=user_id).delete()
      db.session.commit()

      flash('Your account has been deleted.', 'info')
      return redirect(url_for('main.index'))
  ```
- [ ] **4.3.5** Add session management page
  - Show active sessions
  - Allow revocation of other sessions
- [ ] **4.3.6** Add login notifications (email on new login)

### Task 4.4: Export/Import Functionality
- [ ] **4.4.1** Create export endpoint
  ```python
  @main.route('/export_keys')
  @login_required
  def export_keys():
      """Export all API keys (encrypted) as JSON."""
      api_keys = APIKey.query.filter_by(user_id=current_user.id).all()
      categories = Category.query.filter_by(user_id=current_user.id).all()

      export_data = {
          'version': '1.0',
          'exported_at': datetime.utcnow().isoformat(),
          'user_email': current_user.email,
          'categories': [
              {'id': c.id, 'name': c.name}
              for c in categories
          ],
          'api_keys': [
              {
                  'key_name': k.key_name,
                  'encrypted_key': k.encrypted_key,
                  'category_id': k.category_id,
                  'date_added': k.date_added.isoformat()
              }
              for k in api_keys
          ]
      }

      # Log export event
      log_audit_event(
          user_id=current_user.id,
          action='KEYS_EXPORTED',
          resource_type='APIKey',
          details={'key_count': len(api_keys)}
      )

      response = jsonify(export_data)
      response.headers['Content-Disposition'] = f'attachment; filename=keyguardian_export_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json'
      return response
  ```
- [ ] **4.4.2** Create import endpoint
  ```python
  @main.route('/import_keys', methods=['GET', 'POST'])
  @login_required
  def import_keys():
      if request.method == 'POST':
          file = request.files.get('file')
          if not file:
              flash('No file uploaded.', 'danger')
              return redirect(url_for('main.import_keys'))

          try:
              import_data = json.load(file)

              # Validate format
              if import_data.get('version') != '1.0':
                  flash('Unsupported export version.', 'danger')
                  return redirect(url_for('main.import_keys'))

              # Create categories
              category_map = {}
              for cat_data in import_data['categories']:
                  existing = Category.query.filter_by(
                      user_id=current_user.id,
                      name=cat_data['name']
                  ).first()

                  if existing:
                      category_map[cat_data['id']] = existing.id
                  else:
                      new_cat = Category(name=cat_data['name'], user_id=current_user.id)
                      db.session.add(new_cat)
                      db.session.flush()
                      category_map[cat_data['id']] = new_cat.id

              # Import keys
              imported_count = 0
              for key_data in import_data['api_keys']:
                  # Check for duplicates
                  existing = APIKey.query.filter_by(
                      user_id=current_user.id,
                      key_name=key_data['key_name']
                  ).first()

                  if not existing:
                      new_key = APIKey(
                          user_id=current_user.id,
                          key_name=key_data['key_name'],
                          encrypted_key=key_data['encrypted_key'],
                          category_id=category_map.get(key_data['category_id'])
                      )
                      db.session.add(new_key)
                      imported_count += 1

              db.session.commit()

              # Log import event
              log_audit_event(
                  user_id=current_user.id,
                  action='KEYS_IMPORTED',
                  resource_type='APIKey',
                  details={'key_count': imported_count}
              )

              flash(f'Successfully imported {imported_count} keys.', 'success')
              return redirect(url_for('main.wallet'))

          except Exception as e:
              db.session.rollback()
              logger.error(f'Import failed: {e}')
              flash('Import failed. Please check file format.', 'danger')

      return render_template('import_keys.html')
  ```
- [ ] **4.4.3** Add import/export to UI
- [ ] **4.4.4** Document import/export format
- [ ] **4.4.5** Add tests for import/export

---

## **Phase 5: DEPLOYMENT & CI/CD** 🚀
**Priority:** MEDIUM
**Timeline:** Week 7 (5-7 days)
**Goal:** Automate deployment and establish DevOps practices

### Task 5.1: Containerization
- [ ] **5.1.1** Create production Dockerfile
  ```dockerfile
  # apikeywallet-main/Dockerfile
  FROM python:3.12-slim

  # Set working directory
  WORKDIR /app

  # Install system dependencies
  RUN apt-get update && apt-get install -y \
      postgresql-client \
      && rm -rf /var/lib/apt/lists/*

  # Copy requirements
  COPY pyproject.toml uv.lock ./

  # Install Python dependencies
  RUN pip install --no-cache-dir uv && \
      uv pip install --system -r pyproject.toml

  # Copy application code
  COPY . .

  # Create non-root user
  RUN useradd -m -u 1000 appuser && \
      chown -R appuser:appuser /app
  USER appuser

  # Expose port
  EXPOSE 5000

  # Run application
  CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
  ```
- [ ] **5.1.2** Create docker-compose.yml for local development
  ```yaml
  version: '3.8'

  services:
    web:
      build: ./apikeywallet-main
      ports:
        - "5000:5000"
      environment:
        - FLASK_ENV=development
        - DATABASE_URL=postgresql://keyguardian:password@db:5432/keyguardian
        - ENCRYPTION_KEY=${ENCRYPTION_KEY}
        - SECRET_KEY=${SECRET_KEY}
      depends_on:
        - db
        - redis
      volumes:
        - ./apikeywallet-main:/app

    db:
      image: postgres:15-alpine
      environment:
        - POSTGRES_USER=keyguardian
        - POSTGRES_PASSWORD=password
        - POSTGRES_DB=keyguardian
      volumes:
        - postgres_data:/var/lib/postgresql/data
      ports:
        - "5432:5432"

    redis:
      image: redis:7-alpine
      ports:
        - "6379:6379"

  volumes:
    postgres_data:
  ```
- [ ] **5.1.3** Add .dockerignore
  ```
  .git
  .gitignore
  .env
  __pycache__
  *.pyc
  venv/
  .venv/
  tests/
  htmlcov/
  .coverage
  ```
- [ ] **5.1.4** Test Docker build
  ```bash
  docker-compose build
  docker-compose up -d
  docker-compose logs -f
  ```
- [ ] **5.1.5** Add health check endpoint
  ```python
  @app.route('/health')
  def health():
      """Health check endpoint for container orchestration."""
      try:
          # Check database connection
          db.session.execute('SELECT 1')
          return jsonify({'status': 'healthy', 'database': 'connected'}), 200
      except Exception as e:
          return jsonify({'status': 'unhealthy', 'error': str(e)}), 503
  ```

### Task 5.2: CI/CD Pipeline
- [ ] **5.2.1** Create GitHub Actions workflow
  ```yaml
  # .github/workflows/ci.yml
  name: CI/CD Pipeline

  on:
    push:
      branches: [main, develop]
    pull_request:
      branches: [main]

  jobs:
    test:
      runs-on: ubuntu-latest

      services:
        postgres:
          image: postgres:15
          env:
            POSTGRES_USER: test
            POSTGRES_PASSWORD: test
            POSTGRES_DB: test_keyguardian
          options: >-
            --health-cmd pg_isready
            --health-interval 10s
            --health-timeout 5s
            --health-retries 5
          ports:
            - 5432:5432

      steps:
        - uses: actions/checkout@v3

        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.12'

        - name: Install dependencies
          run: |
            cd apikeywallet-main
            pip install -r requirements.txt
            pip install pytest pytest-cov

        - name: Run tests
          env:
            DATABASE_URL: postgresql://test:test@localhost:5432/test_keyguardian
            ENCRYPTION_KEY: ${{ secrets.TEST_ENCRYPTION_KEY }}
            SECRET_KEY: test-secret-key
            FLASK_ENV: testing
          run: |
            cd apikeywallet-main
            pytest --cov=. --cov-report=xml --cov-report=term

        - name: Upload coverage
          uses: codecov/codecov-action@v3
          with:
            file: ./apikeywallet-main/coverage.xml

        - name: Run security scan
          run: |
            pip install bandit safety
            cd apikeywallet-main
            bandit -r . -f json -o bandit-report.json || true
            safety check --json || true

        - name: Lint code
          run: |
            pip install flake8 black
            cd apikeywallet-main
            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
            black --check .

    build:
      needs: test
      runs-on: ubuntu-latest
      if: github.ref == 'refs/heads/main'

      steps:
        - uses: actions/checkout@v3

        - name: Set up Docker Buildx
          uses: docker/setup-buildx-action@v2

        - name: Login to Container Registry
          uses: docker/login-action@v2
          with:
            registry: ghcr.io
            username: ${{ github.actor }}
            password: ${{ secrets.GITHUB_TOKEN }}

        - name: Build and push
          uses: docker/build-push-action@v4
          with:
            context: ./apikeywallet-main
            push: true
            tags: ghcr.io/${{ github.repository }}/keyguardian:latest
            cache-from: type=gha
            cache-to: type=gha,mode=max

    deploy:
      needs: build
      runs-on: ubuntu-latest
      if: github.ref == 'refs/heads/main'

      steps:
        - name: Deploy to production
          # Add your deployment steps here
          # e.g., SSH to server, pull image, restart container
          run: echo "Deploy to production"
  ```
- [ ] **5.2.2** Add secrets to GitHub repository
  - `TEST_ENCRYPTION_KEY`
  - `PRODUCTION_ENCRYPTION_KEY`
  - `SENTRY_DSN`
  - Deployment credentials
- [ ] **5.2.3** Create deployment script
  ```bash
  #!/bin/bash
  # deploy.sh

  set -e

  echo "Pulling latest image..."
  docker pull ghcr.io/yourusername/keyguardian:latest

  echo "Running database migrations..."
  docker-compose run --rm web flask db upgrade

  echo "Restarting containers..."
  docker-compose up -d --no-deps web

  echo "Checking health..."
  sleep 5
  curl -f http://localhost:5000/health || exit 1

  echo "Deployment complete!"
  ```
- [ ] **5.2.4** Set up automatic backups before deployment
- [ ] **5.2.5** Configure rollback procedure

### Task 5.3: Infrastructure as Code
- [ ] **5.3.1** Create Terraform configuration (if using cloud)
  ```hcl
  # terraform/main.tf
  terraform {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"
      }
    }
  }

  provider "aws" {
    region = "us-east-1"
  }

  resource "aws_db_instance" "keyguardian" {
    identifier           = "keyguardian-db"
    engine              = "postgres"
    engine_version      = "15.3"
    instance_class      = "db.t3.micro"
    allocated_storage   = 20
    storage_encrypted   = true

    db_name  = "keyguardian"
    username = "admin"
    password = var.db_password

    backup_retention_period = 7
    backup_window          = "03:00-04:00"
    maintenance_window     = "sun:04:00-sun:05:00"

    skip_final_snapshot = false
    final_snapshot_identifier = "keyguardian-final-snapshot"
  }

  resource "aws_ecs_cluster" "keyguardian" {
    name = "keyguardian-cluster"
  }

  # Add more resources as needed...
  ```
- [ ] **5.3.2** Document infrastructure setup
- [ ] **5.3.3** Create disaster recovery plan

---

## **Phase 6: DOCUMENTATION & LAUNCH PREP** 📚
**Priority:** MEDIUM
**Timeline:** Week 8 (3-5 days)
**Goal:** Finalize documentation and prepare for launch

### Task 6.1: User Documentation
- [ ] **6.1.1** Update README.md
  ```markdown
  # KeyGuardian - Secure API Key Wallet

  ## Features
  - Encrypted storage of API keys
  - Category-based organization
  - Multi-factor authentication
  - Audit logging
  - Import/export functionality

  ## Quick Start
  ...

  ## Security
  ...

  ## Development
  ...
  ```
- [ ] **6.1.2** Create user guide
  - Getting started
  - Adding your first API key
  - Organizing with categories
  - Enabling MFA
  - Exporting your keys
- [ ] **6.1.3** Create admin guide
  - Installation
  - Configuration
  - Backup and restore
  - Monitoring
  - Troubleshooting
- [ ] **6.1.4** Create API documentation (if exposing APIs)
- [ ] **6.1.5** Add inline help text in UI

### Task 6.2: Security Documentation
- [ ] **6.2.1** Create security policy (SECURITY.md)
  ```markdown
  # Security Policy

  ## Supported Versions
  | Version | Supported          |
  | ------- | ------------------ |
  | 1.0.x   | :white_check_mark: |

  ## Reporting a Vulnerability
  Please report security vulnerabilities to security@yourdomain.com

  ## Security Features
  - Fernet symmetric encryption for API keys
  - Bcrypt password hashing
  - Rate limiting
  - MFA support
  - Audit logging

  ## Best Practices
  ...
  ```
- [ ] **6.2.2** Document threat model
- [ ] **6.2.3** Create incident response plan
- [ ] **6.2.4** Document encryption key management procedures

### Task 6.3: Developer Documentation
- [ ] **6.3.1** Add code comments to complex functions
- [ ] **6.3.2** Create architecture documentation
- [ ] **6.3.3** Document database schema
- [ ] **6.3.4** Create contribution guidelines (CONTRIBUTING.md)
- [ ] **6.3.5** Add code of conduct (CODE_OF_CONDUCT.md)

### Task 6.4: Compliance & Legal
- [ ] **6.4.1** Create privacy policy
- [ ] **6.4.2** Create terms of service
- [ ] **6.4.3** Add cookie consent (if needed)
- [ ] **6.4.4** Document data retention policies
- [ ] **6.4.5** Add GDPR compliance features (if applicable)
  - Data export
  - Data deletion
  - Consent management

### Task 6.5: Pre-Launch Checklist
- [ ] **6.5.1** Run full security audit
  - Penetration testing
  - Vulnerability scanning
  - Code review
- [ ] **6.5.2** Performance testing
  - Load testing
  - Stress testing
  - Verify response times
- [ ] **6.5.3** Browser compatibility testing
  - Chrome, Firefox, Safari, Edge
  - Mobile browsers
- [ ] **6.5.4** Accessibility audit (WCAG compliance)
- [ ] **6.5.5** Set up monitoring dashboards
- [ ] **6.5.6** Configure alerting
- [ ] **6.5.7** Train support team (if applicable)
- [ ] **6.5.8** Create runbook for common issues
- [ ] **6.5.9** Final backup before launch
- [ ] **6.5.10** Launch!

---

## **METRICS & SUCCESS CRITERIA** 📊

### Phase Completion Metrics

**Phase 0 (Emergency):**
- ✅ .env removed from git
- ✅ Credentials rotated
- ✅ No secrets in git history
- ✅ .gitignore properly configured

**Phase 1 (Security Fixes):**
- ✅ Rate limiting functional
- ✅ Debug mode disabled
- ✅ Audit logging captures all sensitive operations
- ✅ Password policy enforced
- ✅ No duplicate code

**Phase 2 (Testing):**
- ✅ Test coverage >70%
- ✅ All critical paths tested
- ✅ Security tests passing
- ✅ CI pipeline green

**Phase 3 (Production Hardening):**
- ✅ HTTPS enforced
- ✅ Database encrypted
- ✅ Backups automated
- ✅ Monitoring operational
- ✅ Error tracking configured

**Phase 4 (Additional Features):**
- ✅ MFA implemented
- ✅ Key rotation functional
- ✅ Export/import working
- ✅ Account security features complete

**Phase 5 (Deployment):**
- ✅ Application containerized
- ✅ CI/CD pipeline functional
- ✅ Deployment automated
- ✅ Rollback procedure tested

**Phase 6 (Documentation):**
- ✅ User documentation complete
- ✅ Security policy published
- ✅ Developer docs available
- ✅ Pre-launch checklist completed

### Overall Success Criteria

**Security:**
- Zero critical vulnerabilities
- No exposed secrets
- All sensitive operations logged
- MFA available for users

**Reliability:**
- 99.9% uptime
- <2 second response time (p95)
- Zero data loss
- Successful backup/restore

**Usability:**
- Intuitive UI
- Clear error messages
- Comprehensive documentation
- Accessible to users with disabilities

**Maintainability:**
- Test coverage >70%
- Code follows style guide
- Clear documentation
- Automated deployments

---

## **EFFORT ESTIMATES** ⏱️

| Phase | Tasks | Estimated Hours | Estimated Days |
|-------|-------|----------------|----------------|
| Phase 0 | 5 | 2-4 | 0.5-1 |
| Phase 1 | 6 | 24-32 | 3-4 |
| Phase 2 | 5 | 32-40 | 4-5 |
| Phase 3 | 6 | 40-56 | 5-7 |
| Phase 4 | 4 | 32-48 | 4-6 |
| Phase 5 | 3 | 24-32 | 3-4 |
| Phase 6 | 5 | 16-24 | 2-3 |
| **Total** | **34** | **170-236** | **21.5-30** |

**Calendar Time:** 6-8 weeks (assuming part-time work, 4-5 hours/day)

---

## **PRIORITY ORDER**

If you need to prioritize due to time constraints:

### MUST HAVE (MVP Blockers):
1. Phase 0 - Emergency Security Triage (ALL tasks)
2. Task 1.1 - Delete duplicate code
3. Task 1.2 - Implement rate limiting
4. Task 1.3 - Disable debug mode
5. Task 1.6 - Add audit logging
6. Task 2.1-2.2 - Basic testing (unit tests)
7. Task 3.1 - HTTPS enforcement
8. Task 3.2 - Database security

### SHOULD HAVE (Launch Readiness):
9. Task 1.4 - Fix session management
10. Task 1.5 - Strengthen password policy
11. Task 2.3 - Integration tests
12. Task 3.3 - Secrets management
13. Task 3.4 - Error handling/monitoring
14. Task 5.1 - Containerization
15. Task 6.1 - User documentation

### NICE TO HAVE (Post-Launch):
16. Task 4.1 - Multi-factor authentication
17. Task 4.2 - Key rotation
18. Task 4.3 - Account security features
19. Task 4.4 - Export/import
20. Task 5.2 - Full CI/CD pipeline
21. Task 6.2-6.5 - Comprehensive documentation

---

## **MAINTENANCE & POST-MVP**

After reaching secure MVP:

### Ongoing Security:
- Monthly dependency updates
- Quarterly security audits
- Regular penetration testing
- Key rotation every 90 days
- Review audit logs weekly

### Feature Roadmap:
- API for programmatic access
- Browser extension
- Mobile application
- Team/organization features
- Advanced key sharing
- Integration with password managers

### Operational Excellence:
- Automated testing on every commit
- Performance monitoring
- User feedback collection
- Regular backup testing
- Disaster recovery drills

---

## **GETTING HELP**

If you get stuck:

1. **Security questions:** Consult OWASP guidelines
2. **Flask questions:** Flask documentation and community
3. **Database questions:** PostgreSQL documentation
4. **Testing questions:** pytest documentation
5. **Deployment questions:** Docker/cloud provider docs

Resources:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- Flask Security: https://flask.palletsprojects.com/en/latest/security/
- Cryptography Best Practices: https://www.keylength.com/

---

**Remember:** Security is not a one-time task. It's an ongoing process. This roadmap gets you to secure MVP, but you'll need to maintain vigilance as the application evolves.

Good luck! 🚀
