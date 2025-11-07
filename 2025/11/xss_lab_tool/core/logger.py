"""
Dual logging system for XSS Lab Tool.
Provides both operational (debug/trace) and educational (learning artifact) logs.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class DualLogger:
    """
    Manages two separate log streams:
    1. Operational log - Technical details, debugging info
    2. Educational log - Human-readable learning narrative
    """

    def __init__(self, log_dir: str = "logs"):
        """
        Initialize dual logger.

        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Operational logger - technical details
        self.operational_logger = logging.getLogger("xss_lab.operational")
        self.operational_logger.setLevel(logging.DEBUG)

        op_handler = logging.FileHandler(
            self.log_dir / f"xss_lab_operational_{timestamp}.log",
            encoding='utf-8'
        )
        op_handler.setLevel(logging.DEBUG)
        op_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        op_handler.setFormatter(op_formatter)
        self.operational_logger.addHandler(op_handler)

        # Educational logger - learning narrative
        self.educational_logger = logging.getLogger("xss_lab.educational")
        self.educational_logger.setLevel(logging.INFO)

        edu_handler = logging.FileHandler(
            self.log_dir / f"xss_lab_explained_{timestamp}.log",
            encoding='utf-8'
        )
        edu_handler.setLevel(logging.INFO)
        edu_formatter = logging.Formatter('%(message)s')
        edu_handler.setFormatter(edu_formatter)
        self.educational_logger.addHandler(edu_handler)

        # Console handler for user feedback (with proper encoding)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.educational_logger.addHandler(console_handler)

        self.educational_logger.propagate = False
        self.operational_logger.propagate = False

    def operational(self, message: str, level: str = "INFO"):
        """
        Log operational/technical information.

        Args:
            message: Log message
            level: Log level (DEBUG, INFO, WARNING, ERROR)
        """
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        self.operational_logger.log(level_map.get(level, logging.INFO), message)

    def educational(self, message: str, section: Optional[str] = None):
        """
        Log educational information that helps the user learn.

        Args:
            message: Educational message
            section: Optional section header for organization
        """
        if section:
            separator = "=" * 70
            self.educational_logger.info(f"\n{separator}")
            self.educational_logger.info(f"{section}")
            self.educational_logger.info(separator)

        self.educational_logger.info(message)

    def step(self, step_num: int, title: str, description: str):
        """
        Log a numbered step in the learning process.

        Args:
            step_num: Step number
            title: Step title
            description: Detailed description
        """
        self.educational(f"\n[Step {step_num}] {title}")
        self.educational(f"{description}\n")
        self.operational(f"Step {step_num}: {title}", "INFO")

    def explain_success(self, what_happened: str, why_it_worked: str):
        """
        Explain why an exploit succeeded.

        Args:
            what_happened: Description of what occurred
            why_it_worked: Technical explanation
        """
        self.educational(f"\n✓ SUCCESS: {what_happened}")
        self.educational(f"\nWhy it worked:")
        self.educational(f"  {why_it_worked}\n")
        self.operational(f"Exploit successful: {what_happened}", "INFO")

    def explain_failure(self, what_failed: str, why_it_failed: str, suggestion: Optional[str] = None):
        """
        Explain why an exploit failed and suggest next steps.

        Args:
            what_failed: Description of what was attempted
            why_it_failed: Technical explanation of failure
            suggestion: Optional suggestion for next attempt
        """
        self.educational(f"\n✗ FAILED: {what_failed}")
        self.educational(f"\nWhy it failed:")
        self.educational(f"  {why_it_failed}")

        if suggestion:
            self.educational(f"\nSuggested next step:")
            self.educational(f"  {suggestion}\n")

        self.operational(f"Exploit failed: {what_failed}", "WARNING")

    def payload(self, payload: str, explanation: str):
        """
        Log a payload with explanation.

        Args:
            payload: The actual payload string
            explanation: What the payload does
        """
        self.educational(f"\nPayload: {payload}")
        self.educational(f"Explanation: {explanation}")
        self.operational(f"Payload: {payload}", "INFO")

    def http_request(self, method: str, url: str, data: Optional[dict] = None):
        """
        Log an HTTP request.

        Args:
            method: HTTP method
            url: Request URL
            data: Optional request data
        """
        self.operational(f"HTTP {method} {url}", "DEBUG")
        if data:
            self.operational(f"Request data: {data}", "DEBUG")

    def http_response(self, status_code: int, snippet: Optional[str] = None):
        """
        Log an HTTP response.

        Args:
            status_code: HTTP status code
            snippet: Optional response snippet
        """
        self.operational(f"Response status: {status_code}", "DEBUG")
        if snippet:
            self.operational(f"Response snippet: {snippet[:200]}", "DEBUG")

    def close(self):
        """Close all log handlers."""
        for handler in self.operational_logger.handlers[:]:
            handler.close()
            self.operational_logger.removeHandler(handler)

        for handler in self.educational_logger.handlers[:]:
            handler.close()
            self.educational_logger.removeHandler(handler)
