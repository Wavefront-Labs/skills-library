---
id: computing-software.firmware-embedded-development.esp-idf.wifi-roaming-80211kv
name: wifi-roaming-80211kv
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, wifi-roaming, 80211k, 80211v, 80211r, bss-transition, rssi-threshold, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Make ESP32 stations roam between access points with 802.11k neighbor reports, 802.11v BSS transition and RSSI-threshold triggers in ESP-IDF."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/security-and-roaming.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi.h
  - https://github.com/espressif/esp-idf/blob/master/components/wpa_supplicant/esp_supplicant/include/esp_rrm.h
  - https://github.com/espressif/esp-idf/blob/master/components/wpa_supplicant/esp_supplicant/include/esp_wnm.h
  - https://github.com/espressif/esp-idf/blob/master/examples/wifi/roaming/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi roaming (802.11k/v)

By default an ESP32 station stays on its AP until the link drops. In multi-AP deployments that
means minutes on a weak AP. Roaming support lets it move proactively.

## Enable
```
CONFIG_ESP_WIFI_11KV_SUPPORT=y
CONFIG_ESP_WIFI_RRM_SUPPORT=y      # 802.11k
CONFIG_ESP_WIFI_WNM_SUPPORT=y      # 802.11v
CONFIG_ESP_WIFI_11R_SUPPORT=y      # fast transition, if the network uses FT
```
```c
wifi_config_t wc = { .sta = { .ssid = SSID, .password = PASS,
    .rm_enabled = 1, .btm_enabled = 1, .ft_enabled = 1,
    .scan_method = WIFI_ALL_CHANNEL_SCAN, .sort_method = WIFI_CONNECT_AP_BY_SIGNAL } };
```
ESP-IDF also ships a roaming app (`CONFIG_ESP_WIFI_ENABLE_ROAMING_APP`, default off) that
automates the logic below: periodic environment scans, a cache of best APs and low-RSSI
handling.

## Trigger on weak signal
```c
esp_wifi_set_rssi_threshold(-70);           /* posts WIFI_EVENT_STA_BSS_RSSI_LOW when avg RSSI falls below */
static void on_rssi_low(void *a, esp_event_base_t b, int32_t id, void *d) {
    /* 802.11k: ask the AP for neighbours on the same ESS */
    esp_rrm_send_neighbor_report_request();
}
```
Call `esp_wifi_set_rssi_threshold()` again after each event to receive another one. With 11v
enabled, `esp_wnm_send_bss_transition_mgmt_query` asks the AP for a candidate. Without k/v
support on the AP, fall back to your own scan-and-reconnect logic.

## Hysteresis
Only roam when the candidate is clearly stronger, and rate-limit roams to avoid ping-pong
between two equal APs (thresholds are application choices; tune by walk test).

## Fast transition (11r)
Fast Transition shortens re-association by avoiding the full authentication exchange. The
station supports FT over the air only, for WPA2-PSK networks; enable `ft_enabled` in
`wifi_sta_config_t`.

## Verify
- [ ] Walk test: log BSSID, RSSI and roam timestamps; device moves to the nearer AP.
- [ ] Measure outage per roam with a continuous ping and compare with and without FT.
- [ ] No roam loops when parked between two APs.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed Kconfig symbols (11KV, RRM, WNM, 11R, ENABLE_ROAMING_APP), the sta config fields rm_enabled, btm_enabled, ft_enabled, esp_rrm_send_neighbor_report_request, esp_wnm_send_bss_transition_mgmt_query, RSSI-low event re-arm rule, and that FT is over-the-air only for WPA2-PSK. Wrong: threshold "fires once" (re-arm by calling the API again). Removed unconfirmed dB margins, rate limits, timing figures and the claim about Enterprise roaming times.
Method: documentation only; no commands were run.
