---
id: computing-software.firmware-embedded-development.esp-idf.mbedtls-memory-tuning
name: mbedtls-memory-tuning
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-protocols, mbedtls-memory-tuning, tls-buffer-size, dynamic-tls-buffers, mbedtls-psram, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Cut ESP-IDF mbedTLS RAM use per TLS connection with variable/dynamic buffers, content length limits, PSRAM allocation and cipher suite trimming, without breaking handshakes."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/protocols/mbedtls.rst
  - https://github.com/espressif/esp-idf/blob/master/components/mbedtls/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mbedTLS configuration and memory

The mbedTLS guide measures about 42 KB of heap for the https_request example with server validation
at default settings, and about 22 KB with `CONFIG_MBEDTLS_DYNAMIC_BUFFER`, `..._DYNAMIC_FREE_CONFIG_DATA`
and `..._DYNAMIC_FREE_CA_CERT` enabled (values vary by version and config). Several concurrent
connections exhaust a small chip quickly.

## Measure
```c
size_t before = heap_caps_get_free_size(MALLOC_CAP_INTERNAL);
/* connect */
ESP_LOGI(TAG, "TLS cost %u, min free %u", before - heap_caps_get_free_size(MALLOC_CAP_INTERNAL),
         heap_caps_get_minimum_free_size(MALLOC_CAP_INTERNAL));
```

## Levers (menuconfig > Component config > mbedTLS)
| Option | Saves | Caveat |
|---|---|---|
| `CONFIG_MBEDTLS_DYNAMIC_BUFFER` | allocates TX/RX buffers only while sending or receiving; the lead item in the guide's table | not supported with DTLS; selects ASYMMETRIC_CONTENT_LEN |
| `CONFIG_MBEDTLS_DYNAMIC_FREE_CONFIG_DATA` / `_CA_CERT` | frees private key, DHM data and CA cert after the handshake | you must register the certificate and key on the ssl config again |
| `CONFIG_MBEDTLS_ASYMMETRIC_CONTENT_LEN` (default on) with `SSL_OUT_CONTENT_LEN` (default 4096) | the Kconfig help says about 12 KB per connection with default values | |
| `CONFIG_MBEDTLS_SSL_IN_CONTENT_LEN` (range 512 to 16384, default 16384) | lower values save RAM | servers must honour the Max Fragment Length extension (`CONFIG_MBEDTLS_SSL_MAX_FRAGMENT_LENGTH`), otherwise oversize records fail |
| `CONFIG_MBEDTLS_SSL_KEEP_PEER_CERTIFICATE` off | about 3.7 KB in the guide's table | the peer certificate is not kept after the handshake |
| `CONFIG_MBEDTLS_EXTERNAL_MEM_ALLOC` / `DEFAULT_MEM_ALLOC` | memory allocation strategy (internal, external, custom) | external memory needs PSRAM and is slower |
| `CONFIG_MBEDTLS_CERTIFICATE_BUNDLE_CROSS_SIGNED_VERIFY` off | about 1 KB less peak heap | larger bundle in flash, no cross-signed chains |
| Disable unused features (see "Reducing Binary Size") | flash | check server compatibility |

Most servers send full-size records; reducing IN_CONTENT_LEN without Max Fragment Length support
breaks downloads. Test with your real servers. Mbed TLS 3.x supports only TLS 1.2 and 1.3.

## Handshake peaks
Measure peaks with your real certificate chains. Client session tickets
(`CONFIG_MBEDTLS_CLIENT_SSL_SESSION_TICKETS`) provide TLS session resumption on reconnect.

## Hardware acceleration
`CONFIG_MBEDTLS_HARDWARE_AES`, `_SHA`, `_MPI` (and `_ECC` where supported) enable hardware acceleration
on chips that have the peripheral.

## Verify
- [ ] Peak internal heap use per connection measured before/after tuning.
- [ ] Large download (1 MB) and handshake against every production endpoint pass.
- [ ] N concurrent connections (design max) succeed with margin.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in api-reference/protocols/mbedtls.rst (Reducing Heap Usage table: 42196 B default, 22013 B with dynamic buffers, 38533 B without keep-peer-cert, cross-signed verify note) and components/mbedtls/Kconfig (ASYMMETRIC_CONTENT_LEN default y saving 12 KB, IN/OUT content length ranges and defaults, DYNAMIC_BUFFER dependencies, DYNAMIC_FREE_* help, MAX_FRAGMENT_LENGTH, memory allocation options, session tickets, hardware options). Removed: the 40-50 KB and 20 KB figures, the TLS 1.0/1.1 advice (removed in mbedTLS 3.x), the specific MBEDTLS_ERR_SSL_INVALID_RECORD error name, RSA-4096 and HW MPI memory claims.

Method: documentation only; no commands were run.
