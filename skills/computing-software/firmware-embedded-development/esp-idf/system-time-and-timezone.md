---
id: computing-software.firmware-embedded-development.esp-idf.system-time-and-timezone
name: system-time-and-timezone
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, esp-system-time, timezone-tz, settimeofday, rtc-time-keeping, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Keep wall-clock time on ESP32: settimeofday/gettimeofday, POSIX TZ strings and DST, time across deep sleep, RTC clock source accuracy and external RTC sync."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/system_time.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_libc/Kconfig
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_hw_support/port/esp32/Kconfig.rtc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System time and timezone

## Read and set
```c
#include <time.h>
#include <sys/time.h>
struct timeval tv = { .tv_sec = 1760000000 };
settimeofday(&tv, NULL);               /* from SNTP, GPS, BLE phone, external RTC */

time_t now; time(&now);
struct tm t; localtime_r(&now, &t);
char buf[32]; strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S %Z", &t);
```
Before time is set, `time()` returns a time near the 1970 epoch. Check
`now > 1700000000` (or a build-date floor) before trusting it.

## Timezone
```c
setenv("TZ", "CST-8", 1);               /* China Standard Time, the example in the ESP-IDF docs */
tzset();
```
The TZ string format is the one described in the GNU libc manual's TZ variable page (the ESP-IDF docs note the
implementation differs); that page also covers DST rules. The ESP-IDF docs only describe this POSIX-style format, so
store the POSIX string (for example in NVS) and map from region names on the phone or cloud side. East of UTC is
written with a negative offset (`CST-8` is UTC+8).

## Clock sources
By default system time is kept by the RTC timer plus the high-resolution timer (choice `CONFIG_LIBC_TIME_SYSCALL`,
default "RTC and high-resolution timer"). The RTC timer keeps time in sleep modes and across resets except power-on
reset; the high-resolution timer (APB clock, under +-10 ppm deviation) is not available in sleep and does not persist
over reset. The RTC timer's accuracy depends on its clock source (`CONFIG_RTC_CLK_SRC`):
- Internal RC oscillator (default, 90-150 kHz depending on chip): lowest deep-sleep current, but affected by temperature,
  so time can drift in deep and light sleep; the docs consider drift of several seconds per day acceptable for designs
  that do not need accurate time in sleep.
- External 32 kHz crystal (`CONFIG_RTC_CLK_SRC_EXT_CRYS`, not on ESP32-C2) or external 32 kHz oscillator: better stability,
  about 1 uA more deep-sleep current for the crystal.
- Some chips offer an internal 8 MHz-class oscillator divided by 256 as a middle option.
Long deep-sleep products that need accurate time should use an external 32 kHz source or resync periodically.

## External RTC (DS3231, PCF8563)
Read the external RTC at boot and call `settimeofday`; write back after each SNTP sync, and store UTC in it rather than local time (a design recommendation, not an ESP-IDF requirement).

## Verify
- [ ] Local time correct across a DST transition (set clock just before, observe change).
- [ ] Drift measured over a 24 h deep-sleep cycle and resync interval chosen accordingly.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/system/system_time.rst, esp_hw_support Kconfig.rtc, esp_libc Kconfig).
Confirmed: `settimeofday`/`gettimeofday`, `setenv("TZ", ...)` plus `tzset()` and `localtime_r`, the "CST-8" example and the reference to the GNU libc TZ format, RTC timer persistence across resets, high-resolution timer under +-10 ppm, clock source choices and `CONFIG_RTC_CLK_SRC_EXT_CRYS`, default internal RC with several-seconds-per-day drift guidance, `CONFIG_LIBC_TIME_SYSCALL` (the older `NEWLIB_TIME_SYSCALL_USE_RTC_HRT` name no longer exists), 64-bit time_t from v5.0. Removed unconfirmed claims: IANA names not being understood by newlib, the CET, Sydney and New York TZ strings (the GNU libc page could not be fetched), the percent and minutes-per-day drift figures and the 20 to 50 ppm crystal figure. The `now > 1700000000` threshold in the first example is an arbitrary build-date floor, not an ESP-IDF value.

Method: documentation only; no commands were run.
