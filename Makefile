.PHONY: help install install-dev test coverage lint format check clean docs build

help:
	@echo "Desktop Screenshot Capturer - Development Commands"
	@echo ""
	@echo "  make install          Install the package"
	@echo "  make install-dev      Install development dependencies"
	@echo "  make test             Run tests"
	@echo "  make coverage         Run tests with coverage report"
	@echo "  make lint             Run linters (flake8, pylint, mypy)"
	@echo "  make format           Format code (black, isort)"
	@echo "  make check            Run all quality checks"
	@echo "  make clean            Clean build artifacts"
	@echo "  make docs             Build documentation"
	@echo "  make build            Build distribution packages"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:
	pytest

coverage:
	pytest --cov=screenshot_capturer --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	@echo "Running flake8..."
	flake8 src/ tests/
	@echo "Running pylint..."
	pylint src/screenshot_capturer/
	@echo "Running mypy..."
	mypy src/

format:
	@echo "Running black..."
	black src/ tests/
	@echo "Running isort..."
	isort src/ tests/

check: lint test
	@echo "All checks passed!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

docs:
	@echo "Documentation build not yet configured"
	@echo "TODO: Add Sphinx documentation"

build: clean
	python -m build
	@echo "Distribution packages created in dist/"
