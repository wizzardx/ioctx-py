#!/bin/bash
set -e

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print a header with the step name
print_header() {
    echo -e "\n${YELLOW}=======================================${NC}"
    echo -e "${YELLOW}  $1${NC}"
    echo -e "${YELLOW}=======================================${NC}\n"
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
check_requirements() {
    print_header "Checking requirements"

    local missing_tools=()

    if ! command_exists repomix; then
        missing_tools+=("repomix")
    fi

    if ! command_exists poetry; then
        missing_tools+=("poetry")
    fi

    if ! command_exists pytest; then
        missing_tools+=("pytest")
    fi

    if ! command_exists flake8; then
        missing_tools+=("flake8")
    fi

    if ! command_exists black; then
        missing_tools+=("black")
    fi

    if ! command_exists isort; then
        missing_tools+=("isort")
    fi

    if ! command_exists mypy; then
        missing_tools+=("mypy")
    fi

    if [ ${#missing_tools[@]} -ne 0 ]; then
        echo -e "${RED}Missing required tools: ${missing_tools[*]}${NC}"
        echo -e "Please install them with:"
        if [[ " ${missing_tools[*]} " =~ " repomix " ]]; then
            echo -e "  pip install repomix"
            echo -e "And others with:"
        fi
        echo -e "  poetry add --dev ${missing_tools[*]}"
        exit 1
    fi

    echo -e "${GREEN}All required tools are installed!${NC}"
}

# Run repomix for repository standardization
run_repomix() {
    print_header "Running repomix"

    echo "Standardizing repository with repomix..."
    repomix

    echo -e "${GREEN}Repository has been standardized with repomix!${NC}"
}

# Run code formatting
format_code() {
    print_header "Formatting code"

    echo "Running black to reformat code..."
    poetry run black .

    echo "Running isort to reformat imports..."
    poetry run isort .

    echo -e "${GREEN}Code formatting complete!${NC}"
}

# Run code formatting checks
run_formatting_checks() {
    print_header "Verifying code formatting"

    echo "Checking if code follows Black standards..."
    poetry run black --check .

    echo -e "\nChecking if imports follow isort standards..."
    poetry run isort --check-only --profile black .

    echo -e "${GREEN}All formatting checks passed!${NC}"
}

# Run linting
run_linting() {
    print_header "Running linters"

    echo "Running flake8..."
    poetry run flake8 ioctx tests

    echo -e "${GREEN}All linting checks passed!${NC}"
}

# Run type checking
run_type_checking() {
    print_header "Running type checking"

    echo "Running mypy..."
    poetry run mypy ioctx

    echo -e "${GREEN}All type checks passed!${NC}"
}

# Run tests with coverage
run_tests() {
    print_header "Running tests"

    echo "Running pytest with coverage..."
    poetry run pytest

    echo -e "${GREEN}All tests passed!${NC}"
}

# Run all checks
run_all() {
    check_requirements
    run_repomix        # Run repomix first after requirements check
    format_code        # Format code before linting
    run_linting
    run_formatting_checks
    run_type_checking
    run_tests

    print_header "All checks completed successfully!"
}

# Main script execution
echo -e "${GREEN}Running ioctx-py test suite${NC}"
run_all
