---
id: computing-software.firmware-embedded-development.esp-idf.https-server
name: https-server
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-protocols, esp-https-server, httpd-ssl, tls-server, self-signed-cert, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Serve HTTPS from an ESP32 with esp_https_server: server certificate options, memory per session, client cert auth, and browser trust issues for local devices."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/esp_https_server.html
  - https://github.com/espressif/esp-idf/blob/v6.1/components/esp_https_server/include/esp_https_server.h
  - https://github.com/espressif/esp-idf/tree/master/examples/protocols/https_server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTPS server

`esp_https_server` wraps `esp_http_server` with TLS. Handlers are identical to plain HTTP.

## Start
```c
#include "esp_https_server.h"
extern const uint8_t cert_start[] asm("_binary_servercert_pem_start");
extern const uint8_t cert_end[]   asm("_binary_servercert_pem_end");
extern const uint8_t key_start[]  asm("_binary_prvtkey_pem_start");
extern const uint8_t key_end[]    asm("_binary_prvtkey_pem_end");

httpd_ssl_config_t conf = HTTPD_SSL_CONFIG_DEFAULT();
conf.servercert = cert_start; conf.servercert_len = cert_end - cert_start;
conf.prvtkey_pem = key_start; conf.prvtkey_len = key_end - key_start;
conf.httpd.max_open_sockets = 3;            /* default in HTTPD_SSL_CONFIG_DEFAULT() is 4; each TLS session costs heap */
httpd_handle_t srv;
ESP_ERROR_CHECK(httpd_ssl_start(&srv, &conf));
httpd_register_uri_handler(srv, &status_uri);
```
`CONFIG_ESP_HTTPS_SERVER_ENABLE=y`.

## Certificates
- Shared key embedded in every device = anyone extracting it can impersonate all devices.
  Generate a per-device key and cert at provisioning (or on first boot) and store it in
  encrypted NVS / esp_secure_cert.
- Browsers distrust self-signed certs and private IPs. Options: users accept a warning, a
  companion app pins the device cert, or devices get certs under a real domain via your cloud
  (DNS name pointing to the local IP).
- The `httpd_ssl_config_t` also has `server_key` (unified key config, takes precedence over
  `prvtkey_pem`) and ECDSA-peripheral fields (`use_ecdsa_peripheral`, `ecdsa_key_efuse_blk`,
  `ecdsa_curve` SECP256R1 or SECP384R1) for keys kept in hardware.

## Client certificate auth
```c
conf.cacert_pem = ca_start; conf.cacert_len = ca_end - ca_start;   /* CA that signed the client certs (or the client cert itself) */
/* with CONFIG_ESP_TLS_SERVER_MIN_AUTH_MODE_OPTIONAL: conf.client_cert_authmode_optional = true; */
```

## Performance
The ESP-IDF docs say the initial TLS session setup can take about two seconds (more with a slower
clock or verbose logging), and later requests over the open secure socket are much faster (down to
under 100 ms). `session_tickets` (default false) enables TLS session tickets. Keep `max_open_sockets`
low; `HTTPD_SSL_CONFIG_DEFAULT()` already sets `lru_purge_enable = true`, so the least recently used
connection is purged when the limit is reached.

## Verify
- [ ] `curl -v --cacert ca.pem https://<device>/status` succeeds; wrong CA fails.
- [ ] Free internal heap with max sessions open stays above margin.
- [ ] Private key not identical across two units.

## Checked

Checked against ESP-IDF v6.1 (components/esp_https_server/include/esp_https_server.h, Kconfig, docs/en/api-reference/protocols/esp_https_server.rst).
Confirmed: `httpd_ssl_start`, `HTTPD_SSL_CONFIG_DEFAULT()` defaults (max_open_sockets 4, lru_purge_enable true), field names `servercert`, `servercert_len`, `prvtkey_pem`, `prvtkey_len`, `cacert_pem`, `cacert_len`, `session_tickets` (default false), `server_key`, `use_ecdsa_peripheral`, `transport_mode`, `CONFIG_ESP_HTTPS_SERVER_ENABLE`, the documented setup time of about two seconds. Removed unconfirmed claims: the 40 KB per session figure, the RSA-2048 one second timing, ECDSA being faster and browsers opening six parallel connections.

Method: documentation only; no commands were run.
