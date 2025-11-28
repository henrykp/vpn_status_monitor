# Contributing to VPN Monitor

Thank you for your interest in contributing to VPN Monitor! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Building](#building)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept responsibility for mistakes and learn from them

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/vpn_status_monitor.git
   cd vpn_status_monitor
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/vpn_status_monitor.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Windows OS (for full functionality testing)

### Setting Up Your Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt)
   .\venv\Scripts\activate.bat
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

5. **Verify setup**:
   ```bash
   python run.py --help
   ```

## Branching Strategy

We use a **trunk-based development** model with `main` as the release branch.

### Branch Types

| Branch Pattern | Purpose | Base Branch | Merges Into |
|----------------|---------|-------------|-------------|
| `main` | Production releases | - | - |
| `feature/<name>` | New features | `main` | `main` |
| `fix/<name>` | Bug fixes | `main` | `main` |
| `docs/<name>` | Documentation updates | `main` | `main` |
| `chore/<name>` | Maintenance tasks | `main` | `main` |

### Workflow

1. **Create a feature branch** from `main`:
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** with atomic commits

3. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Push and create a Pull Request**:
   ```bash
   git push origin feature/my-new-feature
   ```

## Commit Messages

We use **[Conventional Commits](https://www.conventionalcommits.org/)** specification for commit messages. This enables automatic changelog generation and semantic versioning.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Code style changes (formatting, whitespace) |
| `refactor` | Code changes that neither fix bugs nor add features |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `build` | Build system or dependency changes |
| `ci` | CI/CD configuration changes |
| `chore` | Other changes that don't modify src or test files |
| `revert` | Reverts a previous commit |

### Scopes (Optional)

- `monitor` - Core monitoring functionality
- `gui` - GUI/warning window
- `tray` - System tray functionality
- `deps` - Dependencies

### Examples

```bash
# Feature
git commit -m "feat(tray): add custom snooze duration option"

# Bug fix
git commit -m "fix(monitor): resolve memory leak in process detection"

# Breaking change (use ! or BREAKING CHANGE footer)
git commit -m "feat(api)!: change configuration file format"

# With body
git commit -m "fix(gui): prevent warning window from appearing behind other windows

The warning window now uses HWND_TOPMOST flag consistently
to ensure visibility across all Windows versions.

Fixes #123"
```

## Pull Request Process

1. **Ensure your code passes all checks**:
   ```bash
   # Run linting
   flake8 vpn_monitor tests
   
   # Run tests
   pytest
   ```

2. **Update documentation** if needed

3. **Fill out the PR template** completely

4. **Request review** from maintainers

5. **Address feedback** promptly

### PR Requirements

- [ ] All CI checks pass
- [ ] Code follows project style guidelines
- [ ] Commits follow conventional commit format
- [ ] Documentation updated (if applicable)
- [ ] Tests added/updated (if applicable)

### Merge Strategy

We use **squash merging** for PRs to keep the main branch history clean. Your PR title should follow conventional commit format as it becomes the squash commit message.

## Code Style

We follow **PEP 8** with some project-specific guidelines.

### Linting

We use `flake8` for linting:

```bash
flake8 vpn_monitor tests
```

### Guidelines

- **Line length**: 100 characters maximum
- **Imports**: Use absolute imports, group in order (stdlib, third-party, local)
- **Docstrings**: Use Google-style docstrings for public functions/classes
- **Type hints**: Encouraged but not required

### Pre-commit Hooks

Pre-commit hooks automatically check your code before each commit:

```bash
# Install hooks (one-time)
pre-commit install
pre-commit install --hook-type commit-msg

# Run manually on all files
pre-commit run --all-files
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vpn_monitor

# Run specific test file
pytest tests/test_monitor.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_<module>.py`
- Name test functions `test_<description>`
- Use pytest fixtures for common setup

## Building

### Building the Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --noconsole --onefile --name vpn-monitor run.py
```

The executable will be created in the `dist/` folder.

### Verifying the Build

```bash
# Run the built executable
.\dist\vpn-monitor.exe --help
```

## Questions?

If you have questions about contributing, feel free to:

1. Open a [Discussion](https://github.com/OWNER/vpn_status_monitor/discussions)
2. Create an [Issue](https://github.com/OWNER/vpn_status_monitor/issues)

Thank you for contributing! 🎉

