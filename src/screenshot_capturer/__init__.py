"""
Desktop Screenshot Capturer

A cross-platform screenshot capture library with support for multiple
capture modes, formats, and platforms.
"""

__version__ = "1.0.0"
__author__ = "Dang Linh Anh"
__license__ = "MIT"

from .capturer import ScreenshotCapturer, CaptureMode
from .exceptions import (
    ScreenshotCapturerError,
    PlatformNotSupportedError,
    CaptureFailedError,
)

__all__ = [
    "ScreenshotCapturer",
    "CaptureMode",
    "ScreenshotCapturerError",
    "PlatformNotSupportedError",
    "CaptureFailedError",
]
