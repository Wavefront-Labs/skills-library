---
id: computing-software.firmware-embedded-development.arduino.arduino-cli-configuration
name: arduino-cli-configuration
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-cli-config, arduino-cli-yaml, additional-urls, directories-data, env-vars, config-set, arduino-cli, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Configure arduino-cli: config init/set/dump, arduino-cli.yaml keys (board manager URLs, data/user dirs, unsafe installs), ARDUINO_ env overrides, and per-project config files."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/configuration.md
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/config/set.go
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/config/init.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# arduino-cli configuration

## Create and inspect
```sh
arduino-cli config init                 # writes the default arduino-cli.yaml
arduino-cli config dump                 # effective config (file + env + flags)
arduino-cli config get directories.data
arduino-cli config set board_manager.additional_urls \
  https://espressif.github.io/arduino-esp32/package_esp32_index.json \
  https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
arduino-cli config add board_manager.additional_urls <url>   # append instead of replace
arduino-cli core update-index           # needed after changing URLs
```
`config init` creates or updates `arduino-cli.yaml` in the data directory (or `--dest-dir` / `--dest-file`; `--overwrite` replaces an existing file). `arduino-cli config dump --verbose` shows which file is active.
Default data directory: Linux `{HOME}/.arduino15`, macOS `{HOME}/Library/Arduino15`, Windows `{HOME}/AppData/Local/Arduino15`.

## Key settings
```yaml
board_manager:
  additional_urls: [ ... ]
  enable_unsafe_install: false     # true allows packages that fail the checksum test
directories:
  data: ...                        # index files and platform installations
  downloads: ...                   # default: {directories.data}/staging
  user: ...                        # sketchbook; libraries/ lives here
library:
  enable_unsafe_install: false     # true allows lib install --git-url / --zip-path
build_cache:
  path: ...                        # build cache folder
logging:
  level: info                      # trace, debug, info, warn, error, fatal, panic
network:
  proxy: http://proxy:3128
updater:
  enable_notification: false
```

## Precedence
Command-line flag > environment variable > config file > default. Every key maps to an env var:
`ARDUINO_` followed by the key path with `_` between components:
```sh
ARDUINO_DIRECTORIES_DATA=$PWD/.arduino ARDUINO_DIRECTORIES_USER=$PWD/sketchbook \
ARDUINO_BOARD_MANAGER_ADDITIONAL_URLS="url1 url2" arduino-cli compile ...
```
(List values in env vars are space-separated.)

## Project-local, reproducible setups
- `arduino-cli --config-file ./arduino-cli.yaml ...` uses a repo-committed config so CI and developers
  share the same settings (the file is used on its own, not merged with others).
- Or set `ARDUINO_DIRECTORIES_*` in the CI job (`ARDUINO_DIRECTORIES_DATA` also selects where the config file is looked for). Combine with `sketch.yaml` profiles for pinned
  platform/library versions.

## Gotchas
- `config set` on a list key replaces the whole list; use `config add`/`config remove`.
- Old docs mention `--additional-urls` per command; still valid but easy to forget in CI.

## Verify
- [ ] `arduino-cli config dump` in CI shows the intended directories and URLs.
- [ ] Fresh container build installs cores into the project-local data dir.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs and source on master (commit 2026-10-22).

Confirmed: keys and defaults in the configuration page (`library.enable_unsafe_install`, `build_cache.path`, `network.proxy`, `updater.enable_notification`, `directories.*`, `ARDUINO_` environment variables, space-separated URL list); precedence flag, environment variable, file; config file search order (`--config-file`, `ARDUINO_CONFIG_FILE`, `ARDUINO_DIRECTORIES_DATA`, files not merged); default data directory per OS; `config set` with several values replaces the list. Fixed: `enable_unsafe_install` also exists under `board_manager` (the configuration page names the zip flag `--zip-file` but the `lib install` source defines `--zip-path`, which the skill keeps); default data and cache locations corrected. Removed unconfirmed claims: IDE 2.x config location, default file path per OS, `<home>` placeholders.

Method: documentation only; no commands were run.
