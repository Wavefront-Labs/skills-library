---
id: computing-software.firmware-embedded-development.iot-protocols.esp-ble-prov
name: esp-ble-prov
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [esp-ble-prov, ble-iot, esp-idf, wifi-provisioning, protocomm, security-1, iot-protocols]
level: practitioner
status: draft
description: "ESP-IDF BLE and SoftAP provisioning: Provision Wi-Fi on ESP32 with the stock manager."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/provisioning/wifi_provisioning.html
  - https://www.bluetooth.com/specifications/specs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ESP-IDF BLE and SoftAP provisioning

**Goal:** Provision Wi-Fi on ESP32 with the stock manager.

## Steps
1. Component wifi_provisioning with scheme wifi_prov_scheme_ble or softap
2. Call wifi_prov_mgr_init, wifi_prov_mgr_start_provisioning(security, pop, service_name, service_key)
3. Security 0 none, 1 X25519 key exchange plus AES-CTR with a proof-of-possession (PoP) string, 2 SRP6a (confirm in your IDF version)
4. Phone apps: ESP BLE Provisioning (Android, iOS) or esp_prov.py
5. Handle WIFI_PROV_CRED_RECV and WIFI_PROV_CRED_FAIL events
6. Deinit manager afterwards to free memory

## Gotcha
Security 0 with BLE sends credentials unprotected; always use 1 or 2 and a per-device PoP such as a label-printed code.

## Verify
- [ ] Credentials stored in NVS
- [ ] Reboot connects without provisioning
- [ ] PoP mismatch rejected
