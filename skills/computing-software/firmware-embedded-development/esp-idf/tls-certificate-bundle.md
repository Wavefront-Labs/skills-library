---
id: computing-software.firmware-embedded-development.esp-idf.tls-certificate-bundle
name: tls-certificate-bundle
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, esp-tls-certificate-bundle, esp-crt-bundle-attach, esp-tls, mbedtls, ca-certificates, mutual-tls, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Verify TLS servers from ESP-IDF with the built-in CA certificate bundle or a pinned CA: esp_crt_bundle_attach, custom bundles, mutual TLS, and planning for CA rotation."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/protocols/esp_crt_bundle.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp-tls/esp_tls.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/esp_https_ota.rst
  - https://github.com/espressif/esp-idf/blob/master/components/mbedtls/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS and the certificate bundle

## Option 1: the CA bundle (talking to public services)
```
CONFIG_MBEDTLS_CERTIFICATE_BUNDLE=y
CONFIG_MBEDTLS_CERTIFICATE_BUNDLE_DEFAULT_CMN=y   # common CAs (smaller) or ..._FULL
```
```c
#include "esp_crt_bundle.h"
esp_http_client_config_t cfg = {
    .url = "https://api.example.com/v1/status",
    .crt_bundle_attach = esp_crt_bundle_attach,
};
```
The same field exists in `esp_tls_cfg_t`, MQTT (`broker.verification.crt_bundle_attach`) and
`esp_https_ota`. The bundle is built from Mozilla's NSS root store (the full list has more than 130 certificates; the
common list picks authorities with more than 1% market share). It stores only each certificate's subject
name and public key. Add your own roots: `CONFIG_MBEDTLS_CUSTOM_CERTIFICATE_BUNDLE=y` with
`CONFIG_MBEDTLS_CUSTOM_CERTIFICATE_BUNDLE_PATH` pointing to a certificate file or a directory; only `.pem`
(PEM) and `.der` (DER) files are parsed and the extension must match the encoding.

## Option 2: pin one CA (your own backend)
```cmake
idf_component_register(SRCS "main.c" EMBED_TXTFILES "certs/backend_ca.pem")
```
```c
extern const char ca_pem_start[] asm("_binary_backend_ca_pem_start");
esp_http_client_config_t cfg = { .url = "https://iot.acme.example", .cert_pem = ca_pem_start };
```
Pin the **root** CA, not the leaf certificate: the esp_https_ota docs say to use the root because it
has the longest validity and usually stays the same when server certificates are renewed.
`EMBED_TXTFILES` embeds the file as a null-terminated string, which mbedTLS needs for PEM.

## Mutual TLS
```c
.client_cert_pem = dev_cert_pem, .client_key_pem = dev_key_pem,
```
Store per-device keys in encrypted NVS or, on chips with the DS peripheral, pass the DS context
(`ds_data` in `esp_tls_cfg_t`) so the private key never exists in plaintext.

## Things that bite
- **CA rotation:** the bundle is frozen at build time. When a service changes CA, devices
  without that root fail. Ship firmware updates regularly and keep an OTA path that doesn't
  depend on the rotating CA (e.g. your own pinned CA for the OTA server).
- **Time:** with `CONFIG_MBEDTLS_HAVE_TIME_DATE` disabled (the default) the certificate "valid from" and
  "valid to" fields are ignored. If you enable it, sync time with SNTP before connecting.
- **Never** ship with `.skip_cert_common_name_check = true` or verification disabled
  (`CONFIG_ESP_TLS_INSECURE` with `CONFIG_ESP_TLS_SKIP_SERVER_CERT_VERIFY`); it makes TLS pointless against an
  active attacker.
- **RAM:** the mbedtls-memory-tuning skill covers heap use (the guide's https_request example uses about
  42 KB by default); with PSRAM you can set `CONFIG_MBEDTLS_EXTERNAL_MEM_ALLOC`. Reduce
  `CONFIG_MBEDTLS_SSL_IN_CONTENT_LEN` only if the server supports max fragment length.
- **Errors:** a failed handshake with a certificate-verify error usually means a missing CA or a
  hostname mismatch; check `common_name` and the bundle.

## Verify
- [ ] Connection to a server with a self-signed or wrong-host certificate fails.
- [ ] Bundle or pinned CA covers every endpoint the device talks to (list them).
- [ ] Heap headroom measured during handshake.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in api-reference/protocols/esp_crt_bundle.rst, esp_tls.h, system/esp_https_ota.rst, the build-system guide and components/mbedtls/Kconfig: bundle contents and file-extension rules, option names (CERTIFICATE_BUNDLE, CERTIFICATE_BUNDLE_DEFAULT_CMN / _FULL, CUSTOM_CERTIFICATE_BUNDLE and _PATH), crt_bundle_attach field, EMBED_TXTFILES null termination, HAVE_TIME_DATE default off, ESP_TLS_INSECURE and ESP_TLS_SKIP_SERVER_CERT_VERIFY, ds_data. Fixed: pin the root rather than an intermediate CA (the OTA docs say root). Removed the unconfirmed 30-50 KB handshake figure and the specific -0x2700 error mapping.

Method: documentation only; no commands were run.
