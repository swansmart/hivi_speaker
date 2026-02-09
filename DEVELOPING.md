# Development Guide

This guide explains how to run and develop the HiVi Speaker integration with the local `hivico` library.

## Project Structure

The integration depends on the `hivico` Python library. For development, keep both projects as siblings:

```
projects/
├── hivi_speaker_github/    # This repo (Home Assistant integration)
└── hivico/                 # HiVi API client library (separate project)
```

## Development Setup

### 1. Install hivico from Local Path

The integration declares `hivico>=0.1.0` in `manifest.json`. For local development, install hivico in editable mode so changes are reflected immediately:

**Option A: Using requirements-dev.txt (recommended)**

```bash
cd hivi_speaker_github
pip install -r requirements-dev.txt
```

**Option B: Manual install**

```bash
pip install -e ../hivico
# or with absolute path:
pip install -e d:\projects\hivico
```

### 2. Install the Integration in Home Assistant

Copy the custom component to your Home Assistant config directory:

```bash
# Create custom_components if it doesn't exist
mkdir -p config/custom_components

# Copy or symlink the integration
cp -r custom_components/hivi_speaker config/custom_components/
# On Windows with symlink (run as Admin): mklink /D config\custom_components\hivi_speaker custom_components\hivi_speaker
```

### 3. Run Home Assistant

**Using Python venv (typical dev setup):**

```bash
# Create venv if needed
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install hivico (editable) + dependencies
pip install -e ../hivico
pip install homeassistant

# Run Home Assistant
hass -c config
```

**Using existing Home Assistant installation:**

Install hivico into the same Python environment Home Assistant uses:

```bash
# Find HA's Python and install hivico there
# For Docker/HA OS: use "ha core ssh" or install via pip in the container
pip install -e /path/to/hivico
```

Then ensure the integration is in `config/custom_components/hivi_speaker` and restart Home Assistant.

## Verifying hivico is Installed

```bash
python -c "from hivico import HivicoClient; print('hivico OK')"
```

## Quick Run (Minimal Test)

For a quick syntax/import check without full HA:

```bash
cd hivi_speaker_github
pip install -e ../hivico
python -c "
from hivico import HivicoClient
from custom_components.hivi_speaker.device_manager import DeviceManager
print('All imports OK')
"
```

## Troubleshooting

- **ModuleNotFoundError: No module named 'hivico'**: Install hivico with `pip install -e ../hivico`
- **Integration fails to load in HA**: Ensure hivico is installed in the same Python environment as Home Assistant
- **Changes to hivico not reflected**: Use `pip install -e ../hivico` (editable mode) so no reinstall is needed
