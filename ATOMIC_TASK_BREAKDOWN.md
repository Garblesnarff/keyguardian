# KeyGuardian - Atomic Task Breakdown for Parallel Execution

**Document Version:** 1.0
**Created:** 2025-11-12
**Purpose:** Granular task breakdown optimized for parallel sub-agent execution
**Total Atomic Tasks:** 245+

---

## 📋 **EXECUTION METHODOLOGY**

### Parallel Execution Waves
Tasks are organized into **waves** - each wave contains tasks that can be executed in parallel with no dependencies on each other. Complete all tasks in Wave N before starting Wave N+1.

### Task Format
```
[WAVE-X.Y] Task Name
├─ Dependencies: [List of prerequisite tasks]
├─ Inputs: [Required files, data, or state]
├─ Outputs: [Files created, state changes]
├─ Validation: [How to verify completion]
├─ Time Estimate: X minutes
└─ Can Run In Parallel With: [Other tasks in same wave]
```

---

## 🚨 **PHASE 0: EMERGENCY SECURITY TRIAGE**
**All Phase 0 tasks must complete before ANY other phase**

### WAVE 0.1 - Assessment (Parallel execution possible)

**[0.1.1] Check Repository Visibility**
```bash
# Task ID: SEC-001
# Dependencies: None
# Time: 2 minutes
```
- **Action**: Verify if GitHub repo is public or private
- **Command**:
  ```bash
  cd /home/user/keyguardian
  REPO_URL=$(git remote get-url origin)
  curl -s https://api.github.com/repos/Garblesnarff/keyguardian | jq '.private'
  ```
- **Output**: Boolean - true (private) or false (public)
- **Success**: Know visibility status
- **Parallel With**: [0.1.2], [0.1.3], [0.1.4]

**[0.1.2] Find First .env Commit**
```bash
# Task ID: SEC-002
# Dependencies: None
# Time: 3 minutes
```
- **Action**: Determine when .env was first committed
- **Command**:
  ```bash
  git log --all --full-history --diff-filter=A -- "apikeywallet-main/.env" --pretty=format:"%H %ai %s" | head -1
  ```
- **Output**: Commit hash, date, message
- **Success**: Know exposure timeline
- **Parallel With**: [0.1.1], [0.1.3], [0.1.4]

**[0.1.3] Search for Hardcoded Encryption Key**
```bash
# Task ID: SEC-003
# Dependencies: None
# Time: 5 minutes
```
- **Action**: Find all occurrences of encryption key in codebase
- **Command**:
  ```bash
  cd /home/user/keyguardian
  grep -r "1-hhfn0oML76BI5vV_RfizBN11Kg5srq6PthetLde1U=" . \
    --exclude-dir=venv \
    --exclude-dir=.venv \
    --exclude-dir=node_modules \
    --exclude="*.pyc" > /tmp/key_occurrences.txt
  cat /tmp/key_occurrences.txt
  ```
- **Output**: List of files containing the key
- **Success**: Complete list of exposure points
- **Parallel With**: [0.1.1], [0.1.2], [0.1.4]

**[0.1.4] Search for Hardcoded Database Password**
```bash
# Task ID: SEC-004
# Dependencies: None
# Time: 5 minutes
```
- **Action**: Find all occurrences of DB password
- **Command**:
  ```bash
  cd /home/user/keyguardian
  grep -r "Ld7au7ld7au7" . \
    --exclude-dir=venv \
    --exclude-dir=.venv \
    --exclude-dir=node_modules \
    --exclude="*.pyc" > /tmp/db_pwd_occurrences.txt
  cat /tmp/db_pwd_occurrences.txt
  ```
- **Output**: List of files containing the password
- **Success**: Complete list of exposure points
- **Parallel With**: [0.1.1], [0.1.2], [0.1.3]

**[0.1.5] Check if .env in Any Branch**
```bash
# Task ID: SEC-005
# Dependencies: None
# Time: 3 minutes
```
- **Action**: Check all branches for .env file
- **Command**:
  ```bash
  git log --all --full-history -- "apikeywallet-main/.env" | wc -l
  git log --all --full-history -- "apikeywallet-main/.env" --oneline
  ```
- **Output**: Number of commits touching .env across all branches
- **Success**: Know scope of cleanup needed
- **Parallel With**: [0.1.1], [0.1.2], [0.1.3], [0.1.4]

### WAVE 0.2 - Create .gitignore (Sequential - depends on 0.1)

**[0.2.1] Create .gitignore File**
```bash
# Task ID: SEC-006
# Dependencies: None (but wait for Wave 0.1 to complete)
# Time: 5 minutes
```
- **Action**: Create comprehensive .gitignore
- **Input**: None
- **Output**: `/home/user/keyguardian/.gitignore`
- **Content**:
  ```gitignore
  # Environment files
  .env
  .env.*
  *.env
  !.env.example

  # Python
  __pycache__/
  *.py[cod]
  *$py.class
  *.so
  .Python
  venv/
  .venv/
  ENV/
  env/

  # Flask
  instance/
  .webassets-cache

  # Database
  *.db
  *.sqlite
  *.sqlite3

  # Testing
  .pytest_cache/
  .coverage
  htmlcov/
  .tox/

  # IDE
  .vscode/
  .idea/
  *.swp
  *.swo
  *~
  .DS_Store

  # Build
  dist/
  build/
  *.egg-info/

  # Logs
  *.log
  logs/

  # Secrets
  secrets/
  credentials/
  *.pem
  *.key
  *.cert
  ```
- **Validation**: File exists and contains all patterns
- **Parallel With**: [0.2.2]

**[0.2.2] Create .env.example Template**
```bash
# Task ID: SEC-007
# Dependencies: None
# Time: 3 minutes
```
- **Action**: Create safe environment template
- **Output**: `/home/user/keyguardian/apikeywallet-main/.env.example`
- **Content**:
  ```bash
  # Database Configuration
  DATABASE_URL=postgresql://username:password@localhost:5432/keyguardian

  # Security Keys
  # Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ENCRYPTION_KEY=your_fernet_key_here

  # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
  SECRET_KEY=your_secret_key_here

  # Flask Configuration
  FLASK_ENV=development
  FLASK_DEBUG=False

  # Optional: Monitoring
  SENTRY_DSN=

  # Optional: Redis
  REDIS_URL=redis://localhost:6379/0
  ```
- **Validation**: File created with placeholder values only
- **Parallel With**: [0.2.1]

### WAVE 0.3 - Git Cleanup (Sequential - depends on 0.2)

**[0.3.1] Stop Tracking .env File**
```bash
# Task ID: SEC-008
# Dependencies: [0.2.1], [0.2.2]
# Time: 2 minutes
```
- **Action**: Remove .env from git index
- **Command**:
  ```bash
  cd /home/user/keyguardian
  git rm --cached apikeywallet-main/.env
  ```
- **Output**: .env removed from staging
- **Validation**: `git status` shows .env as untracked
- **Parallel With**: None (sequential)

**[0.3.2] Commit .gitignore and .env.example**
```bash
# Task ID: SEC-009
# Dependencies: [0.3.1]
# Time: 2 minutes
```
- **Action**: Commit safe files
- **Command**:
  ```bash
  git add .gitignore apikeywallet-main/.env.example
  git commit -m "security: Add .gitignore and remove .env from tracking

- Add comprehensive .gitignore covering secrets, Python artifacts, IDE files
- Add .env.example template with safe placeholder values
- Remove .env from git tracking (credentials to be rotated)"
  ```
- **Output**: Commit hash
- **Validation**: Commit exists in git log
- **Parallel With**: None

### WAVE 0.4 - Generate New Credentials (Parallel)

**[0.4.1] Generate New Fernet Encryption Key**
```python
# Task ID: SEC-010
# Dependencies: None
# Time: 1 minute
```
- **Action**: Create new encryption key
- **Command**:
  ```python
  from cryptography.fernet import Fernet
  new_key = Fernet.generate_key()
  print(f"NEW_ENCRYPTION_KEY={new_key.decode()}")
  ```
- **Output**: New Fernet key string
- **Storage**: Store in secure location (password manager, NOT in code)
- **Validation**: Key is 44 characters, base64 encoded
- **Parallel With**: [0.4.2], [0.4.3]

**[0.4.2] Generate New Flask SECRET_KEY**
```python
# Task ID: SEC-011
# Dependencies: None
# Time: 1 minute
```
- **Action**: Create new Flask secret key
- **Command**:
  ```python
  import secrets
  new_secret = secrets.token_hex(32)
  print(f"NEW_SECRET_KEY={new_secret}")
  ```
- **Output**: 64-character hex string
- **Storage**: Store securely
- **Validation**: Key is 64 characters, hexadecimal
- **Parallel With**: [0.4.1], [0.4.3]

**[0.4.3] Generate New Database Password**
```bash
# Task ID: SEC-012
# Dependencies: None
# Time: 1 minute
```
- **Action**: Create strong database password
- **Command**:
  ```python
  import secrets
  import string
  alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
  password = ''.join(secrets.choice(alphabet) for i in range(32))
  print(f"NEW_DB_PASSWORD={password}")
  ```
- **Output**: 32-character random password
- **Storage**: Store securely
- **Validation**: Password is 32+ characters, mixed case, numbers, symbols
- **Parallel With**: [0.4.1], [0.4.2]

### WAVE 0.5 - Database Password Rotation (Sequential)

**[0.5.1] Backup Current Database**
```bash
# Task ID: SEC-013
# Dependencies: None (but wait for Wave 0.4)
# Time: 5 minutes
```
- **Action**: Create database backup before changes
- **Command**:
  ```bash
  pg_dump -U wonky -h localhost keyguardian > /tmp/keyguardian_backup_$(date +%Y%m%d_%H%M%S).sql
  ```
- **Output**: SQL dump file
- **Validation**: File exists and is >0 bytes
- **Parallel With**: None

**[0.5.2] Change PostgreSQL User Password**
```sql
# Task ID: SEC-014
# Dependencies: [0.5.1], [0.4.3]
# Time: 2 minutes
```
- **Action**: Update database user password
- **Command**:
  ```bash
  psql -U wonky -d postgres -c "ALTER USER wonky WITH PASSWORD 'NEW_PASSWORD_HERE';"
  ```
- **Input**: New password from [0.4.3]
- **Output**: Password changed confirmation
- **Validation**: Can connect with new password
- **Parallel With**: None

**[0.5.3] Update .env with New DB Password**
```bash
# Task ID: SEC-015
# Dependencies: [0.5.2]
# Time: 1 minute
```
- **Action**: Update DATABASE_URL in .env
- **Command**: Manual edit of apikeywallet-main/.env
- **New Value**: `postgresql://wonky:NEW_PASSWORD@localhost:5432/keyguardian`
- **Validation**: Application can connect to database
- **Parallel With**: None

### WAVE 0.6 - Re-encrypt All API Keys (Sequential - CRITICAL)

