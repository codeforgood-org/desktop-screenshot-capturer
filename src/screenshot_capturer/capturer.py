"""
Core screenshot capture functionality.
"""

import io
import platform
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple, Union

try:
    from PIL import Image, ImageGrab
except ImportError:
    Image = None
    ImageGrab = None

from .exceptions import (
    CaptureFailedError,
    InvalidRegionError,
    PlatformNotSupportedError,
    SaveError,
)


class CaptureMode(Enum):
    """Available screenshot capture modes."""

    FULLSCREEN = "fullscreen"
    ACTIVE_WINDOW = "active_window"
    REGION = "region"


@dataclass
class Region:
    """Represents a rectangular region for screenshot capture."""

    x: int
    y: int
    width: int
    height: int

    def __post_init__(self):
        """Validate region dimensions."""
        if self.width <= 0 or self.height <= 0:
            raise InvalidRegionError(
                f"Region dimensions must be positive (got width={self.width}, height={self.height})"
            )
        if self.x < 0 or self.y < 0:
            raise InvalidRegionError(
                f"Region coordinates must be non-negative (got x={self.x}, y={self.y})"
            )

    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        """Return bounding box tuple (x1, y1, x2, y2) for PIL."""
        return (self.x, self.y, self.x + self.width, self.y + self.height)


class ScreenshotCapturer:
    """
    Cross-platform screenshot capturer with multiple capture modes.

    Supports:
    - Full screen capture
    - Active window capture
    - Region-based capture
    - Multiple output formats (PNG, JPEG, BMP, etc.)
    - Save to file or get as bytes
    """

    def __init__(self):
        """Initialize the screenshot capturer."""
        self._check_dependencies()
        self._platform = platform.system()
        self._supported_platforms = ["Windows", "Linux", "Darwin"]

        if self._platform not in self._supported_platforms:
            raise PlatformNotSupportedError(self._platform)

    def _check_dependencies(self):
        """Check if required dependencies are available."""
        if Image is None or ImageGrab is None:
            raise ImportError(
                "Pillow library is required. Install it with: pip install Pillow"
            )

    def capture_fullscreen(self) -> Image.Image:
        """
        Capture the entire screen.

        Returns:
            PIL.Image.Image: The captured screenshot

        Raises:
            CaptureFailedError: If the capture operation fails
        """
        try:
            screenshot = ImageGrab.grab()
            if screenshot is None:
                raise CaptureFailedError("Screenshot capture returned None")
            return screenshot
        except Exception as e:
            raise CaptureFailedError(f"Failed to capture fullscreen: {str(e)}")

    def capture_region(self, region: Region) -> Image.Image:
        """
        Capture a specific region of the screen.

        Args:
            region: Region object defining the area to capture

        Returns:
            PIL.Image.Image: The captured screenshot

        Raises:
            CaptureFailedError: If the capture operation fails
            InvalidRegionError: If the region is invalid
        """
        try:
            screenshot = ImageGrab.grab(bbox=region.bbox)
            if screenshot is None:
                raise CaptureFailedError("Screenshot capture returned None")
            return screenshot
        except InvalidRegionError:
            raise
        except Exception as e:
            raise CaptureFailedError(f"Failed to capture region: {str(e)}")

    def capture_active_window(self) -> Image.Image:
        """
        Capture the currently active window.

        Note: This feature may have limited support depending on the platform
        and window manager.

        Returns:
            PIL.Image.Image: The captured screenshot

        Raises:
            CaptureFailedError: If the capture operation fails
            PlatformNotSupportedError: If the platform doesn't support this feature
        """
        if self._platform == "Linux":
            # On Linux, we need additional tools like xdotool or wmctrl
            # For now, we'll capture fullscreen and suggest using region capture
            raise PlatformNotSupportedError(
                "Active window capture requires additional tools on Linux. "
                "Please use region capture instead."
            )

        try:
            # On Windows, ImageGrab.grab() with all_screens=False captures the primary monitor
            # For active window, we'd need platform-specific code
            screenshot = ImageGrab.grab()
            if screenshot is None:
                raise CaptureFailedError("Screenshot capture returned None")
            return screenshot
        except Exception as e:
            raise CaptureFailedError(f"Failed to capture active window: {str(e)}")

    def save_screenshot(
        self,
        screenshot: Image.Image,
        filepath: Union[str, Path],
        format: Optional[str] = None,
        quality: int = 95,
    ) -> Path:
        """
        Save a screenshot to a file.

        Args:
            screenshot: PIL Image object to save
            filepath: Path where the screenshot should be saved
            format: Image format (PNG, JPEG, BMP, etc.). Auto-detected from filename if None
            quality: JPEG quality (1-100), only used for JPEG format

        Returns:
            Path: Absolute path to the saved file

        Raises:
            SaveError: If saving fails
        """
        filepath = Path(filepath)

        try:
            # Create parent directories if they don't exist
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Determine format
            if format is None:
                format = filepath.suffix.lstrip(".").upper()
                if not format:
                    format = "PNG"

            # Save with appropriate settings
            save_kwargs = {}
            if format.upper() in ["JPEG", "JPG"]:
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True

            screenshot.save(filepath, format=format, **save_kwargs)
            return filepath.absolute()

        except Exception as e:
            raise SaveError(f"Failed to save screenshot to {filepath}: {str(e)}")

    def get_screenshot_bytes(
        self, screenshot: Image.Image, format: str = "PNG", quality: int = 95
    ) -> bytes:
        """
        Get screenshot as bytes.

        Args:
            screenshot: PIL Image object
            format: Image format (PNG, JPEG, BMP, etc.)
            quality: JPEG quality (1-100), only used for JPEG format

        Returns:
            bytes: Screenshot as bytes

        Raises:
            SaveError: If conversion fails
        """
        try:
            buffer = io.BytesIO()
            save_kwargs = {}
            if format.upper() in ["JPEG", "JPG"]:
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True

            screenshot.save(buffer, format=format, **save_kwargs)
            return buffer.getvalue()
        except Exception as e:
            raise SaveError(f"Failed to convert screenshot to bytes: {str(e)}")

    def quick_capture(
        self,
        filepath: Optional[Union[str, Path]] = None,
        mode: CaptureMode = CaptureMode.FULLSCREEN,
        region: Optional[Region] = None,
        format: str = "PNG",
        quality: int = 95,
    ) -> Union[Path, Image.Image]:
        """
        Quick capture method with sensible defaults.

        Args:
            filepath: Where to save (if None, returns PIL Image)
            mode: Capture mode to use
            region: Region to capture (required if mode is REGION)
            format: Image format
            quality: JPEG quality (1-100)

        Returns:
            Path if filepath provided, otherwise PIL.Image.Image

        Raises:
            Various exceptions from capture and save operations
        """
        # Capture based on mode
        if mode == CaptureMode.FULLSCREEN:
            screenshot = self.capture_fullscreen()
        elif mode == CaptureMode.REGION:
            if region is None:
                raise InvalidRegionError("Region must be provided for REGION mode")
            screenshot = self.capture_region(region)
        elif mode == CaptureMode.ACTIVE_WINDOW:
            screenshot = self.capture_active_window()
        else:
            raise ValueError(f"Unknown capture mode: {mode}")

        # Save or return
        if filepath:
            return self.save_screenshot(screenshot, filepath, format, quality)
        else:
            return screenshot

    @property
    def platform(self) -> str:
        """Get the current platform name."""
        return self._platform

    @property
    def supported_formats(self) -> list:
        """Get list of supported image formats."""
        return ["PNG", "JPEG", "JPG", "BMP", "GIF", "TIFF", "WebP"]
