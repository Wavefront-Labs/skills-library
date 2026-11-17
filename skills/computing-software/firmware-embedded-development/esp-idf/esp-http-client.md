---
id: computing-software.firmware-embedded-development.esp-idf.esp-http-client
name: esp-http-client
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-networking, esp-http-client, https-requests, streaming-download, http-events, keep-alive, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Make HTTP/HTTPS requests from ESP-IDF with esp_http_client: simple perform calls, streaming large bodies, POST JSON, connection reuse, redirects and error handling."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/protocols/esp_http_client.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_http_client/include/esp_http_client.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esp_http_client

## Simple request (body fits in RAM)
```c
#include "esp_http_client.h"
#include "esp_crt_bundle.h"

esp_err_t post_status(const char *json)
{
    esp_http_client_config_t cfg = {
        .url = "https://api.acme.example/v1/status",
        .method = HTTP_METHOD_POST,
        .crt_bundle_attach = esp_crt_bundle_attach,
        .timeout_ms = 10000,
    };
    esp_http_client_handle_t c = esp_http_client_init(&cfg);
    esp_http_client_set_header(c, "Content-Type", "application/json");
    esp_http_client_set_header(c, "Authorization", auth_header);
    esp_http_client_set_post_field(c, json, strlen(json));   /* must be set before perform; persists between requests, set NULL to clear */

    esp_err_t err = esp_http_client_perform(c);
    int status = esp_http_client_get_status_code(c);
    esp_http_client_cleanup(c);
    if (err != ESP_OK) return err;                     /* transport error: DNS, TLS, timeout */
    return (status >= 200 && status < 300) ? ESP_OK : ESP_FAIL;   /* HTTP error is not err */
}
```
`perform` returning `ESP_OK` only means the exchange completed; a 500 is still `ESP_OK`.
Always check the status code.

## Streaming (large downloads, constant RAM)
```c
esp_http_client_handle_t c = esp_http_client_init(&cfg);       /* method GET */
ESP_ERROR_CHECK(esp_http_client_open(c, 0));                   /* 0 = no request body */
int64_t len = esp_http_client_fetch_headers(c);                /* content-length; 0 if absent or chunked; -1 on error */
int status = esp_http_client_get_status_code(c);
char buf[1024];
int n;
while ((n = esp_http_client_read(c, buf, sizeof buf)) > 0) consume(buf, n);
bool complete = esp_http_client_is_complete_data_received(c);
esp_http_client_close(c);
esp_http_client_cleanup(c);
```
For uploads: `esp_http_client_open(c, total_len)` then `esp_http_client_write` in chunks.

## Event handler (alternative to reading)
`.event_handler` receives `HTTP_EVENT_ON_HEADER`, `HTTP_EVENT_ON_DATA` (chunks, possibly
chunked transfer encoding), `HTTP_EVENT_ON_FINISH`, `HTTP_EVENT_DISCONNECTED`. Pass a context
with `.user_data`.

## Reuse and redirects
- Keep the handle and call `esp_http_client_set_url` + `perform` again to reuse the connection instead of paying a
  new TLS handshake per request.
- Redirects are followed automatically up to `.max_redirection_count` (default 10 when left at zero); set
  `.disable_auto_redirect = true` to handle them yourself.
- `.buffer_size` (receive) and `.buffer_size_tx` (transmit) limit header size; long headers such as JWTs need larger values (`ESP_ERR_HTTP_HEADER_TOO_LONG` is returned when a single request header exceeds `buffer_size_tx`).

## Errors to expect
`ESP_ERR_HTTP_CONNECT` (error opening the connection), `ESP_ERR_HTTP_EAGAIN` (timed out before data was ready),
`ESP_ERR_HTTP_CONNECTING` (timed out before the connection was made), `ESP_ERR_HTTP_FETCH_HEADER`, `ESP_ERR_HTTP_CONNECTION_CLOSED`. Retry with backoff and jitter; never in a tight loop.

## Verify
- [ ] Server returns 500/404: device reports failure (status checked).
- [ ] 5 MB download completes with flat heap usage (streaming path).
- [ ] TLS verification enabled (bundle or pinned CA), tested against a bad certificate.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from esp_http_client.h and the protocol guide: config fields (timeout_ms, crt_bundle_attach, buffer_size, buffer_size_tx, max_redirection_count default 10, disable_auto_redirect), set_post_field semantics, open/fetch_headers/read/write/close and is_complete_data_received, event IDs, ESP_ERR_HTTP_* codes. Wrong: fetch_headers returns 0 (not -1) for chunked or missing content-length and -1 on error; post data persists between requests (the skill said the pointer is kept). Removed unconfirmed handshake heap figure, 512 default, out-of-buffer message and event-versus-read mixing claim.
Method: documentation only; no commands were run.
