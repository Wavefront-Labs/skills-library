---
id: computing-software.firmware-embedded-development.esp-idf.wifi-provisioning-and-reconnect-resilience
name: wifi-provisioning-and-reconnect-resilience
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-idf, esp32, wifi-provisioning, esp-wifi-prov, softap-provisioning, ble-provisioning, esp-event, wifi-event, ip-event, reconnect-backoff, sta-disconnected, auth-fail, dhcp-timeout, nvs-wifi-creds, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Get an ESP32 onto Wi-Fi and keep it there: unified provisioning flows, the esp_event connect/disconnect state machine, and reconnect backoff that avoids retry storms."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/provisioning/provisioning.rst
  - https://github.com/espressif/idf-extra-components/tree/master/network_provisioning
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi_types_generic.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/station-scenarios.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi provisioning and reconnect resilience on ESP-IDF

**Goal:** get credentials onto a device without hardcoding them, and keep the
device connected (or recovering sanely) through real-world AP flakiness —
distinct from the dual-core/task concerns in this field's other esp-idf
skills; this is specifically the Wi-Fi connection lifecycle.

## Provisioning so credentials aren't hardcoded
Hardcoding SSID/password in firmware means every unit ships with one
network's credentials baked in — unworkable past a single dev board.
Unified Provisioning exposes a SoftAP (HTTP server) or BLE endpoint during a
provisioning window; a companion app (ESP's own provisioning apps, or your own
using the published protocol) sends credentials and the device switches to
station mode. The Wi-Fi provisioning component (`wifi_provisioning`, `WIFI_PROV_*`
names) was moved out of ESP-IDF in April 2024 and renamed `network_provisioning`
(`NETWORK_PROV_*` names) in the idf-extra-components repository; use the new names.
Key decisions:
- **SoftAP vs BLE provisioning**: SoftAP needs the phone to join the device's
  temporary AP. BLE avoids that but needs the BLE stack's flash/RAM budget and a
  capable companion app.
- **Security**: the protocomm layer offers Security 0 (no security),
  `NETWORK_PROV_SECURITY_1` (X25519 key exchange, proof-of-possession
  authentication, AES-CTR) and `NETWORK_PROV_SECURITY_2` (SRP6a-based
  authentication and key exchange, AES-GCM). Do not ship Security 0 beyond a
  bench prototype; the schemes must be enabled in menuconfig.
- Provide a **re-provisioning trigger** (long-press a button, a BLE command, a
  "forget network" API) — a device with stale/changed Wi-Fi credentials and no
  way back into provisioning mode needs a factory reset to recover, which is a
  support cost you can design away.

## The esp_event connection state machine
Wi-Fi/IP state changes arrive as events, not return codes from a blocking
connect call: `WIFI_EVENT_STA_START`, `WIFI_EVENT_STA_DISCONNECTED`,
`IP_EVENT_STA_GOT_IP`. Structure connection logic as an event handler, not a
linear "connect then proceed" function — `esp_wifi_connect()` returns
immediately; success/failure arrives later as an event. Treat
`WIFI_EVENT_STA_DISCONNECTED`'s reason code (`wifi_event_sta_disconnected_t.reason`)
as actionable: `WIFI_REASON_AUTH_FAIL`/`WIFI_REASON_NO_AP_FOUND` mean retrying
immediately with the same credentials won't help (bad password, AP out of
range, or an unsupported band), vs a transient reason code where fast retry
is reasonable.

## Reconnect backoff — don't retry-storm
Reconnecting immediately and unconditionally on every disconnect, forever, at
full retry rate wastes power (relevant given
`computing-software.firmware-embedded-development.esp-idf.deep-sleep-power-budgeting`'s
Wi-Fi-connect-cost concerns) and can hammer a struggling AP. Implement
exponential backoff with a cap (e.g. 1s, 2s, 4s... capped at 60s) on repeated
`STA_DISCONNECTED` events, reset to the fast retry once a connection
succeeds. Distinguish "AP not found / out of range" (keep backing off, maybe
stop trying after N attempts and surface a user-visible state) from "got
disconnected after a long successful connection" (retry fast, this is probably
transient AP reboot/roam).

## DHCP and captive-portal stalls
A `WIFI_EVENT_STA_CONNECTED` without a following `IP_EVENT_STA_GOT_IP` within
a reasonable timeout suggests an IP-layer problem (DHCP or captive portal) rather than
a Wi-Fi association problem — don't report "Wi-Fi failed" from this state;
it's a different failure class needing different handling (or at minimum a
different log message than an auth failure).

## Verify
- [ ] Device can be provisioned and re-provisioned without a firmware reflash, tested end to end with the actual companion app/flow.
- [ ] Provisioning security level is at least Security 1 (or 2); credentials aren't observable in the clear during provisioning (checked with a sniff, not assumed).
- [ ] Disconnect reason codes are logged and drive different retry behavior (auth-fail vs transient) rather than one blind retry loop.
- [ ] Reconnect backoff is capped and verified not to retry-storm against a deliberately unreachable AP for an extended bench test.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: WIFI_EVENT_STA_DISCONNECTED reason field and reason codes AUTH_FAIL (202) and NO_AP_FOUND (201); provisioning transports (SoftAP+HTTP or BLE); security schemes. Wrong: Security 1 was described as SRP6a-based, but the docs say Security 1 is X25519 + PoP + AES-CTR and Security 2 is SRP6a + AES-GCM; the esp_wifi_prov / WIFI_PROV_* API was moved to the network_provisioning component (renamed NETWORK_PROV_*) in April 2024. Removed the unconfirmed NVS storage and phone-UX claims.
Method: documentation only; no commands were run.
