---
id: computing-software.firmware-embedded-development.esphome.esphome-wifi-connection-and-fallback-ap
name: esphome-wifi-connection-and-fallback-ap
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, wifi, static-ip, fallback-ap, reboot-timeout, fast-connect, min-auth-mode, power-save-mode, roaming]
level: practitioner
status: docs-checked
description: "Configure ESPHome WiFi: credentials, multiple networks, static IPs, fallback hotspot, reboot timeout, fast_connect storage, minimum auth mode and roaming."
sources: ["https://esphome.io/components/wifi/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome wifi connection and fallback ap

The wifi component is required unless you configure Ethernet; on ESP32 both can coexist using a `network:` priority list (multiple interfaces are unsupported on other platforms). A static IP is recommended because it can dramatically improve connection times.

Core options:
- `ssid`, `password`, or `networks` for several candidates (the best reachable is chosen).
- `manual_ip`: `static_ip`, `gateway`, `subnet` required; `dns1`, `dns2` optional.
- `use_address`: override what address tools use, for example to OTA to a previously configured IP after changing it.
- `domain` (default `.local`).
- `reboot_timeout` (default 15min, `0s` disables; not applied in AP mode), because the IP stack may need a full reboot to recover.
- `output_power` 8.5 to 20.5 dB; on ESP8266 20 dB is the default and 20.5 dB may cause restarts.
- `power_save_mode`, `enable_on_boot`, `use_psram` (ESP32 with PSRAM configured), `passive_scan`.

Fallback hotspot: adding `ap:` creates an access point; `ssid` defaults to the device name, `channel` 1 to 14 (default 1), `ap_timeout` (default 90s, `0s` disables automatic start, so something else must start it).

`fast_connect` skips the initial scan, connecting to the first network seen; if it fails ESPHome still scans. The block form has `enabled` and `storage` (`flash` survives power loss but wears flash; `rtc` survives software reboots and deep sleep but not power loss, default `rtc` on ESP8266 and `flash` on ESP32). Hidden networks use `hidden: true` per network.

`min_auth_mode` (ESP32 and ESP8266): `WPA`, `WPA2` (default, recommended) or `WPA3` (ESP32 only); `WPA` allows weak TKIP.

`post_connect_roaming` (default true) switches to an AP with the same SSID that is about 10 dB stronger; it is disabled automatically when `enable_btm` or `enable_rrm` is on. Triggers: `on_connect`, `on_disconnect`. ESP8266 `phy_mode: 11G` works around some 802.11n router issues.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/wifi/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
