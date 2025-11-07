"""
Basic tests for XSS Lab Tool components.
Run with: python -m pytest tests/
"""

import pytest
from unittest.mock import Mock, MagicMock
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.target_config import TargetConfig
from core.logger import DualLogger
from explanations.text_blocks import XSSExplanations


class TestTargetConfig:
    """Test target configuration and validation."""

    def test_localhost_is_safe(self):
        """Localhost should always be considered safe."""
        config = TargetConfig(host="localhost", port=80)
        assert config.is_safe_target() is True

    def test_127_0_0_1_is_safe(self):
        """127.0.0.1 should always be considered safe."""
        config = TargetConfig(host="127.0.0.1", port=80)
        assert config.is_safe_target() is True

    def test_private_ip_is_safe(self):
        """Private IPs should be considered safe."""
        config = TargetConfig(host="192.168.1.100", port=80)
        assert config.is_safe_target() is True

        config = TargetConfig(host="10.0.0.1", port=80)
        assert config.is_safe_target() is True

    def test_public_ip_requires_confirmation(self):
        """Public IPs should require explicit confirmation."""
        config = TargetConfig(host="8.8.8.8", port=80)
        assert config.is_safe_target() is False

        config.confirm_target()
        assert config.is_safe_target() is True

    def test_base_url_construction(self):
        """Test URL construction."""
        config = TargetConfig(host="localhost", port=80)
        assert config.base_url == "http://localhost"

        config = TargetConfig(host="localhost", port=8080)
        assert config.base_url == "http://localhost:8080"

        config = TargetConfig(host="localhost", port=443, use_https=True)
        assert config.base_url == "https://localhost"

    def test_get_dvwa_url(self):
        """Test DVWA URL generation."""
        config = TargetConfig(host="localhost", port=80)
        url = config.get_dvwa_url("vulnerabilities/xss_r/")
        assert url == "http://localhost/vulnerabilities/xss_r/"

        url = config.get_dvwa_url("/login.php")
        assert url == "http://localhost/login.php"


class TestDualLogger:
    """Test logging functionality."""

    def test_logger_initialization(self, tmp_path):
        """Test logger can be initialized."""
        logger = DualLogger(log_dir=str(tmp_path))

        # Check loggers exist
        assert logger.operational_logger is not None
        assert logger.educational_logger is not None

        # Check log directory was created
        assert tmp_path.exists()

        logger.close()

    def test_operational_logging(self, tmp_path):
        """Test operational logging."""
        logger = DualLogger(log_dir=str(tmp_path))

        logger.operational("Test message", "INFO")
        logger.operational("Test warning", "WARNING")
        logger.operational("Test error", "ERROR")

        logger.close()

        # Check log file was created
        log_files = list(tmp_path.glob("xss_lab_operational_*.log"))
        assert len(log_files) == 1

        # Check content
        content = log_files[0].read_text()
        assert "Test message" in content
        assert "Test warning" in content
        assert "Test error" in content

    def test_educational_logging(self, tmp_path):
        """Test educational logging."""
        logger = DualLogger(log_dir=str(tmp_path))

        logger.educational("Test educational content")
        logger.step(1, "Test Step", "Step description")

        logger.close()

        # Check log file was created
        log_files = list(tmp_path.glob("xss_lab_explained_*.log"))
        assert len(log_files) == 1

        # Check content
        content = log_files[0].read_text()
        assert "Test educational content" in content
        assert "Test Step" in content


class TestXSSExplanations:
    """Test explanation text blocks."""

    def test_explanations_exist(self):
        """Test that key explanations exist."""
        exp = XSSExplanations()

        assert len(exp.XSS_INTRO) > 0
        assert len(exp.REFLECTED_XSS_INTRO) > 0
        assert len(exp.STORED_XSS_INTRO) > 0
        assert len(exp.DOM_XSS_INTRO) > 0

    def test_payload_explanations_exist(self):
        """Test that payload explanations exist."""
        exp = XSSExplanations()

        assert len(exp.PAYLOAD_BASIC_ALERT) > 0
        assert len(exp.PAYLOAD_IMG_ONERROR) > 0
        assert len(exp.PAYLOAD_SVG_ONLOAD) > 0

    def test_get_explanation(self):
        """Test explanation retrieval."""
        exp = XSSExplanations()

        text = exp.get_explanation("REFLECTED_XSS_INTRO")
        assert len(text) > 0

        # Non-existent key should return empty string
        text = exp.get_explanation("NONEXISTENT_KEY")
        assert text == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
