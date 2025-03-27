# Contributing Guide

## Development Environment

This project uses Visual Studio Code's devcontainer feature for consistent development environments.

Docker and VS Code with the "Dev Containers" extension are required.

### Setup

1. Install prerequisites:

   - Docker
   - Visual Studio Code
   - VS Code "Dev Containers" extension

2. Clone and open the repository:

```bash
git clone https://github.com/Geson-anko/numpy_ndarray_msgs.git
cd numpy_ndarray_msgs
code .
```

3. When prompted by VS Code, click "Reopen in Container" or press `F1` and select "Dev Containers: Reopen in Container"

## Development Workflow

### Building

The ROS2 message interface can be built using:

```bash
./build.sh
```

### Testing

Run tests with:

```bash
make test
```

### Code Style

We use pre-commit hooks for code formatting and linting:

```bash
make format  # Run pre-commit hooks
```

Code style is enforced by:

- Ruff for Python linting and formatting
- Type hints are required for public interfaces
- Google style docstrings required for public classes and methods
- Simple, readable code structure

### Making Changes

1. Create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes, ensuring:

   - All tests pass
   - Code is formatted
   - Type hints are added
   - Docstrings are added for public interfaces
   - Tests are added for new features

3. Commit your changes:

```bash
git add .
git commit -m "feat: your descriptive commit message"
```

### Pull Request Guidelines

- One feature/fix per PR
- Update documentation if needed
- Add tests for new features
- Follow the existing code style
- Keep commits clean and descriptive

## Project Structure

```
.
├── msg/              # ROS2 message definitions
├── src/              # Source code
│   └── ndarray_msg_utils/
├── tests/            # Test files
└── .devcontainer/    # Development container configuration
```

## Documentation

- Add docstrings following Google style
- Type hints are required
- Keep documentation updated with changes
- English only

## Need Help?

Feel free to open an issue for questions or problems.
