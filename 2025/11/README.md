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

## Contributing (tonight)

Keep PRs small; push drafts early.

Add/update docs/decision-log.md for any notable choice.

Prefer structured JSON returns; clear logs over cleverness.

## Troubleshooting

Port 8080 in use → change mapping (-p 8081:80) and use http://localhost:8081

Docker permission denied (Linux) → add user to docker group, re-login

python vs py on Windows → try py -3.11 and .\.venv\Scripts\Activate.ps1

SSL/cert errors on Windows → pip install certifi and retry

## References

Workshop tools & tips: docs/workshop-resources.md

Safety rules: docs/safe-scanning.md

Agenda: docs/agenda.md

Decision log (update during session): docs/decision-log.md