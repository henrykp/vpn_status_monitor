# VPN Monitor

A Windows background application that monitors specific "Windows App" processes (e.g., `msrdc.exe`, `Windows365.exe`) and enforces VPN usage by checking the current region.

## Features

- **Process Monitoring**: Detects if `msrdc.exe` or `Windows365.exe` has a visible window.
- **Region Check**: Verifies if the current public IP is in the allowed country (default: HU).
- **Allowed IPs**: Supports an optional list of allowed external IPs that bypass the country check.
- **Warning System**: Displays a custom, topmost warning window if the region is incorrect while the target app is running.
- **System Tray**:
  - Snooze functionality (5m, 15m, 1h, 8h).
  - Set Allowed Country.
  - Exit.
- **Startup Integration**: Can register itself to run at Windows startup.

## Installation

1.  **Prerequisites**: Python 3.8+
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    (Or `pip install psutil requests pystray Pillow`)

## Usage

### Running from Source

```bash
python run.py
```

### Command Line Arguments

- `--install-startup`: Registers the app to run on Windows startup.
- `--remove-startup`: Removes the app from Windows startup.

### Configuration

#### Allowed Country

The default allowed country is **HU** (Hungary). You can change this via the System Tray menu ("Set Country...") or by setting the `ALLOWED_COUNTRY` environment variable.

#### Allowed IPs (Bypass)

You can create a file named `allowed_ips.txt` in the same directory as the executable (or `run.py`).
Add one IP address per line. If your current external IP matches any IP in this list, the warning will be suppressed regardless of your country.

**Example `allowed_ips.txt`:**

```
203.0.113.1
198.51.100.2
```

## Building Executable

To build a standalone `.exe`:

```bash
pyinstaller --noconsole --onefile --name vpn-monitor run.py
```

The output will be in the `dist` folder.

## Development

### Releasing a New Version

This project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) for version management. To release a new version:

```bash
# Bump version (choose one)
cz bump --increment PATCH  # 0.2.0 → 0.2.1
cz bump --increment MINOR  # 0.2.0 → 0.3.0
cz bump --increment MAJOR  # 0.2.0 → 1.0.0

# Or let commitizen determine the bump from commit messages
cz bump

# Push changes and tag
git push && git push --tags
```

This will:

1. Update the version in `pyproject.toml`
2. Create a git commit with the version bump
3. Create a git tag (e.g., `v0.3.0`)

Pushing the tag triggers the release workflow, which builds the executable and creates a GitHub release.
