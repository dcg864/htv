# Hack the Vibe — 2025/11

Minimal, safe, AI-assisted web scanner you can run locally against DVWA.

- **Target:** `vulnerables/web-dvwa` (Docker)
- **Language:** Python 3.11+
- **MVP:** CLI scan → raw findings → optional AI summary → JSON in `runs/`

---

## Requirements
- **Required:** Docker, Python 3.11+
- **Recommended:** VS Code (Python & Docker extensions), an AI assistant (e.g., ChatGPT for VS Code)

---

## Start the DVWA target
```bash
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
# Open: http://localhost:8080  (run the setup/init page once)
```