**[0.6.1] Create Re-encryption Script**
```python
# Task ID: SEC-016
# Dependencies: [0.4.1]
# Time: 10 minutes
```
- **Action**: Create script to re-encrypt all keys
- **Output**: `/home/user/keyguardian/scripts/reencrypt_keys.py`
- **Content**:
  ```python
  #!/usr/bin/env python3
  """
  Re-encrypt all API keys with new encryption key.

  Usage:
      python reencrypt_keys.py OLD_KEY NEW_KEY
  """
  import sys
  import os
  from cryptography.fernet import Fernet

  # Add parent directory to path
  sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'apikeywallet-main'))

  from app import app, db
  from models import APIKey

  def reencrypt_all_keys(old_key_str, new_key_str):
      """Re-encrypt all API keys."""
      old_fernet = Fernet(old_key_str.encode())
      new_fernet = Fernet(new_key_str.encode())

      with app.app_context():
          api_keys = APIKey.query.all()
          print(f"Found {len(api_keys)} API keys to re-encrypt")

          success = 0
          failed = 0

          for key in api_keys:
              try:
                  # Decrypt with old key
                  decrypted = old_fernet.decrypt(key.encrypted_key.encode())

                  # Encrypt with new key
                  key.encrypted_key = new_fernet.encrypt(decrypted).decode()
                  success += 1
                  print(f"✓ Re-encrypted key ID {key.id}: {key.key_name}")

              except Exception as e:
                  failed += 1
                  print(f"✗ Failed to re-encrypt key ID {key.id}: {e}")

          if failed == 0:
              db.session.commit()
              print(f"\n✓ SUCCESS: Re-encrypted {success} keys")
              print("You can now update ENCRYPTION_KEY in .env")
              return True
          else:
              db.session.rollback()
              print(f"\n✗ FAILURE: {failed} keys failed. Database rolled back.")
              print("DO NOT update ENCRYPTION_KEY in .env")
              return False

  if __name__ == '__main__':
      if len(sys.argv) != 3:
          print("Usage: python reencrypt_keys.py OLD_KEY NEW_KEY")
          sys.exit(1)

      old_key = sys.argv[1]
      new_key = sys.argv[2]

      confirm = input("This will re-encrypt ALL API keys. Continue? (yes/no): ")
      if confirm.lower() != 'yes':
          print("Aborted")
          sys.exit(0)

      success = reencrypt_all_keys(old_key, new_key)
      sys.exit(0 if success else 1)
  ```
- **Validation**: Script file exists and is executable
- **Parallel With**: None

**[0.6.2] Test Re-encryption Script (Dry Run)**
```bash
# Task ID: SEC-017
# Dependencies: [0.6.1]
# Time: 5 minutes
```
- **Action**: Test script logic without committing
- **Command**:
  ```bash
  cd /home/user/keyguardian
  # Add dry-run mode to script first, then test
  python scripts/reencrypt_keys.py "OLD_KEY" "NEW_KEY" --dry-run
  ```
- **Output**: List of keys that would be re-encrypted
- **Validation**: No errors, counts match expected
- **Parallel With**: None

**[0.6.3] Execute Re-encryption**
```bash
# Task ID: SEC-018
# Dependencies: [0.6.2], [0.4.1]
# Time: 5 minutes
```
- **Action**: Re-encrypt all API keys with new key
- **Command**:
  ```bash
  python scripts/reencrypt_keys.py \
    "1-hhfn0oML76BI5vV_RfizBN11Kg5srq6PthetLde1U=" \
    "NEW_ENCRYPTION_KEY_FROM_0.4.1"
  ```
- **Input**: Old key (current), New key from [0.4.1]
- **Output**: Success count, failure count
- **Validation**: All keys re-encrypted successfully (0 failures)
- **Parallel With**: None

**[0.6.4] Update .env with New Encryption Key**
```bash
# Task ID: SEC-019
# Dependencies: [0.6.3]
# Time: 1 minute
```
- **Action**: Update ENCRYPTION_KEY in .env
- **Command**: Manual edit
- **Validation**: Application can decrypt keys
- **Parallel With**: [0.6.5]

**[0.6.5] Update .env with New Secret Key**
```bash
# Task ID: SEC-020
# Dependencies: [0.4.2]
# Time: 1 minute
```
- **Action**: Update SECRET_KEY in .env
- **Command**: Manual edit
- **Validation**: Application starts without errors
- **Parallel With**: [0.6.4]

**[0.6.6] Test Application with New Keys**
```bash
# Task ID: SEC-021
# Dependencies: [0.6.4], [0.6.5], [0.5.3]
# Time: 5 minutes
```
- **Action**: Verify app works with all new credentials
- **Test Steps**:
  1. Start application: `cd apikeywallet-main && python app.py`
  2. Login with existing user
  3. View wallet (keys should decrypt)
  4. Copy a key (should return decrypted value)
  5. Add a new key (should encrypt with new key)
- **Validation**: All operations succeed
- **Parallel With**: None

### WAVE 0.7 - Git History Cleanup (Sequential)

**[0.7.1] Install git-filter-repo**
```bash
# Task ID: SEC-022
# Dependencies: [0.6.6] (wait until app verified working)
# Time: 3 minutes
```
- **Action**: Install git history rewriting tool
- **Command**:
  ```bash
  pip install git-filter-repo
  ```
- **Validation**: `git-filter-repo --version` works
- **Parallel With**: None

**[0.7.2] Create Repository Backup**
```bash
# Task ID: SEC-023
# Dependencies: [0.7.1]
# Time: 5 minutes
```
- **Action**: Backup entire repository before history rewrite
- **Command**:
  ```bash
  cd /home/user
  tar -czf keyguardian_backup_$(date +%Y%m%d_%H%M%S).tar.gz keyguardian/
  ```
- **Output**: Compressed backup file
- **Validation**: Backup file exists and is >0 bytes
- **Parallel With**: None

**[0.7.3] Remove .env from Git History**
```bash
# Task ID: SEC-024
# Dependencies: [0.7.2]
# Time: 10 minutes
```
- **Action**: Purge .env from all commits
- **Command**:
  ```bash
  cd /home/user/keyguardian
  git filter-repo --path apikeywallet-main/.env --invert-paths --force
  ```
- **Output**: Rewritten git history
- **Validation**: `git log --all -- "apikeywallet-main/.env"` returns nothing
- **Parallel With**: None

**[0.7.4] Verify .env Removed from History**
```bash
# Task ID: SEC-025
# Dependencies: [0.7.3]
# Time: 5 minutes
```
- **Action**: Search entire history for old credentials
- **Command**:
  ```bash
  # Search for old encryption key in all commits
  git log --all -p -S "1-hhfn0oML76BI5vV_RfizBN11Kg5srq6PthetLde1U=" | wc -l
  # Should return 0

  # Search for old DB password
  git log --all -p -S "Ld7au7ld7au7" | wc -l
  # Should return 0
  ```
- **Validation**: Both searches return 0 results
- **Parallel With**: None

**[0.7.5] Force Push to Remote**
```bash
# Task ID: SEC-026
# Dependencies: [0.7.4]
# Time: 5 minutes
```
- **Action**: Overwrite remote history
- **Command**:
  ```bash
  git push origin --force --all
  git push origin --force --tags
  ```
- **Output**: Remote repository updated
- **Validation**: Remote history no longer contains .env
- **⚠️ WARNING**: This will break all other clones
- **Parallel With**: None

**[0.7.6] Document Credential Rotation**
```bash
# Task ID: SEC-027
# Dependencies: [0.7.5]
# Time: 5 minutes
```
- **Action**: Create incident report
- **Output**: `/home/user/keyguardian/SECURITY_INCIDENT_REPORT.md`
- **Content**: Date, what was exposed, actions taken, verification steps
- **Validation**: Report exists and is comprehensive
- **Parallel With**: None

---

## 🔐 **PHASE 1: IMMEDIATE SECURITY FIXES**

### WAVE 1.1 - Code Cleanup (Parallel)

**[1.1.1] Verify routes.py Not Imported**
```bash
# Task ID: CODE-001
# Dependencies: Phase 0 complete
# Time: 3 minutes
```
- **Action**: Search codebase for imports of routes.py
- **Command**:
  ```bash
  cd /home/user/keyguardian/apikeywallet-main
  grep -r "from routes import" . --exclude-dir=venv
  grep -r "import routes" . --exclude-dir=venv
  ```
- **Expected**: No results (file not imported)
- **Validation**: Empty output
- **Parallel With**: [1.1.2]

**[1.1.2] Backup routes.py Before Deletion**
```bash
# Task ID: CODE-002
# Dependencies: None
# Time: 1 minute
```
- **Action**: Create backup copy
- **Command**:
  ```bash
  cp apikeywallet-main/routes.py apikeywallet-main/routes.py.backup_$(date +%Y%m%d)
  ```
- **Output**: Backup file
- **Validation**: Backup exists
- **Parallel With**: [1.1.1]

**[1.1.3] Delete routes.py**
```bash
# Task ID: CODE-003
# Dependencies: [1.1.1], [1.1.2]
# Time: 1 minute
```
- **Action**: Remove duplicate file from git
- **Command**:
  ```bash
  git rm apikeywallet-main/routes.py
  ```
- **Validation**: File staged for deletion
- **Parallel With**: None

**[1.1.4] Test Application Without routes.py**
```bash
# Task ID: CODE-004
# Dependencies: [1.1.3]
# Time: 5 minutes
```
- **Action**: Verify app still works
- **Command**:
  ```bash
  cd apikeywallet-main && python app.py
  ```
- **Tests**:
  - App starts without import errors
  - Can access /login
  - Can access /wallet (after login)
- **Validation**: All routes work
- **Parallel With**: None

**[1.1.5] Commit routes.py Deletion**
```bash
# Task ID: CODE-005
# Dependencies: [1.1.4]
# Time: 2 minutes
```
- **Action**: Commit change
- **Command**:
  ```bash
  git commit -m "refactor: Remove duplicate routes.py file

The routes.py file was a 360-line duplicate of auth_routes.py and
wallet_routes.py combined. These separate files are already imported
in app.py, making routes.py unnecessary and a maintenance burden."
  ```
- **Validation**: Commit exists
- **Parallel With**: None

### WAVE 1.2 - Rate Limiting Setup (Parallel)

**[1.2.1] Add Flask-Limiter Dependency**
```bash
# Task ID: SEC-028
# Dependencies: None
# Time: 2 minutes
```
- **Action**: Update pyproject.toml
- **File**: `apikeywallet-main/pyproject.toml`
- **Change**: Add `"flask-limiter>=3.5.0",` to dependencies array
- **Validation**: Dependency listed in file
- **Parallel With**: [1.2.2]

**[1.2.2] Install Flask-Limiter**
```bash
# Task ID: SEC-029
# Dependencies: [1.2.1]
# Time: 2 minutes
```
- **Action**: Install package
- **Command**:
  ```bash
  cd apikeywallet-main && pip install flask-limiter
  ```
- **Validation**: `pip show flask-limiter` returns package info
- **Parallel With**: None (needs [1.2.1])

**[1.2.3] Create extensions.py File**
```python
# Task ID: SEC-030
# Dependencies: [1.2.2]
# Time: 5 minutes
```
- **Action**: Create extensions module
- **Output**: `apikeywallet-main/extensions.py`
- **Content**:
  ```python
  """
  extensions.py - Flask extension instances

  Centralized initialization of Flask extensions to avoid circular imports.
  """

  from flask_limiter import Limiter
  from flask_limiter.util import get_remote_address

  # Initialize rate limiter
  limiter = Limiter(
      key_func=get_remote_address,
      default_limits=["200 per day", "50 per hour"],
      storage_uri="memory://",
      strategy="fixed-window"
  )
  ```
