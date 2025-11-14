"""
Custom exceptions for the screenshot capturer module.
"""


class ScreenshotCapturerError(Exception):
    """Base exception for all screenshot capturer errors."""

    pass


class PlatformNotSupportedError(ScreenshotCapturerError):
    """Raised when the current platform is not supported."""

    def __init__(self, platform: str):
        self.platform = platform
        super().__init__(f"Platform '{platform}' is not supported")


class CaptureFailedError(ScreenshotCapturerError):
    """Raised when screenshot capture fails."""

    pass


class InvalidRegionError(ScreenshotCapturerError):
    """Raised when an invalid region is specified for capture."""

    pass


class SaveError(ScreenshotCapturerError):
    """Raised when saving a screenshot fails."""

    pass
