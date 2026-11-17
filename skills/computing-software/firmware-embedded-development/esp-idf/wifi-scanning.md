---
id: computing-software.firmware-embedded-development.esp-idf.wifi-scanning
name: wifi-scanning
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, wifi-scan, esp-wifi-scan-start, ap-records, channel-scan, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Scan for access points with ESP-IDF esp_wifi_scan_start: active vs passive, channel and dwell settings, retrieving AP records and scanning while connected."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi_types_generic.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/station-scenarios.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi scanning

## Blocking scan
```c
ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
ESP_ERROR_CHECK(esp_wifi_start());

wifi_scan_config_t sc = {
    .ssid = NULL, .bssid = NULL, .channel = 0,      /* 0 = all channels */
    .show_hidden = true,
    .scan_type = WIFI_SCAN_TYPE_ACTIVE,
    .scan_time.active = { .min = 100, .max = 300 }, /* ms per channel */
};
ESP_ERROR_CHECK(esp_wifi_scan_start(&sc, true));    /* block until done */

uint16_t n = 0;
esp_wifi_scan_get_ap_num(&n);
wifi_ap_record_t *ap = calloc(n, sizeof(*ap));
esp_wifi_scan_get_ap_records(&n, ap);               /* frees the driver's list */
for (int i = 0; i < n; i++)
    ESP_LOGI(TAG, "%-32s ch%2d %4d dBm auth=%d", ap[i].ssid, ap[i].primary, ap[i].rssi, ap[i].authmode);
free(ap);
```
Always call `esp_wifi_scan_get_ap_records` (or `esp_wifi_clear_ap_list`) after a scan; the
driver holds the list in heap until you do.

## Non-blocking
Pass `false`, then handle `WIFI_EVENT_SCAN_DONE` (event data `wifi_event_sta_scan_done_t` has
`status` and `number`). Do not start a second scan while one is running (the header lists `ESP_ERR_WIFI_STATE` among its errors).

## Tuning
- Passive scan (`WIFI_SCAN_TYPE_PASSIVE`, `.passive = 360`; 360 ms is the default) for DFS
  channels or when probing is not allowed. Slower. Defaults for active scans are min 0 ms,
  max 120 ms per channel.
- Restrict `channel`, or set the country with `esp_wifi_set_country_code()` so the scanned
  channels match the regulatory domain.
- Scanning a known SSID: set `.ssid` to reduce probe traffic.
- Connecting fast: `wifi_sta_config_t.scan_method = WIFI_ALL_CHANNEL_SCAN` plus
  `sort_method = WIFI_CONNECT_AP_BY_SIGNAL` picks the strongest BSS for mesh/multi-AP networks.

## Scanning while connected
Allowed; the STA leaves its home channel while scanning, so traffic can be delayed. Keep
`active.max` short, set `home_chan_dwell_time` (30 to 150 ms) and avoid scanning during streaming.

## Pitfalls
- Scan results sit in driver-allocated heap until `esp_wifi_scan_get_ap_records()`,
  `esp_wifi_scan_get_ap_record()` or `esp_wifi_clear_ap_list()` frees them.
- Per-channel active and passive scan times are capped at 1500 ms.

## Verify
- [ ] Hidden SSIDs appear with empty names when `show_hidden` is set.
- [ ] Heap returns to baseline after 100 scans (no leaked AP list).

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed against esp_wifi.h and types: scan defaults (active 0/120 ms, passive 360 ms, home dwell 30 ms), 1500 ms cap, AP list freed by get_ap_records or clear_ap_list, scan_method and WIFI_CONNECT_AP_BY_SIGNAL, esp_wifi_set_country_code, WIFI_EVENT_SCAN_DONE struct. Removed unconfirmed claims about connect failing during scan, +/-5 dB RSSI variation, and AP+STA channel effects of scanning.
Method: documentation only; no commands were run.
