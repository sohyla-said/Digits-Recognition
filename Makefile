# Makefile for digits_recognition project

# Variables
PYTHON = python
RUFF = ruff
TEST = pytest
TESTS_DIR = tests
SRC_DIR = src
PROJECT_DIRS = $(SRC_DIR) $(TESTS_DIR)

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  check-tests     - Run ruff check on tests folder"
	@echo "  check-src       - Run ruff check on src folder"
	@echo "  check-all       - Run ruff check on all project directories"
	@echo "  format-tests    - Run ruff format on tests folder"
	@echo "  format-src      - Run ruff format on src folder"
	@echo "  format-all      - Run ruff format on all project directories"
	@echo "  fix-tests       - Run ruff check --fix on tests folder"
	@echo "  fix-src         - Run ruff check --fix on src folder"
	@echo "  fix-all         - Run ruff check --fix on all project directories"
	@echo "  lint            - Run all linting checks (check-all)"
	@echo "  clean           - Remove Python cache files"

# Ruff check targets
.PHONY: check-tests
check-tests:
	@echo "Running ruff check on tests folder..."
	$(RUFF) check $(TESTS_DIR)

.PHONY: check-src
check-src:
	@echo "Running ruff check on src folder..."
	$(RUFF) check $(SRC_DIR)

.PHONY: check-all
check-all:
	@echo "Running ruff check on all project directories..."
	$(RUFF) check $(PROJECT_DIRS)

# Ruff format targets
.PHONY: format-tests
format-tests:
	@echo "Running ruff format on tests folder..."
	$(RUFF) format $(TESTS_DIR)

.PHONY: format-src
format-src:
	@echo "Running ruff format on src folder..."
	$(RUFF) format $(SRC_DIR)

.PHONY: format-all
format-all:
	@echo "Running ruff format on all project directories..."
	$(RUFF) format $(PROJECT_DIRS)

# Ruff fix targets
.PHONY: fix-tests
fix-tests:
	@echo "Running ruff check --fix on tests folder..."
	$(RUFF) check --fix $(TESTS_DIR)

.PHONY: fix-src
fix-src:
	@echo "Running ruff check --fix on src folder..."
	$(RUFF) check --fix $(SRC_DIR)

.PHONY: fix-all
fix-all:
	@echo "Running ruff check --fix on all project directories..."
	$(RUFF) check --fix $(PROJECT_DIRS)

# Combined targets
.PHONY: lint
lint: check-all

.PHONY: format
format: format-all

.PHONY: fix
fix: fix-all

# Testing target
.PHONY: test
unit_tests:
	@echo "Running unit tests..."
	$(TEST) $(TESTS_DIR)/unit_tests.py

# Utility targets
.PHONY: clean
clean:
	@echo "Cleaning Python cache files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Development workflow targets
.PHONY: dev-check
dev-check: check-all
	@echo "Development check completed."

.PHONY: pre-commit
pre-commit: fix-all format-all
	@echo "Pre-commit checks and fixes completed."