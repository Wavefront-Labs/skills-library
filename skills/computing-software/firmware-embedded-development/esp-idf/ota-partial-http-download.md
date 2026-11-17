---
id: computing-software.firmware-embedded-development.esp-idf.ota-partial-http-download
name: ota-partial-http-download
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ota, partial-http-download, http-range-request, ota-resume, esp-https-ota, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Download OTA images in HTTP range chunks with ESP-IDF esp_https_ota partial download to cut RAM use, survive flaky links and work with size-limited servers."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/esp_https_ota/include/esp_https_ota.h
  - https://github.com/espressif/esp-idf/blob/master/examples/system/ota/advanced_https_ota/sdkconfig.ci.ota_resumption_partial_download
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial HTTP download for OTA

## Enable
Partial download needs `CONFIG_ESP_HTTPS_OTA_ENABLE_PARTIAL_DOWNLOAD=y`; the fields `partial_http_download`
and `max_http_request_size` exist in `esp_https_ota_config_t` only when it is set.
```c
esp_http_client_config_t http = { .url = URL, .crt_bundle_attach = esp_crt_bundle_attach,
                                  .keep_alive_enable = true };
esp_https_ota_config_t ota = {
    .http_config = &http,
    .partial_http_download = true,
    .max_http_request_size = 16 * 1024,     /* bytes per Range request */
};
esp_https_ota_handle_t h;
ESP_ERROR_CHECK(esp_https_ota_begin(&ota, &h));
while ((err = esp_https_ota_perform(h)) == ESP_ERR_HTTPS_OTA_IN_PROGRESS) {
    report_progress(esp_https_ota_get_image_len_read(h), esp_https_ota_get_image_size(h));
}
```
Each chunk is a separate HTTP range request; keep-alive lets them share a connection.

## When it helps
- Servers or proxies that cut long downloads (some CDNs, cellular gateways with idle timeouts).
- Metered or flaky links where a single multi-MB stream often fails mid-way.

## Resume after reboot
`esp_https_ota_config_t` has `ota_resumption` ("resumption in downloading of OTA image between reboots")
and `ota_image_bytes_written` ("updated by the application when OTA data is written successfully").
The application is responsible for persisting that byte count; the advanced_https_ota example shows
the pairing with partial download. Confirm the image version did not change between attempts
(compare ETag or version first).

## Server requirements
- Must honour `Range` and return `206 Partial Content` with `Content-Range` (standard HTTP range
  requests; test the server with a ranged request).
- Signed URLs expire during long downloads: generate long enough lifetimes.

## Pitfalls
- Very small `max_http_request_size` multiplies HTTP header overhead and round trips.
- Without keep-alive each chunk may need a new TLS connection.

## Verify
- [ ] Network dropped at 50%: OTA retries (or resumes) and completes.
- [ ] Download time compared with full-stream mode on the real link.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in esp_https_ota.h and the advanced_https_ota example sdkconfig.ci files: partial_http_download and max_http_request_size fields exist only with CONFIG_ESP_HTTPS_OTA_ENABLE_PARTIAL_DOWNLOAD, ota_resumption and ota_image_bytes_written fields, esp_https_ota_get_image_len_read / get_image_size, ESP_ERR_HTTPS_OTA_IN_PROGRESS. Fixed the claim that no Kconfig is needed. Removed the unconfirmed IDF 5.2 gate, NVS storage claim, mbedTLS buffer tip, curl check and handshake timing.

Method: documentation only; no commands were run.
