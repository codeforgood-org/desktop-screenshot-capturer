"""
Basic usage examples for the Desktop Screenshot Capturer.

This script demonstrates the most common use cases.
"""

from pathlib import Path
from screenshot_capturer import ScreenshotCapturer, CaptureMode, Region


def example_1_simple_fullscreen():
    """Example 1: Capture fullscreen and save to file."""
    print("Example 1: Simple fullscreen capture")

    capturer = ScreenshotCapturer()
    screenshot = capturer.capture_fullscreen()
    filepath = capturer.save_screenshot(screenshot, "fullscreen.png")

    print(f"✓ Screenshot saved to: {filepath}")
    print()


def example_2_region_capture():
    """Example 2: Capture a specific region."""
    print("Example 2: Region capture")

    capturer = ScreenshotCapturer()

    # Define region (x, y, width, height)
    region = Region(x=100, y=100, width=800, height=600)

    screenshot = capturer.capture_region(region)
    filepath = capturer.save_screenshot(screenshot, "region.png")

    print(f"✓ Region screenshot saved to: {filepath}")
    print(f"  Region: {region.bbox}")
    print()


def example_3_different_formats():
    """Example 3: Save in different formats."""
    print("Example 3: Multiple formats")

    capturer = ScreenshotCapturer()
    screenshot = capturer.capture_fullscreen()

    formats = [
        ("screenshot.png", "PNG", 95),
        ("screenshot.jpg", "JPEG", 85),
        ("screenshot.bmp", "BMP", 95),
    ]

    for filename, fmt, quality in formats:
        filepath = capturer.save_screenshot(screenshot, filename, fmt, quality)
        print(f"✓ Saved as {fmt}: {filepath}")

    print()


def example_4_quick_capture():
    """Example 4: Using quick_capture method."""
    print("Example 4: Quick capture")

    capturer = ScreenshotCapturer()

    # Quick capture with defaults
    filepath = capturer.quick_capture(filepath="quick.png")
    print(f"✓ Quick capture saved to: {filepath}")

    # Quick capture region
    region = Region(x=0, y=0, width=400, height=300)
    filepath = capturer.quick_capture(
        filepath="quick_region.png", mode=CaptureMode.REGION, region=region
    )
    print(f"✓ Quick region capture saved to: {filepath}")
    print()


def example_5_get_as_bytes():
    """Example 5: Get screenshot as bytes."""
    print("Example 5: Screenshot as bytes")

    capturer = ScreenshotCapturer()
    screenshot = capturer.capture_fullscreen()

    # Get as bytes (useful for uploading, etc.)
    png_bytes = capturer.get_screenshot_bytes(screenshot, format="PNG")
    jpeg_bytes = capturer.get_screenshot_bytes(screenshot, format="JPEG", quality=80)

    print(f"✓ PNG bytes: {len(png_bytes):,} bytes")
    print(f"✓ JPEG bytes: {len(jpeg_bytes):,} bytes")
    print()


def example_6_with_directories():
    """Example 6: Save to specific directories."""
    print("Example 6: Organized directory structure")

    capturer = ScreenshotCapturer()
    screenshot = capturer.capture_fullscreen()

    # Create organized directory structure
    output_dir = Path("screenshots") / "2024-01" / "examples"
    filepath = output_dir / "organized.png"

    # save_screenshot creates directories automatically
    result = capturer.save_screenshot(screenshot, filepath)

    print(f"✓ Screenshot saved to: {result}")
    print(f"  Directory structure created automatically")
    print()


def example_7_platform_info():
    """Example 7: Get platform information."""
    print("Example 7: Platform information")

    capturer = ScreenshotCapturer()

    print(f"Platform: {capturer.platform}")
    print(f"Supported formats: {', '.join(capturer.supported_formats)}")
    print()


def main():
    """Run all examples."""
    print("=" * 60)
    print("Desktop Screenshot Capturer - Basic Usage Examples")
    print("=" * 60)
    print()

    try:
        example_1_simple_fullscreen()
        example_2_region_capture()
        example_3_different_formats()
        example_4_quick_capture()
        example_5_get_as_bytes()
        example_6_with_directories()
        example_7_platform_info()

        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"Error running examples: {e}")
        raise


if __name__ == "__main__":
    main()
