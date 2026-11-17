---
id: computing-software.firmware-embedded-development.esp-idf.wifi-power-save-modes
name: wifi-power-save-modes
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, wifi-power-save, wifi-ps-min-modem, wifi-ps-max-modem, listen-interval, dtim, modem-sleep, auto-light-sleep, target-wake-time, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Cut ESP32 Wi-Fi station current while staying connected: modem-sleep min/max, listen interval vs DTIM, automatic light sleep and the latency costs."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/wifi-performance-and-power-save.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/low-power-mode/low-power-mode-wifi.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi_he.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_pm/include/esp_pm.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi power-save modes (ESP-IDF)

**Goal:** a connected Wi-Fi device that sleeps between beacons, with predictable latency.

## Modes
```c
esp_wifi_set_ps(WIFI_PS_NONE);        /* modem sleep off: lowest latency, higher power */
esp_wifi_set_ps(WIFI_PS_MIN_MODEM);   /* default: wake every DTIM beacon */
esp_wifi_set_ps(WIFI_PS_MAX_MODEM);   /* wake every listen_interval beacons */
```
For `MAX_MODEM`, set `wifi_config.sta.listen_interval` (in beacon intervals) via `esp_wifi_set_config()` before
connecting; it may be longer than the AP's DTIM period.

## DTIM and the AP
Broadcast/multicast traffic is buffered by the AP until the DTIM beacon. MIN_MODEM wakes at
every DTIM (AP setting, often 1-3). You can't change the AP's DTIM from the device; when it's 1
on the customer's router, MIN_MODEM wakes every beacon. MAX_MODEM can sleep through DTIMs, so
broadcasts (ARP requests, mDNS) can be **missed**: the device appears offline to some
discovery protocols. Test with your discovery mechanism.

## Modem sleep vs light sleep
Modem sleep turns off only the radio between beacons; the CPU keeps running. Add **automatic
light sleep** so the CPU also sleeps between beacons:
```
CONFIG_PM_ENABLE=y
CONFIG_FREERTOS_USE_TICKLESS_IDLE=y
```
```c
esp_pm_config_t pm = { .max_freq_mhz = 160, .min_freq_mhz = 40, .light_sleep_enable = true };
esp_pm_configure(&pm);
```
Anything holding a PM lock (`ESP_PM_NO_LIGHT_SLEEP`, e.g. some drivers) prevents light sleep;
see the low-power-mode Wi-Fi guide for per-chip current figures.

## Latency trade-off
With modem sleep on, receive delay can equal the DTIM cycle (MIN_MODEM) or the listen interval
(MAX_MODEM). For a device that must respond quickly, use MIN_MODEM with a short DTIM, or
WIFI_PS_NONE.

## Wi-Fi 6 Target Wake Time (C6, C5)
Wi-Fi 6 targets (for example ESP32-C6) expose individual TWT through
`esp_wifi_sta_itwt_setup()` (flow IDs 0-7); the AP must support TWT.

## Verify
- [ ] Average current measured over minutes for each mode with the real AP.
- [ ] Ping latency and discovery (mDNS/ARP) tested in the chosen mode.
- [ ] `esp_pm_dump_locks(stdout)` shows no unexpected lock blocking light sleep.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: min/max modem semantics, listen interval set via esp_wifi_set_config before connecting, MIN_MODEM is the default, NONE disables modem sleep, esp_wifi_sta_itwt_setup, esp_pm_config_t fields and PM lock names. Removed unconfirmed current figures (~100 mA, 1-5 mA), 102 ms arithmetic and the C5 TWT claim.
Method: documentation only; no commands were run.
