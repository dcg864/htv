# Installation Guide - HackBench

Complete installation instructions for Windows, macOS, and Linux.

---

## Prerequisites

### 1. Python 3.10+

Check your Python version:
```bash
python --version
```

If you need to install Python:
- **Windows**: https://www.python.org/downloads/
- **macOS**: `brew install python3` or python.org
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### 2. pip Package Manager

Usually comes with Python. Verify:
```bash
pip --version
```

---

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd c:\Users\eric2\Documents\GitHub\htv\2025\11\hackbench
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - HTTP library for web requests
- `beautifulsoup4` - HTML parsing
- `colorama` - Cross-platform colored terminal output
- `pytest` - Unit testing framework

### Step 3: Verify Installation

Run the setup check script:
```bash
python setup_check.py
```

Expected output:
```
======================================================================
HackBench - Setup Verification
======================================================================
Checking Python version... ✓ Python 3.13.9

Checking dependencies...
  ✓ HTTP library (requests)
  ✓ BeautifulSoup (HTML parsing) (bs4)
  ✓ Terminal colors (colorama)

Checking project structure...
  ✓ core/auth.py
  ✓ core/http_client.py
  [... all files ...]

Checking DVWA connectivity (optional)...
  ⚠ DVWA not reachable: [Errno 111] Connection refused
     This is OK if you haven't started DVWA yet

======================================================================
SUMMARY
======================================================================
✓ Python version: PASS
✓ Dependencies: PASS
✓ Project structure: PASS
⚠ DVWA connectivity: WARNING
======================================================================
✓ ALL CHECKS PASSED!
```

### Step 4: Set Up DVWA

You need a target DVWA instance. Choose one method:

#### Option A: Docker (Recommended)

```bash
# Pull and run DVWA
docker run -d -p 80:80 vulnerables/web-dvwa

# Wait 30 seconds for startup, then visit:
# http://localhost/setup.php

# Click "Create / Reset Database"
# Login with: admin / password
```

#### Option B: Manual Installation

1. Download DVWA: https://github.com/digininja/DVWA
2. Follow installation guide in DVWA's README
3. Complete database setup at `/setup.php`
4. Login with default credentials

### Step 5: Verify DVWA Connection

```bash
python setup_check.py
```

Now you should see:
```
Checking DVWA connectivity (optional)...
  ✓ DVWA detected at http://localhost
```

---

## Troubleshooting Installation

### Issue: "python: command not found"

**Solution**: Try `python3` instead of `python`
```bash
python3 --version
python3 setup_check.py
```

### Issue: "pip: command not found"

**Solution**: Try `pip3` or install pip
```bash
# Try pip3
pip3 install -r requirements.txt

# Or install pip
python -m ensurepip --upgrade
```

### Issue: "Permission denied" (Linux/macOS)

**Solution**: Use user installation
```bash
pip install --user -r requirements.txt
```

### Issue: Dependencies fail to install

**Solution**: Upgrade pip first
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: UnicodeEncodeError on Windows

**Solution**: Set console to UTF-8
```cmd
chcp 65001
python setup_check.py
```

Or use Windows Terminal instead of cmd.exe

---

## Virtual Environment (Recommended)

For isolated dependency management:

### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies in Virtual Environment

```bash
pip install -r requirements.txt
```

### Deactivate When Done

```bash
deactivate
```

---

## Verifying Everything Works

### Quick Test Run

```bash
python -m hackbench --help
```

Expected: Help text displays with all options

### Full Test (Requires DVWA)

```bash
python -m hackbench --mode reflected --no-interactive
```

Expected: Tool runs, authenticates with DVWA, attempts reflected XSS

---

## Post-Installation

### Project is Ready When:
- ✅ `python setup_check.py` shows all checks passed
- ✅ `python -m hackbench --help` displays help text
- ✅ DVWA is accessible at http://localhost
- ✅ No import errors when running the tool

### Next Steps:
1. Read [QUICKSTART.md](QUICKSTART.md) for first run
2. Read [README.md](README.md) for detailed usage
3. Start with: `python -m hackbench --mode reflected`

---

## Dependencies Reference

| Package | Version | Purpose |
|---------|---------|---------|
| requests | ≥2.31.0 | HTTP requests to DVWA |
| beautifulsoup4 | ≥4.12.0 | HTML parsing and analysis |
| colorama | ≥0.4.6 | Cross-platform colored output |
| pytest | ≥7.4.0 | Unit testing framework |

---

## Uninstallation

To remove the tool and dependencies:

```bash
# If using virtual environment
deactivate
rm -rf venv  # or rmdir /s venv on Windows

# Uninstall global dependencies (optional)
pip uninstall requests beautifulsoup4 colorama pytest

# Remove project directory
cd ..
rm -rf hackbench  # or rmdir /s hackbench on Windows
```

---

## Need Help?

1. Run setup check: `python setup_check.py`
2. Check [QUICKSTART.md](QUICKSTART.md)
3. Read [README.md](README.md) Troubleshooting section
4. Verify DVWA is running: http://localhost

---

**Installation complete! Ready to learn XSS!** 🎓
