---
id: computing-software.firmware-embedded-development.esp-idf.softap-and-apsta-mode
name: softap-and-apsta-mode
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, softap, apsta, wifi-mode-ap, captive-portal, channel-follow, esp-netif-ap, dhcp-server, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Run an ESP32 as a Wi-Fi access point (SoftAP) or AP+STA: configuration, DHCP server, the single-channel constraint, captive portals and client limits."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi_types_generic.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_wifi.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_netif/include/esp_netif.h
  - https://github.com/espressif/esp-idf/blob/master/components/lwip/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/overview.rst
  - https://github.com/espressif/esp-idf/blob/master/examples/wifi/getting_started/softAP/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SoftAP and AP+STA mode

**Goal:** a device that hosts its own network for setup or local control, optionally while
also connected to the home router.

## SoftAP setup
```c
ESP_ERROR_CHECK(esp_netif_init());
ESP_ERROR_CHECK(esp_event_loop_create_default());
esp_netif_create_default_wifi_ap();                 /* default AP netif with DHCP server */
wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
ESP_ERROR_CHECK(esp_wifi_init(&cfg));
wifi_config_t ap = { .ap = {
    .ssid = "Device-1A2B", .ssid_len = 0,
    .password = "setup-pass-123", .channel = 6,
    .max_connection = 4,
    .authmode = WIFI_AUTH_WPA2_PSK,
    .pmf_cfg = { .required = false },
}};
ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &ap));
ESP_ERROR_CHECK(esp_wifi_start());
```
Events: `WIFI_EVENT_AP_STACONNECTED` / `AP_STADISCONNECTED` (MAC, AID),
`IP_EVENT_AP_STAIPASSIGNED`.

## Gotchas
- Use a WPA2 password of at least 8 characters; an empty password needs `WIFI_AUTH_OPEN`.
- Derive the SSID suffix from the MAC (`esp_read_mac`) so multiple devices don't collide; don't
  hard-code a shared default password in production (print a per-device one on the label).
- `max_connection` is limited per chip (`ESP_WIFI_MAX_CONN_NUM`), and soft-AP shares encryption
  hardware keys with ESP-NOW, so `CONFIG_ESP_WIFI_ESPNOW_MAX_ENCRYPT_NUM` affects it.

## AP+STA (WIFI_MODE_APSTA)
- The radio has **one channel**: in soft-AP+station mode the soft-AP adjusts its channel
  automatically to match the station's. AP clients may be disrupted. Plan provisioning flows for this:
  tell the phone app to expect a reconnect, or switch to STA-only after provisioning.
- Both netifs need distinct subnets; to change the AP address use `esp_netif_set_ip_info`
  after stopping its DHCP server (it returns `ESP_ERR_ESP_NETIF_DHCP_NOT_STOPPED` otherwise).
- NAT between AP clients and the STA network is off by default: enable `CONFIG_LWIP_IP_FORWARD`
  and `CONFIG_LWIP_IPV4_NAPT`, then call `esp_netif_napt_enable()`, if you need a range extender.

## Captive portal
Phones detect captive portals by fetching known URLs. Run a DNS server that answers every
query with the AP address and serve the setup page for any path/Host. IDF example:
`examples/protocols/http_server/captive_portal`.

## Verify
- [ ] Phone joins, captive page opens automatically on iOS and Android.
- [ ] In AP+STA, behaviour when STA joins a different channel is handled.
- [ ] Per-device SSID/password, nothing shared across the fleet.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: wifi_ap_config_t fields (ssid_len, password, channel, max_connection note about ESP-NOW encryption keys), soft-AP follows station channel in APSTA mode (esp_wifi_set_config attention), esp_netif_set_ip_info requires DHCP stopped, NAPT needs LWIP_IP_FORWARD and LWIP_IPV4_NAPT, esp_netif_napt_enable, IP_EVENT_AP_STAIPASSIGNED, WIFI_EVENT_AP_STACONNECTED, captive_portal example path. Wrong: NAPT enable omitted CONFIG_LWIP_IP_FORWARD; "max_connection up to 10" is chip-specific. Removed unconfirmed DHCP option 114 claim and 192.168.4.x defaults.
Method: documentation only; no commands were run.
