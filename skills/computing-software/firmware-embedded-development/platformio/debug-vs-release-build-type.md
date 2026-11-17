---
id: computing-software.firmware-embedded-development.platformio.debug-vs-release-build-type
name: debug-vs-release-build-type
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [build-type, debug-build-flags, release-build, build-unflags, debug-build, optimization-level, platformio-ini, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Control PlatformIO debug vs release builds: build_type values, debug_build_flags, build_unflags, separate debug env, and why pio debug may rebuild the project."
sources:
  - https://docs.platformio.org/en/latest/projectconf/build_configurations.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/debug/debug_build_flags.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_unflags.html
  - https://github.com/platformio/platformio-core/blob/develop/platformio/builder/tools/piomisc.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug vs release build_type

## Values
- `build_type = release` (default): no symbolic debug information, optimised for size or speed
  depending on the platform.
- `build_type = debug`: full symbolic debug information and no optimisation by the documented
  definition; the debug flags come from `debug_build_flags` (default `-Og -g2 -ggdb2`). The build
  also defines `__PLATFORMIO_BUILD_DEBUG__`, and PlatformIO first strips the platform's `-Os`,
  `-g` and `-O0..3`, `-g0..3`, `-ggdb0..3` flags.
- `build_type = test`: extends the environment with the `PIO_UNIT_TESTING` macro and the test
  framework's flags.

## Typical config
```ini
[env]
platform = ststm32
board = nucleo_g474re
framework = stm32cube

[env:release]
build_type = release
build_flags = -DNDEBUG

[env:debug]
build_type = debug
debug_build_flags = -O0 -ggdb3 -g3          ; replaces the default debug flags
build_flags = -DLOG_LEVEL=4
```
`debug_build_flags` is useful to adjust the optimisation level, for example when a firmware with
debug information is too big to upload. Other flags are listed in the GCC debugging options.

## Removing default flags
```ini
build_unflags = -Os -std=gnu++11
build_flags = -O2
```
`build_unflags` selectively removes base flags that were set by the development platform.

## Why `pio debug` rebuilds
`pio debug` (and the IDE debugger) automatically switches the project to the `debug`
configuration. To avoid a rebuild, define a separate environment with `build_type = debug` (like
`mydebug` above); it is then used automatically by PlatformIO debugging. Set a default
environment with `default_envs` in the `[platformio]` section.

## Code that depends on build type
```c
#ifdef __PLATFORMIO_BUILD_DEBUG__
  enable_debug_uart();
#endif
```
Prefer your own `-DDEBUG_BUILD` in `build_flags` of the debug env so non-PlatformIO builds behave
the same.

## Gotchas
- `-O0` code may not fit or may miss timing; `-Og` (the default debug level) is the usual
  compromise.
- Test release builds on hardware, not only debug builds.
- Check effective flags: `pio run -e debug -v` prints the compiler command lines.

## Verify
- [ ] Release artefact built from the release env with intended optimisation (check `-v` output).
- [ ] Debugger steps cleanly in the debug env.

## Checked
2026-10-26 against platformio-docs (develop, last commit 2026-09-19): build configurations,
`build_type`, `debug_build_flags` and `build_unflags` pages, and platformio-core `piomisc.py`
(develop). Confirmed: the three build types and default, default debug flags, the debug macro
and flag cleanup, `PIO_UNIT_TESTING`, the separate-env advice and `default_envs`. Removed as
unconfirmed: `-flto` and its inlining remark, "`build_unflags` removes from all flag lists",
the claim that debug and release share a build folder, and the VS Code env-switcher remark.
Method: documentation only; no commands were run.
