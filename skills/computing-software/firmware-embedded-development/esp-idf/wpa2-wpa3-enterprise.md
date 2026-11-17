---
id: computing-software.firmware-embedded-development.esp-idf.wpa2-wpa3-enterprise
name: wpa2-wpa3-enterprise
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, wpa2-enterprise, wpa3-enterprise, eap-tls, peap, esp-eap-client, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Connect ESP32 to WPA2/WPA3-Enterprise networks with esp_eap_client: EAP-TLS, PEAP and TTLS, certificate validation, identity and time requirements."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/wpa_supplicant/esp_supplicant/include/esp_eap_client.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-security.rst
  - https://github.com/espressif/esp-idf/blob/master/examples/wifi/wifi_enterprise/README.md
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WPA2/WPA3 Enterprise

The API is `esp_eap_client.h` (station mode only).

## PEAP / TTLS (username + password)
```c
#include "esp_eap_client.h"
wifi_config_t wc = { .sta = { .ssid = "corp" } };
esp_wifi_set_config(WIFI_IF_STA, &wc);

esp_eap_client_set_identity((uint8_t *)"anonymous", 9);           /* outer identity */
esp_eap_client_set_username((uint8_t *)USER, strlen(USER));
esp_eap_client_set_password((uint8_t *)PASS, strlen(PASS));
esp_eap_client_set_ca_cert(ca_pem_start, ca_pem_end - ca_pem_start); /* validate RADIUS */
esp_eap_client_set_ttls_phase2_method(ESP_EAP_TTLS_PHASE2_MSCHAPV2); /* TTLS only */
esp_wifi_sta_enterprise_enable();
esp_wifi_start();   /* connect on WIFI_EVENT_STA_START */
```

## EAP-TLS (client certificate)
```c
esp_eap_client_set_identity((uint8_t *)"device-123", 10);
esp_eap_client_set_ca_cert(ca, ca_len);
esp_eap_client_set_certificate_and_key(cli_crt, cli_crt_len, cli_key, cli_key_len, NULL, 0);
esp_wifi_sta_enterprise_enable();
```
Store per-device keys in esp_secure_cert or encrypted NVS, not embedded in the app.

## WPA3-Enterprise
WPA3-Enterprise requires Protected Management Frames and server certificate validation, so set
`wc.sta.pmf_cfg.required = true` and always set the CA. For the 192-bit mode enable
`CONFIG_ESP_WIFI_SUITE_B_192` (needs GCMP support in the chip); the example README lists
RSA 3096 or EC certificates with NSA Suite B ciphers for that mode.

## Server validation and time
Always set the CA certificate (WPA3-Enterprise makes server certificate validation mandatory), and optionally `esp_eap_client_set_domain_name()` to
match the server name. Certificate validity checks need correct time; devices with no RTC may
fail before SNTP. The time check can be disabled with
`esp_eap_client_set_disable_time_check(true)`, with documented risk.

## Debugging
- Reason code 15 (`WIFI_REASON_4WAY_HANDSHAKE_TIMEOUT`) and Espressif code 204
  (`WIFI_REASON_HANDSHAKE_TIMEOUT`) are handshake timeouts; check the RADIUS server log for the
  exact failure.
- Large certificates cost time and heap on chips without crypto acceleration (see the
  wifi_enterprise example README); check free heap.

## Verify
- [ ] Connection fails against a test RADIUS with a different CA.
- [ ] Reconnect after AP reboot works without re-setting credentials.
- [ ] Credentials are not printed in logs.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in esp_eap_client.h: set_identity, set_username, set_password, set_ca_cert, set_certificate_and_key (6 arguments, last two optional key password), set_ttls_phase2_method, set_domain_name, set_disable_time_check, esp_wifi_sta_enterprise_enable; wifi-security guide: WPA3-Enterprise requires PMF and CA validation; reason codes 15 and 204. Wrong: ECDSA P-384/RSA 3072 (example README says RSA 3096 or EC) and the "time-check option under CONFIG_ESP_WIFI_ENTERPRISE_SUPPORT" (it is a runtime API; the Kconfig option only enables enterprise support, default y). Removed version gates (5.1, 5.2), wpa log tag and heap figures.
Method: documentation only; no commands were run.
