---
id: computing-software.firmware-embedded-development.low-power-design.wifi-fast-reconnect
name: wifi-fast-reconnect
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [wifi-fast-connect, static-ip, bssid-channel-cache, deep-sleep-wifi, esp32-wifi-reconnect, dhcp-skip, low-power, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Cut Wi-Fi wake energy on battery devices: cache BSSID and channel in RTC memory, fast scan, static IP or DHCP lease reuse, skipping DNS and TLS handshakes, and timing it."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/network/esp_wifi.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/low-power-mode/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fast Wi-Fi reconnect

A Wi-Fi sensor that wakes from deep sleep spends most of its energy associating: scan, auth,
DHCP, DNS, TLS. Shortening that sequence is usually the biggest battery win; measure it on your
own hardware (see Measuring).

## Steps (ESP-IDF)
1. **Cache AP details** after the first successful connection in RTC memory (survives deep sleep):
   ```c
   RTC_DATA_ATTR static uint8_t s_bssid[6]; RTC_DATA_ATTR static uint8_t s_chan; RTC_DATA_ATTR static bool s_valid;
   wifi_config_t cfg = { .sta = { .ssid = SSID, .password = PASS } };
   if (s_valid) { memcpy(cfg.sta.bssid, s_bssid, 6); cfg.sta.bssid_set = true; cfg.sta.channel = s_chan; }
   cfg.sta.scan_method = WIFI_FAST_SCAN;           /* scan ends after the first SSID match */
   esp_wifi_set_config(WIFI_IF_STA, &cfg);
   ```
   `wifi_sta_config_t.channel` is a hint: the scan starts from that channel (0 = no preference).
   The ESP-IDF docs say `bssid_set` is normally 0 and should be 1 only when you need to check the
   AP's MAC address; here that is the point, so clear the cache when the BSSID changes.
   On `WIFI_EVENT_STA_CONNECTED` the event data carries `ssid`, `bssid` and `channel`: save the
   BSSID and channel; on failure clear `s_valid` and fall back to a full scan
   (`WIFI_ALL_CHANNEL_SCAN`).
2. **Skip DHCP:** use a static IP when the network allows it, or keep the leased address and DNS
   in RTC memory and reuse them until the lease expires.
3. **Avoid DNS:** cache the resolved IP with its TTL.
4. **Station config persistence:** `esp_wifi_set_config()` stores the station configuration in
   NVS; the storage default is `WIFI_STORAGE_FLASH`.
5. **TLS resumption:** reuse session tickets/IDs where your TLS stack supports them, or use a
   persistent broker session, instead of a full handshake on every wake.
6. **Send and sleep:** deep sleep immediately after the ACK.

## Other platforms
The same ideas apply on other Wi-Fi stacks: give the driver a channel and BSSID hint where the
API accepts one.

## Measuring
Toggle a GPIO from wake to "data sent" and capture current; report charge per report (mC) for
the cold path (full scan + DHCP) against the cached path on your own board.

## Gotchas
- APs that change channel (auto channel selection, mesh roaming) break the cache; fallback must be
  automatic and bounded.
- Some routers rate-limit or deauth rapid reconnects; back off on repeated failures.
- Static IPs collide with DHCP pools unless reserved on the router.

## Verify
- [ ] Wake-to-sent time logged per report; 95th percentile within budget.
- [ ] Changing the AP channel recovers within one wake via fallback scan.

## Checked
2026-10-31. Confirmed on the ESP-IDF esp_wifi API reference: `esp_wifi_set_config`, `bssid_set`
guidance, `bssid[6]`, `channel` hint semantics, `scan_method` with `WIFI_FAST_SCAN` and
`WIFI_ALL_CHANNEL_SCAN`, connected-event fields (`ssid`, `bssid`, `channel`), config stored in
NVS, `WIFI_STORAGE_FLASH` default. Removed as unconfirmed: all timing, current and charge
figures, the PBKDF2 and PMK-caching claims, `esp_netif_*` and `esp_tls` call names, the Arduino
`WiFi.begin` form and the nRF70/CYW43 claim. The ESP-IDF Wi-Fi driver guide returned an empty
page and was not used.
Method: documentation only; no commands were run.
