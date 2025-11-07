"""
Target configuration and validation for XSS Lab Tool.
Ensures that attacks are only performed against authorized lab environments.
"""

import re
from typing import Optional
from urllib.parse import urlparse


class TargetConfig:
    """Configuration for target DVWA instance with safety validation."""

    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '::1',
        '0.0.0.0'
    ]

    def __init__(self, host: str = "localhost", port: int = 80, use_https: bool = False):
        """
        Initialize target configuration.

        Args:
            host: Target hostname (must be localhost or explicitly confirmed)
            port: Target port
            use_https: Whether to use HTTPS
        """
        self.host = host
        self.port = port
        self.use_https = use_https
        self._confirmed = False

    @property
    def base_url(self) -> str:
        """Get the base URL for the target."""
        scheme = "https" if self.use_https else "http"
        if self.port in (80, 443):
            return f"{scheme}://{self.host}"
        return f"{scheme}://{self.host}:{self.port}"

    def is_safe_target(self) -> bool:
        """
        Check if the target is a known safe lab environment.

        Returns:
            True if target is localhost or explicitly confirmed
        """
        # Check if it's a known safe host
        if self.host.lower() in self.ALLOWED_HOSTS:
            return True

        # Check if it's a private IP range
        if self._is_private_ip(self.host):
            return True

        return self._confirmed

    def _is_private_ip(self, host: str) -> bool:
        """Check if host is a private IP address."""
        private_patterns = [
            r'^10\.',
            r'^172\.(1[6-9]|2[0-9]|3[0-1])\.',
            r'^192\.168\.',
        ]

        for pattern in private_patterns:
            if re.match(pattern, host):
                return True
        return False

    def confirm_target(self):
        """Explicitly confirm that this target is authorized for testing."""
        self._confirmed = True

    def get_dvwa_url(self, path: str) -> str:
        """
        Get a full DVWA URL for a specific path.

        Args:
            path: Path relative to DVWA root (e.g., 'login.php' or 'vulnerabilities/xss_r/')

        Returns:
            Full URL
        """
        # Remove leading slash if present
        path = path.lstrip('/')
        return f"{self.base_url}/{path}"

    def __str__(self) -> str:
        return f"TargetConfig({self.base_url})"

    def __repr__(self) -> str:
        return f"TargetConfig(host={self.host!r}, port={self.port}, use_https={self.use_https})"
