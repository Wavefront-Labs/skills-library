---
id: computing-software.firmware-embedded-development.zephyr.logging-backends-and-levels
name: logging-backends-and-levels
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-logging, log-backend, log-module-register, log-level, runtime-filtering, rtt-backend, uart-backend, log-dictionary, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Set up Zephyr logging: per-module registration and compile-time levels, choosing backends (UART, RTT, file, network), runtime filtering, and dictionary logging to save flash."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/services/logging/index.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/logging/Kconfig.template.log_config
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/logging/log_cmds.c
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/logging/Kconfig.filtering
  - https://docs.zephyrproject.org/latest/services/logging/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr logging: backends and levels

**Goal:** useful, cheap logs: right verbosity per module, sent where you can read them, and
removable from production builds without code changes.

## Per-module registration
```c
#include <zephyr/logging/log.h>
LOG_MODULE_REGISTER(sensor, CONFIG_SENSOR_LOG_LEVEL);    /* one per module (.c file group) */
/* other files of the same module: LOG_MODULE_DECLARE(sensor, CONFIG_SENSOR_LOG_LEVEL); */

LOG_INF("odr set to %u Hz", odr);
LOG_WRN("retry %d", n);
LOG_ERR("i2c read failed: %d", ret);
LOG_DBG("raw=0x%04x", raw);
LOG_HEXDUMP_DBG(buf, len, "rx frame");
```
Define the level symbol in the module's Kconfig with the template:
```
module = SENSOR
module-str = sensor
source "subsys/logging/Kconfig.template.log_config"
```
Then `CONFIG_SENSOR_LOG_LEVEL_DBG=y` in prj.conf. Messages above the compile-time level are
compiled out entirely.

## Backends
| Kconfig | Use |
|---|---|
| `CONFIG_LOG_BACKEND_UART=y` | default console UART |
| `CONFIG_LOG_BACKEND_RTT=y` (+ `CONFIG_USE_SEGGER_RTT=y`) | J-Link RTT: fast, no UART pins needed |
| `CONFIG_LOG_BACKEND_FS=y` | log files on a file system |
| `CONFIG_LOG_BACKEND_NET=y` | syslog to a network server (RFC 5424; UDP or TCP; needs networking and sockets, not immediate mode) |
| `CONFIG_LOG_BACKEND_SWO=y` | Serial Wire Output (needs `HAS_SWO`) |
Several can be active; each has its own runtime filter.

## Runtime control
With `CONFIG_LOG_RUNTIME_FILTERING=y` (not available in minimal mode) and the shell: `log status`,
`log enable <level> <module...>` (for example `log enable dbg sensor`), `log disable <module...>`, `log go`/`log halt`,
and, with several backends, `log list_backends` and `log backend <backend_name> <command>`. Lets you raise verbosity in
the field for one module. Runtime verbosity cannot exceed the compile-time level.

## Saving flash
- `CONFIG_LOG_DEFAULT_LEVEL=2` (warnings; 0 off, 1 error, 2 warning, 3 info, 4 debug; the default is 3) and
  per-module overrides for production.
- **Dictionary logging** (`CONFIG_LOG_BACKEND_UART_OUTPUT_DICTIONARY=y`, which selects
  `CONFIG_LOG_DICTIONARY_SUPPORT`): binary output decoded offline with `log_dictionary.json` and
  `scripts/logging/dictionary/log_parser.py`; see the `dictionary-based-logging` skill.
- `CONFIG_LOG_MODE_MINIMAL` for tiny targets (printk-like, no buffering).

## Gotchas
- String arguments are handled by cbprintf packaging. The guide recommends casting to `const char *` when
  a `%s` pointer is a constant string and to `char *` when it is a transient string (for example a
  stack buffer), and requires a cast to a non-character pointer such as `(void *)` for `%p`.
- String width specifiers (`%8s`, `%.*s`) are not supported.
- The logging API can be called from interrupts; keep ISR logging light.

## Verify
- [ ] Production build has no DBG strings in the binary (`strings zephyr.elf | grep "raw="`).
- [ ] Runtime filter changes take effect via shell.

## Checked

Checked 2026-10-26 against the Zephyr logging guide and Kconfig files on main: `LOG_MODULE_REGISTER`/`LOG_MODULE_DECLARE`,
the `Kconfig.template.log_config` template and `<MODULE>_LOG_LEVEL_*` options, `CONFIG_LOG_DEFAULT_LEVEL` (default 3, range 0-4),
`CONFIG_LOG_RUNTIME_FILTERING` (not in minimal mode), the `log` shell subcommands in `subsys/logging/log_cmds.c`, backend
Kconfig dependencies (UART, RTT with `USE_SEGGER_RTT`, FS, NET, SWO), string-argument recommendations and width limitation.
Removed the claim that `log_strdup()` was removed and a specific backend name in `log backend`; neither is stated in the
current docs. The `LOG_HEXDUMP_X` macro family is documented in the same guide.

Method: documentation only; no commands were run.
