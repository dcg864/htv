"""
Validation utilities for target verification and safety checks.
"""

import requests
from typing import Tuple, Optional
from .banner import display_banner, display_legal_warning


def check_target_reachability(base_url: str, timeout: int = 10) -> Tuple[bool, Optional[str]]:
    """
    Check if target URL is reachable.

    Args:
        base_url: Base URL to check
        timeout: Request timeout in seconds

    Returns:
        Tuple of (is_reachable, error_message)
    """
    try:
        response = requests.get(base_url, timeout=timeout)
        if response.status_code == 200:
            return True, None
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - is DVWA running?"
    except requests.exceptions.Timeout:
        return False, f"Request timed out after {timeout} seconds"
    except requests.exceptions.RequestException as e:
        return False, str(e)


def display_safety_banner():
    """Display the mandatory safety and legal disclaimer banner."""
    tagline = display_banner()
    display_legal_warning()
    return tagline


def confirm_authorization() -> bool:
    """
    Require user to confirm they have authorization.

    Returns:
        True if user confirms authorization
    """
    print("Before proceeding, you must confirm that:")
    print("  1. You have explicit authorization to test the target system")
    print("  2. You understand the legal implications of unauthorized testing")
    print("  3. You will use this tool responsibly and ethically")
    print()

    try:
        response = input("Do you confirm the above? Type 'I AGREE' to proceed: ").strip()
        return response == "I AGREE"
    except (KeyboardInterrupt, EOFError):
        return False


def preflight_check(target_config, logger) -> Tuple[bool, Optional[str]]:
    """
    Perform preflight checks before running any attacks.

    Args:
        target_config: TargetConfig instance
        logger: DualLogger instance

    Returns:
        Tuple of (success, error_message)
    """
    logger.operational("Starting preflight checks", "INFO")

    # Check 1: Safety validation
    if not target_config.is_safe_target():
        return False, (
            f"Target {target_config.host} is not recognized as a safe lab environment.\n"
            f"Only localhost, 127.0.0.1, and private IPs are allowed by default.\n"
            f"If this is truly a lab environment, use --confirm-target flag."
        )

    logger.operational("✓ Target passes safety validation", "INFO")

    # Check 2: Reachability
    is_reachable, error = check_target_reachability(target_config.base_url)
    if not is_reachable:
        return False, f"Target unreachable: {error}"

    logger.operational("✓ Target is reachable", "INFO")

    return True, None
