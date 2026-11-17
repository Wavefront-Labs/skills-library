---
id: computing-software.firmware-embedded-development.zephyr.west-config-settings
name: west-config-settings
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [west-config, build-board, build-pristine, build-dir-fmt, west-configuration-files, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use west config to set defaults per system, user or workspace: build.board, build.dir-fmt, build.pristine, zephyr.base, update options, and config file precedence."
sources:
  - https://docs.zephyrproject.org/latest/develop/west/config.html
  - https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html#configuration-options
  - https://github.com/zephyrproject-rtos/west/blob/main/src/west/configuration.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# west config

## Files and precedence (later wins)
| Level | Flag | Location |
|---|---|---|
| system | `--system` | `/etc/westconfig` (Linux), `%PROGRAMDATA%\west\config` (Windows) |
| global (user) | `--global` | `~/.westconfig` |
| local (workspace) | `--local` (default for writes) | `<workspace>/.west/config` |

macOS system file: `/usr/local/etc/westconfig`. On Linux the global file is
`$XDG_CONFIG_HOME/west/config` when `XDG_CONFIG_HOME` is set.

`WEST_CONFIG_SYSTEM`, `WEST_CONFIG_GLOBAL`, `WEST_CONFIG_LOCAL` env vars override the paths
(useful in CI; the west source documents them in `west/configuration.py`).
Without `--system`/`--global`/`--local`, reads show the final value after overrides.

```bash
west config -l                       # list all options and their values
west config build.board              # read
west config build.board nrf52840dk/nrf52840
west config --global build.pristine auto
west config -d build.board           # delete from local
```

## Useful keys
| Key | Example | Effect |
|---|---|---|
| `build.board` | `nucleo_h743zi` | default `-b` |
| `build.board_warn` | `false` | disable warnings when west build cannot work out the target board (default `true`) |
| `build.dir-fmt` | `build/{board}/{app}` | per-board build directories, no `-d` needed |
| `build.pristine` | `auto` | make the build dir pristine when the build would otherwise fail, e.g. different board or app (`never` is the default; `always` cleans every time) |
| `build.generator` | `Ninja` | CMake generator (default `Ninja`) |
| `build.cmake-args` | `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` | extra CMake args, applied when a new build system is generated; set with `west config build.cmake-args -- "<args>"` |
| `build.sysbuild` | `true` | build with sysbuild by default (default `false`) |
| `zephyr.base` | `zephyr` | which zephyr tree this workspace uses |
| `zephyr.base-prefer` | `configfile` | prefer config over `ZEPHYR_BASE` env var |
| `update.narrow` | `true` | fetch only the needed revision on `west update` |
| `update.fetch` | `smart` | skip fetches when the SHA is already local |
| `manifest.path` / `manifest.file` | `app` / `west.yml` | manifest location (set by `west init`) |
| `manifest.group-filter` | `+optional,-bar` | comma-separated groups to enable (`+`) or disable (`-`) |
| `manifest.project-filter` | `-hal_.*,+hal_foo` | regexes on project names, last match wins |

## Patterns
- Multi-board developer setup: `build.dir-fmt build/{board}` plus `build.pristine auto`;
  switching `-b` no longer clobbers another board's build.
- CI: point `WEST_CONFIG_GLOBAL` at a file you control so runner user settings do not leak in,
  then set explicit local config.
- `ZEPHYR_BASE` set in a shell from another workspace silently builds against the wrong tree;
  `west config zephyr.base-prefer configfile` prevents that.

## Verify
- [ ] `west config -l` in CI logs shows only intended values.
- [ ] `west build` without `-b` picks the team's default board.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2) and west 1.5.0 source (commit 2026-10-20). Confirmed config file locations and precedence, WEST_CONFIG_SYSTEM/GLOBAL/LOCAL (west/configuration.py), west config -l/-d, and the build.*, manifest.*, update.* and zephyr.* option table including defaults (west config and build-flash-debug pages). Removed the unconfirmed drop-in .d directory claim and the /dev/null CI trick; corrected build.pristine auto semantics.
Method: documentation only; no commands were run.
