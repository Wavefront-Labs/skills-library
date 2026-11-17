---
id: computing-software.firmware-embedded-development.esp-idf.wifi-ble-coexistence
name: wifi-ble-coexistence
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, wifi-ble-coexistence, software-coexistence, time-division, esp-coex, bt-wifi-throughput, scan-window, ble-provisioning-coex, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run Wi-Fi and BLE together on one ESP32 radio: how time-division coexistence works, what degrades (BLE scan, Wi-Fi throughput), config knobs and design patterns."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/coexist.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/performance/ram-usage.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_coex/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/components/esp_psram/Kconfig.spiram.common
  - https://github.com/espressif/esp-idf/blob/master/components/bt/controller/esp32/Kconfig.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi and BLE coexistence on ESP32

**Goal:** both radios working well enough at the same time, e.g. BLE provisioning while Wi-Fi
connects, or a BLE sensor gateway forwarding over Wi-Fi.

## How it works
ESP32-family chips have one 2.4 GHz RF front-end. The coexistence module time-slices it between
Wi-Fi and Bluetooth by priority (software coexistence: enable `CONFIG_ESP_COEX_SW_COEXIST_ENABLE` in menuconfig, otherwise the
coexistence functions are unavailable). Neither gets the radio 100 % of the time.

## What degrades
- **BLE scanning** gets only part of the time: scan duty cycle drops, so devices are found
  slower and some advertisements are missed. On classic ESP32 the guide points to
  `CONFIG_BTDM_CTRL_FULL_SCAN_SUPPORTED` so BLE can reacquire the radio inside a scan window.
- **Wi-Fi throughput** drops during BLE activity because the radio is time-shared.
- Espressif's coexistence guide describes the coexistence policy per chip; read the section for
  your target before designing.

## Design patterns
- **Sequence where possible:** BLE provisioning finishes, then deinit BLE and release its
  memory before heavy Wi-Fi use (`esp_bt_mem_release`; Bluetooth is then unavailable until the
  next restart). The network provisioning manager offers
  `NETWORK_PROV_SCHEME_BLE_EVENT_HANDLER_FREE_BTDM` for this (it was
  `WIFI_PROV_SCHEME_BLE_EVENT_HANDLER_FREE_BTDM` in the older `wifi_provisioning` component).
- **Gateways:** keep scan duty cycle modest and batch uplinks over Wi-Fi rather than streaming
  continuously.
- **Power save:** under coexistence Wi-Fi is active only during its own time slice and sleeps
  otherwise, even if `esp_wifi_set_ps(WIFI_PS_NONE)` is called.
- **Core placement:** put the Bluetooth controller and host tasks on one CPU
  (`CONFIG_BT_NIMBLE_PINNED_TO_CORE_CHOICE` for NimBLE) and the Wi-Fi task on the other
  (`CONFIG_ESP_WIFI_TASK_CORE_ID`).
- **Dual-chip** (separate BLE SoC + Wi-Fi) or a second radio when both need full performance.

## Memory
Both stacks together use a lot of internal RAM. Options: PSRAM for Wi-Fi/lwIP buffers
(`CONFIG_SPIRAM_TRY_ALLOCATE_WIFI_LWIP`) and, on classic ESP32, BLE-only controller mode
(`CONFIG_BTDM_CTRL_MODE_BLE_ONLY`).

## Verify
- [ ] Measure Wi-Fi throughput (iperf) with BLE idle, connected and scanning.
- [ ] BLE scan hit rate on a known beacon with Wi-Fi idle vs busy.
- [ ] 24 h soak with both active: no BLE supervision timeouts or Wi-Fi disconnects.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed against the coexistence guide: software coexistence option name and that it must be enabled, Wi-Fi sleeps outside its slice even with WIFI_PS_NONE, core-pinning options, FULL_SCAN option; Kconfig names SPIRAM_TRY_ALLOCATE_WIFI_LWIP and BTDM_CTRL_MODE_BLE_ONLY; esp_bt_mem_release behaviour (RAM guide); FREE_BTDM handler name (network_provisioning headers). Wrong: "IDF refuses WIFI_PS_NONE with BT" and "software coexistence on by default". Removed unconfirmed scan-window, connection-interval and timeout claims.
Method: documentation only; no commands were run.
