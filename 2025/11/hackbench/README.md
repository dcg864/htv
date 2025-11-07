# HackBench

An **interactive, educational Python CLI tool** for learning and demonstrating Cross-Site Scripting (XSS) vulnerabilities against [DVWA (Damn Vulnerable Web Application)](https://github.com/digininja/DVWA).

## ⚠️ Legal Notice

**AUTHORIZED USE ONLY**

This tool is designed **exclusively** for:
- ✅ Educational purposes in controlled lab environments
- ✅ Testing against deliberately vulnerable applications (e.g., DVWA)
- ✅ Authorized security testing with explicit written permission

**NEVER** use this tool against:
- ❌ Production systems without authorization
- ❌ Systems you do not own or have explicit permission to test
- ❌ Any unauthorized targets

**Unauthorized access to computer systems is illegal.** The authors assume no liability for misuse.

---

## 🎯 Features

### Three XSS Types Covered

1. **Reflected XSS** - Demonstrates how malicious scripts are reflected from HTTP requests
2. **Stored XSS** - Shows persistent XSS attacks via database storage
3. **DOM-Based XSS** - Explains client-side JavaScript vulnerabilities (demonstration mode)

### Educational Focus

- **Step-by-step guidance** - Walks through each attack phase with explanations
- **Interactive learning** - Requires user approval before executing exploits
- **Detailed explanations** - Explains *what*, *why*, and *how* at each step
- **Failure analysis** - When payloads fail, explains why and suggests alternatives
- **OWASP references** - Links concepts to industry-standard security knowledge

### Dual Logging System

- **Operational logs** - Technical details, HTTP requests, debugging info
- **Educational logs** - Human-readable learning narrative for review

### Safety Features

- **Target validation** - Only runs against localhost/private IPs by default
- **Mandatory authorization** - Requires explicit user confirmation
- **DVWA verification** - Checks target is actually DVWA before attacking
- **Authentication handling** - Manages DVWA login and CSRF tokens automatically

---

## 📋 Prerequisites

### 1. Python Requirements

- Python 3.10 or higher
- pip package manager

### 2. DVWA Setup

You need a running instance of DVWA. The easiest way is using Docker:

#### Option A: Docker (Recommended)

```bash
# Pull and run DVWA
docker run -d -p 80:80 vulnerables/web-dvwa

# Access DVWA at http://localhost
# Default credentials: admin / password
```

#### Option B: Manual Installation

Follow the [official DVWA installation guide](https://github.com/digininja/DVWA#installation).

### 3. DVWA Initial Setup

1. Navigate to `http://localhost/setup.php`
2. Click "Create / Reset Database"
3. Login with credentials: `admin` / `password`
4. (Optional) Set security level to "Low" for initial learning

---

## 🚀 Installation

### Clone or Download

```bash
cd c:\Users\eric2\Documents\GitHub\htv\2025\11\hackbench
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📖 Usage

### Basic Usage

Run all XSS modules interactively:

```bash
python -m hackbench --mode all
```

### Module Selection

Run specific XSS types:

```bash
# Reflected XSS only
python -m hackbench --mode reflected

# Stored XSS only
python -m hackbench --mode stored

# DOM-based XSS only (demonstration)
python -m hackbench --mode dom
```

### Custom Target

Target DVWA on a custom port:

```bash
python -m hackbench --host localhost --port 8080
```

### Non-Interactive Mode

Auto-approve all steps (useful for demos):

```bash
python -m hackbench --mode all --no-interactive
```

### Custom Credentials

```bash
python -m hackbench --username admin --password mypassword
```

### Set Security Level

Automatically set DVWA security level before testing:

```bash
python -m hackbench --security-level low
```

### Full Command Reference

```
python -m hackbench [OPTIONS]

Options:
  --mode {reflected,stored,dom,all}
                        XSS attack type to demonstrate (default: all)
  --host HOST           Target hostname (default: localhost)
  --port PORT           Target port (default: 80)
  --https               Use HTTPS instead of HTTP
  --username USERNAME   DVWA username (default: admin)
  --password PASSWORD   DVWA password (default: password)
  --security-level {low,medium,high,impossible}
                        Set DVWA security level before testing
  --no-interactive      Run without pausing for approval
  --log-dir LOG_DIR     Directory for log files (default: logs)
  --confirm-target      Explicitly confirm target authorization
  --skip-banner         Skip safety banner (not recommended)
```

---

## 📂 Project Structure

```
hackbench/
├── __init__.py              # Package initialization
├── __main__.py              # Entry point for python -m
├── cli.py                   # Command-line interface
├── requirements.txt         # Python dependencies
├── README.md                # This file
│
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── auth.py              # DVWA authentication & session management
│   ├── http_client.py       # HTTP wrapper with logging
│   ├── logger.py            # Dual logging system
│   └── target_config.py     # Target configuration & validation
│
├── modules/                 # XSS attack modules
│   ├── __init__.py
│   ├── reflected.py         # Reflected XSS module
│   ├── stored.py            # Stored XSS module
│   └── dom_based.py         # DOM XSS demonstration module
│
├── explanations/            # Educational content
│   ├── __init__.py
│   └── text_blocks.py       # OWASP-based explanations
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── validators.py        # Target validation, safety checks
│
└── logs/                    # Generated log files (created at runtime)
    ├── xss_lab_operational_YYYYMMDD_HHMMSS.log
    └── xss_lab_explained_YYYYMMDD_HHMMSS.log
```

---

## 🎓 Learning Path

### Recommended Order

1. **Start with Reflected XSS** (`--mode reflected`)
   - Simplest to understand
   - See immediate cause-and-effect
   - Learn about URL-based attacks

2. **Progress to Stored XSS** (`--mode stored`)
   - Understand persistence
   - See multi-user impact
   - Learn about database-backed attacks

3. **Finish with DOM XSS** (`--mode dom`)
   - Most advanced concept
   - Client-side only attacks
   - Requires manual browser testing

### Security Levels

Try each module at different DVWA security levels:

- **Low** - No protections (educational starting point)
- **Medium** - Basic filtering (learn evasion techniques)
- **High** - Strong protections (understand robust defenses)
- **Impossible** - Properly secured (goal state for real applications)

---

## 📝 Logs

Each session generates two log files in the `logs/` directory:

### 1. Operational Log
**File**: `xss_lab_operational_YYYYMMDD_HHMMSS.log`

Contains technical details:
- HTTP requests and responses
- Status codes and errors
- Authentication flow
- Debugging information

### 2. Educational Log
**File**: `xss_lab_explained_YYYYMMDD_HHMMSS.log`

Contains learning narrative:
- Step-by-step walkthrough
- Payload explanations
- Success/failure analysis
- Prevention techniques

**Tip**: Review educational logs after sessions to reinforce learning.

---

## 🛡️ Security Levels & Expected Behavior

### Low Security
- No input validation or output encoding
- All payloads should succeed
- Best for initial learning

### Medium Security
- Basic filtering (blocks `<script>` tags)
- Alternative payloads needed (e.g., `<img>`, `<svg>`)
- Teaches filter evasion concepts

### High Security
- Strong filtering and output encoding
- Most payloads blocked
- Demonstrates proper defenses

### Impossible Security
- Comprehensive protections (CSP, encoding, validation)
- Payloads should fail
- Shows gold-standard security

---

## 🔧 Troubleshooting

### "Target unreachable" Error

**Solution**: Verify DVWA is running
```bash
# Check if DVWA is accessible
curl http://localhost

# For Docker, check container status
docker ps
```

### "Target does not appear to be DVWA"

**Solution**: Verify URL and ensure DVWA setup is complete
- Visit `http://localhost/setup.php` and complete database setup
- Check that login page is accessible at `http://localhost/login.php`

### "Authentication failed"

**Solution**: Verify credentials
- Default DVWA credentials: `admin` / `password`
- If changed, use `--username` and `--password` flags

### "Payload not found in response"

**Solution**: Security level may be too high
```bash
# Set security to low
python -m hackbench --security-level low --mode reflected
```

### Permission Issues (Non-localhost targets)

**Solution**: Use `--confirm-target` flag
```bash
python -m hackbench --host 192.168.1.100 --confirm-target
```

---

## 🧪 Example Session

```bash
$ python -m hackbench --mode reflected

╔═══════════════════════════════════════════════════════════════════════════╗
║                         XSS LAB TOOL - LEGAL NOTICE                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

⚠  WARNING: AUTHORIZED USE ONLY ⚠
[Safety banner displayed...]

Do you confirm the above? Type 'I AGREE' to proceed: I AGREE

======================================================================
XSS LAB TOOL - Educational XSS Demonstration
======================================================================
Target: http://localhost
Mode: reflected
Interactive: True
======================================================================

Running preflight checks...
✓ All preflight checks passed

Authenticating with DVWA...
✓ DVWA detected (version: 1.10)
✓ Successfully authenticated with DVWA
Current DVWA security level: low

======================================================================
REFLECTED XSS MODULE
======================================================================

[Step 1] Understanding the Target
We're going to examine DVWA's Reflected XSS page...

Proceed to examine the vulnerable page? [y/N]: y

[Step 2] Testing Normal Behavior
First, let's send a normal, non-malicious input...

✓ Input 'TestUser123' was reflected in the response
This means the server is taking our input and including it directly in the HTML.

Proceed to attempt XSS payloads? [y/N]: y

[... educational walkthrough continues ...]
```

---

## 📚 References & Further Learning

### OWASP Resources
- [OWASP XSS Overview](https://owasp.org/www-community/attacks/xss/)
- [XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [XSS Filter Evasion Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html)

### Additional Practice
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/cross-site-scripting)
- [HackTheBox XSS Challenges](https://www.hackthebox.com/)
- [TryHackMe XSS Rooms](https://tryhackme.com/)

---

## 🤝 Contributing

This is an educational tool. Contributions that enhance learning value are welcome:
- Improved explanations
- Additional payloads with educational context
- Support for other vulnerable labs
- Enhanced error messages

---

## 📄 License

This tool is provided for educational purposes only. Use at your own risk.

---

## 👥 Authors

Security Education Lab

---

## 🙏 Acknowledgments

- **DVWA Team** - For providing an excellent vulnerable testing platform
- **OWASP** - For comprehensive web security documentation
- **Security Education Community** - For promoting ethical hacking education

---

**Remember**: With great power comes great responsibility. Use this knowledge to build more secure applications, not to harm others.
