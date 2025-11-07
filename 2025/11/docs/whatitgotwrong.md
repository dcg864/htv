# What It Got Wrong (And How We Repaired It)

| # | Concern | Remediation |
|---|---------|-------------|
| 1 | **No proof of exploits succeeding** | `hackbench/modules/reflected.py` and `hackbench/modules/stored.py` now print the HTTP status, key headers, and a body excerpt with the payload highlighted via `<<PAYLOAD>>` markers every time a payload hits (or gets filtered). |
| 2 | **Missing cURL walk-throughs** | Each payload attempt emits two ready-to-run cURL commands (direct + `--proxy http://127.0.0.1:8080`) so attendees can reproduce traffic manually or in Burp. |
| 3 | **Burp request import** | `hackbench/utils/request_recorder.py` captures every prepared request and `hackbench/cli.py` reports the timestamped `logs/hackbench_burp_replay_*.txt` file so you can paste raw requests into Burp. |
| 4 | **No clarity on injection surface** | Both XSS modules now log an “Injection breakdown” block that spells out the HTTP method, form/query fields, and whether the payload lands in headers or the HTML body. |
| 5 | **Log noise in Git** | Added a repository-level `.gitignore` that excludes every `logs/` directory and loose `*.log` files so operational evidence stays local. |
| 6 | **General “plz fix” catch-all** | Addressed by implementing items 1–5 and 7–12 below; the lab now records evidence, reproductions, and prevention steps automatically. |
| 7 | **Generic Reflected XSS remediation tips** | `hackbench/explanations/text_blocks.py` now lists concrete mitigations (context-aware encoders, CSP examples, cookie flags, regression testing). |
| 8 | **Stored XSS lacked attribution** | Each guestbook entry includes the request’s User-Agent inside an HTML comment so blue teams can trace which student posted it (`hackbench/modules/stored.py`). |
| 9 | **DOM lab needed Klingon option** | `hackbench/modules/dom_based.py` now demonstrates a payload that injects a Klingon (`tlh`) option into the dropdown so students can literally select the new language. |
|10 | **Need manual DOM instructions** | The DOM module includes step-by-step, browser-only guidance (no Selenium) covering dropdown interaction, DevTools inspection, and Burp interception. |
|11 | **Weak ASCII art** | `hackbench/utils/banner.py` ships a full-width block-art banner plus the legal warning, making the intro slide-worthy. |
|12 | **Static tagline** | The same module now cycles through ten fresh taglines on every run; `hackbench/cli.py` echoes whichever line appeared so recordings capture it. |
