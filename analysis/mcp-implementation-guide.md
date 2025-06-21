# API Key Wallet - MCP Server Implementation Guide

## Overview

This guide provides a detailed technical roadmap for transforming API Key Wallet into a Model Context Protocol (MCP) server, enabling AI assistants like Claude to securely manage API keys.

---

## MCP Architecture Design

### Server Configuration
```json
{
  "name": "apikeywallet-mcp",
  "version": "1.0.0",
  "description": "Secure API key management for AI assistants",
  "transport": ["stdio"],
  "capabilities": {
    "resources": true,
    "tools": true,
    "prompts": true
  }
}
```

### Core Components

```
apikeywallet-mcp/
├── src/
│   ├── server.ts          # MCP server entry point
│   ├── handlers/          # Request handlers
│   │   ├── resources.ts   # Resource handlers
│   │   ├── tools.ts       # Tool implementations
│   │   └── prompts.ts     # Prompt templates
│   ├── services/          # Business logic
│   │   ├── keyManager.ts  # Key management service
│   │   ├── auth.ts        # Authentication service
│   │   └── encryption.ts  # Encryption utilities
│   └── types/             # TypeScript definitions
├── config/
│   └── mcp-config.json    # Server configuration
└── package.json
```

---

## MCP Resources Implementation

### 1. List Keys Resource
```typescript
{
  "uri": "apikey://list",
  "name": "List API Keys",
  "description": "View all stored API keys with metadata",
  "mimeType": "application/json"
}
```

**Response Format:**
```json
{
  "keys": [
    {
      "id": "key_123",
      "name": "OpenAI Production",
      "category": "AI Services",
      "created": "2025-01-15T10:00:00Z",
      "lastUsed": "2025-01-20T15:30:00Z",
      "expiresAt": "2025-07-15T10:00:00Z",
      "status": "active"
    }
  ],
  "total": 15,
  "categories": ["AI Services", "Databases", "Third-party APIs"]
}
```

### 2. Key Details Resource
```typescript
{
  "uri": "apikey://details/{keyId}",
  "name": "API Key Details",
  "description": "Detailed information about a specific key",
  "mimeType": "application/json"
}
```

### 3. Security Audit Resource
```typescript
{
  "uri": "apikey://audit",
  "name": "Security Audit Report",
  "description": "Security analysis of stored keys",
  "mimeType": "application/json"
}
```

---

## MCP Tools Implementation

### 1. Create Key Tool
```typescript
{
  "name": "create_api_key",
  "description": "Store a new API key securely",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": { 
        "type": "string", 
        "description": "Display name for the key" 
      },
      "key": { 
        "type": "string", 
        "description": "The API key value" 
      },
      "category": { 
        "type": "string", 
        "description": "Category for organization" 
      },
      "expiresIn": { 
        "type": "number", 
        "description": "Expiration in days (optional)" 
      }
    },
    "required": ["name", "key"]
  }
}
```

### 2. Retrieve Key Tool
```typescript
{
  "name": "get_api_key",
  "description": "Securely retrieve an API key",
  "inputSchema": {
    "type": "object",
    "properties": {
      "keyId": { 
        "type": "string", 
        "description": "ID of the key to retrieve" 
      },
      "reason": { 
        "type": "string", 
        "description": "Reason for access (audit trail)" 
      }
    },
    "required": ["keyId", "reason"]
  }
}
```

### 3. Rotate Key Tool
```typescript
{
  "name": "rotate_api_key",
  "description": "Rotate an existing API key",
  "inputSchema": {
    "type": "object",
    "properties": {
      "keyId": { "type": "string" },
      "newKey": { "type": "string" },
      "deprecateOld": { 
        "type": "boolean", 
        "description": "Keep old key for grace period" 
      }
    },
    "required": ["keyId", "newKey"]
  }
}
```

### 4. Delete Key Tool
```typescript
{
  "name": "delete_api_key",
  "description": "Permanently delete an API key",
  "inputSchema": {
    "type": "object",
    "properties": {
      "keyId": { "type": "string" },
      "confirmation": { 
        "type": "string", 
        "description": "Type 'DELETE' to confirm" 
      }
    },
    "required": ["keyId", "confirmation"]
  }
}
```

### 5. Search Keys Tool
```typescript
{
  "name": "search_api_keys",
  "description": "Search for keys by name or category",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "category": { "type": "string" },
      "status": { 
        "type": "string", 
        "enum": ["active", "expired", "deprecated"] 
      }
    }
  }
}
```

---

## MCP Prompts Implementation

### 1. New Project Setup
```typescript
{
  "name": "setup_new_project",
  "description": "Guide through setting up API keys for a new project",
  "arguments": [
    {
      "name": "projectName",
      "description": "Name of your project",
      "required": true
    }
  ],
  "template": `
    I'll help you set up API keys for {{projectName}}. 
    
    Common services you might need:
    - OpenAI/Anthropic (AI services)
    - Database connections
    - Third-party APIs
    - Cloud services
    
    Which services will {{projectName}} use?
  `
}
```

### 2. Security Audit
```typescript
{
  "name": "security_audit",
  "description": "Perform a security audit of stored keys",
  "template": `
    I'll analyze your API keys for security issues:
    
    1. Checking for expired keys
    2. Identifying unused keys
    3. Finding keys without expiration dates
    4. Detecting weak key patterns
    5. Reviewing access logs
    
    Would you like a full audit or focus on specific concerns?
  `
}
```

