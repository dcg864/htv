# Hack the Vibe

Community-driven build nights for creating practical, open-source security tools—fast. Each session is a **timeboxed, collaborative sprint** where we choose a scoped problem, assemble a minimal architecture, and ship an MVP by the end of the meeting.

---

## What is Hack the Vibe?

Hack the Vibe is a recurring, hands-on meetup format built around:

* **Sharpening skills** through small, shippable projects
* **Collective learning** across security, dev, and data roles
* **Low ceremony**: simple rules, safe targets, and a bias for action

Every event aims to produce:

* A working **prototype** (CLI or tiny service)
* Clear **docs** (README, quickstart, decision log)
* A short list of **follow‑ups** for the community

---

## Repo Layout

This repository stores **multiple Hack the Vibe events**, organized by **year/month**. Each event folder is a self-contained project with its own README, code, and docs.

```
.
├─ README.md                # You are here (concept + index)
├─ 2025/
│  └─ 11/
│     ├─ README.md          # Event-specific overview + quickstart
│     ├─ src/               # Source code for the 2025-11 project
│     ├─ docs/              # Agenda, decision log, prompts, etc.
│     ├─ tests/             # Tests for the event project
│     └─ runs/              # Run artifacts (gitignored if large)
└─ <future years>/
   └─ <month>/
```

> The first event in this repo is **2025/11**.

---

## Event Rhythm (2–3 hours)

1. **Kickoff & scope** (10–15m) – pick a problem, define guardrails
2. **Scaffold** (15–20m) – repo skeleton, roles, issues
3. **Build** (60–80m) – minimal feature set, tests, docs
4. **Polish** (20–30m) – quickstart, examples, demo script
5. **Demo & debrief** (10m) – lessons learned, next steps

---

## Principles

* **Safety first**: only scan permitted targets; non-intrusive defaults
* **Make it real**: runnable quickstart in the first PR
* **Observable by default**: save artifacts, log decisions
* **Swappable parts**: adapters and scanners are pluggable
* **Teach as you build**: pair, comment, and document

---

## How to Start a New Event

1. Create a folder using `YYYY/MM` (e.g., `2026/02`).
2. Copy the minimal scaffold from the most recent event.
3. Update the event `README.md` with:

   * Goal/MVP
   * Safety rules
   * Run of show & roles
   * Quickstart commands
4. Open seed Issues (scanner ideas, adapters, docs, CI).
5. Tag the event in the top-level README index (below).

---

## Event Index

* **2025/11** – AI-assisted security scan prototype (HTTP headers + model analysis). See `2025/11/`.

> Want to host a new session? Open a PR adding your `YYYY/MM` folder and an entry here.

---

## Contributing

PRs welcome. Keep changes atomic and well-documented. For event-night hacks, open a draft PR early and push often. Follow each event’s `CONTRIBUTING.md` where available.

---

## License

Unless stated otherwise inside an event folder, content in this repo is released under the **MIT License**.
