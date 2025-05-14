# Contributing to ioctx-py

Thank you for your interest in contributing to the ioctx-py project! This document provides guidelines and instructions to help you get started.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct. Please be respectful, inclusive, and considerate in all interactions.

## Setting Up Your Development Environment

1. Fork the repository on GitHub.

2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/ioctx-py.git
   cd ioctx-py
   ```

3. Set up a virtual environment and install dependencies:
   ```bash
   # Using poetry (recommended)
   poetry install

   # Alternatively, using pip
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes.

3. Run the tests to ensure your changes don't break existing functionality:
   ```bash
   pytest
   ```

4. Format your code:
   ```bash
   black .
   isort .
   ```

5. Run type checking:
   ```bash
   mypy ioctx
   ```

6. Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add feature X" -m "This implements feature X which helps with Y"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Open a pull request from your fork to the main repository.

## Testing

Testing is at the heart of ioctx-py, as the library itself is designed to make testing easier. We follow a "dogfooding" approach, using the library to test itself wherever possible.

- All code should be accompanied by tests.
- Aim for high test coverage, particularly for core functionality.
- Tests should be clear and demonstrate how features are intended to be used.

## Code Style

We follow these coding standards:

- Use [Black](https://black.readthedocs.io/) for code formatting.
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
- Use type hints for all function signatures.
- Document all public APIs with docstrings (following the Google style).
- Keep functions focused on a single responsibility.

## Pull Request Process

1. Update the README.md or documentation with details of any changes to the interface.
2. Update the tests to cover your changes.
3. Make sure your code passes all checks (tests, type checking, linting).
4. Your PR should be reviewed by at least one maintainer.
5. When your PR is approved, it will be merged into the main branch.

## Reporting Issues

When reporting issues, please include:

- A clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version
- ioctx-py version
- Any relevant code samples or error messages

## Feature Requests

We welcome feature requests! Please provide:

- A clear description of the feature
- The rationale for the feature
- Examples of how the feature would be used
- Any relevant references or prior art

## Areas for Contribution

We're particularly interested in contributions in these areas:

1. Additional IO backend implementations
2. Integration with popular Python frameworks
3. Performance optimizations
4. Documentation improvements
5. Examples demonstrating real-world usage
6. IO category extensions (database access, message queues, etc.)

## Releasing

For maintainers, the release process is:

1. Update the version in pyproject.toml
2. Update the CHANGELOG.md
3. Create a new GitHub release with release notes
4. GitHub Actions will automatically publish to PyPI

## Questions?

If you have any questions about contributing, please open an issue or reach out to the maintainers directly.

Thank you for contributing to ioctx-py! Your efforts help make Python testing better for everyone.
