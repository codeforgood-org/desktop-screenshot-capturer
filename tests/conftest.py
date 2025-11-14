"""
Pytest configuration and shared fixtures.
"""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_config_file(temp_dir):
    """Create a temporary config file path."""
    return temp_dir / "test_config.json"


@pytest.fixture
def sample_image_path(temp_dir):
    """Return path for a sample image file."""
    return temp_dir / "test_screenshot.png"
