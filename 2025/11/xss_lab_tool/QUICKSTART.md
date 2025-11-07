# Quick Start Guide - XSS Lab Tool

Get up and running in **5 minutes**!

## Step 1: Start DVWA (2 minutes)

### Using Docker (Easiest)
```bash
docker run -d -p 80:80 vulnerables/web-dvwa
```

Wait ~30 seconds for DVWA to start, then:

1. Visit: http://localhost/setup.php
2. Click: **"Create / Reset Database"**
3. Login with: `admin` / `password`

✅ DVWA is ready!

---

## Step 2: Install Dependencies (1 minute)

```bash
cd c:\Users\eric2\Documents\GitHub\htv\2025\11\xss_lab_tool
pip install -r requirements.txt
```

---

## Step 3: Run Your First Attack! (2 minutes)

### Try Reflected XSS

**Option A - Using run.py (EASIEST):**
```bash
cd c:\Users\eric2\Documents\GitHub\htv\2025\11\xss_lab_tool
python run.py --mode reflected
```

**Option B - Run as module (from parent directory):**
```bash
cd c:\Users\eric2\Documents\GitHub\htv\2025\11
python -m xss_lab_tool --mode reflected
```

**What happens:**
1. Safety banner appears → Type `I AGREE`
2. Tool authenticates with DVWA
3. Step-by-step walkthrough begins
4. At each prompt, type `y` to continue
5. Watch as XSS payloads are tested and explained!

---

## Example Commands

**Note**: Run from parent directory (`cd c:\Users\eric2\Documents\GitHub\htv\2025\11`) or use `python cli.py` from inside xss_lab_tool/

### Run all three XSS types
```bash
python -m xss_lab_tool --mode all
```

### Non-interactive mode (auto-approve everything)
```bash
python -m xss_lab_tool --mode all --no-interactive
```

### Set DVWA to low security first
```bash
python -m xss_lab_tool --security-level low --mode reflected
```

---

## Troubleshooting

### "Target unreachable"
**Fix:** Check DVWA is running
```bash
curl http://localhost
```

### "Authentication failed"
**Fix:** Complete DVWA setup
- Visit http://localhost/setup.php
- Click "Create / Reset Database"

### "Payload not found"
**Fix:** Lower DVWA security level
- Login to DVWA
- Click "DVWA Security"
- Set to "Low"
- OR use: `--security-level low` flag

---

## What to Learn

1. **Reflected XSS** - URL-based attacks
2. **Stored XSS** - Database persistence attacks
3. **DOM XSS** - Client-side JavaScript attacks

Each module explains:
- ✅ How the vulnerability works
- ✅ Why it's dangerous
- ✅ How to prevent it

---

## Next Steps

After completing the basic runs:

1. **Try different security levels**
   ```bash
   python -m xss_lab_tool --security-level medium --mode reflected
   ```

2. **Review the logs**
   - Check `logs/xss_lab_explained_*.log` for learning summary
   - Check `logs/xss_lab_operational_*.log` for technical details

3. **Read the full README.md** for advanced usage

---

## Quick Reference Card

| Command | Description |
|---------|-------------|
| `--mode reflected` | Reflected XSS only |
| `--mode stored` | Stored XSS only |
| `--mode dom` | DOM XSS demonstration |
| `--mode all` | Run all three (default) |
| `--no-interactive` | Auto-approve all steps |
| `--security-level low` | Set DVWA security |
| `--help` | Show all options |

---

**You're ready! Start with:**
```bash
cd c:\Users\eric2\Documents\GitHub\htv\2025\11
python -m xss_lab_tool --mode reflected
```
