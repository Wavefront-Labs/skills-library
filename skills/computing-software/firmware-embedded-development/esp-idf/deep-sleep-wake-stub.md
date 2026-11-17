---
id: computing-software.firmware-embedded-development.esp-idf.deep-sleep-wake-stub
name: deep-sleep-wake-stub
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-sleep, deep-sleep-stub, rtc-iram-attr, wake-stub, fast-wake, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run code immediately on deep-sleep wake before the bootloader with an ESP-IDF wake stub in RTC fast memory, and decide whether to boot fully or sleep again."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/deep-sleep-stub.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_hw_support/include/esp_wake_stub.h
  - https://github.com/espressif/esp-idf/tree/master/examples/system/deep_sleep_wake_stub
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deep-sleep wake stub

A wake stub runs from RTC fast memory right after deep-sleep wake, before the full boot (after wake the CPU must SPI-boot, which takes much longer than light sleep). Use it to check a sensor or counter and go back to
sleep quickly when there is nothing to do.

## Write the stub
```c
#include "esp_sleep.h"
#include "esp_wake_stub.h"      /* esp_wake_stub_sleep, esp_wake_stub_set_wakeup_time, ESP_RTC_LOGx */
RTC_DATA_ATTR int wake_count;

void RTC_IRAM_ATTR esp_wake_deep_sleep(void)    /* overrides weak default */
{
    esp_default_wake_deep_sleep();              /* must run first */
    wake_count++;
    if (wake_count % 10) {                      /* 9 of 10 wakes: back to sleep */
        esp_wake_stub_set_wakeup_time(60 * 1000000ULL);
        esp_wake_stub_sleep(&esp_wake_deep_sleep);   /* does not return */
    }
    /* return -> normal boot into app_main */
}
```
Or register a different function at runtime with `esp_set_deep_sleep_wake_stub(fn)`. Instead of `RTC_IRAM_ATTR`, the function and its data can live in a source file whose name starts with `rtc_wake_stub`; the linker places those into RTC fast memory automatically.

## Constraints
- Code must be in RTC fast memory (`RTC_IRAM_ATTR`) and data in RTC memory (`RTC_DATA_ATTR`,
  `RTC_RODATA_ATTR` for constants; string constants must be arrays marked `RTC_RODATA_ATTR`). The SPI flash is not mapped and other RAM is uninitialised.
- The stub can only call ROM functions or functions loaded into RTC fast memory, and most peripherals are in their reset state. Use
  `ESP_RTC_LOGI` or ROM `esp_rom_printf` for output, and direct register access.
- The stub size is limited by the size of RTC fast memory.
- RTC fast memory is validated with a CRC on wake; the stub only runs if validation passes.
- Some chips have only RTC fast memory, so data then lives there too; `CONFIG_<TARGET>_RTCDATA_IN_FAST_MEM` moves `RTC_DATA_ATTR` data into fast memory on chips that also have slow memory.

## Typical uses
- Count pulses or wake events, only boot every Nth time.
- Read a GPIO or RTC register to decide if the wake was a false trigger.
- Toggle a pin for a fast acknowledgement before full boot.

## Verify
- [ ] Current trace shows the short stub wake versus a full boot.
- [ ] Counter in RTC memory matches expected after N wakes.
- [ ] Power-on reset path still boots normally (stub only matters after deep sleep).

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the deep-sleep stub guide and esp_wake_stub.h: esp_wake_deep_sleep weak override with esp_default_wake_deep_sleep first, RTC_IRAM_ATTR and the rtc_wake_stub file-name rule, RTC_DATA_ATTR and RTC_RODATA_ATTR, ROM and RTC-only calls, CRC validation of RTC fast memory, esp_set_deep_sleep_wake_stub, esp_wake_stub_sleep, esp_wake_stub_set_wakeup_time and ESP_RTC_LOGx. Removed unconfirmed timing and current figures, the 8 KB size, the per-chip support claim and the CRC option names.
Method: documentation only; no commands were run.
