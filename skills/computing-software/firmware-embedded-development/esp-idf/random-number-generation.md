---
id: computing-software.firmware-embedded-development.esp-idf.random-number-generation
name: random-number-generation
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-system, esp-random, hardware-rng, entropy-source, bootloader-random, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Get cryptographically strong random numbers on ESP32 with esp_random and esp_fill_random, and know when the hardware RNG has real entropy (RF on, SAR ADC source)."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/random.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random number generation

## API
```c
#include "esp_random.h"
uint32_t r = esp_random();
uint8_t key[32];
esp_fill_random(key, sizeof key);
```

## Is it truly random
Physical noise is continuously mixed into the RNG state only while one of these is true:
- the RF subsystem is enabled (Wi-Fi, Bluetooth or 802.15.4 depending on the chip), or
- the internal SAR ADC entropy source has been enabled with `bootloader_random_enable()` and not yet
  disabled (the ADC is not usable meanwhile), or
- the second-stage bootloader is running (it enables that source at start and disables it at the end).
After app start, normally only pseudo-random numbers are available until RF is initialised or the
source is enabled again. Chips other than ESP32 also have a secondary entropy source (an asynchronous
internal oscillator) that is always on, but the docs only guarantee true random numbers when the main
source is also enabled.

## Generating keys at boot (before Wi-Fi)
```c
#include "bootloader_random.h"
bootloader_random_enable();
esp_fill_random(seed, sizeof seed);
bootloader_random_disable();     /* frees the ADC */
```
The second-stage bootloader enables this source while it runs (used for first-boot key generation);
after the app takes over, the source stops unless RF is on.

## Bulk data
The hardware RNG state is not large enough to give a continuous stream of true random numbers. If you
cannot keep a hardware source on, the docs suggest a strong DRBG (mbedTLS CTR-DRBG or HMAC-DRBG) seeded
with true random numbers from the hardware RNG.

## Do not
- Use `rand()`/`srand(time(NULL))` for anything security related; time before SNTP is 1970.
- Seed from `esp_timer_get_time()` alone: predictable.

## Verify
- [ ] Key generation code path runs with RF on or `bootloader_random_enable()` active (code review).
- [ ] Statistical sanity check of a captured stream during bring-up (the guide mentions the Dieharder suite).

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in api-reference/system/random.rst: esp_random and esp_fill_random, conditions under which noise is mixed in, bootloader_random_enable and bootloader_random_disable, bootloader behaviour, secondary entropy source (non-ESP32), DRBG recommendation. Removed the unconfirmed RNG read-rate figure and the mbedtls_entropy macro name.

Method: documentation only; no commands were run.
