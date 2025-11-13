# Examples

This directory contains example scripts demonstrating various features of the Desktop Screenshot Capturer.

## Available Examples

### basic_usage.py

Demonstrates fundamental features:
- Simple fullscreen capture
- Region-based capture
- Saving in different formats
- Quick capture method
- Getting screenshots as bytes
- Working with directories
- Platform information

**Run it:**
```bash
python examples/basic_usage.py
```

### advanced_usage.py

Demonstrates advanced features:
- Sequential captures (time-lapse)
- Multiple region captures
- Screenshot annotation
- Format comparison and file sizes
- Batch processing
- Error handling
- In-memory processing
- Creating screenshot grids/mosaics

**Run it:**
```bash
python examples/advanced_usage.py
```

## Quick Start

1. Install the package:
```bash
pip install -e .
```

2. Run any example:
```bash
python examples/basic_usage.py
```

## Example Output

All examples save screenshots to the current directory or organized subdirectories:

```
examples/
├── basic_usage.py
├── advanced_usage.py
├── README.md
└── screenshots/           # Created when running examples
    ├── timelapse/
    ├── regions/
    ├── batch/
    └── ...
```

## Creating Your Own

Use these examples as templates for your own projects. The basic pattern is:

```python
from screenshot_capturer import ScreenshotCapturer, Region

# Initialize
capturer = ScreenshotCapturer()

# Capture
screenshot = capturer.capture_fullscreen()
# or
screenshot = capturer.capture_region(Region(0, 0, 800, 600))

# Save
capturer.save_screenshot(screenshot, "output.png")
```

## Tips

- All examples handle errors gracefully
- Screenshots are saved with descriptive names
- Directories are created automatically
- Examples are self-contained and can run independently
- Check the source code for detailed comments

## Need Help?

- Check the main [README.md](../README.md) for full documentation
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
- Open an issue if you find problems with examples
