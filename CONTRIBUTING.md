# Contributing to Desktop Screenshot Capturer

Thank you for your interest in contributing to Desktop Screenshot Capturer! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful, inclusive, and considerate in all interactions.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of screenshot capture concepts

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/desktop-screenshot-capturer.git
cd desktop-screenshot-capturer
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies**

```bash
make install-dev
# or manually:
pip install -r requirements-dev.txt
pip install -e .
```

4. **Install pre-commit hooks**

```bash
pre-commit install
```

## Making Changes

### Branching Strategy

- Create a new branch for each feature or bugfix
- Use descriptive branch names:
  - `feature/add-clipboard-support`
  - `bugfix/fix-region-capture`
  - `docs/update-readme`

```bash
git checkout -b feature/your-feature-name
```

### Development Workflow

1. **Make your changes** in the appropriate files
2. **Add tests** for new functionality
3. **Run tests** to ensure nothing breaks
4. **Format code** to match project style
5. **Commit your changes** with clear messages
6. **Push to your fork** and create a pull request

## Code Style

We follow PEP 8 and use automated tools to enforce code style:

### Python Code Standards

- **Line length**: 88 characters (Black default)
- **Docstrings**: Google-style docstrings for all public functions/classes
- **Type hints**: Required for all function signatures
- **Import organization**: Sorted with isort

### Running Code Formatters

```bash
# Format all code
make format

# Or individually:
black src/ tests/
isort src/ tests/
```

### Running Linters

```bash
# Run all linters
make lint

# Or individually:
flake8 src/ tests/
pylint src/screenshot_capturer/
mypy src/
```

### Example Code Style

```python
from typing import Optional
from pathlib import Path


def capture_screenshot(
    filepath: Optional[Path] = None,
    format: str = "PNG",
    quality: int = 95,
) -> Path:
    """
    Capture a screenshot and save it to a file.

    Args:
        filepath: Output file path. Auto-generated if None.
        format: Image format (PNG, JPEG, etc.)
        quality: JPEG quality (1-100)

    Returns:
        Path: Absolute path to saved screenshot

    Raises:
        SaveError: If saving fails
    """
    # Implementation here
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run specific test file
pytest tests/test_capturer.py

# Run specific test
pytest tests/test_capturer.py::TestScreenshotCapturer::test_capture_fullscreen
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_<what>_<condition>_<expected>`
- Follow AAA pattern: Arrange, Act, Assert
- Use fixtures for common setup
- Aim for high coverage (>80%)

Example test:

```python
def test_capture_region_with_valid_dimensions(self):
    """Test capturing a region with valid dimensions."""
    # Arrange
    capturer = ScreenshotCapturer()
    region = Region(x=0, y=0, width=100, height=100)

    # Act
    screenshot = capturer.capture_region(region)

    # Assert
    assert screenshot.width == 100
    assert screenshot.height == 100
```

### Test Coverage

We strive for high test coverage. Check coverage with:

```bash
pytest --cov=screenshot_capturer --cov-report=html
# Open htmlcov/index.html in browser
```

## Submitting Changes

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(capturer): add clipboard support for screenshots

- Implement clipboard copy functionality
- Add tests for clipboard operations
- Update documentation

Closes #123
```

```
fix(cli): handle invalid region coordinates gracefully

Previously, the CLI would crash with invalid coordinates.
Now it shows a helpful error message.

Fixes #456
```

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass** (`make check`)
4. **Update CHANGELOG.md** with your changes
5. **Create pull request** with:
   - Clear title and description
   - Link to related issues
   - Screenshots/examples if relevant
   - Checklist of completed items

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No breaking changes (or documented)
```

## Reporting Issues

### Bug Reports

When reporting bugs, include:

- **Clear title** describing the issue
- **Python version** and OS
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Error messages** or logs
- **Screenshots** if applicable

### Feature Requests

When requesting features, include:

- **Clear description** of the feature
- **Use case** explaining why it's needed
- **Proposed solution** if you have one
- **Alternative solutions** considered

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Community help needed

## Development Tips

### Useful Commands

```bash
# Run all quality checks
make check

# Clean build artifacts
make clean

# Build distribution
make build

# View all available commands
make help
```

### Debugging

- Use `pytest -vv` for verbose test output
- Use `pytest -s` to see print statements
- Use `pytest --pdb` to drop into debugger on failures
- Add `breakpoint()` in code for interactive debugging

### Platform-Specific Testing

If you're adding platform-specific code:

1. Test on multiple platforms (Windows, Linux, macOS)
2. Use platform checks: `platform.system()`
3. Document platform limitations
4. Add tests with platform skipping if needed:

```python
@pytest.mark.skipif(platform.system() == "Linux", reason="Not supported on Linux")
def test_active_window_capture(self):
    # Test code
    pass
```

## Questions?

If you have questions:

- Check existing [Issues](https://github.com/codeforgood-org/desktop-screenshot-capturer/issues)
- Start a [Discussion](https://github.com/codeforgood-org/desktop-screenshot-capturer/discussions)
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to Desktop Screenshot Capturer!
