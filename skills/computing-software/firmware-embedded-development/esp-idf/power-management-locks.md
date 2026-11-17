---
id: computing-software.firmware-embedded-development.esp-idf.power-management-locks
name: power-management-locks
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-pm-lock, esp-pm-configure, dynamic-frequency-scaling, auto-light-sleep, esp-pm-dump-locks, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use ESP-IDF power management (DFS and automatic light sleep) with PM locks: configuring esp_pm, holding CPU/APB/no-sleep locks around timing-critical work, and auditing them."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/power_management.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_pm/include/esp_pm.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_pm/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_uart/include/driver/uart.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Power management locks

With power management on, ESP-IDF lowers the CPU/APB clock and enters light sleep whenever no
**PM lock** forbids it. Drivers take locks automatically while busy; your code takes them for
anything the framework can't see.

## Enable
```
CONFIG_PM_ENABLE=y
CONFIG_FREERTOS_USE_TICKLESS_IDLE=y     # automatic light sleep is based on tickless idle
CONFIG_PM_PROFILING=y                    # dev only: lock statistics
```
```c
#include "esp_pm.h"
esp_pm_config_t pm = {
    .max_freq_mhz = 160,
    .min_freq_mhz = 40,              /* CPU frequency when no locks are held */
    .light_sleep_enable = true,
};
ESP_ERROR_CHECK(esp_pm_configure(&pm));
```
(Older IDF versions used chip-specific `esp_pm_config_esp32_t`; the generic type is current.)

## Lock types
| Type | Effect while held |
|---|---|
| `ESP_PM_CPU_FREQ_MAX` | CPU at `max_freq_mhz` |
| `ESP_PM_APB_FREQ_MAX` | APB at the maximum frequency the chip supports |
| `ESP_PM_NO_LIGHT_SLEEP` | no automatic light sleep |

```c
static esp_pm_lock_handle_t sample_lock;
esp_pm_lock_create(ESP_PM_NO_LIGHT_SLEEP, 0, "adc_burst", &sample_lock);

esp_pm_lock_acquire(sample_lock);     /* recursive: release as many times as acquired */
run_adc_burst();
esp_pm_lock_release(sample_lock);
```
Create locks once at init and match each acquire with a release.

## What drivers already do
- Wi-Fi/BLE hold locks as needed and wake for beacons/connection events.
- SPI master, I2C and I2S (depending on clock source) are DFS-aware and hold `ESP_PM_APB_FREQ_MAX`
  during transfers (see the power management page for the current list per chip).
- Light sleep clock-gates peripherals and GPIO/peripheral interrupts are not generated; wake from
  light sleep needs a configured wakeup source. For UART use `uart_wakeup_setup()`
  (`uart_set_wakeup_threshold()` is deprecated), or hold NO_LIGHT_SLEEP during expected traffic.
- Peripherals you drive directly through registers or the LL layer get no locks. Add your own.

## Auditing
```c
esp_pm_dump_locks(stdout);   /* per-lock count, time held; per-mode time (with PROFILING) */
```
If light sleep never happens, a lock is leaked or held by a driver (often a UART console or
an always-busy peripheral). Measure current with a power analyser to confirm sleep entry.

## Gotchas
- Light sleep pauses execution. Automatic light sleep wakes the chip for pending `esp_timer`
  callbacks; do not configure the timer wakeup source manually. GPIO-driven protocols with tight
  timing break unless you hold a lock.
- `CONFIG_FREERTOS_IDLE_TIME_BEFORE_SLEEP` sets the minimum idle time before the chip sleeps.
- Long-held CPU_FREQ_MAX locks reduce the energy savings.

## Verify
- [ ] `esp_pm_dump_locks` shows every custom lock with released state at idle.
- [ ] Idle current drops to the light-sleep level for your chip (measure it).
- [ ] Timing-critical operations tested with PM on (they fail in subtle ways otherwise).

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: esp_pm_config_t fields (max_freq_mhz, min_freq_mhz, light_sleep_enable), esp_pm_lock_create / acquire (recursive) / release, lock types, esp_pm_dump_locks, CONFIG_PM_ENABLE, CONFIG_PM_PROFILING, CONFIG_FREERTOS_USE_TICKLESS_IDLE (esp_pm_configure fails if light sleep is requested without it), SPI master/I2C/I2S use APB_FREQ_MAX, timer wakeup used by automatic light sleep. Wrong: APB lock does not mean 80 MHz on every chip; uart_set_wakeup_threshold is deprecated in favour of uart_wakeup_setup. Removed unconfirmed ISR-safety, RMT, USB Serial/JTAG and current-range claims.
Method: documentation only; no commands were run.
