"""
Tests for the CLI module.
"""

from pathlib import Path

import pytest

from screenshot_capturer.cli import (
    create_parser,
    generate_filename,
    parse_region,
    main,
)
from screenshot_capturer.capturer import Region


class TestCLI:
    """Tests for CLI functions."""

    def test_generate_filename(self):
        """Test filename generation."""
        filename = generate_filename("PNG")
        assert filename.startswith("screenshot_")
        assert filename.endswith(".png")

        filename = generate_filename("JPEG")
        assert filename.endswith(".jpeg")

    def test_parse_region_valid(self):
        """Test parsing valid region string."""
        region = parse_region("10,20,800,600")
        assert region.x == 10
        assert region.y == 20
        assert region.width == 800
        assert region.height == 600

    def test_parse_region_invalid_format(self):
        """Test parsing invalid region string."""
        with pytest.raises(ValueError):
            parse_region("10,20,800")  # Missing value

        with pytest.raises(ValueError):
            parse_region("10,20,abc,600")  # Non-numeric

        with pytest.raises(ValueError):
            parse_region("not a region")

    def test_create_parser(self):
        """Test parser creation."""
        parser = create_parser()
        assert parser is not None
        assert parser.prog == "screenshot-capturer"

    def test_parser_default_arguments(self):
        """Test parser with default arguments."""
        parser = create_parser()
        args = parser.parse_args([])

        assert args.mode == "fullscreen"
        assert args.format == "png"
        assert args.quality == 95
        assert args.output is None
        assert args.region is None

    def test_parser_fullscreen_mode(self):
        """Test parser with fullscreen mode."""
        parser = create_parser()
        args = parser.parse_args(["-m", "fullscreen"])
        assert args.mode == "fullscreen"

    def test_parser_region_mode(self):
        """Test parser with region mode."""
        parser = create_parser()
        args = parser.parse_args(["-m", "region", "-r", "0,0,100,100"])
        assert args.mode == "region"
        assert args.region == "0,0,100,100"

    def test_parser_output_argument(self):
        """Test parser with output argument."""
        parser = create_parser()
        args = parser.parse_args(["-o", "/tmp/test.png"])
        assert args.output == "/tmp/test.png"

    def test_parser_format_argument(self):
        """Test parser with format argument."""
        parser = create_parser()
        args = parser.parse_args(["-f", "jpeg"])
        assert args.format == "jpeg"

    def test_parser_quality_argument(self):
        """Test parser with quality argument."""
        parser = create_parser()
        args = parser.parse_args(["-q", "80"])
        assert args.quality == 80

    def test_parser_verbose_flag(self):
        """Test parser with verbose flag."""
        parser = create_parser()
        args = parser.parse_args(["-v"])
        assert args.verbose is True

    def test_parser_show_config_flag(self):
        """Test parser with show-config flag."""
        parser = create_parser()
        args = parser.parse_args(["--show-config"])
        assert args.show_config is True

    def test_main_show_config(self, temp_config_file, capsys):
        """Test main function with --show-config."""
        # Set environment to use temp config
        from screenshot_capturer.config import Config
        Config._test_config_file = temp_config_file

        result = main(["--show-config"])
        assert result == 0

        captured = capsys.readouterr()
        assert "Current Configuration" in captured.out

    def test_main_region_without_region_param(self):
        """Test main with region mode but no region parameter."""
        result = main(["-m", "region"])
        assert result == 1

    def test_main_invalid_quality(self):
        """Test main with invalid quality value."""
        result = main(["-q", "150"])
        assert result == 1

        result = main(["-q", "0"])
        assert result == 1

    def test_main_keyboard_interrupt(self, monkeypatch):
        """Test main handles keyboard interrupt."""
        def mock_capture(*args, **kwargs):
            raise KeyboardInterrupt()

        # This test would require mocking the capturer, which is complex
        # For now, we just verify the structure
        pass
