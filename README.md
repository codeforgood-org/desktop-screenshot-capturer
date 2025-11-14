# Desktop Screenshot Capturer

A cross-platform, feature-rich desktop screenshot capture tool with support for multiple capture modes, formats, and intuitive CLI interface.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- **Multiple Capture Modes**
  - Full screen capture
  - Region-based capture (specify exact coordinates)
  - Active window capture (platform-dependent)

- **Wide Format Support**
  - PNG, JPEG, BMP, GIF, TIFF, WebP
  - Configurable JPEG quality settings

- **Cross-Platform**
  - Windows, Linux, macOS support
  - Platform-specific optimizations

- **Flexible Configuration**
  - Command-line arguments for one-time use
  - Persistent configuration file for defaults
  - Easy-to-use configuration commands

- **Developer-Friendly**
  - Clean, well-documented API
  - Type hints throughout
  - Comprehensive test coverage
  - Easy to integrate into other projects

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/codeforgood-org/desktop-screenshot-capturer.git
cd desktop-screenshot-capturer

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (when published)

```bash
pip install screenshot-capturer
```

## Quick Start

### Command Line Usage

```bash
# Capture full screen (saves to current directory with timestamp)
screenshot-capturer

# Capture to specific file
screenshot-capturer -o ~/Pictures/my_screenshot.png

# Capture a specific region (x, y, width, height)
screenshot-capturer -m region -r 100,100,800,600

# Capture as JPEG with custom quality
screenshot-capturer -f jpeg -q 85 -o screenshot.jpg

# Show current configuration
screenshot-capturer --show-config

# Set default output format
screenshot-capturer --set-default-format png

# Set default output directory
screenshot-capturer --set-default-dir ~/Pictures
```

### Python API Usage

```python
from screenshot_capturer import ScreenshotCapturer, CaptureMode, Region

# Initialize the capturer
capturer = ScreenshotCapturer()

# Capture full screen
screenshot = capturer.capture_fullscreen()
capturer.save_screenshot(screenshot, "fullscreen.png")

# Capture a specific region
region = Region(x=100, y=100, width=800, height=600)
screenshot = capturer.capture_region(region)
capturer.save_screenshot(screenshot, "region.png")

# Quick capture with sensible defaults
capturer.quick_capture(
    filepath="screenshot.png",
    mode=CaptureMode.FULLSCREEN,
    format="PNG",
    quality=95
)

# Get screenshot as bytes (e.g., for uploading)
screenshot = capturer.capture_fullscreen()
image_bytes = capturer.get_screenshot_bytes(screenshot, format="PNG")
```

## CLI Options

```
usage: screenshot-capturer [-h] [--version] [-m {fullscreen,region,active_window}]
                           [-r X,Y,W,H] [-o PATH] [-f {png,jpeg,jpg,bmp,gif,tiff,webp}]
                           [-q N] [--show-config] [--set-default-format FORMAT]
                           [--set-default-dir PATH] [-v] [-q]

Cross-platform desktop screenshot capture tool

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -m, --mode            Screenshot capture mode (default: fullscreen)
  -r, --region X,Y,W,H  Region to capture in format 'x,y,width,height'
  -o, --output PATH     Output file path
  -f, --format          Output image format (default: png)
  -q, --quality N       JPEG quality 1-100 (default: 95)
  --show-config         Display current configuration and exit
  --set-default-format  Set default output format in config
  --set-default-dir     Set default output directory in config
  -v, --verbose         Enable verbose output
  -q, --quiet           Suppress all output except errors
```

## Configuration

The tool stores configuration in `~/.config/screenshot-capturer/config.json`.

Default configuration:
```json
{
  "default_format": "PNG",
  "default_quality": 95,
  "default_output_dir": "."
}
```

You can modify these defaults using command-line arguments or by editing the config file directly.

## Requirements

- Python 3.8 or higher
- Pillow (PIL) library

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/codeforgood-org/desktop-screenshot-capturer.git
cd desktop-screenshot-capturer

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=screenshot_capturer --cov-report=html

# Run specific test file
pytest tests/test_capturer.py
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type check with mypy
mypy src/

# Run all checks
make check
```

### Using Make Commands

```bash
make install     # Install the package
make test        # Run tests
make coverage    # Run tests with coverage
make lint        # Run linters
make format      # Format code
make check       # Run all quality checks
make clean       # Clean build artifacts
make docs        # Build documentation
```

## Architecture

```
src/screenshot_capturer/
├── __init__.py        # Package initialization and exports
├── __main__.py        # Entry point for module execution
├── capturer.py        # Core screenshot capture functionality
├── cli.py             # Command-line interface
├── config.py          # Configuration management
└── exceptions.py      # Custom exceptions

tests/                 # Comprehensive test suite
docs/                  # Additional documentation
examples/              # Usage examples
```

## Platform Support

| Platform | Fullscreen | Region | Active Window |
|----------|-----------|---------|---------------|
| Windows  | ✅        | ✅      | ✅            |
| Linux    | ✅        | ✅      | ⚠️*           |
| macOS    | ✅        | ✅      | ✅            |

*Active window capture on Linux requires additional tools (xdotool, wmctrl). Use region capture as an alternative.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and code quality checks (`make check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## Support

- **Issues**: [GitHub Issues](https://github.com/codeforgood-org/desktop-screenshot-capturer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/codeforgood-org/desktop-screenshot-capturer/discussions)

## Acknowledgments

- Built with [Pillow (PIL)](https://python-pillow.org/)
- Inspired by various screenshot tools in the Python ecosystem

## Roadmap

- [ ] GUI interface using tkinter or PyQt
- [ ] Screen recording functionality
- [ ] OCR text extraction from screenshots
- [ ] Cloud storage integration
- [ ] Screenshot annotation tools
- [ ] Hotkey support for quick captures
- [ ] Multi-monitor support improvements
- [ ] Image optimization and compression options

## Authors

- **Dang Linh Anh** - *Initial work* - [linhanhh1203@hotmail.com](mailto:linhanhh1203@hotmail.com)

---

Made with ❤️ by the Code for Good community
