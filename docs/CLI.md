# CLI Documentation

Complete command-line interface reference for Desktop Screenshot Capturer.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Commands and Options](#commands-and-options)
- [Configuration](#configuration)
- [Examples](#examples)
- [Tips and Tricks](#tips-and-tricks)

---

## Installation

After installing the package, two command-line tools are available:

```bash
screenshot-capturer  # Full name
screencap           # Short alias
```

Both commands are identical and can be used interchangeably.

---

## Basic Usage

### Simplest Usage

```bash
# Capture fullscreen to current directory with timestamp
screenshot-capturer
```

This creates a file like `screenshot_20240115_143052.png` in the current directory.

### Specify Output File

```bash
screenshot-capturer -o myscreen.png
```

### Different Format

```bash
screenshot-capturer -f jpeg -o screenshot.jpg
```

---

## Commands and Options

### Capture Modes

#### Fullscreen (default)

```bash
screenshot-capturer -m fullscreen
# or simply
screenshot-capturer
```

#### Region Capture

```bash
screenshot-capturer -m region -r 100,100,800,600
```

Format: `-r X,Y,WIDTH,HEIGHT`
- `X`: X-coordinate of top-left corner
- `Y`: Y-coordinate of top-left corner
- `WIDTH`: Width of region
- `HEIGHT`: Height of region

#### Active Window

```bash
screenshot-capturer -m active_window
```

**Note:** Limited support on Linux. May require additional tools.

### Output Options

#### Output Path (`-o, --output`)

Specify where to save the screenshot:

```bash
screenshot-capturer -o /path/to/screenshot.png
screenshot-capturer -o ~/Pictures/screenshot.png
screenshot-capturer -o "./screenshots/capture.png"
```

- Absolute or relative paths supported
- Parent directories created automatically
- If omitted, uses current directory with timestamp

#### Format (`-f, --format`)

Specify image format:

```bash
screenshot-capturer -f png
screenshot-capturer -f jpeg
screenshot-capturer -f bmp
```

Supported formats:
- `png` (default, lossless)
- `jpeg` / `jpg` (lossy compression)
- `bmp` (uncompressed)
- `gif`
- `tiff`
- `webp`

If format is not specified, it's auto-detected from the file extension.

#### Quality (`-q, --quality`)

Set JPEG quality (1-100, default: 95):

```bash
screenshot-capturer -f jpeg -q 85
screenshot-capturer -f jpeg -q 60  # Smaller file, lower quality
```

**Note:** Quality only affects JPEG format.

### Configuration Options

#### Show Configuration

```bash
screenshot-capturer --show-config
```

Displays:
```
Current Configuration:
  Default Format: PNG
  Default Directory: .
  Default Quality: 95
  Config File: /home/user/.config/screenshot-capturer/config.json
```

#### Set Default Format

```bash
screenshot-capturer --set-default-format jpeg
screenshot-capturer --set-default-format png
```

#### Set Default Directory

```bash
screenshot-capturer --set-default-dir ~/Pictures
screenshot-capturer --set-default-dir /tmp/screenshots
```

### Output Control

#### Verbose Mode (`-v, --verbose`)

Show detailed information:

```bash
screenshot-capturer -v
```

Output:
```
Initializing screenshot capturer...
Platform: Linux
Capture mode: fullscreen
Capturing screenshot...
Screenshot saved to: /home/user/screenshot_20240115_143052.png
```

#### Quiet Mode (`-q, --quiet`)

Suppress all output except errors:

```bash
screenshot-capturer -q -o screenshot.png
```

Useful for scripts and automation.

### Help and Version

#### Show Help

```bash
screenshot-capturer -h
screenshot-capturer --help
```

#### Show Version

```bash
screenshot-capturer --version
```

---

## Configuration

The CLI stores persistent configuration in `~/.config/screenshot-capturer/config.json`.

### Default Configuration

```json
{
  "default_format": "PNG",
  "default_quality": 95,
  "default_output_dir": "."
}
```

### Modifying Configuration

**Via CLI:**
```bash
screenshot-capturer --set-default-format jpeg
screenshot-capturer --set-default-dir ~/Pictures
```

**Via Config File:**
Edit `~/.config/screenshot-capturer/config.json` directly:
```json
{
  "default_format": "JPEG",
  "default_quality": 85,
  "default_output_dir": "/home/user/Pictures"
}
```

### Configuration Priority

1. Command-line arguments (highest priority)
2. Configuration file
3. Built-in defaults (lowest priority)

**Example:**
```bash
# Config says format is JPEG, but -f overrides it
screenshot-capturer -f png  # Saves as PNG despite config
```

---

## Examples

### Basic Examples

**Capture fullscreen:**
```bash
screenshot-capturer
```

**Save to specific location:**
```bash
screenshot-capturer -o ~/Pictures/myscreen.png
```

**Capture as JPEG:**
```bash
screenshot-capturer -f jpeg -o screenshot.jpg
```

### Region Capture Examples

**Capture top-left corner (400x300):**
```bash
screenshot-capturer -m region -r 0,0,400,300 -o corner.png
```

**Capture center region:**
```bash
screenshot-capturer -m region -r 400,300,800,600 -o center.png
```

### Quality and Format Examples

**High quality JPEG:**
```bash
screenshot-capturer -f jpeg -q 95 -o high_quality.jpg
```

**Low quality JPEG (smaller file):**
```bash
screenshot-capturer -f jpeg -q 50 -o small_file.jpg
```

**Uncompressed BMP:**
```bash
screenshot-capturer -f bmp -o uncompressed.bmp
```

### Advanced Examples

**Sequential captures with timestamps:**
```bash
for i in {1..5}; do
    screenshot-capturer -o "capture_$i.png"
    sleep 2
done
```

**Capture to organized directory:**
```bash
screenshot-capturer -o "$(date +%Y-%m)/$(date +%Y%m%d_%H%M%S).png"
```

**Silent capture for scripts:**
```bash
screenshot-capturer -q -o /tmp/screenshot.png && echo "Success"
```

**Verbose capture for debugging:**
```bash
screenshot-capturer -v -m region -r 0,0,800,600
```

### Scripting Examples

**Bash script for automated capture:**
```bash
#!/bin/bash
OUTPUT_DIR="$HOME/screenshots/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"
screenshot-capturer -o "$OUTPUT_DIR/$(date +%H%M%S).png"
```

**Python script using CLI:**
```python
import subprocess
from datetime import datetime

output = f"screenshot_{datetime.now():%Y%m%d_%H%M%S}.png"
subprocess.run(["screenshot-capturer", "-o", output])
```

---

## Tips and Tricks

### Tip 1: Use Aliases

Add to your `.bashrc` or `.zshrc`:
```bash
alias ss='screenshot-capturer'
alias ssc='screenshot-capturer -m region -r 0,0,800,600'  # Common region
```

Usage:
```bash
ss -o quick.png
ssc -o region.png
```

### Tip 2: Quick Region Capture

Create a script for frequently-used regions:
```bash
#!/bin/bash
# ~/bin/screenshot-region
screenshot-capturer -m region -r "$1,$2,$3,$4" -o "${5:-screenshot.png}"
```

Usage:
```bash
screenshot-region 100 100 800 600 output.png
```

### Tip 3: Timestamp in Filename

The default behavior already includes timestamps, but you can customize:
```bash
screenshot-capturer -o "screen_$(date +%Y%m%d_%H%M%S).png"
```

### Tip 4: Compression Comparison

Test different quality settings:
```bash
for q in 100 85 70 50; do
    screenshot-capturer -f jpeg -q $q -o "test_q${q}.jpg"
done
ls -lh test_q*.jpg  # Compare file sizes
```

### Tip 5: Integration with Other Tools

**Upload immediately:**
```bash
screenshot-capturer -o /tmp/screen.png && \
    curl -F "file=@/tmp/screen.png" https://example.com/upload
```

**Open immediately:**
```bash
screenshot-capturer -o temp.png && xdg-open temp.png  # Linux
screenshot-capturer -o temp.png && open temp.png      # macOS
```

### Tip 6: Keyboard Shortcuts

Set up keyboard shortcuts in your desktop environment:

**GNOME/Ubuntu:**
Settings → Keyboard → Custom Shortcuts

**KDE:**
System Settings → Shortcuts

**Example shortcut:**
- Command: `screenshot-capturer -o ~/Pictures/$(date +%Y%m%d_%H%M%S).png`
- Key: `Print` or `Super+Shift+S`

---

## Troubleshooting

### Common Issues

**Issue:** "Command not found"
```bash
# Solution: Ensure package is installed
pip install -e .
```

**Issue:** Permission denied when saving
```bash
# Solution: Check directory permissions
ls -la /path/to/directory
# Or save to a different location
screenshot-capturer -o ~/Pictures/screenshot.png
```

**Issue:** Invalid region error
```bash
# Solution: Check coordinates are non-negative and dimensions are positive
screenshot-capturer -m region -r 0,0,800,600  # Valid
screenshot-capturer -m region -r -10,0,800,600  # Invalid (negative X)
```

### Debug Mode

For troubleshooting, use verbose mode:
```bash
screenshot-capturer -v -o test.png
```

---

## See Also

- [API Documentation](API.md) - Python API reference
- [README.md](../README.md) - General documentation
- [Examples](../examples/) - Usage examples
