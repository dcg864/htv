"""
ASCII art banner and tagline selection for HackBench.
"""

from __future__ import annotations

import random

HACKBENCH_BANNER = r"""
██╗  ██╗ █████╗  ██████╗██╗  ██╗██████╗ ███████╗███╗   ██╗ ██████╗██╗  ██╗
██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔════╝████╗  ██║██╔════╝██║ ██╔╝
███████║███████║██║     █████╔╝ ██████╔╝█████╗  ██╔██╗ ██║██║     █████╔╝
██╔══██║██╔══██║██║     ██╔═██╗ ██╔══██╗██╔══╝  ██║╚██╗██║██║     ██╔═██╗
██║  ██║██║  ██║╚██████╗██║  ██╗██║  ██║███████╗██║ ╚████║╚██████╗██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝
"""

TAGLINES = [
    "Payloads With A Lesson Plan.",
    "Offense Practice, Defense Insights.",
    "Classroom Drills For Curious Hackers.",
    "Red-Team Reps Without The Warrants.",
    "Lab-Grade Mischief, Teacher Approved.",
    "Because Exploits Deserve Office Hours.",
    "Tutorials For Trouble (The Legal Kind).",
    "Where Payloads Earn Their Diplomas.",
    "Hands-On Vulns, Zero Production Drama.",
    "Proof-of-Concepts With A Syllabus.",
]

_CURRENT_TAGLINE: str | None = None


def _pick_new_tagline() -> str:
    """Select a tagline, avoiding immediate repeats."""
    global _CURRENT_TAGLINE
    candidate = random.choice(TAGLINES)

    if _CURRENT_TAGLINE and len(TAGLINES) > 1:
        attempts = 0
        while candidate == _CURRENT_TAGLINE and attempts < 5:
            candidate = random.choice(TAGLINES)
            attempts += 1

    _CURRENT_TAGLINE = candidate
    return _CURRENT_TAGLINE


def get_current_tagline(force_refresh: bool = False) -> str:
    """
    Return the current tagline, optionally forcing a fresh selection.
    """
    if force_refresh or _CURRENT_TAGLINE is None:
        return _pick_new_tagline()
    return _CURRENT_TAGLINE


def display_banner() -> str:
    """Display the HackBench banner and a rotating tagline."""
    tagline = get_current_tagline(force_refresh=True)
    print(HACKBENCH_BANNER)
    underline = "═" * 86
    print(underline)
    print(f"⚡  {tagline}")
    print(underline)
    return tagline

LEGAL_WARNING = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                         HACKBENCH - LEGAL NOTICE                          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

⚠  WARNING: AUTHORIZED USE ONLY ⚠

This tool is designed EXCLUSIVELY for:
  ✓ Educational purposes in controlled lab environments
  ✓ Testing against YOUR OWN deliberately vulnerable applications (e.g., DVWA)
  ✓ Authorized security testing with explicit written permission

This tool is FORBIDDEN for:
  ✗ Unauthorized access to computer systems
  ✗ Testing production systems without permission
  ✗ Any malicious or illegal activity

═══════════════════════════════════════════════════════════════════════════

LEGAL DISCLAIMER:
Unauthorized access to computer systems is illegal under laws including but
not limited to:
  - Computer Fraud and Abuse Act (CFAA) - United States
  - Computer Misuse Act - United Kingdom
  - Similar laws in virtually every jurisdiction worldwide

The authors assume NO LIABILITY for misuse of this tool. By using this tool,
you agree that you have explicit authorization to test the target system.

═══════════════════════════════════════════════════════════════════════════
"""
def display_legal_warning():
    """Display the legal warning banner."""
    print(LEGAL_WARNING)
