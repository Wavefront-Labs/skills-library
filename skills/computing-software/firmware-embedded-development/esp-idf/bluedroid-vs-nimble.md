---
id: computing-software.firmware-embedded-development.esp-idf.bluedroid-vs-nimble
name: bluedroid-vs-nimble
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, bluedroid, nimble, bt-classic, bluetooth-host-stack, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose between Bluedroid and NimBLE host stacks in ESP-IDF: Classic BT support, RAM/flash cost, API style, and how to switch or port a project."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/ble/overview.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/bluetooth/index.rst
  - https://github.com/espressif/esp-idf/blob/master/components/bt/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bluedroid vs NimBLE

ESP-IDF ships two Bluetooth host stacks on the same controller. `CONFIG_BT_BLUEDROID_ENABLED`
or `CONFIG_BT_NIMBLE_ENABLED`; only one per build.

## Decision
| Need | Pick |
|---|---|
| Classic BT (A2DP audio, SPP, HFP) on ESP32 | Bluedroid (NimBLE is BLE only) |
| BLE only, RAM tight | NimBLE (documented to need less heap and flash) |
| BLE Mesh | either (ESP-BLE-MESH supports both) |
| Existing code on `esp_ble_gatts_*` / `esp_gap_ble_*` | Bluedroid unless porting |
| Portable code / Apache Mynewt API | NimBLE |

Classic BT is supported only on the original ESP32; Bluedroid on other chips is BLE only.

## API differences
- Bluedroid: callback registration (`esp_ble_gap_register_callback`, `esp_ble_gatts_register_callback`),
  attribute tables (`esp_ble_gatts_create_attr_tab`), event enums per profile.
- NimBLE: service definitions as static `ble_gatt_svc_def` arrays, one GAP callback per
  connection/advertising instance, mbufs for data.
Porting is a rewrite of the BLE layer: keep your application logic behind your own small
interface (send, on_receive, on_connect) so the stack is swappable.

## Memory
Measure, do not guess: build both variants of a minimal app and run `idf.py size` plus
`heap_caps_get_free_size(MALLOC_CAP_INTERNAL)` after init. Release memory for unused modes:
```c
esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT);    /* BLE only on ESP32, before init */
```

## Config gotchas
- `CONFIG_BTDM_CTRL_MODE` (ESP32): `BTDM_CTRL_MODE_BLE_ONLY` / `BTDM_CTRL_MODE_BR_EDR_ONLY` / `BTDM_CTRL_MODE_BTDM` (dual). Use dual with Bluedroid for
  combined Classic + BLE.
- NimBLE task stack (`CONFIG_BT_NIMBLE_HOST_TASK_STACK_SIZE`) needs raising when your callbacks log heavily.

## Verify
- [ ] Chosen stack documented with the reason (Classic need or RAM).
- [ ] Free internal heap after BT init meets the application budget.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed: host choice Kconfig (BT_BLUEDROID_ENABLED / BT_NIMBLE_ENABLED), Classic BT only on ESP32, NimBLE lower heap and flash, ESP-BLE-MESH selecting for both hosts, esp_bt_controller_mem_release modes, BT_NIMBLE_HOST_TASK_STACK_SIZE. Wrong: CONFIG_BT_CONTROLLER_MODE does not exist; the ESP32 option is CONFIG_BTDM_CTRL_MODE. Removed the unconfirmed 'tens of KB' figure and the SPIRAM-first option.
Method: documentation only; no commands were run.
