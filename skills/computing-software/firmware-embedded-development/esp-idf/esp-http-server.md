---
id: computing-software.firmware-embedded-development.esp-idf.esp-http-server
name: esp-http-server
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-networking, esp-http-server, httpd-register-uri-handler, websocket-server, https-server, rest-api, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Serve a local REST API, web UI or WebSocket from ESP32 with esp_http_server: URI handlers, reading request bodies safely, chunked responses, socket limits and HTTPS."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/protocols/esp_http_server.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_http_server/include/esp_http_server.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/protocols/esp_https_server.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esp_http_server

## Start and register
```c
#include "esp_http_server.h"

static esp_err_t status_get(httpd_req_t *req)
{
    char json[128];
    int n = snprintf(json, sizeof json, "{\"uptime\":%lld}", esp_timer_get_time() / 1000000);
    httpd_resp_set_type(req, "application/json");
    return httpd_resp_send(req, json, n);
}

static esp_err_t config_post(httpd_req_t *req)
{
    char body[512];
    if (req->content_len >= sizeof body) {
        return httpd_resp_send_err(req, HTTPD_413_CONTENT_TOO_LARGE, "too large");
    }
    int got = 0;
    while (got < req->content_len) {
        int r = httpd_req_recv(req, body + got, req->content_len - got);
        if (r == HTTPD_SOCK_ERR_TIMEOUT) continue;          /* retry on timeout */
        if (r <= 0) return ESP_FAIL;                         /* closes the socket */
        got += r;
    }
    body[got] = '\0';
    if (!apply_config_json(body)) return httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "bad json");
    return httpd_resp_sendstr(req, "ok");
}

httpd_handle_t web_start(void)
{
    httpd_config_t cfg = HTTPD_DEFAULT_CONFIG();
    cfg.max_uri_handlers = 16;              /* default 8; more returns ESP_ERR_HTTPD_HANDLERS_FULL */
    cfg.lru_purge_enable = true;            /* drop oldest socket when out of sockets */
    cfg.uri_match_fn = httpd_uri_match_wildcard;
    httpd_handle_t srv = NULL;
    ESP_ERROR_CHECK(httpd_start(&srv, &cfg));
    httpd_uri_t s = { .uri = "/api/status", .method = HTTP_GET,  .handler = status_get };
    httpd_uri_t c = { .uri = "/api/config", .method = HTTP_POST, .handler = config_post };
    httpd_register_uri_handler(srv, &s);
    httpd_register_uri_handler(srv, &c);
    return srv;
}
```

## Larger responses
Send in chunks to avoid big buffers (e.g. a file from a mounted filesystem):
```c
while ((n = fread(buf, 1, sizeof buf, f)) > 0) httpd_resp_send_chunk(req, buf, n);
httpd_resp_send_chunk(req, NULL, 0);        /* terminates the chunked response */
```
Serve gzipped static assets with `httpd_resp_set_hdr(req, "Content-Encoding", "gzip")`.

## Concurrency and limits
- Handlers run in the server task (`cfg.stack_size`, default 4096; increase for JSON
  parsing or TLS), so a slow handler delays other requests. For long operations use async handlers
  (`httpd_req_async_handler_begin`, see the `async_handlers` example) or hand off to a worker task.
- `cfg.max_open_sockets` (default 7) is the maximum number of connected clients; 3 sockets are reserved for the server's internal use, so it must fit within the lwIP socket limit. Browsers open several sockets each; enable `lru_purge_enable` (default false).
- Validate every input: content length, JSON fields, path parameters. This is a network-facing
  parser.

## WebSocket
`CONFIG_HTTPD_WS_SUPPORT=y`, register with `.is_websocket = true`; in the handler use
`httpd_ws_recv_frame`; push from other tasks with `httpd_ws_send_frame_async(srv, fd, &frame)`.

## HTTPS and auth
`esp_https_server` (`httpd_ssl_config_t`, `HTTPD_SSL_CONFIG_DEFAULT()`) adds TLS; each TLS connection costs extra heap, so lower `max_open_sockets` and measure. Add authentication (token header or basic auth over TLS)
for anything that changes configuration; a LAN is not a security boundary.

## Verify
- [ ] Oversized and malformed bodies rejected without crash (fuzz with curl/scripts).
- [ ] Several browser tabs plus API clients: no socket exhaustion lockups.
- [ ] Config-changing endpoints require authentication.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from esp_http_server.h and the server guides: HTTPD_DEFAULT_CONFIG defaults (stack_size 4096, max_open_sockets 7 with 3 reserved, max_uri_handlers 8, lru_purge_enable false), ESP_ERR_HTTPD_HANDLERS_FULL, httpd_uri_match_wildcard, HTTPD_SOCK_ERR_TIMEOUT, httpd_resp_send_err codes, send_chunk, httpd_req_async_handler_begin, CONFIG_HTTPD_WS_SUPPORT with is_websocket and httpd_ws_recv_frame and send_frame_async, httpd_ssl_config_t. Removed unconfirmed single-task blocking claim, TLS heap figure and LWIP_MAX_SOCKETS formula; reworded the socket limit from the header text.
Method: documentation only; no commands were run.
