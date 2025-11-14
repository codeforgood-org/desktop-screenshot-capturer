"""
Tests for custom exceptions.
"""

import pytest

from screenshot_capturer.exceptions import (
    ScreenshotCapturerError,
    PlatformNotSupportedError,
    CaptureFailedError,
    InvalidRegionError,
    SaveError,
)


class TestExceptions:
    """Tests for custom exception classes."""

    def test_base_exception(self):
        """Test base ScreenshotCapturerError."""
        error = ScreenshotCapturerError("test error")
        assert str(error) == "test error"
        assert isinstance(error, Exception)

    def test_platform_not_supported_error(self):
        """Test PlatformNotSupportedError."""
        error = PlatformNotSupportedError("AmigaOS")
        assert "AmigaOS" in str(error)
        assert "not supported" in str(error)
        assert error.platform == "AmigaOS"
        assert isinstance(error, ScreenshotCapturerError)

    def test_capture_failed_error(self):
        """Test CaptureFailedError."""
        error = CaptureFailedError("Capture failed")
        assert str(error) == "Capture failed"
        assert isinstance(error, ScreenshotCapturerError)

    def test_invalid_region_error(self):
        """Test InvalidRegionError."""
        error = InvalidRegionError("Invalid region dimensions")
        assert "Invalid region" in str(error)
        assert isinstance(error, ScreenshotCapturerError)

    def test_save_error(self):
        """Test SaveError."""
        error = SaveError("Failed to save file")
        assert "Failed to save" in str(error)
        assert isinstance(error, ScreenshotCapturerError)

    def test_exception_inheritance(self):
        """Test that all exceptions inherit from base."""
        exceptions = [
            PlatformNotSupportedError("test"),
            CaptureFailedError("test"),
            InvalidRegionError("test"),
            SaveError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, ScreenshotCapturerError)
            assert isinstance(exc, Exception)
