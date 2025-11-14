"""
Tests for the screenshot capturer module.
"""

import io
from pathlib import Path

import pytest
from PIL import Image

from screenshot_capturer.capturer import (
    CaptureMode,
    Region,
    ScreenshotCapturer,
)
from screenshot_capturer.exceptions import (
    CaptureFailedError,
    InvalidRegionError,
    SaveError,
)


class TestRegion:
    """Tests for the Region class."""

    def test_valid_region(self):
        """Test creating a valid region."""
        region = Region(x=10, y=20, width=800, height=600)
        assert region.x == 10
        assert region.y == 20
        assert region.width == 800
        assert region.height == 600

    def test_region_bbox(self):
        """Test bbox property."""
        region = Region(x=100, y=100, width=400, height=300)
        assert region.bbox == (100, 100, 500, 400)

    def test_invalid_dimensions(self):
        """Test region with invalid dimensions."""
        with pytest.raises(InvalidRegionError):
            Region(x=10, y=10, width=0, height=100)

        with pytest.raises(InvalidRegionError):
            Region(x=10, y=10, width=100, height=-10)

    def test_negative_coordinates(self):
        """Test region with negative coordinates."""
        with pytest.raises(InvalidRegionError):
            Region(x=-10, y=20, width=100, height=100)

        with pytest.raises(InvalidRegionError):
            Region(x=10, y=-20, width=100, height=100)


class TestScreenshotCapturer:
    """Tests for the ScreenshotCapturer class."""

    def test_capturer_initialization(self):
        """Test capturer can be initialized."""
        capturer = ScreenshotCapturer()
        assert capturer is not None
        assert capturer.platform in ["Windows", "Linux", "Darwin"]

    def test_supported_formats(self):
        """Test supported formats property."""
        capturer = ScreenshotCapturer()
        formats = capturer.supported_formats
        assert "PNG" in formats
        assert "JPEG" in formats
        assert "BMP" in formats

    def test_capture_fullscreen(self):
        """Test fullscreen capture."""
        capturer = ScreenshotCapturer()
        screenshot = capturer.capture_fullscreen()
        assert isinstance(screenshot, Image.Image)
        assert screenshot.width > 0
        assert screenshot.height > 0

    def test_capture_region(self):
        """Test region capture."""
        capturer = ScreenshotCapturer()
        region = Region(x=0, y=0, width=100, height=100)
        screenshot = capturer.capture_region(region)
        assert isinstance(screenshot, Image.Image)
        assert screenshot.width == 100
        assert screenshot.height == 100

    def test_save_screenshot_png(self, temp_dir):
        """Test saving screenshot as PNG."""
        capturer = ScreenshotCapturer()
        screenshot = capturer.capture_fullscreen()
        filepath = temp_dir / "test.png"

        result = capturer.save_screenshot(screenshot, filepath)
        assert result.exists()
        assert result.suffix == ".png"

        # Verify the saved image can be loaded
        loaded = Image.open(result)
        assert loaded.size == screenshot.size

    def test_save_screenshot_jpeg(self, temp_dir):
        """Test saving screenshot as JPEG."""
        capturer = ScreenshotCapturer()
        screenshot = capturer.capture_fullscreen()
        filepath = temp_dir / "test.jpg"

        result = capturer.save_screenshot(screenshot, filepath, quality=85)
        assert result.exists()
        assert result.suffix == ".jpg"

    def test_save_screenshot_auto_format(self, temp_dir):
        """Test auto-detecting format from filename."""
        capturer = ScreenshotCapturer()
        screenshot = capturer.capture_fullscreen()

        # Test various extensions
        for ext in [".png", ".jpg", ".bmp"]:
            filepath = temp_dir / f"test{ext}"
            result = capturer.save_screenshot(screenshot, filepath)
            assert result.exists()
            assert result.suffix == ext

    def test_save_screenshot_creates_directories(self, temp_dir):
        """Test that save_screenshot creates parent directories."""
        capturer = ScreenshotCapturer()
        screenshot = capturer.capture_fullscreen()
        filepath = temp_dir / "subdir1" / "subdir2" / "test.png"

        result = capturer.save_screenshot(screenshot, filepath)
        assert result.exists()
        assert result.parent.exists()

    def test_get_screenshot_bytes_png(self):
        """Test getting screenshot as PNG bytes."""
        capturer = ScreenshotCapturer()
        screenshot = capturer.capture_fullscreen()
        data = capturer.get_screenshot_bytes(screenshot, format="PNG")

        assert isinstance(data, bytes)
        assert len(data) > 0

        # Verify bytes can be loaded as image
        img = Image.open(io.BytesIO(data))
        assert img.size == screenshot.size

    def test_get_screenshot_bytes_jpeg(self):
        """Test getting screenshot as JPEG bytes."""
        capturer = ScreenshotCapturer()
        screenshot = capturer.capture_fullscreen()
        data = capturer.get_screenshot_bytes(screenshot, format="JPEG", quality=80)

        assert isinstance(data, bytes)
        assert len(data) > 0

        # Verify bytes can be loaded as image
        img = Image.open(io.BytesIO(data))
        assert img.size == screenshot.size

    def test_quick_capture_fullscreen(self, temp_dir):
        """Test quick_capture in fullscreen mode."""
        capturer = ScreenshotCapturer()
        filepath = temp_dir / "quick.png"

        result = capturer.quick_capture(filepath=filepath)
        assert result.exists()
        assert isinstance(result, Path)

    def test_quick_capture_region(self, temp_dir):
        """Test quick_capture in region mode."""
        capturer = ScreenshotCapturer()
        filepath = temp_dir / "quick_region.png"
        region = Region(x=0, y=0, width=200, height=200)

        result = capturer.quick_capture(
            filepath=filepath, mode=CaptureMode.REGION, region=region
        )
        assert result.exists()

    def test_quick_capture_no_filepath(self):
        """Test quick_capture without filepath returns Image."""
        capturer = ScreenshotCapturer()
        result = capturer.quick_capture()
        assert isinstance(result, Image.Image)

    def test_quick_capture_region_without_region_param(self):
        """Test quick_capture region mode without region raises error."""
        capturer = ScreenshotCapturer()
        with pytest.raises(InvalidRegionError):
            capturer.quick_capture(mode=CaptureMode.REGION)


class TestCaptureMode:
    """Tests for CaptureMode enum."""

    def test_capture_mode_values(self):
        """Test CaptureMode enum values."""
        assert CaptureMode.FULLSCREEN.value == "fullscreen"
        assert CaptureMode.REGION.value == "region"
        assert CaptureMode.ACTIVE_WINDOW.value == "active_window"

    def test_capture_mode_from_string(self):
        """Test creating CaptureMode from string."""
        mode = CaptureMode("fullscreen")
        assert mode == CaptureMode.FULLSCREEN
