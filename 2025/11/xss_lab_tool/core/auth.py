"""
Authentication and session management for DVWA.
Handles login, session cookies, and CSRF token management.
"""

import re
import requests
from typing import Optional, Tuple
from bs4 import BeautifulSoup


class DVWAAuthenticator:
    """Manages authentication and session for DVWA."""

    def __init__(self, base_url: str, logger):
        """
        Initialize DVWA authenticator.

        Args:
            base_url: Base URL of DVWA instance
            logger: DualLogger instance for logging
        """
        self.base_url = base_url.rstrip('/')
        self.logger = logger
        self.session = requests.Session()
        self.security_level = None
        self._logged_in = False

    def login(self, username: str = "admin", password: str = "password") -> bool:
        """
        Authenticate with DVWA.

        Args:
            username: DVWA username (default: admin)
            password: DVWA password (default: password)

        Returns:
            True if login successful, False otherwise
        """
        self.logger.operational(f"Attempting DVWA login as {username}", "INFO")

        try:
            # First, get the login page to obtain CSRF token
            login_url = f"{self.base_url}/login.php"
            self.logger.operational(f"Fetching login page: {login_url}", "DEBUG")

            response = self.session.get(login_url, timeout=10)

            if response.status_code != 200:
                self.logger.operational(f"Failed to fetch login page: {response.status_code}", "ERROR")
                return False

            # Extract CSRF token from login form
            csrf_token = self._extract_csrf_token(response.text)

            # Perform login
            login_data = {
                'username': username,
                'password': password,
                'Login': 'Login'
            }

            if csrf_token:
                login_data['user_token'] = csrf_token
                self.logger.operational(f"Using CSRF token: {csrf_token[:10]}...", "DEBUG")

            self.logger.operational("Submitting login credentials", "DEBUG")
            response = self.session.post(login_url, data=login_data, timeout=10)

            # Check if login was successful
            if 'login.php' not in response.url and response.status_code == 200:
                self._logged_in = True
                self.logger.operational("Login successful", "INFO")
                self.logger.educational("\n✓ Successfully authenticated with DVWA")
                return True
            else:
                self.logger.operational("Login failed - still on login page", "ERROR")
                return False

        except requests.exceptions.RequestException as e:
            self.logger.operational(f"Login request failed: {e}", "ERROR")
            return False

    def detect_security_level(self) -> Optional[str]:
        """
        Detect current DVWA security level.

        Returns:
            Security level string ('low', 'medium', 'high', 'impossible') or None
        """
        if not self._logged_in:
            self.logger.operational("Cannot detect security level - not logged in", "WARNING")
            return None

        try:
            security_url = f"{self.base_url}/security.php"
            response = self.session.get(security_url, timeout=10)

            if response.status_code != 200:
                self.logger.operational(f"Failed to fetch security page: {response.status_code}", "ERROR")
                return None

            # Parse the security level from the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for selected option in security level form
            selected = soup.find('option', selected=True)
            if selected:
                level = selected.get('value', '').lower()
                self.security_level = level
                self.logger.operational(f"Detected security level: {level}", "INFO")
                return level

            # Alternative: check for radio buttons or other indicators
            level_match = re.search(r'Security Level is currently: (\w+)', response.text, re.IGNORECASE)
            if level_match:
                level = level_match.group(1).lower()
                self.security_level = level
                self.logger.operational(f"Detected security level: {level}", "INFO")
                return level

            self.logger.operational("Could not determine security level", "WARNING")
            return None

        except Exception as e:
            self.logger.operational(f"Error detecting security level: {e}", "ERROR")
            return None

    def set_security_level(self, level: str) -> bool:
        """
        Set DVWA security level.

        Args:
            level: Security level ('low', 'medium', 'high', 'impossible')

        Returns:
            True if successful, False otherwise
        """
        if not self._logged_in:
            self.logger.operational("Cannot set security level - not logged in", "WARNING")
            return False

        level = level.lower()
        if level not in ['low', 'medium', 'high', 'impossible']:
            self.logger.operational(f"Invalid security level: {level}", "ERROR")
            return False

        try:
            security_url = f"{self.base_url}/security.php"

            # Get current page to extract CSRF token
            response = self.session.get(security_url, timeout=10)
            csrf_token = self._extract_csrf_token(response.text)

            # Submit security level change
            data = {
                'security': level,
                'seclev_submit': 'Submit'
            }

            if csrf_token:
                data['user_token'] = csrf_token

            self.logger.operational(f"Setting security level to: {level}", "INFO")
            response = self.session.post(security_url, data=data, timeout=10)

            if response.status_code == 200:
                self.security_level = level
                self.logger.operational("Security level updated", "INFO")
                self.logger.educational(f"\n✓ DVWA security level set to: {level}")
                return True
            else:
                self.logger.operational(f"Failed to set security level: {response.status_code}", "ERROR")
                return False

        except Exception as e:
            self.logger.operational(f"Error setting security level: {e}", "ERROR")
            return False

    def get_csrf_token(self, url: str) -> Optional[str]:
        """
        Extract CSRF token from a given page.

        Args:
            url: URL to fetch and extract token from

        Returns:
            CSRF token if found, None otherwise
        """
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return self._extract_csrf_token(response.text)
        except Exception as e:
            self.logger.operational(f"Error fetching CSRF token: {e}", "ERROR")

        return None

    def _extract_csrf_token(self, html: str) -> Optional[str]:
        """
        Extract CSRF token from HTML.

        Args:
            html: HTML content

        Returns:
            CSRF token if found, None otherwise
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Look for user_token hidden input
        token_input = soup.find('input', {'name': 'user_token'})
        if token_input and token_input.get('value'):
            return token_input.get('value')

        return None

    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        return self._logged_in

    def get_session(self) -> requests.Session:
        """Get the authenticated session object."""
        return self.session

    def verify_dvwa_presence(self) -> Tuple[bool, Optional[str]]:
        """
        Verify that target is actually DVWA.

        Returns:
            Tuple of (is_dvwa, version_or_error_message)
        """
        try:
            self.logger.operational("Verifying DVWA presence", "INFO")
            response = self.session.get(f"{self.base_url}/login.php", timeout=10)

            if response.status_code != 200:
                return False, f"HTTP {response.status_code}"

            # Check for DVWA markers in the page
            if 'Damn Vulnerable Web Application' in response.text or 'DVWA' in response.text:
                # Try to extract version
                version_match = re.search(r'v([\d.]+)', response.text)
                version = version_match.group(1) if version_match else "unknown"

                self.logger.operational(f"DVWA detected (version: {version})", "INFO")
                return True, version

            return False, "DVWA markers not found in response"

        except requests.exceptions.RequestException as e:
            return False, str(e)
