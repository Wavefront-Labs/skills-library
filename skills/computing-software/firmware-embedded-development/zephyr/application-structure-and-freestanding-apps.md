---
id: computing-software.firmware-embedded-development.zephyr.application-structure-and-freestanding-apps
name: application-structure-and-freestanding-apps
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-build-system, zephyr-application-structure, workspace-application, freestanding-application, find-package-zephyr, zephyr-base, cmakelists, board-root, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Lay out a Zephyr application (repository, workspace or freestanding), write its CMakeLists.txt, and add app-local boards, DTS roots and Kconfig."
sources:
  - https://docs.zephyrproject.org/latest/develop/application/index.html
  - https://docs.zephyrproject.org/latest/develop/modules.html
  - https://github.com/zephyrproject-rtos/example-application
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr application structure

**Goal:** an application that builds reproducibly outside the Zephyr tree, with its own
boards, bindings and Kconfig, and pins the Zephyr version it needs.

## Three application types
| Type | Where | When |
|---|---|---|
| Repository app | inside the Zephyr repository (for example `samples/hello_world`) | upstream samples |
| **Workspace app** | inside a west workspace where Zephyr is installed, outside the zephyr repository | products that track Zephyr with west |
| Freestanding app | anywhere outside a Zephyr workspace; set the `ZEPHYR_BASE` environment variable | quick experiments |
The `zephyrproject-rtos/example-application` repository is the reference workspace application:
it demonstrates custom board ports, devicetree bindings, device drivers, CI with twister and a
custom west extension command.

## Minimal files
```
app/
  CMakeLists.txt
  prj.conf
  Kconfig            (optional: app symbols, must source "Kconfig.zephyr")
  boards/<board>.overlay, boards/<board>.conf   (optional per-board)
  src/main.c
```
```cmake
cmake_minimum_required(VERSION 3.28.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(my_app)
target_sources(app PRIVATE src/main.c)
```
`find_package(Zephyr)` must come before `project()` and `target_sources()`. The build system
creates a CMake target named `app`. `HINTS $ENV{ZEPHYR_BASE}` is only needed to force a specific
Zephyr installation; plain `find_package(Zephyr)` is the documented minimum.

## App-local hardware definitions
Point the build at extra roots (in `CMakeLists.txt` before `find_package`, using absolute
paths, or via `-DBOARD_ROOT=<path>`, or via the module `zephyr/module.yml` `build: settings:`
block):
```cmake
list(APPEND BOARD_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/..)     # contains a boards/ folder
list(APPEND DTS_ROOT   ${CMAKE_CURRENT_SOURCE_DIR}/..)     # contains a dts/ folder
```
In a workspace app, declare the repo as a Zephyr module with this in `zephyr/module.yml` so
every app in it sees the roots:
```yaml
build:
  settings:
    board_root: .
    dts_root: .
```

## Kconfig for the app
```
# app/Kconfig (detected automatically next to CMakeLists.txt)
config APP_SAMPLE_PERIOD_MS
	int "Sampling period"
	default 1000
source "Kconfig.zephyr"
```

## Gotchas
- Building from a different directory: always pass the app path (`west build -b x app/`), and
  use `-d build-x` for multiple boards side by side.
- A `ZEPHYR_BASE` environment variable forces CMake to use that Zephyr installation; make sure
  it is not left over from a different tree.
- Version pinning lives in the manifest (`west.yml` `revision:`), not in the app.

## Verify
- [ ] Fresh clone + `west init -l <manifest-repo> && west update && west build -b <board> app` works on CI.
- [ ] App-local board appears in `west boards` output.

## Checked

Checked 2026-10-25 against the Zephyr documentation source (main, latest release v4.4.2): doc/develop/application/index.rst, doc/develop/modules.rst, doc/develop/west/build-flash-debug.rst and samples/hello_world/CMakeLists.txt.
Confirmed: the three application types and their locations; `cmake_minimum_required(VERSION 3.28.0)` in current samples; `find_package(Zephyr)` before `project()`; the `app` target; `BOARD_ROOT`/`DTS_ROOT` rules (set before `find_package`, absolute paths in CMakeLists.txt); `board_root`/`dts_root` under `build: settings:` in module.yml; application `Kconfig` auto-detection and `source "Kconfig.zephyr"`; `west build -d`; `west boards`; example-application contents.

Method: documentation only; no commands were run.
