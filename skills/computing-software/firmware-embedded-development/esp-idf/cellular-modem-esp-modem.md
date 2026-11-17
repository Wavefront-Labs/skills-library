---
id: computing-software.firmware-embedded-development.esp-idf.cellular-modem-esp-modem
name: cellular-modem-esp-modem
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-protocols, esp-modem, ppp-cellular, at-commands, lte-cat-m1, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Bring an ESP32 online over a cellular modem (SIM7600, BG96, SIM7070) with the esp_modem component: AT setup, PPP data mode, CMUX, netif integration and recovery."
sources:
  - https://github.com/espressif/esp-protocols/blob/master/components/esp_modem/README.md
  - https://github.com/espressif/esp-protocols/blob/master/components/esp_modem/include/esp_modem_config.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cellular modems with esp_modem

```yaml
dependencies:
  espressif/esp_modem: "^2.1.0"
```

## Bring-up
```c
#include "esp_modem_api.h"
esp_netif_config_t ncfg = ESP_NETIF_DEFAULT_PPP();
esp_netif_t *ppp = esp_netif_new(&ncfg);

esp_modem_dte_config_t dte = ESP_MODEM_DTE_DEFAULT_CONFIG();
dte.uart_config.tx_io_num = 17; dte.uart_config.rx_io_num = 16;
dte.uart_config.rts_io_num = 18; dte.uart_config.cts_io_num = 19;
dte.uart_config.flow_control = ESP_MODEM_FLOW_CONTROL_HW;
dte.uart_config.rx_buffer_size = 4096;
esp_modem_dce_config_t dce_cfg = ESP_MODEM_DCE_DEFAULT_CONFIG("internet.apn");
esp_modem_dce_t *dce = esp_modem_new_dev(ESP_MODEM_DCE_SIM7600, &dte, &dce_cfg, ppp);

int rssi, ber;
esp_modem_get_signal_quality(dce, &rssi, &ber);
ESP_ERROR_CHECK(esp_modem_set_mode(dce, ESP_MODEM_MODE_DATA));   /* starts PPP */
/* wait for IP_EVENT_PPP_GOT_IP, then sockets/HTTP/MQTT work as with Wi-Fi */
```
Device enums in `esp_modem_dce_device_t`: `ESP_MODEM_DCE_GENERIC`, `SIM7600`, `SIM7070`, `SIM7000`, `BG96`, `EC20`, `SIM800`, `SQNGM02S` and `CUSTOM`; use the generic one for unlisted modems.

## CMUX
`ESP_MODEM_MODE_CMUX` is the multiplexed terminal mode (there are also manual CMUX modes in the same enum). Not every modem firmware supports CMUX reliably; test.

## Power and recovery
- Drive the modem's power key with the timing in its datasheet and wait for it to answer `AT`.
- Network registration can take a while. Poll registration through
  `esp_modem_at(dce, "AT+CEREG?", out, timeout_ms)` (the `timeout` parameter is in milliseconds).
- If PPP drops (`IP_EVENT_PPP_LOST_IP`), go to command mode, check registration, re-enter data
  mode; after N failures power-cycle the modem.
- Cellular modules draw large current peaks: follow the modem datasheet for supply and bulk capacitance.
## Throughput
The UART baud rate caps PPP throughput (115200 baud is at most about 11.5 KB/s at 8N1); raise the modem and DTE baud rates together and use hardware flow control (`ESP_MODEM_FLOW_CONTROL_HW`).

## Verify
- [ ] Cold boot to IP within the expected time in a weak-signal location.
- [ ] Pull the antenna, restore: link recovers without reboot.
- [ ] Data usage per day measured (TLS handshakes dominate on Cat-M).

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the esp_modem headers (esp-protocols master, component version 2.1.0): ESP_MODEM_DTE_DEFAULT_CONFIG and DCE_DEFAULT_CONFIG, uart_config fields and flow-control enum, esp_modem_new_dev, esp_modem_set_mode with DATA and CMUX modes, esp_modem_get_signal_quality, esp_modem_at (timeout in ms), IP_EVENT_PPP_GOT_IP and LOST_IP, ESP_NETIF_DEFAULT_PPP. Wrong: the dependency pin ^1.1.0 (current component is 2.x) and the device list (SIM7672 is not in the enum; EC20, SQNGM02S and CUSTOM are). Removed unconfirmed power-key timing, current peak and capacitor figures, signal-quality sentinel value, 921600 baud advice and USB modem claim.
Method: documentation only; no commands were run.