- **Validation**: File created, valid Python syntax
- **Parallel With**: [1.2.4]

**[1.2.4] Initialize Limiter in app.py**
```python
# Task ID: SEC-031
# Dependencies: [1.2.3]
# Time: 3 minutes
```
- **Action**: Add limiter to app initialization
- **File**: `apikeywallet-main/app.py`
- **Location**: After line 53 (after login_manager init)
- **Add**:
  ```python
  from extensions import limiter
  limiter.init_app(app)
  ```
- **Validation**: App starts without errors
- **Parallel With**: None

**[1.2.5] Add Rate Limit to Login Route**
```python
# Task ID: SEC-032
# Dependencies: [1.2.4]
# Time: 3 minutes
```
- **Action**: Protect login endpoint
- **File**: `apikeywallet-main/auth_routes.py`
- **Location**: Line 83 (login route)
- **Change**:
  ```python
  from extensions import limiter

  @auth.route('/login', methods=['GET', 'POST'])
  @limiter.limit("5 per minute")
  def login():
  ```
- **Validation**: Decorator added
- **Parallel With**: [1.2.6], [1.2.7]

**[1.2.6] Add Rate Limit to Register Route**
```python
# Task ID: SEC-033
# Dependencies: [1.2.4]
# Time: 3 minutes
```
- **Action**: Protect registration endpoint
- **File**: `apikeywallet-main/auth_routes.py`
- **Location**: Line 46 (register route)
- **Change**:
  ```python
  @auth.route('/register', methods=['GET', 'POST'])
  @limiter.limit("3 per hour")
  def register():
  ```
- **Validation**: Decorator added
- **Parallel With**: [1.2.5], [1.2.7]

**[1.2.7] Add Rate Limit to Copy Key Route**
```python
# Task ID: SEC-034
# Dependencies: [1.2.4]
# Time: 3 minutes
```
- **Action**: Prevent rapid key exfiltration
- **File**: `apikeywallet-main/wallet_routes.py`
- **Location**: Line 149 (copy_key route)
- **Change**:
  ```python
  from extensions import limiter

  @main.route('/copy_key/<int:key_id>', methods=['POST'])
  @login_required
  @limiter.limit("30 per minute")
  def copy_key(key_id):
  ```
- **Validation**: Decorator added
- **Parallel With**: [1.2.5], [1.2.6]

**[1.2.8] Add Rate Limit Error Handler**
```python
# Task ID: SEC-035
# Dependencies: [1.2.5], [1.2.6], [1.2.7]
# Time: 5 minutes
```
- **Action**: Create user-friendly error response
- **File**: `apikeywallet-main/app.py`
- **Location**: After blueprint registration
- **Add**:
  ```python
  @app.errorhandler(429)
  def ratelimit_handler(e):
      """Handle rate limit exceeded errors."""
      return jsonify({
          'error': 'Rate limit exceeded. Please try again later.',
          'retry_after': str(e.description)
      }), 429
  ```
- **Validation**: Handler defined
- **Parallel With**: None

**[1.2.9] Test Rate Limiting**
```python
# Task ID: SEC-036
# Dependencies: [1.2.8]
# Time: 10 minutes
```
- **Action**: Verify rate limits work
- **Test Script**:
  ```python
  import requests

  # Test login rate limit (5 per minute)
  url = "http://localhost:5000/login"
  for i in range(6):
      resp = requests.post(url, data={'email': 'test@test.com', 'password': 'wrong'})
      print(f"Attempt {i+1}: Status {resp.status_code}")
      if i == 5:
          assert resp.status_code == 429, "Rate limit should trigger"
  ```
- **Validation**: 6th request returns 429
- **Parallel With**: None

### WAVE 1.3 - Configuration Management (Parallel)

**[1.3.1] Create config.py File**
```python
# Task ID: CONFIG-001
# Dependencies: None
# Time: 15 minutes
```
- **Action**: Create configuration module
- **Output**: `apikeywallet-main/config.py`
- **Content**: (Full config.py from roadmap)
- **Validation**: Valid Python syntax, all config classes defined
- **Parallel With**: [1.3.2]

**[1.3.2] Update app.py to Use Config**
```python
# Task ID: CONFIG-002
# Dependencies: [1.3.1]
# Time: 5 minutes
```
- **Action**: Replace hardcoded config with classes
- **File**: `apikeywallet-main/app.py`
- **Changes**:
  - Import config
  - Replace lines 58-62 with config loading
  - Set log level based on environment
- **Validation**: App starts in development mode
- **Parallel With**: None

**[1.3.3] Add FLASK_ENV to .env**
```bash
# Task ID: CONFIG-003
# Dependencies: [1.3.2]
# Time: 1 minute
```
- **Action**: Set environment variable
- **File**: `apikeywallet-main/.env`
- **Add**: `FLASK_ENV=development`
- **Validation**: Variable set
- **Parallel With**: [1.3.4]

**[1.3.4] Update .env.example**
```bash
# Task ID: CONFIG-004
# Dependencies: None
# Time: 1 minute
```
- **Action**: Add FLASK_ENV to template
- **File**: `apikeywallet-main/.env.example`
- **Add**: `FLASK_ENV=development  # Options: development, testing, production`
- **Validation**: Variable documented
- **Parallel With**: [1.3.3]

**[1.3.5] Test Production Config**
```bash
# Task ID: CONFIG-005
# Dependencies: [1.3.3]
# Time: 5 minutes
```
- **Action**: Verify production mode disables debug
- **Command**:
  ```bash
  export FLASK_ENV=production
  cd apikeywallet-main && python app.py
  # Check logs for SQL queries (should be absent)
  ```
- **Validation**: No SQL queries in logs
- **Parallel With**: None

### WAVE 1.4 - Disable Debug Logging (Parallel)

**[1.4.1] Remove Debug Logging from utils.py**
```python
# Task ID: LOG-001
# Dependencies: None
# Time: 5 minutes
```
- **Action**: Replace debug calls with info
- **File**: `apikeywallet-main/utils.py`
- **Changes**:
  - Line 73: Change `logging.debug(f'Encrypted key type: {type(encrypted_key)}')` to info (remove key data)
  - Line 74: Remove or change to not log actual key
  - Line 76: Change to info
- **Validation**: No sensitive data logged
- **Parallel With**: [1.4.2]

**[1.4.2] Update Logging Configuration in app.py**
```python
# Task ID: LOG-002
# Dependencies: [1.3.2]
# Time: 3 minutes
```
- **Action**: Set log level based on environment
- **File**: `apikeywallet-main/app.py`
- **Location**: Line 45
- **Change**:
  ```python
  config_name = os.environ.get('FLASK_ENV', 'development')
  log_level = logging.INFO if config_name == 'production' else logging.DEBUG
  logging.basicConfig(level=log_level)
  ```
- **Validation**: Log level changes with FLASK_ENV
- **Parallel With**: [1.4.1]

**[1.4.3] Test Logging Levels**
```bash
# Task ID: LOG-003
# Dependencies: [1.4.1], [1.4.2]
# Time: 5 minutes
```
- **Action**: Verify appropriate logging in each environment
- **Tests**:
  - Development: Debug messages appear
  - Production: Only info+ messages appear
- **Validation**: Log levels work correctly
- **Parallel With**: None

### WAVE 1.5 - Session Management (Parallel)

**[1.5.1] Remove os.urandom Fallback**
```python
# Task ID: SESSION-001
# Dependencies: [1.3.1]
# Time: 3 minutes
```
- **Action**: Require SECRET_KEY in environment
- **File**: `apikeywallet-main/config.py`
- **Location**: Config class
- **Change**:
  ```python
  SECRET_KEY = os.environ.get('SECRET_KEY')
  if not SECRET_KEY:
      raise ValueError("SECRET_KEY environment variable is required")
  ```
- **Validation**: App fails to start without SECRET_KEY
- **Parallel With**: [1.5.2]

**[1.5.2] Add Session Configuration**
```python
# Task ID: SESSION-002
# Dependencies: [1.3.1]
# Time: 3 minutes
```
- **Action**: Configure session security
- **File**: `apikeywallet-main/config.py`
- **Location**: ProductionConfig class
- **Add**:
  ```python
  PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
  SESSION_REFRESH_EACH_REQUEST = True
  SESSION_COOKIE_SECURE = True
  SESSION_COOKIE_HTTPONLY = True
  SESSION_COOKIE_SAMESITE = 'Lax'
  ```
- **Validation**: Config values set
- **Parallel With**: [1.5.1], [1.5.3]

**[1.5.3] Mark Sessions as Permanent on Login**
```python
# Task ID: SESSION-003
# Dependencies: None
# Time: 3 minutes
```
- **Action**: Enable session timeout
- **File**: `apikeywallet-main/auth_routes.py`
- **Location**: login() function, after line 105
- **Add**:
  ```python
  from flask import session
  session.permanent = True
  login_user(user)
  ```
- **Validation**: Session marked permanent
- **Parallel With**: [1.5.2]

**[1.5.4] Test Session Timeout**
```python
# Task ID: SESSION-004
# Dependencies: [1.5.2], [1.5.3]
# Time: 35 minutes (includes 30 min wait)
```
- **Action**: Verify sessions expire after 30 minutes
- **Test Steps**:
  1. Login
  2. Wait 31 minutes
  3. Try to access /wallet
  4. Should redirect to login
- **Validation**: Session expires correctly
- **Parallel With**: Can run in background

### WAVE 1.6 - Password Strength (Sequential)

**[1.6.1] Create Password Validator**
```python
# Task ID: PWD-001
# Dependencies: None
# Time: 10 minutes
```
- **Action**: Add validation function to utils.py
- **File**: `apikeywallet-main/utils.py`
- **Add**: Password validation function (from roadmap)
- **Validation**: Function defined, handles all cases
- **Parallel With**: [1.6.2]

**[1.6.2] Create WTForms Validator**
```python
# Task ID: PWD-002
# Dependencies: [1.6.1]
# Time: 5 minutes
```
- **Action**: Create custom validator for forms
- **File**: `apikeywallet-main/forms.py`
- **Add**: password_complexity validator function
- **Validation**: Validator defined
- **Parallel With**: None (needs [1.6.1])

**[1.6.3] Update RegistrationForm**
```python
# Task ID: PWD-003
# Dependencies: [1.6.2]
# Time: 3 minutes
```
- **Action**: Apply password complexity requirements
- **File**: `apikeywallet-main/forms.py`
- **Location**: RegistrationForm class, line 34
- **Change**: Add password_complexity validator
- **Validation**: Form validates password strength
- **Parallel With**: None

**[1.6.4] Test Password Validation**
```python
# Task ID: PWD-004
# Dependencies: [1.6.3]
# Time: 10 minutes
```
- **Action**: Test password requirements
- **Tests**:
  - "short" → rejected
  - "nouppercase123!" → rejected
  - "NOLOWERCASE123!" → rejected
  - "NoNumbers!@#" → rejected
  - "NoSpecials123" → rejected
  - "ValidPass123!" → accepted
- **Validation**: All tests pass
- **Parallel With**: None

### WAVE 1.7 - Audit Logging (Sequential due to database)

