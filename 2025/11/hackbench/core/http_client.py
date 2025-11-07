"""
HTTP client wrapper with logging integration.
Provides convenient methods for making requests with automatic logging.
"""

import requests
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup


class HTTPClient:
    """HTTP client wrapper with integrated logging."""

    def __init__(self, session: requests.Session, logger, request_recorder=None):
        """
        Initialize HTTP client.

        Args:
            session: requests.Session instance (from authenticator)
            logger: DualLogger instance
            request_recorder: Optional BurpRequestRecorder for raw HTTP capture
        """
        self.session = session
        self.logger = logger
        self.request_recorder = request_recorder

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 10) -> Optional[requests.Response]:
        """
        Perform GET request with logging.

        Args:
            url: Target URL
            params: Optional query parameters
            timeout: Request timeout in seconds

        Returns:
            Response object or None on failure
        """
        return self._send("GET", url, params=params, timeout=timeout)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, timeout: int = 10) -> Optional[requests.Response]:
        """
        Perform POST request with logging.

        Args:
            url: Target URL
            data: Optional POST data
            timeout: Request timeout in seconds

        Returns:
            Response object or None on failure
        """
        return self._send("POST", url, data=data, timeout=timeout)

    def _send(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: int = 10,
    ) -> Optional[requests.Response]:
        """Prepare, optionally record, and send an HTTP request."""
        try:
            request = requests.Request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                headers=dict(self.session.headers),
            )
            prepared = self.session.prepare_request(request)

            log_payload = params if method.upper() == "GET" else data
            self.logger.http_request(method.upper(), prepared.url, log_payload)

            if self.request_recorder:
                self.request_recorder.record(prepared)

            response = self.session.send(prepared, timeout=timeout)
            self.logger.http_response(response.status_code, response.text[:200])
            return response

        except requests.exceptions.RequestException as e:
            self.logger.operational(f"{method.upper()} request failed: {e}", "ERROR")
            return None

    def check_xss_reflection(self, response: requests.Response, payload: str) -> bool:
        """
        Check if XSS payload appears unencoded in response.

        Args:
            response: HTTP response to check
            payload: Original payload string

        Returns:
            True if payload appears unencoded, False otherwise
        """
        if not response:
            return False

        # Check if exact payload appears in response
        if payload in response.text:
            self.logger.operational("Payload appears unencoded in response", "INFO")
            return True

        # Check for common HTML-encoded versions
        encoded_variants = [
            payload.replace('<', '&lt;').replace('>', '&gt;'),
            payload.replace('<', '%3C').replace('>', '%3E'),
        ]

        for variant in encoded_variants:
            if variant in response.text:
                self.logger.operational("Payload appears encoded in response", "INFO")
                return False

        self.logger.operational("Payload not found in response", "INFO")
        return False

    def extract_text_content(self, response: requests.Response, selector: Optional[str] = None) -> str:
        """
        Extract text content from HTML response.

        Args:
            response: HTTP response
            selector: Optional CSS selector to narrow extraction

        Returns:
            Extracted text
        """
        if not response:
            return ""

        try:
            soup = BeautifulSoup(response.text, 'html.parser')

            if selector:
                element = soup.select_one(selector)
                if element:
                    return element.get_text(strip=True)
                return ""

            return soup.get_text()

        except Exception as e:
            self.logger.operational(f"Error extracting text: {e}", "ERROR")
            return ""

    def find_form_inputs(self, response: requests.Response) -> Dict[str, str]:
        """
        Extract form input names from HTML response.

        Args:
            response: HTTP response containing form

        Returns:
            Dictionary of input names and their types
        """
        if not response:
            return {}

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            inputs = {}

            for form_input in soup.find_all('input'):
                name = form_input.get('name')
                input_type = form_input.get('type', 'text')

                if name:
                    inputs[name] = input_type

            for textarea in soup.find_all('textarea'):
                name = textarea.get('name')
                if name:
                    inputs[name] = 'textarea'

            return inputs

        except Exception as e:
            self.logger.operational(f"Error extracting form inputs: {e}", "ERROR")
            return {}

    def get_user_agent(self) -> str:
        """Return the session's configured User-Agent string."""
        return self.session.headers.get("User-Agent", "python-requests")

    def get_cookie(self, name: str) -> Optional[str]:
        """Return a cookie value if present on the session."""
        return self.session.cookies.get(name)
