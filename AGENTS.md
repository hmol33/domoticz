# AGENTS.md — Domoticz

This file provides guidance for AI agents (and human contributors) working in the Domoticz codebase.

## Project Overview

Domoticz is a free, open-source home automation system for Linux, Windows, macOS, Raspberry Pi, and embedded devices. It supports 150+ hardware types (Z-Wave, Zigbee, MQTT, RFXCOM, Philips Hue, etc.) with an HTML5 web frontend.

- **Language**: C++ (core), Python (plugins + some tools), Lua (dzVents event scripting)
- **Build system**: CMake (Linux/macOS), MSBuild/Visual Studio (Windows)
- **License**: GPL v3
- **Default branch**: `development` (master = release)

## Build

### Linux / macOS
```bash
# Install dependencies (Ubuntu/Debian)
sudo apt-get install cmake make gcc g++ libssl-dev git libcurl4-gnutls-dev \
  libusb-dev libmosquitto-dev python3-dev zlib1g-dev liblua5.3-dev \
  uthash-dev libsqlite3-dev libboost-system-dev

# Build
mkdir build && cd build
cmake ..
make -j$(nproc)
```

### Windows
Open `msbuild/domoticz.sln` in Visual Studio 2022. Windows libraries are bundled via NuGet (see `windows-development-build.yml`).

## Test Suite

Tests live under `test/`:

| Directory | Type | Requires running server? |
|-----------|------|--------------------------|
| `test/python/` | pytest (standalone scripts) | Some tests need server |
| `test/gherkin/` | pytest-bdd (BDD features) | Some tests need server |
| `test/www-test/` | Node.js (frontend) | Yes |

### Running tests
```bash
# Install test deps
pip install pytest pytest-bdd

# Syntax-check all test files (no server needed)
python3 -m py_compile test/python/test_*.py

# Verify pytest collection
cd test/python && python3 -m pytest --collect-only -q

# Run static-only tests (no server required)
cd test/python && python3 -m pytest test_command_rights.py -v

# Run full suite (requires running Domoticz at 127.0.0.1:8080)
cd test/python && python3 -m pytest -v
```

Set `DOMOTICZ_HOST` and `DOMOTICZ_PORT` environment variables to point to a non-default instance.

### Test file purposes

- `test_command_rights.py` — verifies minimum user rights of JSON commands against `command_rights.json`
- `test_oauth2_response_splitting.py` — regression test for CWE-113 (HTTP response splitting)
- `test_api_sweep.py` — walks the entire JSON API surface against a running server
- `test_calibration.py` — verifies device calibration on every ingest path
- `test_plugin_websocket.py` — end-to-end test for Plugin WebSocket Channel feature

## CI Workflows

| Workflow | File | Trigger |
|----------|------|---------|
| Linux build (beta) | `.github/workflows/development.yml` | push to development/master |
| Linux PR check | `.github/workflows/pull_request_check.yml` | PRs to development/master |
| Windows build | `.github/workflows/windows-development-build.yml` | push to development |
| Windows PR check | `.github/workflows/windows-pr-check.yml` | PRs to development/master |
| Native (ARM/x64) builds | `.github/workflows/beta-native-build.yml` | gated on Linux CI success |
| Arch packages | `.github/workflows/build_arch.yml` | release / manual |
| Source tarball | `.github/workflows/source-release.yml` | release published |
| Stale issues | `.github/workflows/stale.yml` | daily cron |
| **Lint and Test** | `.github/workflows/lint-and-test.yml` | push/PR to development/master |
| **Gource visualization** | `.github/workflows/gource.yml` | weekly cron + push |

## Code Conventions

### C++
- **Formatting**: `clang-format` with config in `clang-format.txt` (root). Run `clang-format -i <file>` before committing.
- **Style**: K&R braces, 4-space indent, `m_` prefix for member variables, `C` prefix for classes.
- **Headers**: Include guards via `#pragma once`.

### Python (tests)
- PEP 8, 4-space indent
- Self-contained scripts (no shared framework beyond stdlib + pytest)
- Each test file has a module docstring explaining its purpose

### Shell scripts
- POSIX-compatible (`#!/bin/sh`)
- Lint with `shellcheck`

## Architecture

```
domoticz/
├── main/           # Core application (mainworker, webserver, JSON API)
├── hardware/       # Hardware drivers (Z-Wave, Zigbee, MQTT, etc.)
├── httpclient/     # HTTP client library
├── tcpserver/      # TCP server framework
├── dzVents/        # Lua event scripting engine
├── plugins/        # Python plugin system + examples
├── www/            # HTML5 web frontend (JavaScript/CSS)
├── extern/         # Bundled third-party libraries (submodules)
├── msbuild/        # Visual Studio solution + build scripts
├── test/           # Python/BDD/JS test suites
└── tools/          # Utility scripts (backup, update, etc.)
```

### Key components

- **MainWorker** (`main/mainworker.cpp`): Central scheduler and device manager
- **WebServer** (`main/WebServer.cpp`): HTTP server, JSON API endpoint routing
- **SQLHelper** (`main/SQLHelper.cpp`): SQLite database access layer
- **dzVents** (`dzVents/`): Lua-based event scripting engine
- **PythonPlugins** (`main/` + `plugins/`): Python plugin runtime

### JSON API

Commands are registered in `main/WebServer.cpp` via `RegisterCommandCode(name, fn, minRights, bypassAuthentication)`. The minimum-rights list is maintained in `test/python/command_rights.json` — changes require updating that file.

## Submodules

Domoticz bundles third-party libraries as git submodules under `extern/`:

```bash
git submodule update --init --recursive
```

The CI workflows automatically update submodules to the latest upstream commit.

## Gource Visualization

A weekly CI workflow (`.github/workflows/gource.yml`) generates a development timeline video. See the README "Development visualization" section for details.

## Common Tasks

### Adding a new JSON API command
1. Register in `main/WebServer.cpp` with `RegisterCommandCode`
2. Update `test/python/command_rights.json` with the command name and minimum rights level
3. Run `test_command_rights.py` to verify

### Adding a Python test
1. Create `test/python/test_<name>.py`
2. Add a module docstring explaining purpose
3. Ensure it passes `python3 -m py_compile test/python/test_<name>.py`
4. Run `python3 -m pytest test/python/test_<name>.py -v` to verify

### Updating documentation
- `README.md` — project overview, build instructions
- `SECURITY.md` — security policy
- `SECURITY_SETUP.md` — security configuration guide
- `INSTALL.md` — installation instructions
- `History.txt` — changelog
