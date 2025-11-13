"""
Command-line interface for the screenshot capturer.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import __version__
from .capturer import CaptureMode, Region, ScreenshotCapturer
from .config import Config
from .exceptions import ScreenshotCapturerError


def generate_filename(format: str = "PNG") -> str:
    """
    Generate a default filename with timestamp.

    Args:
        format: Image format extension

    Returns:
        str: Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"screenshot_{timestamp}.{format.lower()}"


def parse_region(region_str: str) -> Region:
    """
    Parse region string in format 'x,y,width,height'.

    Args:
        region_str: String representation of region

    Returns:
        Region: Parsed region object

    Raises:
        ValueError: If the region string is invalid
    """
    try:
        parts = region_str.split(",")
        if len(parts) != 4:
            raise ValueError("Region must have 4 values: x,y,width,height")

        x, y, width, height = map(int, parts)
        return Region(x=x, y=y, width=width, height=height)
    except Exception as e:
        raise ValueError(f"Invalid region format: {e}")


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser
    """
    parser = argparse.ArgumentParser(
        prog="screenshot-capturer",
        description="Cross-platform desktop screenshot capture tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture full screen to default location
  screenshot-capturer

  # Capture to specific file
  screenshot-capturer -o ~/Pictures/my_screenshot.png

  # Capture a region (x, y, width, height)
  screenshot-capturer -m region -r 100,100,800,600

  # Capture as JPEG with custom quality
  screenshot-capturer -f jpeg -q 85

  # Show current configuration
  screenshot-capturer --show-config

For more information, visit: https://github.com/codeforgood-org/desktop-screenshot-capturer
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # Capture mode options
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["fullscreen", "region", "active_window"],
        default="fullscreen",
        help="Screenshot capture mode (default: fullscreen)",
    )

    parser.add_argument(
        "-r",
        "--region",
        type=str,
        metavar="X,Y,W,H",
        help="Region to capture in format 'x,y,width,height' (required for region mode)",
    )

    # Output options
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="PATH",
        help="Output file path (default: auto-generated in current directory)",
    )

    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["png", "jpeg", "jpg", "bmp", "gif", "tiff", "webp"],
        default="png",
        help="Output image format (default: png)",
    )

    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        metavar="N",
        default=95,
        help="JPEG quality 1-100 (default: 95, only for JPEG format)",
    )

    # Configuration options
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Display current configuration and exit",
    )

    parser.add_argument(
        "--set-default-format",
        type=str,
        metavar="FORMAT",
        help="Set default output format in config",
    )

    parser.add_argument(
        "--set-default-dir",
        type=str,
        metavar="PATH",
        help="Set default output directory in config",
    )

    # Verbosity
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress all output except errors"
    )

    return parser


def handle_config_display(config: Config):
    """Display current configuration."""
    print("Current Configuration:")
    print(f"  Default Format: {config.default_format}")
    print(f"  Default Directory: {config.default_output_dir}")
    print(f"  Default Quality: {config.default_quality}")
    print(f"  Config File: {config.config_file}")


def handle_config_update(config: Config, args: argparse.Namespace):
    """Update configuration based on arguments."""
    updated = False

    if args.set_default_format:
        config.default_format = args.set_default_format.upper()
        updated = True
        print(f"Default format set to: {config.default_format}")

    if args.set_default_dir:
        config.default_output_dir = Path(args.set_default_dir)
        updated = True
        print(f"Default directory set to: {config.default_output_dir}")

    if updated:
        config.save()
        print("Configuration saved successfully")


def main(argv: Optional[list] = None) -> int:
    """
    Main CLI entry point.

    Args:
        argv: Command-line arguments (uses sys.argv if None)

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        # Load configuration
        config = Config()

        # Handle configuration display
        if args.show_config:
            handle_config_display(config)
            return 0

        # Handle configuration updates
        if args.set_default_format or args.set_default_dir:
            handle_config_update(config, args)
            return 0

        # Initialize capturer
        if args.verbose:
            print("Initializing screenshot capturer...")

        capturer = ScreenshotCapturer()

        if args.verbose:
            print(f"Platform: {capturer.platform}")
            print(f"Capture mode: {args.mode}")

        # Parse capture mode
        mode = CaptureMode(args.mode)

        # Handle region mode
        region = None
        if mode == CaptureMode.REGION:
            if not args.region:
                print("Error: --region is required for region mode", file=sys.stderr)
                return 1
            try:
                region = parse_region(args.region)
                if args.verbose:
                    print(f"Region: {region}")
            except ValueError as e:
                print(f"Error: {e}", file=sys.stderr)
                return 1

        # Determine output path
        if args.output:
            output_path = Path(args.output)
        else:
            output_dir = config.default_output_dir
            format_ext = args.format if args.format else config.default_format
            filename = generate_filename(format_ext)
            output_path = output_dir / filename

        # Validate quality
        if not 1 <= args.quality <= 100:
            print("Error: Quality must be between 1 and 100", file=sys.stderr)
            return 1

        # Capture screenshot
        if args.verbose:
            print("Capturing screenshot...")

        result = capturer.quick_capture(
            filepath=output_path,
            mode=mode,
            region=region,
            format=args.format.upper(),
            quality=args.quality,
        )

        # Report success
        if not args.quiet:
            print(f"Screenshot saved to: {result}")

        return 0

    except ScreenshotCapturerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
