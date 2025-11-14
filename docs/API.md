# API Documentation

Complete API reference for the Desktop Screenshot Capturer library.

## Table of Contents

- [ScreenshotCapturer](#screenshotcapturer)
- [Region](#region)
- [CaptureMode](#capturemode)
- [Config](#config)
- [Exceptions](#exceptions)

---

## ScreenshotCapturer

The main class for capturing screenshots.

### Constructor

```python
ScreenshotCapturer()
```

Initializes the screenshot capturer.

**Raises:**
- `ImportError`: If Pillow is not installed
- `PlatformNotSupportedError`: If the platform is not supported

**Example:**
```python
from screenshot_capturer import ScreenshotCapturer

capturer = ScreenshotCapturer()
```

### Methods

#### capture_fullscreen()

```python
capture_fullscreen() -> Image.Image
```

Captures the entire screen.

**Returns:**
- `PIL.Image.Image`: The captured screenshot

**Raises:**
- `CaptureFailedError`: If the capture operation fails

**Example:**
```python
screenshot = capturer.capture_fullscreen()
```

#### capture_region()

```python
capture_region(region: Region) -> Image.Image
```

Captures a specific region of the screen.

**Parameters:**
- `region` (Region): Region object defining the area to capture

**Returns:**
- `PIL.Image.Image`: The captured screenshot

**Raises:**
- `CaptureFailedError`: If the capture operation fails
- `InvalidRegionError`: If the region is invalid

**Example:**
```python
from screenshot_capturer import Region

region = Region(x=100, y=100, width=800, height=600)
screenshot = capturer.capture_region(region)
```

#### capture_active_window()

```python
capture_active_window() -> Image.Image
```

Captures the currently active window.

**Note:** Limited support on Linux. Platform-dependent feature.

**Returns:**
- `PIL.Image.Image`: The captured screenshot

**Raises:**
- `CaptureFailedError`: If the capture operation fails
- `PlatformNotSupportedError`: If the platform doesn't support this feature

**Example:**
```python
screenshot = capturer.capture_active_window()
```

#### save_screenshot()

```python
save_screenshot(
    screenshot: Image.Image,
    filepath: Union[str, Path],
    format: Optional[str] = None,
    quality: int = 95
) -> Path
```

Saves a screenshot to a file.

**Parameters:**
- `screenshot` (Image.Image): PIL Image object to save
- `filepath` (Union[str, Path]): Path where the screenshot should be saved
- `format` (Optional[str]): Image format (PNG, JPEG, BMP, etc.). Auto-detected from filename if None
- `quality` (int): JPEG quality (1-100), only used for JPEG format

**Returns:**
- `Path`: Absolute path to the saved file

**Raises:**
- `SaveError`: If saving fails

**Example:**
```python
screenshot = capturer.capture_fullscreen()
path = capturer.save_screenshot(screenshot, "screenshot.png", "PNG", 95)
```

#### get_screenshot_bytes()

```python
get_screenshot_bytes(
    screenshot: Image.Image,
    format: str = "PNG",
    quality: int = 95
) -> bytes
```

Converts a screenshot to bytes.

**Parameters:**
- `screenshot` (Image.Image): PIL Image object
- `format` (str): Image format (PNG, JPEG, BMP, etc.)
- `quality` (int): JPEG quality (1-100), only used for JPEG format

**Returns:**
- `bytes`: Screenshot as bytes

**Raises:**
- `SaveError`: If conversion fails

**Example:**
```python
screenshot = capturer.capture_fullscreen()
data = capturer.get_screenshot_bytes(screenshot, "PNG")
```

#### quick_capture()

```python
quick_capture(
    filepath: Optional[Union[str, Path]] = None,
    mode: CaptureMode = CaptureMode.FULLSCREEN,
    region: Optional[Region] = None,
    format: str = "PNG",
    quality: int = 95
) -> Union[Path, Image.Image]
```

Quick capture method with sensible defaults.

**Parameters:**
- `filepath` (Optional[Union[str, Path]]): Where to save (if None, returns PIL Image)
- `mode` (CaptureMode): Capture mode to use
- `region` (Optional[Region]): Region to capture (required if mode is REGION)
- `format` (str): Image format
- `quality` (int): JPEG quality (1-100)

**Returns:**
- `Union[Path, Image.Image]`: Path if filepath provided, otherwise PIL.Image.Image

**Raises:**
- Various exceptions from capture and save operations

**Example:**
```python
# Save to file
path = capturer.quick_capture(filepath="screenshot.png")

# Return as Image
screenshot = capturer.quick_capture()
```

### Properties

#### platform

```python
@property
platform -> str
```

Gets the current platform name.

**Returns:**
- `str`: Platform name ("Windows", "Linux", or "Darwin")

**Example:**
```python
print(capturer.platform)  # "Linux"
```

#### supported_formats

```python
@property
supported_formats -> list
```

Gets list of supported image formats.

**Returns:**
- `list`: List of supported format strings

**Example:**
```python
print(capturer.supported_formats)
# ['PNG', 'JPEG', 'JPG', 'BMP', 'GIF', 'TIFF', 'WebP']
```

---

## Region

Represents a rectangular region for screenshot capture.

### Constructor

```python
Region(x: int, y: int, width: int, height: int)
```

**Parameters:**
- `x` (int): X-coordinate of top-left corner
- `y` (int): Y-coordinate of top-left corner
- `width` (int): Width of region
- `height` (int): Height of region

**Raises:**
- `InvalidRegionError`: If dimensions are invalid

**Example:**
```python
from screenshot_capturer import Region

region = Region(x=100, y=100, width=800, height=600)
```

### Properties

#### bbox

```python
@property
bbox -> Tuple[int, int, int, int]
```

Returns bounding box tuple (x1, y1, x2, y2) for PIL.

**Returns:**
- `Tuple[int, int, int, int]`: Bounding box coordinates

**Example:**
```python
region = Region(10, 10, 100, 100)
print(region.bbox)  # (10, 10, 110, 110)
```

---

## CaptureMode

Enum defining available capture modes.

### Values

- `CaptureMode.FULLSCREEN`: Full screen capture
- `CaptureMode.REGION`: Region-based capture
- `CaptureMode.ACTIVE_WINDOW`: Active window capture

**Example:**
```python
from screenshot_capturer import CaptureMode

mode = CaptureMode.FULLSCREEN
```

---

## Config

Configuration manager for the screenshot capturer.

### Constructor

```python
Config(config_file: Optional[Path] = None)
```

**Parameters:**
- `config_file` (Optional[Path]): Path to configuration file. Uses default if None.

**Example:**
```python
from screenshot_capturer.config import Config

config = Config()
```

### Methods

#### load()

```python
load() -> None
```

Loads configuration from file or creates default if it doesn't exist.

#### save()

```python
save() -> None
```

Saves current configuration to file.

**Raises:**
- `IOError`: If saving fails

#### get()

```python
get(key: str, default: Any = None) -> Any
```

Gets a configuration value.

**Parameters:**
- `key` (str): Configuration key
- `default` (Any): Default value if key doesn't exist

**Returns:**
- `Any`: Configuration value or default

#### set()

```python
set(key: str, value: Any) -> None
```

Sets a configuration value.

**Parameters:**
- `key` (str): Configuration key
- `value` (Any): Configuration value

#### reset()

```python
reset() -> None
```

Resets configuration to defaults.

### Properties

#### default_format

```python
@property
default_format -> str

@default_format.setter
default_format(value: str) -> None
```

Gets or sets default image format.

#### default_quality

```python
@property
default_quality -> int

@default_quality.setter
default_quality(value: int) -> None
```

Gets or sets default JPEG quality (1-100).

**Raises:**
- `ValueError`: If quality is not between 1 and 100

#### default_output_dir

```python
@property
default_output_dir -> Path

@default_output_dir.setter
default_output_dir(value: Path) -> None
```

Gets or sets default output directory.

---

## Exceptions

All custom exceptions inherit from `ScreenshotCapturerError`.

### ScreenshotCapturerError

Base exception for all screenshot capturer errors.

```python
class ScreenshotCapturerError(Exception)
```

### PlatformNotSupportedError

Raised when the current platform is not supported.

```python
class PlatformNotSupportedError(ScreenshotCapturerError)
```

**Attributes:**
- `platform` (str): The unsupported platform name

### CaptureFailedError

Raised when screenshot capture fails.

```python
class CaptureFailedError(ScreenshotCapturerError)
```

### InvalidRegionError

Raised when an invalid region is specified.

```python
class InvalidRegionError(ScreenshotCapturerError)
```

### SaveError

Raised when saving a screenshot fails.

```python
class SaveError(ScreenshotCapturerError)
```

**Example:**
```python
from screenshot_capturer.exceptions import (
    ScreenshotCapturerError,
    CaptureFailedError
)

try:
    screenshot = capturer.capture_fullscreen()
except CaptureFailedError as e:
    print(f"Capture failed: {e}")
except ScreenshotCapturerError as e:
    print(f"General error: {e}")
```

---

## Type Hints

The library uses type hints throughout. Import types for your own code:

```python
from pathlib import Path
from typing import Optional, Union, Tuple
from PIL import Image

from screenshot_capturer import ScreenshotCapturer, Region
from screenshot_capturer.capturer import CaptureMode
```

---

## See Also

- [README.md](../README.md) - General documentation
- [Examples](../examples/) - Usage examples
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guide