**[1.7.1] Create AuditLog Model**
```python
# Task ID: AUDIT-001
# Dependencies: None
# Time: 10 minutes
```
- **Action**: Add audit model to models.py
- **File**: `apikeywallet-main/models.py`
- **Add**: AuditLog class (from roadmap)
- **Validation**: Model defined with all fields
- **Parallel With**: [1.7.2]

**[1.7.2] Create Audit Logging Utility**
```python
# Task ID: AUDIT-002
# Dependencies: None
# Time: 10 minutes
```
- **Action**: Add helper function to utils.py
- **File**: `apikeywallet-main/utils.py`
- **Add**: log_audit_event() function
- **Validation**: Function defined
- **Parallel With**: [1.7.1]

**[1.7.3] Create Database Migration**
```bash
# Task ID: AUDIT-003
# Dependencies: [1.7.1]
# Time: 3 minutes
```
- **Action**: Generate migration for audit_log table
- **Command**:
  ```bash
  cd apikeywallet-main
  flask db migrate -m "Add audit log table"
  ```
- **Output**: Migration file created
- **Validation**: Migration file exists in migrations/versions/
- **Parallel With**: None

**[1.7.4] Review Migration File**
```bash
# Task ID: AUDIT-004
# Dependencies: [1.7.3]
# Time: 3 minutes
```
- **Action**: Verify migration correctness
- **Check**:
  - Creates audit_log table
  - All columns present
  - Foreign key to user table
  - Indexes on common queries
- **Validation**: Migration looks correct
- **Parallel With**: None

**[1.7.5] Apply Migration**
```bash
# Task ID: AUDIT-005
# Dependencies: [1.7.4]
# Time: 2 minutes
```
- **Action**: Run migration
- **Command**:
  ```bash
  flask db upgrade
  ```
- **Validation**: Table exists in database
- **Parallel With**: None

**[1.7.6] Add Audit Log to copy_key()**
```python
# Task ID: AUDIT-006
# Dependencies: [1.7.2], [1.7.5]
# Time: 5 minutes
```
- **Action**: Log key access events
- **File**: `apikeywallet-main/wallet_routes.py`
- **Location**: copy_key() function
- **Add**: Audit logging call before decryption
- **Validation**: Audit entry created when key copied
- **Parallel With**: [1.7.7], [1.7.8], [1.7.9], [1.7.10], [1.7.11]

**[1.7.7] Add Audit Log to add_key()**
```python
# Task ID: AUDIT-007
# Dependencies: [1.7.2], [1.7.5]
# Time: 5 minutes
```
- **Action**: Log key creation
- **File**: `apikeywallet-main/wallet_routes.py`
- **Add**: log_audit_event() in add_key()
- **Action Type**: 'KEY_CREATED'
- **Validation**: Creates audit entry
- **Parallel With**: [1.7.6], [1.7.8], [1.7.9], [1.7.10], [1.7.11]

**[1.7.8] Add Audit Log to delete_key()**
```python
# Task ID: AUDIT-008
# Dependencies: [1.7.2], [1.7.5]
# Time: 5 minutes
```
- **Action**: Log key deletion
- **File**: `apikeywallet-main/wallet_routes.py`
- **Add**: log_audit_event() in delete_key()
- **Action Type**: 'KEY_DELETED'
- **Parallel With**: [1.7.6], [1.7.7], [1.7.9], [1.7.10], [1.7.11]

**[1.7.9] Add Audit Log to edit_key()**
```python
# Task ID: AUDIT-009
# Dependencies: [1.7.2], [1.7.5]
# Time: 5 minutes
```
- **Action**: Log key modifications
- **File**: `apikeywallet-main/wallet_routes.py`
- **Add**: log_audit_event() in edit_key()
- **Action Type**: 'KEY_MODIFIED'
- **Parallel With**: [1.7.6], [1.7.7], [1.7.8], [1.7.10], [1.7.11]

**[1.7.10] Add Audit Log to login()**
```python
# Task ID: AUDIT-010
# Dependencies: [1.7.2], [1.7.5]
# Time: 5 minutes
```
- **Action**: Log user logins
- **File**: `apikeywallet-main/auth_routes.py`
- **Add**: log_audit_event() in login()
- **Action Type**: 'USER_LOGIN'
- **Parallel With**: [1.7.6], [1.7.7], [1.7.8], [1.7.9], [1.7.11]

**[1.7.11] Add Audit Log to register()**
```python
# Task ID: AUDIT-011
# Dependencies: [1.7.2], [1.7.5]
# Time: 5 minutes
```
- **Action**: Log new user registrations
- **File**: `apikeywallet-main/auth_routes.py`
- **Add**: log_audit_event() in register()
- **Action Type**: 'USER_REGISTERED'
- **Parallel With**: [1.7.6], [1.7.7], [1.7.8], [1.7.9], [1.7.10]

**[1.7.12] Test Audit Logging**
```python
# Task ID: AUDIT-012
# Dependencies: [1.7.6] through [1.7.11]
# Time: 10 minutes
```
- **Action**: Verify audit logs created
- **Tests**:
  - Register → check audit_log table
  - Login → check audit entry
  - Add key → check entry
  - Copy key → check entry
  - Delete key → check entry
- **Validation**: All events logged
- **Parallel With**: None

---

## 🧪 **PHASE 2: TESTING INFRASTRUCTURE**

### WAVE 2.1 - Test Framework Setup (Sequential)

**[2.1.1] Create Test Directory Structure**
```bash
# Task ID: TEST-001
# Dependencies: Phase 1 complete
# Time: 2 minutes
```
- **Action**: Create test directories
- **Commands**:
  ```bash
  mkdir -p apikeywallet-main/tests/{unit,integration,security}
  touch apikeywallet-main/tests/__init__.py
  touch apikeywallet-main/tests/conftest.py
  ```
- **Validation**: Directories exist
- **Parallel With**: [2.1.2], [2.1.3]

**[2.1.2] Add Testing Dependencies**
```bash
# Task ID: TEST-002
# Dependencies: None
# Time: 3 minutes
```
- **Action**: Update pyproject.toml
- **Add**:
  ```toml
  "pytest>=8.0.0",
  "pytest-cov>=4.1.0",
  "pytest-flask>=1.3.0",
  ```
- **Validation**: Dependencies listed
- **Parallel With**: [2.1.1], [2.1.3]

