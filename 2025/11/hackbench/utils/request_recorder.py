"""
Utility to capture raw HTTP requests for Burp Suite or other tooling.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from requests import PreparedRequest


class BurpRequestRecorder:
    """
    Writes each HTTP request to a timestamped file so it can be replayed
    from Burp Suite (Project options ➜ Misc ➜ Paste raw requests).
    """

    def __init__(self, log_dir: str, logger: Optional[object] = None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_path = Path(log_dir) / f"hackbench_burp_replay_{timestamp}.txt"
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text("", encoding="utf-8")
        self.logger = logger

    def record(self, prepared_request: PreparedRequest):
        """Persist a prepared request in raw HTTP format."""
        try:
            url_bits = urlparse(prepared_request.url)
            path = url_bits.path or "/"

            if url_bits.query:
                path = f"{path}?{url_bits.query}"

            lines = [f"{prepared_request.method} {path} HTTP/1.1"]
            headers = dict(prepared_request.headers)

            if "Host" not in headers and url_bits.netloc:
                headers["Host"] = url_bits.netloc

            for key, value in headers.items():
                lines.append(f"{key}: {value}")

            lines.append("")

            body = prepared_request.body
            if body:
                if isinstance(body, bytes):
                    body = body.decode("utf-8", errors="replace")
                lines.append(body)

            entry = "\n".join(lines) + "\n\n"

            with self.output_path.open("a", encoding="utf-8") as handle:
                handle.write(entry)

        except Exception as exc:  # pragma: no cover - defensive logging
            if self.logger:
                self.logger.operational(
                    f"Failed to record request for Burp export: {exc}", "WARNING"
                )

