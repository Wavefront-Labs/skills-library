---
id: computing-software.firmware-embedded-development.arduino.arduino-cli-and-multi-board-builds
name: arduino-cli-and-multi-board-builds
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino, arduino-cli, fqbn, boards-txt, platform-txt, core-install, library-manager, library-json, board-package-pinning, ci, github-actions, headless-build, compile-flags, build-property, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build and verify Arduino sketches headlessly with arduino-cli across multiple boards: FQBNs, pinned core/library versions, custom build properties, and CI without the IDE."
sources:
  - https://arduino.github.io/arduino-cli/latest/
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/sketch-project-file.md
  - https://github.com/arduino/compile-sketches
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/compile/compile.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# arduino-cli and multi-board builds

**Goal:** build the same sketch for several boards reproducibly, outside the IDE,
so CI catches a break before it ships and "works on my machine" core versions
stop causing it.

## Core concepts
- **FQBN** (Fully Qualified Board Name) identifies board + options, e.g.
  `arduino:avr:uno` or `attiny:avr:ATtinyX5:cpu=attiny85,clock=internal16`.
  Options after the third segment are board-menu choices (`name=value`, comma separated);
  list them with `arduino-cli board details -b <fqbn>` and find FQBNs with
  `arduino-cli board listall`.
- Install cores explicitly and pin versions, don't rely on "latest":
  ```
  arduino-cli core update-index
  arduino-cli core install <vendor>:<arch>@<version>
  ```
  Third-party cores also need their index URL in `board_manager.additional_urls`.
  An unpinned core update is one of the most common "it used to build" breakages —
  board package updates change HAL behavior (pin numbering, default flash mode)
  silently.
- Libraries: `arduino-cli lib install "<name>@<version>"` — same pinning rule.

## Compiling for several boards
```
arduino-cli compile --fqbn arduino:avr:uno sketch/
arduino-cli compile --fqbn <other-vendor>:<arch>:<board> sketch/
```
Wrap this in a matrix (shell loop or CI matrix) over a list of FQBNs so one
sketch is verified against every target board on every change. `--warnings` sets
the compiler warning level (`none`, `default`, `more` or `all`; default `none`),
so use `--warnings all` in CI to surface issues early.

## Custom build properties and conditional code
Pass compiler defines per build without editing the sketch:
```
arduino-cli compile --fqbn arduino:avr:uno --build-property "build.extra_flags=-DDEBUG_VERBOSE=1" sketch/
```
In code, gate board-specific sections with the core's own macros, not your own
board list:
```c
#if defined(ARDUINO_ARCH_ESP32)
  // ...
#elif defined(ARDUINO_ARCH_AVR)
  // ...
#endif
```
The platform's compile recipes pass `-DARDUINO_ARCH_{build.arch}` and `-DARDUINO_{build.board}`
(for example `ARDUINO_ARCH_AVR`), and `{build.extra_flags}` is where the `build.extra_flags`
property lands. Use `arduino-cli compile --show-properties` to see the properties for a given FQBN.

## CI (GitHub Actions)
The `arduino/compile-sketches` action installs the platforms and libraries you list,
compiles the sketches, and can write a size and warnings report (see the
`compile-sketches-ci` skill); use it before hand-rolling a matrix.

## Verify
- [ ] `arduino-cli compile --fqbn <exact FQBN> sketch/` succeeds locally for every target board, not just the one on the desk.
- [ ] Core and library versions are pinned in the CI config, not "latest".
- [ ] `--warnings all` produces no new warnings versus the last known-good build.
- [ ] A fresh clone + CI run reproduces the binary without needing the Arduino IDE installed.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs and source on the master branch (latest commit 2026-10-22); arduino/compile-sketches README (latest commit 2026-10-14).

Confirmed: the FQBN form `vendor:arch:board:option=value,...` (sketch project file docs); `board details` and `board listall` exist; `compile` flags `--warnings` (values none, default, more, all; default none), `--build-property`, `--show-properties`; the platform recipes pass `-DARDUINO_ARCH_{build.arch}` and `{build.extra_flags}`; compile-sketches installs platforms and libraries and writes size and warning reports. Removed claims no document covers: pinned example versions, a specific ESP32 board FQBN, the IDE status-bar tip, the `lib list` resolution claim and the AVR cast remark.

Method: documentation only; no commands were run.