**[2.1.3] Add Pytest Configuration**
```toml
# Task ID: TEST-003
# Dependencies: None
# Time: 5 minutes
```
- **Action**: Configure pytest in pyproject.toml
- **Add**:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  python_classes = ["Test*"]
  python_functions = ["test_*"]
  addopts = "-v --cov=. --cov-report=html --cov-report=term"
  ```
- **Validation**: Config section added
- **Parallel With**: [2.1.1], [2.1.2]

**[2.1.4] Install Testing Dependencies**
```bash
# Task ID: TEST-004
# Dependencies: [2.1.2]
# Time: 2 minutes
```
- **Action**: Install packages
- **Command**:
  ```bash
  cd apikeywallet-main
  pip install pytest pytest-cov pytest-flask
  ```
- **Validation**: Packages installed
- **Parallel With**: None

**[2.1.5] Create conftest.py**
```python
# Task ID: TEST-005
# Dependencies: [2.1.4]
# Time: 15 minutes
```
- **Action**: Create pytest fixtures
- **File**: `apikeywallet-main/tests/conftest.py`
- **Content**: Complete conftest with app, client, auth_client fixtures
- **Validation**: File created, valid syntax
- **Parallel With**: None

**[2.1.6] Test Pytest Installation**
```bash
# Task ID: TEST-006
# Dependencies: [2.1.5]
# Time: 2 minutes
```
- **Action**: Verify pytest works
- **Command**:
  ```bash
  cd apikeywallet-main
  pytest --collect-only
  ```
- **Validation**: No errors (even with 0 tests)
- **Parallel With**: None

### WAVE 2.2 - Unit Tests (Parallel within subcategories)

**[2.2.1] Create test_models.py Structure**
```python
# Task ID: TEST-007
# Dependencies: [2.1.6]
# Time: 3 minutes
```
- **Action**: Create test file
- **File**: `apikeywallet-main/tests/unit/test_models.py`
- **Add**: Imports and file structure
- **Validation**: File exists
- **Parallel With**: [2.2.5], [2.2.8]

**[2.2.2] Write test_user_password_hashing**
```python
# Task ID: TEST-008
# Dependencies: [2.2.1]
# Time: 10 minutes
```
- **Action**: Test User password methods
- **File**: `apikeywallet-main/tests/unit/test_models.py`
- **Content**: Complete test function
- **Validation**: Test passes
- **Parallel With**: [2.2.3], [2.2.4]

**[2.2.3] Write test_user_creation**
```python
# Task ID: TEST-009
# Dependencies: [2.2.1]
# Time: 5 minutes
```
- **Action**: Test User model creation
- **Validation**: Test passes
- **Parallel With**: [2.2.2], [2.2.4]

**[2.2.4] Write test_apikey_creation**
```python
# Task ID: TEST-010
# Dependencies: [2.2.1]
# Time: 10 minutes
```
- **Action**: Test APIKey model
- **Content**: Test with encryption
- **Validation**: Test passes
- **Parallel With**: [2.2.2], [2.2.3]

**[2.2.5] Create test_utils.py Structure**
```python
# Task ID: TEST-011
# Dependencies: [2.1.6]
# Time: 3 minutes
```
- **Action**: Create test file
- **File**: `apikeywallet-main/tests/unit/test_utils.py`
- **Validation**: File exists
- **Parallel With**: [2.2.1], [2.2.8]

**[2.2.6] Write test_encryption_decryption**
```python
# Task ID: TEST-012
# Dependencies: [2.2.5]
# Time: 10 minutes
```
- **Action**: Test crypto functions
- **Validation**: Test passes
- **Parallel With**: [2.2.7]

**[2.2.7] Write test_password_strength_validator**
```python
# Task ID: TEST-013
# Dependencies: [2.2.5]
# Time: 10 minutes
```
- **Action**: Test password validation
- **Tests**: All strength requirements
- **Validation**: Test passes
- **Parallel With**: [2.2.6]

**[2.2.8] Create test_forms.py Structure**
```python
# Task ID: TEST-014
# Dependencies: [2.1.6]
# Time: 3 minutes
```
- **Action**: Create test file
- **File**: `apikeywallet-main/tests/unit/test_forms.py`
- **Validation**: File exists
- **Parallel With**: [2.2.1], [2.2.5]

**[2.2.9] Write test_registration_form_validation**
```python
# Task ID: TEST-015
# Dependencies: [2.2.8]
# Time: 15 minutes
```
- **Action**: Test RegistrationForm
- **Cases**: Valid, invalid email, password mismatch, weak password
- **Validation**: All tests pass
- **Parallel With**: [2.2.10], [2.2.11]

**[2.2.10] Write test_login_form_validation**
```python
# Task ID: TEST-016
# Dependencies: [2.2.8]
# Time: 10 minutes
```
- **Action**: Test LoginForm
- **Validation**: Tests pass
- **Parallel With**: [2.2.9], [2.2.11]

**[2.2.11] Write test_add_api_key_form**
```python
# Task ID: TEST-017
# Dependencies: [2.2.8]
# Time: 10 minutes
```
- **Action**: Test AddAPIKeyForm
- **Validation**: Tests pass
- **Parallel With**: [2.2.9], [2.2.10]

**[2.2.12] Run All Unit Tests**
```bash
# Task ID: TEST-018
# Dependencies: [2.2.2] through [2.2.11]
# Time: 3 minutes
```
- **Action**: Execute unit test suite
- **Command**:
  ```bash
  cd apikeywallet-main
  pytest tests/unit/ -v
  ```
- **Validation**: All tests pass
- **Parallel With**: None

### WAVE 2.3 - Integration Tests (Parallel within subcategories)

**[2.3.1] Create test_auth.py**
```python
# Task ID: TEST-019
# Dependencies: [2.2.12]
# Time: 3 minutes
```
- **Action**: Create auth integration tests file
- **File**: `apikeywallet-main/tests/integration/test_auth.py`
- **Validation**: File exists
- **Parallel With**: [2.3.7], [2.3.12]

**[2.3.2] Write test_registration_flow**
```python
# Task ID: TEST-020
# Dependencies: [2.3.1]
# Time: 10 minutes
```
- **Action**: Test complete registration
- **Validation**: Test passes
- **Parallel With**: [2.3.3], [2.3.4], [2.3.5], [2.3.6]

**[2.3.3] Write test_login_logout_flow**
```python
# Task ID: TEST-021
# Dependencies: [2.3.1]
# Time: 10 minutes
```
- **Action**: Test login/logout cycle
- **Validation**: Test passes
- **Parallel With**: [2.3.2], [2.3.4], [2.3.5], [2.3.6]

**[2.3.4] Write test_login_invalid_credentials**
```python
# Task ID: TEST-022
# Dependencies: [2.3.1]
# Time: 5 minutes
```
- **Action**: Test failed login
- **Validation**: Test passes
- **Parallel With**: [2.3.2], [2.3.3], [2.3.5], [2.3.6]

**[2.3.5] Write test_login_rate_limiting**
```python
# Task ID: TEST-023
# Dependencies: [2.3.1]
# Time: 10 minutes
```
- **Action**: Test rate limiter
- **Validation**: 6th attempt blocked
- **Parallel With**: [2.3.2], [2.3.3], [2.3.4], [2.3.6]

**[2.3.6] Write test_protected_route_access**
```python
# Task ID: TEST-024
# Dependencies: [2.3.1]
# Time: 5 minutes
```
- **Action**: Test login requirement
- **Validation**: Unauthenticated redirected
- **Parallel With**: [2.3.2], [2.3.3], [2.3.4], [2.3.5]

**[2.3.7] Create test_wallet.py**
```python
# Task ID: TEST-025
# Dependencies: [2.2.12]
# Time: 3 minutes
```
- **Action**: Create wallet tests file
- **File**: `apikeywallet-main/tests/integration/test_wallet.py`
- **Validation**: File exists
- **Parallel With**: [2.3.1], [2.3.12]

**[2.3.8] Write test_add_key_flow**
```python
# Task ID: TEST-026
# Dependencies: [2.3.7]
# Time: 10 minutes
```
- **Action**: Test adding API key
- **Validation**: Key added successfully
- **Parallel With**: [2.3.9], [2.3.10], [2.3.11]

**[2.3.9] Write test_copy_key_authorization**
```python
# Task ID: TEST-027
# Dependencies: [2.3.7]
# Time: 15 minutes
```
- **Action**: Test user can only copy own keys
- **Validation**: 403 for other user's keys
- **Parallel With**: [2.3.8], [2.3.10], [2.3.11]

**[2.3.10] Write test_delete_key_flow**
```python
# Task ID: TEST-028
# Dependencies: [2.3.7]
# Time: 10 minutes
```
- **Action**: Test key deletion
- **Validation**: Key removed
- **Parallel With**: [2.3.8], [2.3.9], [2.3.11]

**[2.3.11] Write test_edit_key_flow**
```python
# Task ID: TEST-029
# Dependencies: [2.3.7]
# Time: 10 minutes
```
- **Action**: Test renaming key
- **Validation**: Name updated
- **Parallel With**: [2.3.8], [2.3.9], [2.3.10]

**[2.3.12] Create test_categories.py**
```python
# Task ID: TEST-030
# Dependencies: [2.2.12]
# Time: 3 minutes
```
- **Action**: Create category tests file
- **File**: `apikeywallet-main/tests/integration/test_categories.py`
- **Validation**: File exists
- **Parallel With**: [2.3.1], [2.3.7]

**[2.3.13] Write test_category_crud**
```python
# Task ID: TEST-031
# Dependencies: [2.3.12]
# Time: 20 minutes
```
- **Action**: Test create, read, update, delete
- **Validation**: All CRUD operations work
- **Parallel With**: [2.3.14]

**[2.3.14] Write test_category_key_assignment**
```python
# Task ID: TEST-032
# Dependencies: [2.3.12]
# Time: 10 minutes
```
- **Action**: Test assigning keys to categories
- **Validation**: Keys grouped correctly
- **Parallel With**: [2.3.13]

**[2.3.15] Run All Integration Tests**
```bash
# Task ID: TEST-033
# Dependencies: [2.3.2] through [2.3.14]
# Time: 5 minutes
```
- **Action**: Execute integration test suite
- **Command**:
  ```bash
  pytest tests/integration/ -v
  ```
- **Validation**: All tests pass
- **Parallel With**: None

### WAVE 2.4 - Security Tests (Parallel)

**[2.4.1] Create test_vulnerabilities.py**
```python
# Task ID: TEST-034
# Dependencies: [2.3.15]
# Time: 3 minutes
```
- **Action**: Create security tests file
- **File**: `apikeywallet-main/tests/security/test_vulnerabilities.py`
- **Validation**: File exists
- **Parallel With**: [2.4.6]

**[2.4.2] Write test_sql_injection_prevention**
```python
# Task ID: TEST-035
# Dependencies: [2.4.1]
# Time: 10 minutes
```
- **Action**: Test SQLi protection
- **Validation**: Malicious input escaped
- **Parallel With**: [2.4.3], [2.4.4], [2.4.5]

**[2.4.3] Write test_xss_prevention**
```python
# Task ID: TEST-036
# Dependencies: [2.4.1]
# Time: 10 minutes
```
- **Action**: Test XSS protection
- **Validation**: Scripts escaped
- **Parallel With**: [2.4.2], [2.4.4], [2.4.5]

**[2.4.4] Write test_csrf_protection**
```python
# Task ID: TEST-037
# Dependencies: [2.4.1]
# Time: 10 minutes
```
- **Action**: Test CSRF tokens
- **Validation**: Requests without token fail
- **Parallel With**: [2.4.2], [2.4.3], [2.4.5]

**[2.4.5] Write test_encryption_key_isolation**
```python
# Task ID: TEST-038
# Dependencies: [2.4.1]
# Time: 10 minutes
```
- **Action**: Test encryption security
- **Validation**: Wrong key can't decrypt
- **Parallel With**: [2.4.2], [2.4.3], [2.4.4]

**[2.4.6] Create test_authentication.py**
```python
# Task ID: TEST-039
# Dependencies: [2.3.15]
# Time: 3 minutes
```
- **Action**: Create auth security tests
- **File**: `apikeywallet-main/tests/security/test_authentication.py`
- **Validation**: File exists
- **Parallel With**: [2.4.1]

**[2.4.7] Write test_unauthorized_access_blocked**
```python
# Task ID: TEST-040
# Dependencies: [2.4.6]
# Time: 10 minutes
```
- **Action**: Test all protected routes
- **Validation**: All require login
- **Parallel With**: [2.4.8]

**[2.4.8] Write test_password_hashing_security**
```python
# Task ID: TEST-041
# Dependencies: [2.4.6]
# Time: 10 minutes
```
- **Action**: Test passwords never stored plaintext
- **Validation**: Hash changes each time
- **Parallel With**: [2.4.7]

**[2.4.9] Run All Security Tests**
```bash
# Task ID: TEST-042
# Dependencies: [2.4.2] through [2.4.8]
# Time: 3 minutes
```
- **Action**: Execute security test suite
- **Command**:
  ```bash
  pytest tests/security/ -v
  ```
- **Validation**: All tests pass
- **Parallel With**: None

### WAVE 2.5 - Coverage & CI Setup (Sequential)

**[2.5.1] Run Full Test Suite with Coverage**
```bash
# Task ID: TEST-043
# Dependencies: [2.4.9]
# Time: 5 minutes
```
- **Action**: Generate coverage report
- **Command**:
  ```bash
  cd apikeywallet-main
  pytest --cov=. --cov-report=html --cov-report=term
  ```
- **Output**: Coverage percentage, HTML report
- **Validation**: Coverage >50%
- **Parallel With**: None

**[2.5.2] Review Coverage Report**
```bash
# Task ID: TEST-044
# Dependencies: [2.5.1]
# Time: 10 minutes
```
- **Action**: Identify untested code
- **Command**:
  ```bash
  open htmlcov/index.html
  ```
- **Output**: List of files/lines not covered
- **Validation**: Critical paths identified
- **Parallel With**: None

**[2.5.3] Create .coveragerc Configuration**
```ini
# Task ID: TEST-045
# Dependencies: [2.5.2]
# Time: 5 minutes
```
- **Action**: Configure coverage tool
- **File**: `apikeywallet-main/.coveragerc`
- **Content**:
  ```ini
  [run]
  omit =
      */tests/*
      */venv/*
      */migrations/*
      */__pycache__/*

  [report]
  fail_under = 70
  precision = 2
  show_missing = True
  ```
- **Validation**: File created
- **Parallel With**: [2.5.4]

**[2.5.4] Add Coverage Badge**
```markdown
# Task ID: TEST-046
# Dependencies: [2.5.1]
# Time: 5 minutes
```
- **Action**: Add badge to README
- **File**: `README.md` (create if needed)
- **Add**: `![Coverage](https://img.shields.io/badge/coverage-XX%25-green)`
- **Validation**: Badge added
- **Parallel With**: [2.5.3]

**[2.5.5] Write Additional Tests for Low Coverage Areas**
```python
# Task ID: TEST-047
# Dependencies: [2.5.2]
# Time: 30 minutes
```
- **Action**: Increase coverage to 70%+
- **Target**: Files with <50% coverage
- **Validation**: Coverage ≥70%
- **Parallel With**: None

**[2.5.6] Final Coverage Check**
```bash
# Task ID: TEST-048
# Dependencies: [2.5.5]
# Time: 3 minutes
```
- **Action**: Verify coverage target met
- **Command**:
  ```bash
  pytest --cov=. --cov-fail-under=70
  ```
- **Validation**: Command exits 0, coverage ≥70%
- **Parallel With**: None

---

## 🛡️ **PHASE 3: PRODUCTION HARDENING**

I'll continue with Phase 3-6 in the same atomic detail...

**Due to length constraints, I've created the first 48 atomic tasks (Phase 0-2). Would you like me to:**

1. **Continue creating atomic tasks for Phases 3-6** (will be another ~200 tasks)
2. **Focus on a specific phase** for complete breakdown
3. **Create a separate execution script** that can run these tasks programmatically

The current breakdown shows:
- **48 atomic tasks** for Phases 0-2
- **Clear dependencies** (what must complete before each task)
- **Parallel execution groups** (which tasks can run simultaneously)
- **Time estimates** (5 minutes to 35 minutes per task)
- **Validation criteria** (how to know it's done)

Each task is designed to be handed to a sub-agent with all context needed.

---

## 🛡️ **PHASE 3: PRODUCTION HARDENING** (Continued)

### WAVE 3.1 - HTTPS & Security Headers (Parallel preparation)

**[3.1.1] Add Flask-Talisman Dependency**
```bash
# Task ID: HTTPS-001
# Dependencies: Phase 2 complete
# Time: 2 minutes
```
- **Action**: Add Talisman to dependencies
- **File**: `apikeywallet-main/pyproject.toml`
- **Add**: `"flask-talisman>=1.1.0",`
- **Validation**: Dependency listed
- **Parallel With**: [3.1.2]

**[3.1.2] Install Flask-Talisman**
```bash
# Task ID: HTTPS-002
# Dependencies: [3.1.1]
# Time: 2 minutes
```
- **Action**: Install package
- **Command**: `pip install flask-talisman`
- **Validation**: Package installed
- **Parallel With**: None

**[3.1.3] Initialize Talisman in app.py**
```python
# Task ID: HTTPS-003
# Dependencies: [3.1.2]
# Time: 10 minutes
```
- **Action**: Add HTTPS enforcement and security headers
- **File**: `apikeywallet-main/app.py`
- **Location**: After app creation, before routes
- **Add**:
  ```python
  from flask_talisman import Talisman

  if not app.config.get('TESTING'):
      Talisman(app,
          force_https=True,
          strict_transport_security=True,
          strict_transport_security_max_age=31536000,
          content_security_policy={
              'default-src': "'self'",
              'script-src': "'self' 'unsafe-inline'",
              'style-src': "'self' 'unsafe-inline'",
              'img-src': "'self' data:",
              'font-src': "'self'"
          },
          force_https_permanent=True
      )
  ```
- **Validation**: Headers added to responses
- **Parallel With**: [3.1.4]

**[3.1.4] Create nginx Configuration File**
```nginx
# Task ID: HTTPS-004
# Dependencies: None
# Time: 15 minutes
```
- **Action**: Create reverse proxy config
- **Output**: `/home/user/keyguardian/deployment/nginx.conf`
- **Content**:
  ```nginx
  # Redirect HTTP to HTTPS
  server {
      listen 80;
      server_name keyguardian.yourdomain.com;
      return 301 https://$server_name$request_uri;
  }

  # HTTPS server
  server {
      listen 443 ssl http2;
      server_name keyguardian.yourdomain.com;

      # SSL certificates (will be set up with certbot)
      ssl_certificate /etc/letsencrypt/live/keyguardian.yourdomain.com/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/keyguardian.yourdomain.com/privkey.pem;

      # SSL configuration
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
      ssl_prefer_server_ciphers on;
      ssl_session_cache shared:SSL:10m;
      ssl_session_timeout 10m;

      # Security headers (redundant with Talisman, but good practice)
      add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
      add_header X-Frame-Options "SAMEORIGIN" always;
      add_header X-Content-Type-Options "nosniff" always;
      add_header X-XSS-Protection "1; mode=block" always;

      # Proxy to Flask app
      location / {
          proxy_pass http://127.0.0.1:5000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_redirect off;
      }

      # Static files (optional optimization)
      location /static {
          alias /home/user/keyguardian/apikeywallet-main/static;
          expires 30d;
          add_header Cache-Control "public, immutable";
      }
  }
  ```
- **Validation**: File created
- **Parallel With**: [3.1.3]

**[3.1.5] Document SSL Certificate Setup**
```markdown
# Task ID: HTTPS-005
# Dependencies**: [3.1.4]
# Time: 10 minutes
```
- **Action**: Create SSL setup instructions
- **Output**: `/home/user/keyguardian/deployment/SSL_SETUP.md`
- **Content**:
  ```markdown
  # SSL Certificate Setup with Let's Encrypt

  ## Prerequisites
  - Domain name pointing to your server
  - nginx installed
  - Port 80 and 443 open in firewall

  ## Install Certbot
  ```bash
  sudo apt-get update
  sudo apt-get install certbot python3-certbot-nginx
  ```

  ## Obtain Certificate
  ```bash
  sudo certbot --nginx -d keyguardian.yourdomain.com
  ```

  ## Auto-renewal
  Certbot installs a cron job automatically. Verify:
  ```bash
  sudo certbot renew --dry-run
  ```

  ## Test SSL Configuration
  Visit: https://www.ssllabs.com/ssltest/
  Target grade: A or A+
  ```
- **Validation**: Documentation complete
- **Parallel With**: None

### WAVE 3.2 - Database Security (Parallel)

**[3.2.1] Enable PostgreSQL SSL in Config**
```python
# Task ID: DB-001
# Dependencies: None
# Time: 5 minutes
```
- **Action**: Require SSL for database connections
- **File**: `apikeywallet-main/config.py`
- **Location**: ProductionConfig class
- **Modify**:
  ```python
  # Change DATABASE_URL to append SSL mode
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  if SQLALCHEMY_DATABASE_URI and not SQLALCHEMY_DATABASE_URI.endswith('sslmode=require'):
      SQLALCHEMY_DATABASE_URI += '?sslmode=require'
  ```
- **Validation**: SSL mode added
- **Parallel With**: [3.2.2], [3.2.3]

**[3.2.2] Configure Connection Pooling**
```python
# Task ID: DB-002
# Dependencies: None
# Time: 5 minutes
```
- **Action**: Add connection pool settings
- **File**: `apikeywallet-main/config.py`
- **Location**: ProductionConfig class
- **Add**:
  ```python
  SQLALCHEMY_ENGINE_OPTIONS = {
      'pool_size': 10,
      'pool_recycle': 3600,
      'pool_pre_ping': True,
      'max_overflow': 20
  }
  ```
- **Validation**: Settings added
- **Parallel With**: [3.2.1], [3.2.3]

**[3.2.3] Document Database User Creation**
```sql
# Task ID: DB-003
# Dependencies: None
# Time: 10 minutes
```
- **Action**: Create SQL script for minimal privilege user
- **Output**: `/home/user/keyguardian/deployment/create_db_user.sql`
- **Content**:
  ```sql
  -- Create dedicated application user (run as postgres superuser)

  -- Create user
  CREATE USER keyguardian_app WITH PASSWORD 'REPLACE_WITH_STRONG_PASSWORD';

  -- Grant connection
  GRANT CONNECT ON DATABASE keyguardian TO keyguardian_app;

  -- Grant schema usage
  GRANT USAGE ON SCHEMA public TO keyguardian_app;

  -- Grant table permissions
  GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO keyguardian_app;

  -- Grant sequence permissions (for auto-increment IDs)
  GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO keyguardian_app;

  -- Grant permissions on future tables (important for migrations)
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO keyguardian_app;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO keyguardian_app;

  -- Verify permissions
  \dp
  ```
- **Validation**: Script created
- **Parallel With**: [3.2.1], [3.2.2]

**[3.2.4] Create Database Backup Script**
```bash
# Task ID: DB-004
# Dependencies: None
# Time: 20 minutes
```
- **Action**: Create automated backup script
- **Output**: `/home/user/keyguardian/deployment/backup_database.sh`
- **Content**:
  ```bash
  #!/bin/bash
  #
  # Database backup script for KeyGuardian
  # Run daily via cron
  #

  set -e

  # Configuration
  DB_NAME="keyguardian"
  DB_USER="keyguardian_app"
  BACKUP_DIR="/var/backups/keyguardian"
  RETENTION_DAYS=30
  GPG_RECIPIENT="admin@yourdomain.com"

  # Create backup directory if needed
  mkdir -p "$BACKUP_DIR"

  # Generate filename with timestamp
  DATE=$(date +%Y%m%d_%H%M%S)
  BACKUP_FILE="$BACKUP_DIR/keyguardian_$DATE.sql"
  COMPRESSED_FILE="$BACKUP_FILE.gz"
  ENCRYPTED_FILE="$COMPRESSED_FILE.gpg"

  echo "Starting backup at $(date)"

  # Dump database
  pg_dump -U "$DB_USER" -h localhost "$DB_NAME" > "$BACKUP_FILE"

  # Compress
  gzip "$BACKUP_FILE"

  # Encrypt
  gpg --encrypt --recipient "$GPG_RECIPIENT" "$COMPRESSED_FILE"

  # Remove unencrypted compressed file
  rm "$COMPRESSED_FILE"

  # Set permissions
  chmod 600 "$ENCRYPTED_FILE"

  # Delete old backups
  find "$BACKUP_DIR" -name "keyguardian_*.sql.gz.gpg" -mtime +$RETENTION_DAYS -delete

  echo "Backup completed: $ENCRYPTED_FILE"
  echo "Backup size: $(du -h "$ENCRYPTED_FILE" | cut -f1)"

  # Optional: Upload to cloud storage
  # aws s3 cp "$ENCRYPTED_FILE" s3://your-backup-bucket/keyguardian/

  # Log completion
  logger "KeyGuardian database backup completed successfully"
  ```
- **Make executable**: `chmod +x backup_database.sh`
- **Validation**: Script created and executable
- **Parallel With**: [3.2.5]

**[3.2.5] Create Backup Restoration Script**
```bash
# Task ID: DB-005
# Dependencies: None
# Time: 15 minutes
```
- **Action**: Create restore script
- **Output**: `/home/user/keyguardian/deployment/restore_database.sh`
- **Content**:
  ```bash
  #!/bin/bash
  #
  # Database restore script for KeyGuardian
  #

  set -e

  if [ $# -ne 1 ]; then
      echo "Usage: $0 <backup_file.sql.gz.gpg>"
      exit 1
  fi

  BACKUP_FILE="$1"

  if [ ! -f "$BACKUP_FILE" ]; then
      echo "Error: Backup file not found: $BACKUP_FILE"
      exit 1
  fi

  echo "WARNING: This will overwrite the current database!"
  read -p "Are you sure you want to continue? (yes/no): " CONFIRM

  if [ "$CONFIRM" != "yes" ]; then
      echo "Restore cancelled"
      exit 0
  fi

  # Decrypt
  gpg --decrypt "$BACKUP_FILE" > /tmp/restore_temp.sql.gz

  # Decompress
  gunzip /tmp/restore_temp.sql.gz

  # Stop application (if running)
  sudo systemctl stop keyguardian 2>/dev/null || true

  # Drop and recreate database
  psql -U postgres -c "DROP DATABASE IF EXISTS keyguardian;"
  psql -U postgres -c "CREATE DATABASE keyguardian;"

  # Restore
  psql -U postgres keyguardian < /tmp/restore_temp.sql

  # Clean up
  rm /tmp/restore_temp.sql

  # Restart application
  sudo systemctl start keyguardian 2>/dev/null || true

  echo "Database restore completed successfully"
  ```
- **Make executable**: `chmod +x restore_database.sh`
- **Validation**: Script created
- **Parallel With**: [3.2.4]

**[3.2.6] Create Cron Job for Backups**
```bash
# Task ID: DB-006
# Dependencies: [3.2.4]
# Time: 5 minutes
```
- **Action**: Document cron setup
- **Output**: `/home/user/keyguardian/deployment/BACKUP_CRON.md`
- **Content**:
  ```markdown
  # Automated Backup Setup

  ## Add to crontab
  ```bash
  sudo crontab -e
  ```

  ## Add this line (runs daily at 2 AM)
  ```
  0 2 * * * /home/user/keyguardian/deployment/backup_database.sh >> /var/log/keyguardian_backup.log 2>&1
  ```

  ## Verify cron job
  ```bash
  sudo crontab -l
  ```

  ## Test backup manually
  ```bash
  sudo /home/user/keyguardian/deployment/backup_database.sh
  ```

  ## Monitor logs
  ```bash
  tail -f /var/log/keyguardian_backup.log
  ```
  ```
- **Validation**: Documentation created
- **Parallel With**: None

### WAVE 3.3 - Error Handling & Monitoring (Parallel)

**[3.3.1] Add Sentry SDK Dependency**
```bash
# Task ID: MON-001
# Dependencies: None
# Time: 2 minutes
```
- **Action**: Add Sentry to dependencies
- **File**: `apikeywallet-main/pyproject.toml`
- **Add**: `"sentry-sdk[flask]>=2.0.0",`
- **Validation**: Dependency listed
- **Parallel With**: [3.3.3]

**[3.3.2] Install Sentry SDK**
```bash
# Task ID: MON-002
# Dependencies: [3.3.1]
# Time: 2 minutes
```
- **Action**: Install package
- **Command**: `pip install "sentry-sdk[flask]"`
- **Validation**: Package installed
- **Parallel With**: None

**[3.3.3] Initialize Sentry in app.py**
```python
# Task ID: MON-003
# Dependencies: [3.3.2]
# Time: 10 minutes
```
- **Action**: Add error tracking
- **File**: `apikeywallet-main/app.py`
- **Location**: After imports, before app creation
- **Add**:
  ```python
  import sentry_sdk
  from sentry_sdk.integrations.flask import FlaskIntegration

  # Load config first to get environment
  config_name = os.environ.get('FLASK_ENV', 'development')

  # Initialize Sentry for production only
  if config_name == 'production':
      sentry_sdk.init(
          dsn=os.environ.get('SENTRY_DSN'),
          integrations=[FlaskIntegration()],
          traces_sample_rate=0.1,  # 10% transaction sampling
          environment=config_name,
          release=os.environ.get('APP_VERSION', 'unknown'),
          before_send=lambda event, hint: filter_sensitive_data(event)
      )

  def filter_sensitive_data(event):
      """Remove sensitive data from Sentry events."""
      if 'request' in event:
          # Remove authentication headers
          if 'headers' in event['request']:
              event['request']['headers'].pop('Authorization', None)
              event['request']['headers'].pop('Cookie', None)

          # Remove sensitive form data
          if 'data' in event['request']:
              sensitive_fields = ['password', 'api_key', 'secret']
              for field in sensitive_fields:
                  if field in event['request']['data']:
                      event['request']['data'][field] = '[REDACTED]'

      return event
  ```
- **Validation**: Sentry initialized
- **Parallel With**: [3.3.4]

**[3.3.4] Create Custom Error Pages**
```html
# Task ID: MON-004
# Dependencies: None
# Time: 30 minutes
```
- **Action**: Create error templates
- **Output Files**:
  - `apikeywallet-main/templates/errors/404.html`
  - `apikeywallet-main/templates/errors/403.html`
  - `apikeywallet-main/templates/errors/500.html`
  - `apikeywallet-main/templates/errors/429.html`
- **Base Template** (404.html):
  ```html
  {% extends "base.html" %}

  {% block title %}Page Not Found - KeyGuardian{% endblock %}

  {% block content %}
  <div class="error-container">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you're looking for doesn't exist.</p>
      <a href="{{ url_for('main.wallet') }}" class="btn btn-primary">Go to Dashboard</a>
  </div>
  {% endblock %}
  ```
- **Validation**: All 4 error templates created
- **Parallel With**: [3.3.3], [3.3.5]

**[3.3.5] Add Error Handlers to app.py**
```python
# Task ID: MON-005
# Dependencies: [3.3.4]
# Time: 10 minutes
```
- **Action**: Register error handlers
- **File**: `apikeywallet-main/app.py`
- **Location**: After blueprint registration
- **Add**:
  ```python
  # Error handlers
  @app.errorhandler(404)
  def not_found(error):
      """Handle 404 errors."""
      return render_template('errors/404.html'), 404

  @app.errorhandler(403)
  def forbidden(error):
      """Handle 403 errors."""
      return render_template('errors/403.html'), 403

  @app.errorhandler(500)
  def internal_error(error):
      """Handle 500 errors."""
      db.session.rollback()
      return render_template('errors/500.html'), 500

  @app.errorhandler(429)
  def ratelimit_error(error):
      """Handle rate limit exceeded."""
      return render_template('errors/429.html'), 429
  ```
- **Validation**: Handlers registered
- **Parallel With**: [3.3.4]

**[3.3.6] Add SENTRY_DSN to .env.example**
```bash
# Task ID: MON-006
# Dependencies: None
# Time: 2 minutes
```
- **Action**: Document Sentry configuration
- **File**: `apikeywallet-main/.env.example`
- **Add**: `SENTRY_DSN=https://your-sentry-dsn-here@sentry.io/project-id`
- **Validation**: Variable documented
- **Parallel With**: All above

**[3.3.7] Create Health Check Endpoint**
```python
# Task ID: MON-007
# Dependencies: None
# Time: 10 minutes
```
- **Action**: Add health check for monitoring
- **File**: `apikeywallet-main/app.py`
- **Location**: After error handlers
- **Add**:
  ```python
  @app.route('/health')
  def health():
      """
      Health check endpoint for monitoring and load balancers.

      Checks:
      - Application is running
      - Database connection works
      - Basic application state

      Returns:
          JSON response with health status
      """
      health_status = {
          'status': 'healthy',
          'timestamp': datetime.utcnow().isoformat(),
          'checks': {}
      }

      # Check database
      try:
          db.session.execute('SELECT 1')
          health_status['checks']['database'] = 'connected'
      except Exception as e:
          health_status['status'] = 'unhealthy'
          health_status['checks']['database'] = f'error: {str(e)}'
          return jsonify(health_status), 503

      # Check migrations are up to date
      try:
          from flask_migrate import current, heads
          current_rev = current()
          head_rev = heads()
          if current_rev != head_rev:
              health_status['checks']['migrations'] = 'outdated'
          else:
              health_status['checks']['migrations'] = 'current'
      except Exception as e:
          health_status['checks']['migrations'] = f'unknown: {str(e)}'

      return jsonify(health_status), 200
  ```
- **Validation**: Endpoint returns 200
- **Parallel With**: All above

### WAVE 3.4 - Structured Logging (Sequential due to app.py changes)

**[3.4.1] Create logging_config.py**
```python
# Task ID: LOG-004
# Dependencies: None
# Time: 20 minutes
```
- **Action**: Create JSON logging module
- **Output**: `apikeywallet-main/logging_config.py`
- **Content**:
  ```python
  """
  logging_config.py - Structured logging configuration

  Implements JSON logging for easier parsing and analysis.
  """

  import logging
  import json
  from datetime import datetime


  class JSONFormatter(logging.Formatter):
      """Format logs as JSON for structured logging."""

      def format(self, record):
          """Format log record as JSON."""
          log_data = {
              'timestamp': datetime.utcnow().isoformat() + 'Z',
              'level': record.levelname,
              'message': record.getMessage(),
              'logger': record.name,
              'module': record.module,
              'function': record.funcName,
              'line': record.lineno
          }

          # Add exception info if present
          if record.exc_info:
              log_data['exception'] = self.formatException(record.exc_info)

          # Add custom fields if present
          if hasattr(record, 'user_id'):
              log_data['user_id'] = record.user_id
          if hasattr(record, 'request_id'):
              log_data['request_id'] = record.request_id
          if hasattr(record, 'ip_address'):
              log_data['ip_address'] = record.ip_address

          return json.dumps(log_data)


  def setup_logging(app):
      """
      Configure application logging.

      Args:
          app: Flask application instance
      """
      # Create handler
      handler = logging.StreamHandler()

      # Use JSON formatter in production, simple in development
      if app.config.get('ENV') == 'production':
          handler.setFormatter(JSONFormatter())
      else:
          formatter = logging.Formatter(
              '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
          )
          handler.setFormatter(formatter)

      # Set log level
      log_level = app.config.get('LOG_LEVEL', logging.INFO)
      handler.setLevel(log_level)
      app.logger.addHandler(handler)
      app.logger.setLevel(log_level)

      # Reduce noise from third-party libraries
      logging.getLogger('werkzeug').setLevel(logging.WARNING)
      logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
  ```
- **Validation**: Module created
- **Parallel With**: [3.4.2]

**[3.4.2] Add Request ID Middleware**
```python
# Task ID: LOG-005
# Dependencies: None
# Time: 15 minutes
```
- **Action**: Add request tracking
- **File**: `apikeywallet-main/app.py`
- **Location**: After app creation
- **Add**:
  ```python
  import uuid
  from flask import g, request

  @app.before_request
  def before_request():
      """Attach request ID and database session before each request."""
      # Generate unique request ID
      g.request_id = str(uuid.uuid4())

      # Attach database session (existing code)
      g.db = get_db_session()

  @app.after_request
  def after_request(response):
      """Log request completion and add request ID header."""
      # Add request ID to response headers
      response.headers['X-Request-ID'] = g.request_id

      # Log request completion
      app.logger.info('Request completed', extra={
          'request_id': g.request_id,
          'method': request.method,
          'path': request.path,
          'status': response.status_code,
          'user_id': current_user.id if current_user.is_authenticated else None,
          'ip_address': request.remote_addr
      })

      return response
  ```
- **Validation**: Request ID added to responses
- **Parallel With**: [3.4.1]

**[3.4.3] Initialize Logging in app.py**
```python
# Task ID: LOG-006
# Dependencies: [3.4.1], [3.4.2]
# Time: 5 minutes
```
- **Action**: Set up structured logging
- **File**: `apikeywallet-main/app.py`
- **Location**: After config loading
- **Add**:
  ```python
  from logging_config import setup_logging

  # Setup logging
  setup_logging(app)
  ```
- **Validation**: JSON logs in production
- **Parallel With**: None

**[3.4.4] Add LOG_LEVEL to Config**
```python
# Task ID: LOG-007
# Dependencies: None
# Time: 3 minutes
```
- **Action**: Make log level configurable
- **File**: `apikeywallet-main/config.py`
- **Add to each config class**:
  ```python
  class DevelopmentConfig(Config):
      DEBUG = True
      LOG_LEVEL = logging.DEBUG

  class ProductionConfig(Config):
      DEBUG = False
      LOG_LEVEL = logging.INFO
  ```
- **Validation**: Config updated
- **Parallel With**: [3.4.5]

**[3.4.5] Update Sensitive Logging**
```python
# Task ID: LOG-008
# Dependencies: None
# Time: 15 minutes
```
- **Action**: Remove sensitive data from logs
- **Files**: All route files
- **Changes**:
  - Remove `logging.debug(f'Encrypted key: {encrypted_key}')` statements
  - Remove `logging.debug(f'Decrypted key: {decrypted_key}')` statements
  - Replace with: `logging.info('Key operation completed', extra={'key_id': key_id})`
- **Validation**: No sensitive data in logs
- **Parallel With**: [3.4.4]

### WAVE 3.5 - Performance Optimization (Parallel)

**[3.5.1] Add Database Indexes Migration**
```python
# Task ID: PERF-001
# Dependencies: None
# Time: 15 minutes
```
- **Action**: Create migration for performance indexes
- **File**: New migration file
- **Content**:
  ```python
  """Add performance indexes

  Revision ID: perf_indexes_001
  """
  from alembic import op

  def upgrade():
      # APIKey indexes
      op.create_index(
          'idx_apikey_user_category',
          'api_key',
          ['user_id', 'category_id']
      )
      op.create_index(
          'idx_apikey_user_name',
          'api_key',
          ['user_id', 'key_name']
      )

      # AuditLog indexes
      op.create_index(
          'idx_audit_user_timestamp',
          'audit_log',
          ['user_id', 'timestamp']
      )
      op.create_index(
          'idx_audit_action_timestamp',
          'audit_log',
          ['action', 'timestamp']
      )

      # Category indexes
      op.create_index(
          'idx_category_user',
          'category',
          ['user_id']
      )

  def downgrade():
      op.drop_index('idx_apikey_user_category', 'api_key')
      op.drop_index('idx_apikey_user_name', 'api_key')
      op.drop_index('idx_audit_user_timestamp', 'audit_log')
      op.drop_index('idx_audit_action_timestamp', 'audit_log')
      op.drop_index('idx_category_user', 'category')
  ```
- **Command**: `flask db migrate -m "Add performance indexes"`
- **Validation**: Migration created
- **Parallel With**: [3.5.2], [3.5.3]

**[3.5.2] Add Flask-Caching Dependency**
```bash
# Task ID: PERF-002
# Dependencies: None
# Time: 2 minutes
```
- **Action**: Add caching support
- **File**: `apikeywallet-main/pyproject.toml`
- **Add**: `"Flask-Caching>=2.1.0",`
- **Validation**: Dependency listed
- **Parallel With**: [3.5.1], [3.5.3]

**[3.5.3] Install Flask-Caching**
```bash
# Task ID: PERF-003
# Dependencies: [3.5.2]
# Time: 2 minutes
```
- **Action**: Install package
- **Command**: `pip install Flask-Caching`
- **Validation**: Package installed
- **Parallel With**: None (needs [3.5.2])

**[3.5.4] Initialize Cache in extensions.py**
```python
# Task ID: PERF-004
# Dependencies: [3.5.3]
# Time: 10 minutes
```
- **Action**: Add cache instance
- **File**: `apikeywallet-main/extensions.py`
- **Add**:
  ```python
  from flask_caching import Cache

  # Initialize cache
  cache = Cache(config={
      'CACHE_TYPE': 'simple',  # Use 'redis' in production
      'CACHE_DEFAULT_TIMEOUT': 300
  })
  ```
- **Validation**: Cache defined
- **Parallel With**: [3.5.5]

**[3.5.5] Initialize Cache in app.py**
```python
# Task ID: PERF-005
# Dependencies: [3.5.4]
# Time: 5 minutes
```
- **Action**: Bind cache to app
- **File**: `apikeywallet-main/app.py`
- **Location**: After limiter initialization
- **Add**:
  ```python
  from extensions import cache

  # Configure cache based on environment
  if config_name == 'production':
      cache.init_app(app, config={
          'CACHE_TYPE': 'redis',
          'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
          'CACHE_DEFAULT_TIMEOUT': 300
      })
  else:
      cache.init_app(app)
  ```
- **Validation**: Cache initialized
- **Parallel With**: None

**[3.5.6] Add Caching to Category Queries**
```python
# Task ID: PERF-006
# Dependencies: [3.5.5]
# Time: 10 minutes
```
- **Action**: Cache category lists
- **File**: `apikeywallet-main/wallet_routes.py`
- **Location**: wallet() function
- **Change**:
  ```python
  from extensions import cache

  @main.route('/wallet')
  @main.route('/wallet/<int:category_id>')
  @login_required
  def wallet(category_id=None):
      # Cache categories per user for 5 minutes
      cache_key = f'categories_user_{current_user.id}'
      categories = cache.get(cache_key)

      if categories is None:
          categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
          cache.set(cache_key, categories, timeout=300)

      # ... rest of function
  ```
- **Validation**: Categories cached
- **Parallel With**: [3.5.7]

**[3.5.7] Add Cache Invalidation on Category Changes**
```python
# Task ID: PERF-007
# Dependencies: [3.5.6]
# Time: 15 minutes
```
- **Action**: Clear cache when categories modified
- **File**: `apikeywallet-main/category_routes.py`
- **Add to each route that modifies categories**:
  ```python
  from extensions import cache

  @categories.route('/add_category', methods=['POST'])
  @login_required
  def add_category():
      # ... existing code to add category ...

      # Clear cache
      cache.delete(f'categories_user_{current_user.id}')

      # ... rest of function
  ```
- **Apply to**: add_category, edit_category, delete_category
- **Validation**: Cache invalidated on changes
- **Parallel With**: [3.5.6]

**[3.5.8] Add Flask-Compress Dependency**
```bash
# Task ID: PERF-008
# Dependencies: None
# Time: 2 minutes
```
- **Action**: Add response compression
- **File**: `apikeywallet-main/pyproject.toml`
- **Add**: `"Flask-Compress>=1.14",`
- **Validation**: Dependency listed
- **Parallel With**: All above

**[3.5.9] Install and Enable Flask-Compress**
```python
# Task ID: PERF-009
# Dependencies: [3.5.8]
# Time: 5 minutes
```
- **Action**: Enable gzip compression
- **Commands**:
  ```bash
  pip install Flask-Compress
  ```
- **File**: `apikeywallet-main/app.py`
- **Add**:
  ```python
  from flask_compress import Compress

  Compress(app)
  ```
- **Validation**: Responses compressed
- **Parallel With**: None

---

## 🔒 **PHASE 4: ADDITIONAL SECURITY FEATURES**

### WAVE 4.1 - Multi-Factor Authentication (MFA) Foundation

**[4.1.1] Add pyotp and qrcode Dependencies**
```bash
# Task ID: MFA-001
# Dependencies: Phase 3 complete
# Time: 3 minutes
```
- **Action**: Add MFA libraries
- **File**: `apikeywallet-main/pyproject.toml`
- **Add**:
  ```python
  "pyotp>=2.9.0",
  "qrcode[pil]>=7.4.2",
  ```
- **Validation**: Dependencies listed
- **Parallel With**: [4.1.2]

**[4.1.2] Install MFA Dependencies**
```bash
# Task ID: MFA-002
# Dependencies: [4.1.1]
# Time: 3 minutes
```
- **Action**: Install packages
- **Command**: `pip install pyotp "qrcode[pil]"`
- **Validation**: Packages installed
- **Parallel With**: None

**[4.1.3] Add MFA Fields to User Model**
```python
# Task ID: MFA-003
# Dependencies: [4.1.2]
# Time: 5 minutes
```
- **Action**: Extend User model
- **File**: `apikeywallet-main/models.py`
- **Location**: User class, after is_admin field
- **Add**:
  ```python
  mfa_enabled = db.Column(db.Boolean, default=False, nullable=False)
  mfa_secret = db.Column(db.String(32), nullable=True)
  backup_codes = db.Column(db.Text, nullable=True)  # JSON array
  ```
- **Validation**: Fields added
- **Parallel With**: [4.1.4]

**[4.1.4] Create MFA Migration**
```bash
# Task ID: MFA-004
# Dependencies: [4.1.3]
# Time: 3 minutes
```
- **Action**: Generate database migration
- **Command**: `flask db migrate -m "Add MFA fields to User model"`
- **Validation**: Migration created
- **Parallel With**: None

**[4.1.5] Apply MFA Migration**
```bash
# Task ID: MFA-005
# Dependencies: [4.1.4]
# Time: 2 minutes
```
- **Action**: Update database
- **Command**: `flask db upgrade`
- **Validation**: Fields exist in database
- **Parallel With**: None

**[4.1.6] Create MFA Setup Route**
```python
# Task ID: MFA-006
# Dependencies: [4.1.5]
# Time: 30 minutes
```
- **Action**: Add MFA enrollment endpoint
- **File**: `apikeywallet-main/auth_routes.py`
- **Content**: Complete setup_mfa() function (from roadmap)
- **Validation**: Route accessible
- **Parallel With**: [4.1.7], [4.1.8]

**[4.1.7] Create MFA Verification Route**
```python
# Task ID: MFA-007
# Dependencies: [4.1.5]
# Time: 25 minutes
```
- **Action**: Add MFA verification endpoint
- **File**: `apikeywallet-main/auth_routes.py`
- **Content**: Complete verify_mfa() function
- **Validation**: Route works
- **Parallel With**: [4.1.6], [4.1.8]

**[4.1.8] Update Login Flow for MFA**
```python
# Task ID: MFA-008
# Dependencies: [4.1.5]
# Time: 15 minutes
```
- **Action**: Check MFA on login
- **File**: `apikeywallet-main/auth_routes.py`
- **Location**: login() function
- **Modify**: Add MFA check before login_user()
- **Validation**: MFA users redirected to verification
- **Parallel With**: [4.1.6], [4.1.7]

**[4.1.9] Create MFA Setup Template**
```html
# Task ID: MFA-009
# Dependencies: [4.1.6]
# Time: 20 minutes
```
- **Action**: Create QR code display page
- **Output**: `apikeywallet-main/templates/setup_mfa.html`
- **Content**: QR code, secret key, instructions
- **Validation**: Template renders
- **Parallel With**: [4.1.10], [4.1.11]

**[4.1.10] Create MFA Verification Template**
```html
# Task ID: MFA-010
# Dependencies: [4.1.7]
# Time: 15 minutes
```
- **Action**: Create code entry page
- **Output**: `apikeywallet-main/templates/verify_mfa.html`
- **Content**: 6-digit code input
- **Validation**: Template renders
- **Parallel With**: [4.1.9], [4.1.11]

**[4.1.11] Create Backup Codes Template**
```html
# Task ID: MFA-011
# Dependencies: [4.1.6]
# Time: 15 minutes
```
- **Action**: Display backup codes
- **Output**: `apikeywallet-main/templates/mfa_backup_codes.html`
- **Content**: List of codes with download option
- **Validation**: Codes displayed
- **Parallel With**: [4.1.9], [4.1.10]

**[4.1.12] Add Disable MFA Route**
```python
# Task ID: MFA-012
# Dependencies: [4.1.8]
# Time: 15 minutes
```
- **Action**: Allow MFA removal
- **File**: `apikeywallet-main/auth_routes.py`
- **Add**: disable_mfa() function
- **Requires**: Password confirmation
- **Validation**: MFA can be disabled
- **Parallel With**: None

**[4.1.13] Test MFA Flow**
```python
# Task ID: MFA-013
# Dependencies: [4.1.6] through [4.1.12]
# Time: 20 minutes
```
- **Action**: End-to-end MFA testing
- **Tests**:
  - Enable MFA
  - Scan QR code with authenticator app
  - Login with MFA
  - Test backup code
  - Disable MFA
- **Validation**: All flows work
- **Parallel With**: None

Due to character limit, I'll commit this portion and continue with the remaining phases.
