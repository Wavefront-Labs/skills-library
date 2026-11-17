---
id: computing-software.firmware-embedded-development.esp-idf.wifi-throughput-tuning
name: wifi-throughput-tuning
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, wifi-throughput, iperf, lwip-tuning, wifi-buffers, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Raise ESP32 Wi-Fi TCP/UDP throughput by measuring with iperf and tuning Wi-Fi buffers, lwIP windows, IRAM options, CPU clock and power save."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/wifi-performance-and-power-save.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/wifi-mac-protocols.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/overview.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/performance/speed.rst
  - https://github.com/espressif/esp-idf/blob/master/examples/wifi/iperf/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi throughput tuning

## Measure first
Flash `examples/wifi/iperf`, connect, then:
```
iperf> sta_connect <ssid> <pass>
iperf> iperf -s -i 3                # device as TCP server
pc$   iperf -c <device-ip> -i 3 -t 30
```
Test in a clean channel close to the AP, then in the real environment. The Wi-Fi overview
quotes up to 20 Mbit/s TCP and 30 Mbit/s UDP for ESP32 as best-case figures.

## Kconfig knobs (the iperf example's sdkconfig.defaults is the reference)
| Option | Effect |
|---|---|
| `CONFIG_ESP_WIFI_STATIC_RX_BUFFER_NUM` / `DYNAMIC_RX_BUFFER_NUM` | more RX buffers, more RAM |
| `CONFIG_ESP_WIFI_DYNAMIC_TX_BUFFER_NUM` | TX queue depth |
| `CONFIG_ESP_WIFI_RX_BA_WIN` | RX block-ack aggregation window |
| `CONFIG_LWIP_TCP_SND_BUF_DEFAULT`, `TCP_WND_DEFAULT` | TCP send buffer and receive window |
| `CONFIG_LWIP_TCP_RECVMBOX_SIZE`, `TCPIP_RECVMBOX_SIZE` | lwIP queue depth |
| `CONFIG_ESP_WIFI_IRAM_OPT`, `RX_IRAM_OPT`, `LWIP_IRAM_OPTIMIZATION` | hot paths in IRAM |

Each Wi-Fi buffer is a fixed 1.6 KB; with PSRAM enable `CONFIG_SPIRAM_TRY_ALLOCATE_WIFI_LWIP`.

## Runtime
- `esp_wifi_set_ps(WIFI_PS_NONE)` (power save adds latency and cuts throughput sharply).
- `esp_wifi_set_bandwidth(WIFI_IF_STA, WIFI_BW_HT40)`: HT40 has a higher raw PHY rate (150 vs
  72 Mbit/s) but the Wi-Fi guide warns it can be worse where many other devices share the band;
  use HT20 there.
- Pin the heavy application task to the core not running Wi-Fi (`CONFIG_ESP_WIFI_TASK_CORE_ID`).

## Interpreting limits
- Watch free internal heap (`heap_caps_get_free_size(MALLOC_CAP_INTERNAL)`) while tuning buffers.
- BLE coexistence time-shares the radio; expect lower throughput while BLE is active.
- Check RSSI (`esp_wifi_sta_get_ap_info`): antenna and board layout limit throughput.

## Verify
- [ ] Baseline and tuned iperf results recorded with the sdkconfig diff.
- [ ] Free heap under peak load stays above a safety margin chosen for the product.
- [ ] No regression in latency-sensitive tasks after IRAM changes.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed Kconfig names in the performance guide (STATIC/DYNAMIC RX, DYNAMIC TX, RX_BA_WIN, TCP_SND_BUF_DEFAULT, TCP_WND_DEFAULT, IRAM_OPT options, LWIP_IRAM_OPTIMIZATION), 1.6 KB fixed buffer size, HT40 vs HT20 guidance, ESP_WIFI_TASK_CORE_ID. Removed unconfirmed "4x RX buffers x 1436" formula, CPU 240 MHz option, TCP_NODELAY and send-size advice, and speed claims for S3/C6. Note: CONFIG_ESP_WIFI_AMPDU_TX_ENABLED was not found in the docs and was dropped from the table.
Method: documentation only; no commands were run.
