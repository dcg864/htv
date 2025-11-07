"""
Command-line interface for XSS Lab Tool.
Provides interactive, educational XSS demonstrations against DVWA.
"""

import argparse
import sys
import codecs

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from .core.target_config import TargetConfig
from .core.logger import DualLogger
from .core.auth import DVWAAuthenticator
from .core.http_client import HTTPClient
from .modules.reflected import ReflectedXSSModule
from .modules.stored import StoredXSSModule
from .modules.dom_based import DOMXSSModule
from .utils.validators import display_safety_banner, confirm_authorization, preflight_check
from .utils.banner import get_current_tagline
from .utils.request_recorder import BurpRequestRecorder


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="HackBench | Educational XSS lab companion with a rotating safety banner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all XSS modules interactively
  python -m hackbench --mode all

  # Run only reflected XSS
  python -m hackbench --mode reflected

  # Target DVWA on custom port
  python -m hackbench --host localhost --port 8080

  # Non-interactive mode (auto-approve all steps)
  python -m hackbench --mode all --no-interactive

  # Custom credentials
  python -m hackbench --username admin --password admin123
        """
    )

    parser.add_argument(
        '--mode',
        choices=['reflected', 'stored', 'dom', 'all'],
        default='all',
        help='XSS attack type to demonstrate (default: all)'
    )

    parser.add_argument(
        '--host',
        default='localhost',
        help='Target hostname (default: localhost)'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=80,
        help='Target port (default: 80)'
    )

    parser.add_argument(
        '--https',
        action='store_true',
        help='Use HTTPS instead of HTTP'
    )

    parser.add_argument(
        '--username',
        default='admin',
        help='DVWA username (default: admin)'
    )

    parser.add_argument(
        '--password',
        default='password',
        help='DVWA password (default: password)'
    )

    parser.add_argument(
        '--security-level',
        choices=['low', 'medium', 'high', 'impossible'],
        help='Set DVWA security level before testing (optional)'
    )

    parser.add_argument(
        '--no-interactive',
        action='store_true',
        help='Run in non-interactive mode (auto-approve all steps)'
    )

    parser.add_argument(
        '--log-dir',
        default='logs',
        help='Directory for log files (default: logs)'
    )

    parser.add_argument(
        '--confirm-target',
        action='store_true',
        help='Explicitly confirm target is authorized for testing (required for non-localhost targets)'
    )

    parser.add_argument(
        '--skip-banner',
        action='store_true',
        help='Skip the safety banner (not recommended)'
    )

    return parser.parse_args()


def main():
    """Main entry point for XSS Lab Tool."""
    args = parse_arguments()

    # Display safety banner
    if not args.skip_banner:
        tagline = display_safety_banner()

        if not confirm_authorization():
            print("\n❌ Authorization not confirmed. Exiting.")
            return 1
    else:
        tagline = get_current_tagline(force_refresh=True)

    # Initialize configuration
    target = TargetConfig(host=args.host, port=args.port, use_https=args.https)

    if args.confirm_target:
        target.confirm_target()

    # Initialize logger
    logger = DualLogger(log_dir=args.log_dir)
    request_recorder = BurpRequestRecorder(args.log_dir, logger)

    try:
        logger.educational(f"\n{'='*70}")
        logger.educational(f"HACKBENCH - {tagline}")
        logger.educational(f"{'='*70}")
        logger.educational(f"Target: {target.base_url}")
        logger.educational(f"Mode: {args.mode}")
        logger.educational(f"Interactive: {not args.no_interactive}")
        logger.educational(f"{'='*70}\n")

        # Preflight checks
        logger.educational("Running preflight checks...")
        success, error = preflight_check(target, logger)

        if not success:
            logger.educational(f"\n❌ Preflight check failed: {error}")
            logger.operational(f"Preflight check failed: {error}", "ERROR")
            return 1

        logger.educational("✓ All preflight checks passed\n")

        # Initialize authenticator
        logger.educational("Authenticating with DVWA...")
        auth = DVWAAuthenticator(target.base_url, logger)

        # Verify DVWA presence
        is_dvwa, version = auth.verify_dvwa_presence()
        if not is_dvwa:
            logger.educational(f"\n❌ Target does not appear to be DVWA: {version}")
            logger.educational("Please verify:")
            logger.educational("  1. DVWA is running")
            logger.educational("  2. Target URL is correct")
            logger.educational(f"  3. {target.base_url}/login.php is accessible")
            return 1

        logger.educational(f"✓ DVWA detected (version: {version})")

        # Login
        if not auth.login(username=args.username, password=args.password):
            logger.educational("\n❌ Authentication failed")
            logger.educational("Please verify:")
            logger.educational("  1. DVWA credentials are correct")
            logger.educational("  2. DVWA setup is complete")
            return 1

        # Detect and optionally set security level
        current_level = auth.detect_security_level()
        if current_level:
            logger.educational(f"Current DVWA security level: {current_level}")

        if args.security_level and args.security_level != current_level:
            logger.educational(f"Setting security level to: {args.security_level}")
            if auth.set_security_level(args.security_level):
                logger.educational(f"✓ Security level changed to: {args.security_level}")
            else:
                logger.educational(f"⚠ Failed to change security level")

        # Initialize HTTP client
        http_client = HTTPClient(
            auth.get_session(),
            logger,
            request_recorder=request_recorder,
        )

        # Run selected modules
        interactive = not args.no_interactive
        modules_run = []
        modules_succeeded = []

        if args.mode in ['reflected', 'all']:
            logger.educational("\n" + "="*70)
            logger.educational("Starting Reflected XSS Module")
            logger.educational("="*70)
            reflected = ReflectedXSSModule(http_client, logger, target)
            modules_run.append('Reflected XSS')
            if reflected.run_interactive(interactive):
                modules_succeeded.append('Reflected XSS')

        if args.mode in ['stored', 'all']:
            logger.educational("\n" + "="*70)
            logger.educational("Starting Stored XSS Module")
            logger.educational("="*70)
            stored = StoredXSSModule(http_client, logger, target, auth)
            modules_run.append('Stored XSS')
            if stored.run_interactive(interactive):
                modules_succeeded.append('Stored XSS')

        if args.mode in ['dom', 'all']:
            logger.educational("\n" + "="*70)
            logger.educational("Starting DOM-Based XSS Module")
            logger.educational("="*70)
            dom = DOMXSSModule(http_client, logger, target)
            modules_run.append('DOM-Based XSS')
            if dom.run_interactive(interactive):
                modules_succeeded.append('DOM-Based XSS')

        # Summary
        logger.educational("\n" + "="*70)
        logger.educational("SESSION SUMMARY")
        logger.educational("="*70)
        logger.educational(f"Modules run: {', '.join(modules_run)}")
        logger.educational(f"Modules succeeded: {', '.join(modules_succeeded) if modules_succeeded else 'None'}")
        logger.educational(f"\nLogs saved to: {args.log_dir}/")
        logger.educational(f"Raw HTTP replays: {request_recorder.output_path}")
        logger.educational("="*70)

        return 0

    except KeyboardInterrupt:
        logger.educational("\n\n⚠ Operation cancelled by user")
        logger.operational("User interrupted with Ctrl+C", "INFO")
        return 130

    except Exception as e:
        logger.educational(f"\n❌ Unexpected error: {e}")
        logger.operational(f"Unexpected error: {e}", "ERROR")
        import traceback
        logger.operational(traceback.format_exc(), "ERROR")
        return 1

    finally:
        logger.close()


if __name__ == '__main__':
    sys.exit(main())
