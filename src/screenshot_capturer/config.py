"""
Configuration management for screenshot capturer.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """
    Configuration manager for screenshot capturer.

    Handles loading, saving, and accessing configuration options.
    Configuration is stored in a JSON file in the user's home directory.
    """

    DEFAULT_CONFIG = {
        "default_format": "PNG",
        "default_quality": 95,
        "default_output_dir": ".",
    }

    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        if config_file is None:
            config_dir = Path.home() / ".config" / "screenshot-capturer"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.json"

        self.config_file = config_file
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from file or create default if it doesn't exist."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
                # Ensure all default keys exist
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in self._config:
                        self._config[key] = value
            except (json.JSONDecodeError, IOError):
                # If config is corrupted, use defaults
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            # Create default config
            self._config = self.DEFAULT_CONFIG.copy()
            self.save()

    def save(self):
        """Save current configuration to file."""
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """
        Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value

    @property
    def default_format(self) -> str:
        """Get default image format."""
        return self._config["default_format"]

    @default_format.setter
    def default_format(self, value: str):
        """Set default image format."""
        self._config["default_format"] = value.upper()

    @property
    def default_quality(self) -> int:
        """Get default JPEG quality."""
        return self._config["default_quality"]

    @default_quality.setter
    def default_quality(self, value: int):
        """Set default JPEG quality."""
        if not 1 <= value <= 100:
            raise ValueError("Quality must be between 1 and 100")
        self._config["default_quality"] = value

    @property
    def default_output_dir(self) -> Path:
        """Get default output directory."""
        return Path(self._config["default_output_dir"]).expanduser()

    @default_output_dir.setter
    def default_output_dir(self, value: Path):
        """Set default output directory."""
        self._config["default_output_dir"] = str(value)

    def reset(self):
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save()

    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"Config({self._config})"
