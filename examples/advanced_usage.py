"""
Advanced usage examples for the Desktop Screenshot Capturer.

This script demonstrates advanced features and use cases.
"""

import io
import time
from datetime import datetime
from pathlib import Path
from typing import List

from PIL import Image, ImageDraw, ImageFont
from screenshot_capturer import ScreenshotCapturer, Region
from screenshot_capturer.exceptions import ScreenshotCapturerError


def example_1_sequential_captures():
    """Example 1: Take multiple screenshots over time."""
    print("Example 1: Sequential captures (time-lapse)")

    capturer = ScreenshotCapturer()
    output_dir = Path("screenshots") / "timelapse"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Taking 5 screenshots, 2 seconds apart...")

    for i in range(5):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{i+1}_{timestamp}.png"
        filepath = output_dir / filename

        screenshot = capturer.capture_fullscreen()
        capturer.save_screenshot(screenshot, filepath)

        print(f"  ✓ Captured: {filename}")

        if i < 4:  # Don't wait after last capture
            time.sleep(2)

    print()


def example_2_multiple_regions():
    """Example 2: Capture multiple regions at once."""
    print("Example 2: Multiple region captures")

    capturer = ScreenshotCapturer()

    # Define multiple regions of interest
    regions = [
        ("top_left", Region(x=0, y=0, width=400, height=300)),
        ("top_right", Region(x=800, y=0, width=400, height=300)),
        ("center", Region(x=400, y=300, width=400, height=300)),
    ]

    output_dir = Path("screenshots") / "regions"
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, region in regions:
        screenshot = capturer.capture_region(region)
        filepath = output_dir / f"{name}.png"
        capturer.save_screenshot(screenshot, filepath)
        print(f"  ✓ Captured {name}: {region.bbox}")

    print()


def example_3_with_annotation():
    """Example 3: Capture and annotate screenshot."""
    print("Example 3: Screenshot with annotation")

    capturer = ScreenshotCapturer()
    screenshot = capturer.capture_fullscreen()

    # Add annotation
    draw = ImageDraw.Draw(screenshot)

    # Draw rectangle
    draw.rectangle([10, 10, 300, 100], outline="red", width=3)

    # Add text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((20, 20), f"Captured: {timestamp}", fill="red")

    # Save annotated screenshot
    filepath = capturer.save_screenshot(screenshot, "annotated.png")
    print(f"✓ Annotated screenshot saved to: {filepath}")
    print()


def example_4_compare_formats():
    """Example 4: Compare file sizes across formats."""
    print("Example 4: Format comparison")

    capturer = ScreenshotCapturer()
    screenshot = capturer.capture_fullscreen()

    formats_and_qualities = [
        ("PNG", None, 95),
        ("JPEG", None, 100),
        ("JPEG", None, 85),
        ("JPEG", None, 60),
        ("BMP", None, 95),
    ]

    print(f"Screenshot size: {screenshot.width}x{screenshot.height}\n")
    print(f"{'Format':<12} {'Quality':<10} {'File Size':<15} {'Compression':<15}")
    print("-" * 55)

    png_size = None

    for fmt, suffix, quality in formats_and_qualities:
        if suffix is None:
            suffix = fmt.lower()

        filename = f"compare_{fmt.lower()}_{quality}.{suffix}"
        filepath = capturer.save_screenshot(screenshot, filename, fmt, quality)

        file_size = filepath.stat().st_size

        if fmt == "PNG":
            png_size = file_size

        compression = ""
        if png_size and file_size != png_size:
            ratio = (1 - file_size / png_size) * 100
            compression = f"{ratio:+.1f}%"

        print(
            f"{fmt:<12} {quality:<10} {file_size:>10,} bytes {compression:<15}"
        )

    print()


def example_5_batch_processing():
    """Example 5: Batch process multiple screenshots."""
    print("Example 5: Batch processing")

    capturer = ScreenshotCapturer()

    # Capture base screenshot
    base_screenshot = capturer.capture_fullscreen()

    # Define processing operations
    operations = [
        ("original", lambda img: img),
        ("thumbnail", lambda img: img.resize((400, 300))),
        ("grayscale", lambda img: img.convert("L")),
        ("low_quality", lambda img: img),  # Will use low JPEG quality
    ]

    output_dir = Path("screenshots") / "batch"
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, operation in operations:
        processed = operation(base_screenshot.copy())
        filepath = output_dir / f"{name}.jpg"

        quality = 20 if name == "low_quality" else 85
        capturer.save_screenshot(processed, filepath, "JPEG", quality)

        print(f"  ✓ Processed '{name}': {filepath}")

    print()


