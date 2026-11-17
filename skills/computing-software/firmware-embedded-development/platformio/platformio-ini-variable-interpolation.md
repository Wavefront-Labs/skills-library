---
id: computing-software.firmware-embedded-development.platformio.platformio-ini-variable-interpolation
name: platformio-ini-variable-interpolation
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-interpolation, platformio-ini-variables, sysenv, this-variable, extends, common-section, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Reuse values in platformio.ini with ${section.option}, ${this.*}, ${sysenv.VAR}, ${platformio.*} and built-in variables like ${PROJECT_DIR}; extends vs interpolation."
sources:
  - https://docs.platformio.org/en/latest/projectconf/interpolation.html
  - https://docs.platformio.org/en/latest/projectconf/sections/env/options/advanced/extends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable interpolation in platformio.ini

## Syntax
```ini
[extra]
lib_deps_external =
  bblanchon/ArduinoJson@>5.6.0

[env:esp32dev]
platform = platformio/espressif32
board = esp32dev
build_flags = ${env.build_flags} -Wall
lib_deps =
  ${extra.lib_deps_external}
test_testing_command =
  ${platformio.build_dir}/${this.__env__}/firmware.elf
```
| Form | Meaning |
|---|---|
| `${<section>.<option>}` | value from another section, e.g. `${extra.lib_deps_external}` |
| `${this.<option>}` | option of the current section, e.g. `${this.board}` |
| `${this.__env__}` | env name of the current `[env:foo]` section (`foo`) |
| `${sysenv.<name>}` | operating-system environment variable, e.g. `${sysenv.HOME}` |
| `${platformio.<option>}` | option from the `[platformio]` section, e.g. `${platformio.packages_dir}` |
| `${env.<option>}` | option from the global `[env]` section |
| `${PROJECT_DIR}`, `${PROJECT_HASH}`, `${UNIX_TIME}` | built-in variables (project directory, hash of the project path, 10-digit Unix time) |

Rules from the docs: interpolation applies only to an option's value, can span multiple
levels, and several interpolations are allowed in one value. `[platformio]` and `[env]` are
reserved section names, so name custom shared sections something like `extra` or `custom`.

## extends vs interpolation
- `extends` inherits configuration from other sections or environments; several items are
  separated by `,` or a new line (`extends = base, strict_ldf`). It does NOT merge values
  across multiple parents: when several items are listed, only the values from the latter one
  are used for an option both define.
- For only a few options, use interpolation instead. A value set in an env replaces an
  inherited one unless you interpolate it, e.g. `build_flags = ${env.build_flags} -Wall`.

## Gotchas
- Keep sensitive data in environment variables and read them with `${sysenv.NAME}`. On Unix,
  characters such as `$`, `&` and `~` in those variables must be escaped when they are used
  as values for preprocessor directives.
- Values passed with `-D` are compiled into the firmware, so a secret read this way ends up
  in the binary: use per-device provisioning for real secrets.

## Verify
- [ ] Every `${sysenv.*}` used is set on each machine and in CI.
- [ ] Each env builds with the flags you expect (check with a verbose build).

## Checked
2026-10-31. Confirmed on the PlatformIO "Interpolation of Values" and "extends" pages: the
interpolation forms and built-in variables in the table, the multi-level and reserved-section
rules, `extends` semantics and the no-merge warning, Unix escaping warning. Removed: the
claim that `${PROJECT_DIR}` is not valid interpolation (the page lists it as a built-in
variable), the SCons `$VAR` section, `pio project config` and circular-reference claims, and
the empty-when-unset claim, none of which the pages state.
Method: documentation only; no commands were run.
