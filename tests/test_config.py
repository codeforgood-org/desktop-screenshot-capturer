"""
Tests for the configuration module.
"""

import json
from pathlib import Path

import pytest

from screenshot_capturer.config import Config


class TestConfig:
    """Tests for the Config class."""

    def test_config_initialization(self, temp_config_file):
        """Test config initialization creates file with defaults."""
        config = Config(temp_config_file)
        assert config.config_file == temp_config_file
        assert temp_config_file.exists()

    def test_default_values(self, temp_config_file):
        """Test default configuration values."""
        config = Config(temp_config_file)
        assert config.default_format == "PNG"
        assert config.default_quality == 95
        assert config.default_output_dir == Path(".")

    def test_load_existing_config(self, temp_config_file):
        """Test loading existing configuration file."""
        # Create config file manually
        test_config = {
            "default_format": "JPEG",
            "default_quality": 80,
            "default_output_dir": "/tmp",
        }
        with open(temp_config_file, "w") as f:
            json.dump(test_config, f)

        config = Config(temp_config_file)
        assert config.default_format == "JPEG"
        assert config.default_quality == 80
        assert config.default_output_dir == Path("/tmp")

    def test_save_config(self, temp_config_file):
        """Test saving configuration."""
        config = Config(temp_config_file)
        config.default_format = "BMP"
        config.default_quality = 90
        config.save()

        # Reload and verify
        with open(temp_config_file, "r") as f:
            data = json.load(f)

        assert data["default_format"] == "BMP"
        assert data["default_quality"] == 90

    def test_get_method(self, temp_config_file):
        """Test get method."""
        config = Config(temp_config_file)
        assert config.get("default_format") == "PNG"
        assert config.get("nonexistent", "default") == "default"

    def test_set_method(self, temp_config_file):
        """Test set method."""
        config = Config(temp_config_file)
        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"

    def test_default_format_property(self, temp_config_file):
        """Test default_format property."""
        config = Config(temp_config_file)
        config.default_format = "jpeg"
        assert config.default_format == "JPEG"  # Should be uppercase

    def test_default_quality_property(self, temp_config_file):
        """Test default_quality property."""
        config = Config(temp_config_file)
        config.default_quality = 75
        assert config.default_quality == 75

    def test_invalid_quality_value(self, temp_config_file):
        """Test setting invalid quality value."""
        config = Config(temp_config_file)

        with pytest.raises(ValueError):
            config.default_quality = 0

        with pytest.raises(ValueError):
            config.default_quality = 101

    def test_default_output_dir_property(self, temp_config_file, temp_dir):
        """Test default_output_dir property."""
        config = Config(temp_config_file)
        config.default_output_dir = temp_dir
        assert config.default_output_dir == temp_dir

    def test_reset_config(self, temp_config_file):
        """Test resetting configuration to defaults."""
        config = Config(temp_config_file)
        config.default_format = "JPEG"
        config.default_quality = 50
        config.reset()

        assert config.default_format == "PNG"
        assert config.default_quality == 95
        assert config.default_output_dir == Path(".")

    def test_corrupted_config_file(self, temp_config_file):
        """Test handling of corrupted config file."""
        # Write invalid JSON
        with open(temp_config_file, "w") as f:
            f.write("not valid json {{{")

        # Should load defaults without crashing
        config = Config(temp_config_file)
        assert config.default_format == "PNG"
        assert config.default_quality == 95

    def test_missing_keys_in_config(self, temp_config_file):
        """Test handling config file with missing keys."""
        # Create config with only some keys
        partial_config = {"default_format": "JPEG"}
        with open(temp_config_file, "w") as f:
            json.dump(partial_config, f)

        config = Config(temp_config_file)
        assert config.default_format == "JPEG"
        assert config.default_quality == 95  # Should use default
        assert config.default_output_dir == Path(".")  # Should use default

    def test_config_repr(self, temp_config_file):
        """Test config string representation."""
        config = Config(temp_config_file)
        repr_str = repr(config)
        assert "Config" in repr_str