### 3. Key Rotation Reminder
```typescript
{
  "name": "rotation_reminder",
  "description": "Set up key rotation reminders",
  "arguments": [
    {
      "name": "frequency",
      "description": "How often to rotate (days)",
      "required": false
    }
  ]
}
```

---

## Security Implementation

### Authentication Flow
```typescript
interface AuthConfig {
  method: 'oauth' | 'api_key' | 'local';
  credentials: {
    clientId?: string;
    clientSecret?: string;
    apiKey?: string;
    localPath?: string;
  };
}

class MCPAuthService {
  async authenticate(config: AuthConfig): Promise<Session> {
    // Implement secure authentication
    // Store session with encryption
    // Set appropriate TTL
  }
}
```

### Encryption Strategy
```typescript
class EncryptionService {
  private masterKey: Buffer;
  
  async encryptKey(plaintext: string): Promise<EncryptedKey> {
    // Use AES-256-GCM encryption
    // Generate unique IV per key
    // Include authentication tag
  }
  
  async decryptKey(encrypted: EncryptedKey): Promise<string> {
    // Verify authentication tag
    // Decrypt with stored IV
    // Audit access attempt
  }
}
```

### Access Control
```typescript
interface AccessPolicy {
  user: string;
  permissions: Permission[];
  restrictions: {
    ipWhitelist?: string[];
    timeWindow?: TimeWindow;
    rateLimit?: RateLimit;
  };
}
```

---

## Integration Examples

### Claude Desktop Configuration
```json
{
  "mcpServers": {
    "apikeywallet": {
      "command": "node",
      "args": ["/path/to/apikeywallet-mcp/dist/server.js"],
      "env": {
        "APIKEYWALLET_AUTH": "your-auth-token",
        "APIKEYWALLET_ENDPOINT": "https://api.apikeywallet.com"
      }
    }
  }
}
```

### Usage Examples

**Storing a new key:**
```
Human: Store my new OpenAI API key for the ChatBot project

Claude: I'll help you store that API key securely. I'll need:
1. The API key value
2. A name for easy reference
3. Optional expiration date

Please provide the API key, and I'll store it encrypted in your vault.
```

**Retrieving a key:**
```
Human: I need the Stripe API key for deployment

Claude: I'll retrieve the Stripe API key for you. For security, I need to log this access. 
What's the reason for accessing this key?

[After reason provided]
Here's your Stripe API key: sk_live_...
This access has been logged for audit purposes.
```

**Security audit:**
```
Human: Run a security audit on my API keys

Claude: I'll perform a comprehensive security audit of your API keys:

📊 Security Audit Report:
- Total Keys: 23
- ⚠️ Expired: 3 keys need rotation
- ⏰ Expiring Soon: 5 keys (next 30 days)
- ❌ No Expiration Set: 8 keys
- ✅ Secure: 7 keys

Recommendations:
1. Rotate the 3 expired keys immediately
2. Set expiration dates for the 8 keys without them
3. Plan rotation for keys expiring soon

Would you like me to help with any of these actions?
```

---

## Development Timeline

### Week 1-2: Core MCP Server
- [ ] Set up TypeScript project structure
- [ ] Implement stdio transport
- [ ] Create basic resource handlers
- [ ] Implement authentication

### Week 3-4: Tools Implementation
- [ ] Implement all CRUD tools
- [ ] Add search functionality
- [ ] Create audit tools
- [ ] Implement key rotation

### Week 5-6: Security & Testing
- [ ] Enhance encryption
- [ ] Add comprehensive logging
- [ ] Write test suite
- [ ] Security audit

### Week 7-8: Polish & Launch
- [ ] Create documentation
- [ ] Build demo videos
- [ ] Submit to MCP registry
- [ ] Launch beta program

---

## Monetization for MCP

### Pricing Model
1. **Free Tier**
   - 10 keys
   - Basic tools
   - Community support

2. **Pro Tier** ($9/month)
   - Unlimited keys
   - All tools & prompts
   - Priority support
   - Audit logs

3. **Team Tier** ($29/month)
   - Multi-user support
   - Shared workspaces
   - Advanced permissions
   - API access

### Distribution Strategy
1. **MCP Registry**: Official Anthropic registry
2. **NPM Package**: Easy installation
3. **Docker Image**: One-command deployment
4. **Cloud Hosted**: Managed service option

---

## Success Metrics

### Technical KPIs
- Response time < 100ms
- 99.9% uptime
- Zero security breaches
- < 1% error rate

### Business KPIs
- 1,000 installations in 3 months
- 100 paying customers in 6 months
- 50% month-over-month growth
- 4.5+ star rating

---

## Competitive Advantages

1. **First Native MCP Key Manager**: First-mover advantage
2. **AI-First Design**: Built specifically for AI workflows
3. **Simple Pricing**: No per-user traps
4. **Developer Focus**: Built by developers, for developers
5. **Open Source Core**: Trust through transparency

---

## Next Steps

1. **Validate with Anthropic Community**
   - Post in MCP discussions
   - Get feedback on design
   - Find beta testers

2. **Build MVP**
   - Focus on core tools first
   - Launch with 5 essential features
   - Iterate based on feedback

3. **Create Content**
   - Tutorial videos
   - Blog posts
   - Documentation
   - Demo projects

This MCP transformation positions API Key Wallet as the go-to solution for AI-assisted development, creating a new category in the secrets management space.