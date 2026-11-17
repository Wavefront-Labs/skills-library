---
id: computing-software.firmware-embedded-development.esp-idf.esp-log-logging
name: esp-log-logging
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, esp-log, esp-log-level-set, log-maximum-level, esp-log-set-vprintf, early-and-dram-log, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use ESP-IDF logging well: per-tag runtime levels, compile-time maximum level, logging from ISRs and early boot, redirecting output to files or the network, and cost control."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/log.rst
  - https://github.com/espressif/esp-idf/blob/master/components/log/Kconfig.level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esp_log logging

## Basics
```c
#include "esp_log.h"
static const char *TAG = "sensor";         /* one tag per module */

ESP_LOGE(TAG, "read failed: %s", esp_err_to_name(err));
ESP_LOGW(TAG, "retry %d", n);
ESP_LOGI(TAG, "temp=%.2f", t);
ESP_LOGD(TAG, "raw=0x%04x", raw);
ESP_LOGV(TAG, "reg dump follows");
ESP_LOG_BUFFER_HEX_LEVEL(TAG, buf, len, ESP_LOG_DEBUG);
```

## Two levels: compile-time and run-time
```
CONFIG_LOG_DEFAULT_LEVEL_INFO=y       # runtime default for all tags
CONFIG_LOG_MAXIMUM_LEVEL_DEBUG=y      # highest level compiled in at all
```
- Messages above `CONFIG_LOG_MAXIMUM_LEVEL` are removed at compile time: zero cost, and can't
  be enabled later.
- At run time:
  ```c
  esp_log_level_set("*", ESP_LOG_WARN);       /* everything quiet */
  esp_log_level_set("sensor", ESP_LOG_DEBUG); /* except this module */
  esp_log_level_set("wifi", ESP_LOG_ERROR);   /* tame chatty IDF components */
  ```
  Expose this through a console command so field units can raise verbosity without a reflash.
- Per-file override of the maximum level: `#define LOG_LOCAL_LEVEL ESP_LOG_VERBOSE` **before** `#include "esp_log.h"` (not in headers); for a whole component use `target_compile_definitions(${COMPONENT_LIB} PUBLIC "-DLOG_LOCAL_LEVEL=ESP_LOG_VERBOSE")`.

## Where you can't use ESP_LOGx
Use `ESP_LOGx` in normal application code; avoid it in ISRs, early startup, or while the flash cache is
disabled.
- ISR / cache-disabled code: `ESP_DRAM_LOGx(DRAM_STR("TAG"), "...")`; the tag and format string must be in DRAM, and use these macros sparingly.
- Early startup, before the heap allocator or syscalls are initialised: `ESP_EARLY_LOGx`.
- High-rate paths: even a debug log that is filtered out at runtime still costs a level check; in hot
  loops gate on a counter or remove it.

## Redirecting output
```c
static int log_to_ring(const char *fmt, va_list ap)
{
    char line[160];
    va_list ap2;
    va_copy(ap2, ap);                      /* the list is consumed twice */
    int n = vsnprintf(line, sizeof line, fmt, ap2);
    va_end(ap2);
    ring_push(line, n);                    /* e.g. for upload or a crash report */
    return vprintf(fmt, ap);               /* still print to console */
}
esp_log_set_vprintf(log_to_ring);          /* returns the previous function */
```
Redirect targets: a file on a mounted filesystem, UDP syslog,
apptrace over JTAG (`esp_apptrace_vprintf`). The vprintf hook must not log itself (recursion)
and must be fast; queue to a task for network output.

## Output details
- Timestamps: `CONFIG_LOG_TIMESTAMP_SOURCE` choices include milliseconds since boot (default, `_RTOS`), system time (`_SYSTEM`, `_SYSTEM_FULL`), Unix time (`_UNIX`) and, with Log V2 only, none.
- Colours: `CONFIG_LOG_COLORS` is off by default because IDF Monitor adds colours itself; leave it off when logs go to files or CI parsers.
- A serial console is slow (115200 baud is about 11.5 KB/s at 8N1). Heavy logging delays the calling task
  and distorts timing; raise the console baud rate (`CONFIG_ESP_CONSOLE_UART_BAUDRATE`) or reduce volume.
- Log V2 (`CONFIG_LOG_VERSION`, V1 or V2) reduces flash usage and centralises formatting but needs a bit more stack; it is backward compatible with V1 code, but code using V2-only features cannot go back to V1.

## Verify
- [ ] Release config: maximum level INFO or WARN, so debug messages are compiled out.
- [ ] Runtime level change reachable in the field (console or remote command).
- [ ] No `ESP_LOGx` inside IRAM ISRs (grep for IRAM_ATTR functions).

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the log guide, esp_log headers and log Kconfig: CONFIG_LOG_DEFAULT_LEVEL and CONFIG_LOG_MAXIMUM_LEVEL choices, compile-time removal above the maximum, LOG_LOCAL_LEVEL per file and per component, esp_log_level_set, ESP_EARLY_LOGx and ESP_DRAM_LOGx with DRAM_STR, ESP_LOG_BUFFER_HEX_LEVEL, esp_log_set_vprintf returning the previous function, timestamp source choices, CONFIG_LOG_COLORS default off, Log V1/V2 trade-offs. Wrong or stale: the lock-based explanation for ISR restrictions and the Log V2 'formats more at run time' description were replaced by the documented behaviour; a malformed code fence was repaired. Removed the unconfirmed strings-based check.
Method: documentation only; no commands were run.
