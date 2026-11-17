---
id: computing-software.firmware-embedded-development.bare-metal-programming.log-levels-and-compile-time-stripping
name: log-levels-and-compile-time-stripping
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [log-level-filtering, semihosting, logging-macros, per-module-log-level, flash-savings, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build a firmware logging macro set with per-module compile-time levels that remove strings and calls entirely, plus a runtime level for what remains."
sources:
  - https://docs.zephyrproject.org/latest/services/logging/index.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/log.html
  - https://gcc.gnu.org/onlinedocs/cpp/Variadic-Macros.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log levels and compile-time stripping

Log strings are often the largest single consumer of flash in a mature firmware. Debug-level
messages should cost **zero bytes** in release builds, while warnings and errors stay available.

## Macro design
```c
/* log.h */
#define LOG_LVL_NONE 0
#define LOG_LVL_ERR  1
#define LOG_LVL_WRN  2
#define LOG_LVL_INF  3
#define LOG_LVL_DBG  4

#ifndef LOG_LEVEL_GLOBAL_MAX
#define LOG_LEVEL_GLOBAL_MAX LOG_LVL_INF          /* set per build type from CMake */
#endif

extern uint8_t g_log_runtime_level;
void log_write(uint8_t lvl, const char *mod, const char *fmt, ...) __attribute__((format(printf, 3, 4)));

#define LOG_AT(lvl, fmt, ...) do { \
    if ((lvl) <= LOG_MODULE_LEVEL && (lvl) <= LOG_LEVEL_GLOBAL_MAX && (lvl) <= g_log_runtime_level) \
        log_write((lvl), LOG_MODULE_NAME, fmt, ##__VA_ARGS__); \
} while (0)
#define LOG_ERR(...) LOG_AT(LOG_LVL_ERR, __VA_ARGS__)
#define LOG_DBG(...) LOG_AT(LOG_LVL_DBG, __VA_ARGS__)
```
In each source file:
```c
#define LOG_MODULE_NAME  "imu"
#define LOG_MODULE_LEVEL LOG_LVL_WRN
#include "log.h"
```
The first two comparisons are constants: when false, the compiler can drop the call and, usually,
the format string (confirm with the size check below). The third is a runtime check for levels
that survived compilation. `##__VA_ARGS__` is a GNU extension that drops the preceding comma when
there are no variable arguments (documented in the GCC preprocessor manual).

## Why `do { if (...) } while (0)` rather than `#if`
The disabled call is still parsed and type-checked, so debug logs don't rot.

## Avoid side effects in arguments
`LOG_DBG("val=%d", read_sensor());` skips `read_sensor()` in release builds. Lint rule: no
function calls with side effects inside log arguments.

## Size check
Compare `size` output and the strings present in the image between a DBG build and a release build.

## Beyond levels
- Deferred/binary/tokenised logging removes format strings from flash entirely (see deferred logging).
- Rate limiting for repeated errors protects slow UARTs (Zephyr has `LOG_ERR_RATELIMIT`, with
  `CONFIG_LOG_RATELIMIT_INTERVAL_MS` as the default interval).
- Ready-made: Zephyr `LOG_MODULE_REGISTER(name, CONFIG_..._LOG_LEVEL)` (optional second
  parameter is the compile-time level of the module), ESP-IDF `CONFIG_LOG_MAXIMUM_LEVEL` plus
  `esp_log_level_set()` for the runtime level.

## Verify
- [ ] A release image contains no DBG-level message strings.
- [ ] Raising the runtime level via your CLI enables only levels compiled in.

## Checked
2026-10-31. Confirmed in the Zephyr logging page: `LOG_MODULE_REGISTER` with an optional compile-time level, `LOG_ERR_RATELIMIT`, `CONFIG_LOG_RATELIMIT_INTERVAL_MS`. Confirmed in the ESP-IDF log page: `esp_log_level_set()` and the compile-time maximum level versus runtime level split. Confirmed in the GCC preprocessor manual: `##__VA_ARGS__`.
Removed: the `-O1` and `--gc-sections` claim, the `format` attribute warning claim, the `strings` command, the `log level 4` example.
Method: documentation only; no commands were run.
