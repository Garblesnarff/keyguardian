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

Should I continue with the remaining phases?
