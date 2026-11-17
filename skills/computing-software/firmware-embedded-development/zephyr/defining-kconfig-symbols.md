---
id: computing-software.firmware-embedded-development.zephyr.defining-kconfig-symbols
name: defining-kconfig-symbols
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [kconfig, kconfig-symbols, depends-on, select-vs-imply, kconfig-choice, is-enabled, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Define your own Kconfig symbols in a Zephyr app or module: types, prompts, defaults, depends on vs select vs imply, choices, and consuming them in CMake and C."
sources:
  - https://docs.zephyrproject.org/latest/build/kconfig/setting.html
  - https://docs.zephyrproject.org/latest/build/kconfig/tips.html
  - https://docs.zephyrproject.org/latest/build/dts/dt-vs-kconfig.html
  - https://docs.zephyrproject.org/latest/develop/modules.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/scripts/kconfig/kconfig.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining Kconfig symbols

## Where the file goes
- **Application:** `Kconfig` next to the app's `CMakeLists.txt`. It must source Zephyr's tree:
  ```kconfig
  menu "ACME app"
  config ACME_TELEMETRY
      bool "Telemetry uploads"
      default y
      depends on NETWORKING
      select JSON_LIBRARY
      help
        Periodically uploads device health to the backend.

  config ACME_TELEMETRY_PERIOD_S
      int "Upload period (seconds)"
      range 10 86400
      default 300
      depends on ACME_TELEMETRY
  endmenu

  source "Kconfig.zephyr"
  ```
- **Module:** `build: kconfig: <directory>/Kconfig` in `zephyr/module.yml` (the default is
  `zephyr/Kconfig`; no `source "Kconfig.zephyr"` there).
- Driver symbols conventionally: `default y` + `depends on DT_HAS_ACME_TMP42_ENABLED`, so the
  driver turns on when the devicetree node is enabled.

## depends on vs select vs imply
| Keyword | Meaning | Use for |
|---|---|---|
| `depends on X` | symbol invisible/forced n unless X | real requirements |
| `select X` | forces X=y, **ignoring X's own dependencies** | simple helper symbols with no dependencies |
| `imply X` | like `select` but respects dependencies and doesn't force a value; a suggestion | nice-to-have features |

The Zephyr guide's example: if `CONSOLE` later gains `depends on STRING_ROUTINES`, a symbol that
`select CONSOLE` still forces it on even when `STRING_ROUTINES` is `n`. Prefer `depends on`
(optionally with `default y` on the dependency) for anything non-trivial.

## Prompts matter
Only symbols **with a prompt** (`bool "text"`) can be set from `prj.conf`. Assigning a
promptless (invisible) symbol in a configuration file is an error ("is assigned in a
configuration file, but is not directly user-configurable"); invisible symbols take their value
from defaults or other symbols. Assignments that don't take effect, for example because the
dependencies aren't met, print warnings; `KCONFIG_WARNING_AS_ERROR=y` turns every Kconfig warning
into an error.

## Choices
```kconfig
choice ACME_LOG_BACKEND
    prompt "Log transport"
    default ACME_LOG_UART
config ACME_LOG_UART
    bool "UART"
config ACME_LOG_RTT
    bool "Segger RTT"
endchoice
```

## Consuming
```cmake
zephyr_library_sources_ifdef(CONFIG_ACME_TELEMETRY telemetry.c)
```
```c
#include <zephyr/kernel.h>
if (IS_ENABLED(CONFIG_ACME_TELEMETRY)) { start_telemetry(CONFIG_ACME_TELEMETRY_PERIOD_S); }
```
`IS_ENABLED()` expands to 1 if the macro is defined to 1 and 0 otherwise, so the code stays
visible to the compiler (it can report errors in it even when the symbol is off). Prefer it over
`#ifdef`; in a preprocessor `#if` it gives no benefit over `#if defined()`.

## Tools
`west build -t menuconfig` (or `guiconfig`): `/` jumps to a symbol. `build/zephyr/.config` is the
final resolved configuration; `prj.conf` is only input.

## Verify
- [ ] Setting each new symbol in `prj.conf` produces no Kconfig warnings.
- [ ] menuconfig help text explains every user-visible symbol.
- [ ] Builds with the feature on and off both pass in CI.

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/build/kconfig/setting.rst and tips.rst, doc/develop/modules.rst, scripts/kconfig/kconfig.py and include/zephyr/sys/util_macro.h.
Confirmed: application `Kconfig` auto-detection and `source "Kconfig.zephyr"`; `build: kconfig:` in module.yml with its default; `select` forcing a symbol on despite its dependencies; `imply` semantics; the build-time error for assigning promptless symbols; `KCONFIG_WARNING_AS_ERROR`; `IS_ENABLED()` semantics; `zephyr_library_sources_ifdef` exists; `DT_HAS_<COMPAT>_ENABLED` convention in the devicetree-vs-Kconfig guide.

Method: documentation only; no commands were run.
