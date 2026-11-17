---
id: computing-software.firmware-embedded-development.esp-idf.mqtt-mutual-tls
name: mqtt-mutual-tls
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-protocols, mqtt-mutual-tls, mqtts, client-certificate, aws-iot-core, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Connect ESP-MQTT to brokers that require client certificates (AWS IoT Core, Azure, Mosquitto mTLS): config fields, key storage options, ALPN and common handshake failures."
sources:
  - https://github.com/espressif/esp-mqtt
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/protocols/mqtt.html
  - https://github.com/espressif/esp-mqtt/tree/master/examples/ssl_mutual_auth
  - https://github.com/awsdocs/aws-iot-docs/blob/main/developerguide/protocols.md
  - https://github.com/Mbed-TLS/mbedtls/tree/mbedtls-3.6/include/mbedtls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT with mutual TLS

## Component
Since ESP-IDF v6.0 the MQTT client is no longer part of ESP-IDF: add it with `idf.py add-dependency espressif/mqtt`
(repository espressif/esp-mqtt, header `mqtt_client.h`). The mutual-TLS examples live in that repository
(`examples/ssl_mutual_auth`, and `examples/ssl_ds` for a DS-peripheral key).

## Config
```c
esp_mqtt_client_config_t cfg = {
    .broker.address.uri = "mqtts://a1b2c3-ats.iot.eu-west-1.amazonaws.com:8883",
    .broker.verification.crt_bundle_attach = esp_crt_bundle_attach,   /* or .certificate = root CA PEM */
    .credentials.client_id = thing_name,                     /* if NULL the client generates one */
    .credentials.authentication.certificate = dev_cert_pem,
    .credentials.authentication.key = dev_key_pem,
    /* key in hardware instead: .credentials.authentication.ds_data = esp_secure_cert_get_ds_ctx() */
    .session.keepalive = 60,                                  /* default is 120 seconds */
    .network.reconnect_timeout_ms = 10000,                    /* used when auto-reconnect is active */
};
esp_mqtt_client_handle_t c = esp_mqtt_client_init(&cfg);
esp_mqtt_client_register_event(c, ESP_EVENT_ANY_ID, mqtt_handler, NULL);
esp_mqtt_client_start(c);
```
PEM buffers must be NUL-terminated (`EMBED_TXTFILES` embeds a null-terminated string) or pass `certificate_len`/`key_len`. The client does not copy or free the certificate buffers, so keep them valid for the client's lifetime.

## Port 443 with ALPN
Networks blocking 8883: the AWS IoT protocols page (2023 documentation snapshot) lists MQTT with an X.509 client certificate on port 443 using ALPN protocol name `x-amzn-mqtt-ca`, and on port 8883 without ALPN:
```c
static const char *alpn[] = { "x-amzn-mqtt-ca", NULL };
cfg.broker.address.uri = "mqtts://...:443"; cfg.broker.verification.alpn_protos = alpn;
```

## Key storage
Never embed one key for all devices. Options in order of strength: DS peripheral (key never in
RAM), esp_secure_cert partition with flash encryption, encrypted NVS. See the DS and
esp_secure_cert skills.

## Handshake failures
| Log | Cause |
|---|---|
| `MBEDTLS_ERR_X509_CERT_VERIFY_FAILED` (-0x2700) | the broker certificate did not verify: wrong root CA, or the system time is not set yet so the certificate looks not yet valid (sync SNTP first) |
| `mbedtls_ssl_handshake returned -0x7780` (`MBEDTLS_ERR_SSL_FATAL_ALERT_MESSAGE`) | the broker sent a fatal alert, for example rejecting the client certificate; check the broker side |
| `MBEDTLS_ERR_PEM_NO_HEADER_FOOTER_PRESENT` (-0x1080), `MBEDTLS_ERR_X509_INVALID_FORMAT` (-0x2180) | certificate or key could not be parsed: missing NUL terminator or length, wrong header |
| connects then immediate disconnect | broker-side policy or a duplicate client ID; consult the broker's logs |

Raise the `esp-tls` log level (`esp_log_level_set("esp-tls", ESP_LOG_VERBOSE)`) and read the broker-side logs.

## Rotation
Plan certificate rotation before expiry: provision a new cert via a job or claim flow, store
in the second slot, switch, then delete the old.

## Verify
- [ ] Connection with an unregistered cert is rejected by the broker.
- [ ] Reconnect after Wi-Fi loss without heap growth (100 cycles).

## Checked

Checked against ESP-IDF v6.1 docs (api-reference/protocols/mqtt.rst, build-system.rst), the esp-mqtt repository (master, last commit 2026-10-23, tag v1.1.0; include/mqtt_client.h and the ssl_mutual_auth and ssl_ds examples), the Mbed TLS 3.6 headers and the awsdocs aws-iot-docs protocols page (archived snapshot, last commit 2023-06-15).
Confirmed: MQTT moved out of ESP-IDF in v6.0 to `espressif/mqtt`; config fields `broker.address.uri`, `broker.verification.certificate`/`crt_bundle_attach`/`alpn_protos`, `credentials.client_id`, `credentials.authentication.certificate`/`key`/`ds_data`, `session.keepalive` (default 120 s), `network.reconnect_timeout_ms`; `esp_secure_cert_get_ds_ctx` use in the ssl_ds example; `esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, ...)` as used in the examples; EMBED_TXTFILES null-termination; AWS IoT port 443 with ALPN `x-amzn-mqtt-ca` and port 8883; mbedTLS codes -0x2700 (cert verify failed), -0x7780 (fatal alert), -0x1080 (PEM header/footer missing), -0x2180 (X.509 invalid format). Corrected: -0x2700 was listed as a parse error. Removed unconfirmed claims: AWS CloudWatch logging and the specific AWS IoT policy and client ID causes of immediate disconnects.

Method: documentation only; no commands were run.
