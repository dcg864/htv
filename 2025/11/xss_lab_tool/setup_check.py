#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup verification script for XSS Lab Tool.
Checks that all dependencies and prerequisites are met.

Usage: python setup_check.py
"""

import sys
import importlib
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def check_python_version():
    """Check Python version is 3.10+"""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro}")
        print(f"   ERROR: Python 3.10+ required")
        return False


def check_dependencies():
    """Check required dependencies are installed"""
    print("\nChecking dependencies...")

    dependencies = [
        ("requests", "HTTP library"),
        ("bs4", "BeautifulSoup (HTML parsing)"),
        ("colorama", "Terminal colors"),
    ]

    all_ok = True
    for module_name, description in dependencies:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {description} ({module_name})")
        except ImportError:
            print(f"  ✗ {description} ({module_name}) - NOT INSTALLED")
            all_ok = False

    return all_ok


def check_project_structure():
    """Check project files exist"""
    print("\nChecking project structure...")

    required_files = [
        "core/auth.py",
        "core/http_client.py",
        "core/logger.py",
        "core/target_config.py",
        "modules/reflected.py",
        "modules/stored.py",
        "modules/dom_based.py",
        "explanations/text_blocks.py",
        "utils/validators.py",
        "cli.py",
        "__main__.py",
    ]

    all_ok = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING")
            all_ok = False

    return all_ok


def check_dvwa_connectivity():
    """Check if DVWA is reachable (optional check)"""
    print("\nChecking DVWA connectivity (optional)...")

    try:
        import requests
        response = requests.get("http://localhost", timeout=5)
        if response.status_code == 200:
            if "DVWA" in response.text or "Damn Vulnerable" in response.text:
                print("  ✓ DVWA detected at http://localhost")
                return True
            else:
                print("  ⚠ Server at http://localhost is not DVWA")
                return None  # Warning, not error
        else:
            print(f"  ⚠ Server at http://localhost returned HTTP {response.status_code}")
            return None
    except ImportError:
        print("  ⚠ Cannot check (requests not installed)")
        return None
    except Exception as e:
        print(f"  ⚠ DVWA not reachable: {e}")
        print("     This is OK if you haven't started DVWA yet")
        return None


def main():
    """Run all checks"""
    print("="*70)
    print("XSS Lab Tool - Setup Verification")
    print("="*70)

    results = []

    # Python version (critical)
    results.append(("Python version", check_python_version()))

    # Dependencies (critical)
    results.append(("Dependencies", check_dependencies()))

    # Project structure (critical)
    results.append(("Project structure", check_project_structure()))

    # DVWA connectivity (optional)
    dvwa_result = check_dvwa_connectivity()
    if dvwa_result is not None:
        results.append(("DVWA connectivity", dvwa_result))

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    critical_checks = [r for r in results if r[1] is not None]
    passed = sum(1 for r in critical_checks if r[1])
    total = len(critical_checks)

    for name, result in results:
        if result is True:
            print(f"✓ {name}: PASS")
        elif result is False:
            print(f"✗ {name}: FAIL")
        else:
            print(f"⚠ {name}: WARNING")

    print("="*70)

    if passed == total:
        print("✓ ALL CHECKS PASSED!")
        print("\nYou're ready to use XSS Lab Tool:")
        print("  python -m xss_lab_tool --mode all")
        return 0
    else:
        print(f"✗ {total - passed}/{total} checks failed")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
