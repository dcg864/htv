# 2025/11 – Workshop Resources

This folder contains the **required** and **recommended** setup for tonight’s Hack the Vibe session. The safe target we’ll scan is the Docker image **`vulnerables/web-dvwa`** (Damn Vulnerable Web Application).

---

## 📦 Tools & Applications

### Required

* **Docker** (Desktop on Windows/macOS; Engine on Linux)

  * We use it to run the safe target `vulnerables/web-dvwa` locally.

* **Python 3.11+**

  * Cross‑platform (Windows/Linux/macOS) and our scanner is Python‑based.

### Recommended

* **Visual Studio Code** (or your preferred IDE)

  * Helpful extensions: Python, Docker.
* **AI assistant plugin** of your choice (e.g., **ChatGPT** extension for VS Code)

  * Great for boilerplate, docstrings, unit‑test scaffolding, and prompt iteration.

> If you prefer another editor (PyCharm, Vim, etc.), that’s fine—VS Code is simply easy for newcomers.

---

## ✅ Pre‑flight Checklist

* [ ] Docker installed and can run `docker run hello-world`
* [ ] Python ≥ 3.11 on PATH (`python -V` or `py -V` on Windows)
* [ ] A terminal you’re comfortable with (PowerShell, Windows Terminal, macOS Terminal, Linux shell)

---

## 🧪 Run the Safe Target (DVWA) via Docker

The DVWA image exposes a web app intentionally designed for learning and testing.

### Option A: One‑liner (simple)

```bash
# maps container port 80 -> host 8080
# WARNING: runs intentionally vulnerable software; keep it local only
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
```

Open [http://localhost:8080](http://localhost:8080) in your browser. The default credentials are shown on DVWA’s home page once it’s initialized (set the DB in the setup screen).

### Option B: docker-compose (repeatable)

Create `docker-compose.yml` in `2025/11/`:

```yaml
version: "3.8"
services:
  dvwa:
    image: vulnerables/web-dvwa
    container_name: dvwa
    ports:
      - "8080:80"
    restart: unless-stopped
```

Run:

```bash
docker compose up -d
# to stop and remove
# docker compose down
```

---

## 🐍 Python Environment Setup

From the `2025/11/` folder (or project root for the day’s code):

```bash
# Create and activate a virtual environment
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install project deps once the repo code is pulled
dpip install -r requirements.txt
```

> Windows tip: If `python` opens the Microsoft Store, try `py -3.11 -m venv .venv`.

---

## 🛠️ Minimal Scanner Smoke Test

Once the group repo is cloned (or after you copy in the scaffold), try:

```bash
python cli.py scan --url http://localhost:8080 --analyze
```

You should see raw findings (headers/status) and an AI analysis block if enabled.

---

## 🧩 VS Code Setup (Optional but Helpful)

1. Install **Python** and **Docker** extensions.

2. (Optional) Install the ChatGPT **Codex** VS Code extension or your preferred AI tool and authenticate with your account. Use it to:

   * Generate test cases
   * Draft docstrings and comments
   * Iterate on prompt templates for analysis

---

## 🧯 Safety Reminders

* Keep DVWA **local only** and do not expose it to the internet.
* Do not scan third‑party systems without explicit permission.
* Our MVP performs **non‑intrusive GET requests**; advanced tests require a group review.

---

## 📁 Suggested File Adds for `2025/11/`

```
2025/
└─ 11/
   ├─ docker-compose.yml           # optional convenience
   └─ docs/
      └─ workshop-resources.md     # this file
```

---

## 📝 Troubleshooting

* **Port in use (8080):** change to `-p 8081:80` and visit [http://localhost:8081](http://localhost:8081)
* **Docker permission denied (Linux):** add user to `docker` group and re‑login
* **Python SSL issues on Windows:** ensure latest Python and `pip install certifi`

---

## Next Steps Tonight

* Confirm DVWA reachable at `http://localhost:8080`
* Run the minimal scan against it
* Start adding scanners (TLS, cookies, simple fingerprint) and refine the AI analysis prompt
