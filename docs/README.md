# Documentation

Welcome to the Desktop Screenshot Capturer documentation!

## Available Documentation

### User Documentation

- **[CLI Documentation](CLI.md)** - Complete command-line interface reference
  - Installation
  - All commands and options
  - Configuration
  - Examples and tips

- **[API Documentation](API.md)** - Python API reference
  - Complete class and method reference
  - Type hints and signatures
  - Examples for each API

### Developer Documentation

- **[README.md](../README.md)** - Project overview and quick start
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contributing guidelines
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history and changes
- **[Examples](../examples/)** - Practical code examples

## Quick Links

### For Users

- **Getting Started:** See main [README.md](../README.md)
- **Command-Line Usage:** See [CLI Documentation](CLI.md)
- **Python API:** See [API Documentation](API.md)
- **Examples:** See [examples/](../examples/)

### For Developers

- **Setup Development Environment:** [CONTRIBUTING.md](../CONTRIBUTING.md#development-setup)
- **Running Tests:** [CONTRIBUTING.md](../CONTRIBUTING.md#testing)
- **Code Style:** [CONTRIBUTING.md](../CONTRIBUTING.md#code-style)
- **Submit Changes:** [CONTRIBUTING.md](../CONTRIBUTING.md#submitting-changes)

## Documentation Structure

```
docs/
├── README.md           # This file - documentation overview
├── API.md             # Complete Python API reference
└── CLI.md             # Complete CLI reference

../
├── README.md          # Project overview and quick start
├── CONTRIBUTING.md    # Contributing guidelines
├── CHANGELOG.md       # Version history
└── examples/          # Practical examples
    ├── basic_usage.py
    ├── advanced_usage.py
    └── README.md
```

## Getting Help

### Documentation

1. Check this documentation
2. Review [examples/](../examples/)
3. Read the [README.md](../README.md)

### Issues and Support

- **Bug Reports:** [GitHub Issues](https://github.com/codeforgood-org/desktop-screenshot-capturer/issues)
- **Feature Requests:** [GitHub Issues](https://github.com/codeforgood-org/desktop-screenshot-capturer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/codeforgood-org/desktop-screenshot-capturer/discussions)

### Contributing

Want to improve the documentation?

1. Fork the repository
2. Make your changes
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## Frequently Asked Questions

### How do I install?

```bash
pip install desktop-screenshot-capturer
# or from source
git clone https://github.com/codeforgood-org/desktop-screenshot-capturer.git
cd desktop-screenshot-capturer
pip install -e .
```

### How do I capture a screenshot?

**CLI:**
```bash
screenshot-capturer -o screenshot.png
```

**Python:**
```python
from screenshot_capturer import ScreenshotCapturer
capturer = ScreenshotCapturer()
capturer.quick_capture(filepath="screenshot.png")
```

### What formats are supported?

PNG, JPEG, BMP, GIF, TIFF, WebP

See [API.md](API.md#supported_formats) for details.

### What platforms are supported?

Windows, Linux, and macOS

See [README.md](../README.md#platform-support) for platform-specific notes.

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

This project is licensed under the MIT License - see [LICENSE](../LICENSE) for details.

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for version history.