def example_6_error_handling():
    """Example 6: Proper error handling."""
    print("Example 6: Error handling")

    capturer = ScreenshotCapturer()

    # Example 1: Invalid region
    try:
        invalid_region = Region(x=-10, y=-10, width=100, height=100)
        print("  ✗ This should have raised an error!")
    except ScreenshotCapturerError as e:
        print(f"  ✓ Caught expected error: {e}")

    # Example 2: Invalid dimensions
    try:
        invalid_region = Region(x=10, y=10, width=-100, height=100)
        print("  ✗ This should have raised an error!")
    except ScreenshotCapturerError as e:
        print(f"  ✓ Caught expected error: {e}")

    # Example 3: Successful capture with validation
    try:
        valid_region = Region(x=0, y=0, width=100, height=100)
        screenshot = capturer.capture_region(valid_region)
        print(f"  ✓ Valid capture succeeded: {screenshot.size}")
    except ScreenshotCapturerError as e:
        print(f"  ✗ Unexpected error: {e}")

    print()


def example_7_in_memory_processing():
    """Example 7: Process screenshots in memory without saving."""
    print("Example 7: In-memory processing")

    capturer = ScreenshotCapturer()

    # Capture without saving
    screenshot = capturer.capture_fullscreen()

    print(f"  Screenshot dimensions: {screenshot.width}x{screenshot.height}")
    print(f"  Screenshot mode: {screenshot.mode}")
    print(f"  Screenshot format: {screenshot.format or 'N/A (in memory)'}")

    # Get as bytes for different purposes
    png_bytes = capturer.get_screenshot_bytes(screenshot, "PNG")
    jpeg_bytes = capturer.get_screenshot_bytes(screenshot, "JPEG", quality=85)

    print(f"  PNG size in memory: {len(png_bytes):,} bytes")
    print(f"  JPEG size in memory: {len(jpeg_bytes):,} bytes")

    # You could now upload these bytes, send over network, etc.
    print("  ✓ Ready for network transmission or further processing")
    print()


def example_8_create_screenshot_grid():
    """Example 8: Create a grid of multiple screenshots."""
    print("Example 8: Screenshot grid/mosaic")

    capturer = ScreenshotCapturer()

    # Capture base screenshot
    full = capturer.capture_fullscreen()

    # Create 4 smaller captures from different regions
    grid_size = 2
    img_width = full.width // grid_size
    img_height = full.height // grid_size

    # Create new image for grid
    grid = Image.new("RGB", (img_width * 2, img_height * 2))

    positions = [
        (0, 0),
        (img_width, 0),
        (0, img_height),
        (img_width, img_height),
    ]

    for idx, (paste_x, paste_y) in enumerate(positions):
        # Capture different regions
        x_offset = (idx % 2) * img_width
        y_offset = (idx // 2) * img_height

        region = Region(x=x_offset, y=y_offset, width=img_width, height=img_height)
        screenshot = capturer.capture_region(region)

        # Resize to smaller
        small = screenshot.resize((img_width, img_height))
        grid.paste(small, (paste_x, paste_y))

    # Save grid
    filepath = capturer.save_screenshot(grid, "screenshot_grid.png")
    print(f"✓ Screenshot grid saved to: {filepath}")
    print()


def main():
    """Run all advanced examples."""
    print("=" * 60)
    print("Desktop Screenshot Capturer - Advanced Usage Examples")
    print("=" * 60)
    print()

    try:
        example_1_sequential_captures()
        example_2_multiple_regions()
        example_3_with_annotation()
        example_4_compare_formats()
        example_5_batch_processing()
        example_6_error_handling()
        example_7_in_memory_processing()
        example_8_create_screenshot_grid()

        print("=" * 60)
        print("All advanced examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"Error running examples: {e}")
        raise


if __name__ == "__main__":
    main()
