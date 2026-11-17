---
id: computing-software.firmware-embedded-development.esp-idf.websocket-client
name: websocket-client
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-protocols, esp-websocket, esp-websocket-client, wss, websocket-reconnect, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Connect ESP32 to WebSocket servers with the esp_websocket_client component: wss with certificate validation, text/binary frames, fragmentation, ping and reconnect."
sources:
  - https://docs.espressif.com/projects/esp-protocols/esp_websocket_client/docs/latest/index.html
  - https://components.espressif.com/components/espressif/esp_websocket_client
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebSocket client

The client is the `esp_websocket_client` component from esp-protocols, distributed through
the component registry. Add it to `idf_component.yml` as `espressif/esp_websocket_client` and
pin the version shown on the registry page.

## Connect
```c
#include "esp_websocket_client.h"
static void ws_handler(void *arg, esp_event_base_t b, int32_t id, void *data) {
    esp_websocket_event_data_t *d = data;
    switch (id) {
    case WEBSOCKET_EVENT_CONNECTED: ESP_LOGI(TAG, "connected"); break;
    case WEBSOCKET_EVENT_DATA:
        if (d->op_code == 0x1 || d->op_code == 0x2 || d->op_code == 0x0)    /* text, binary, continuation */
            on_chunk(d->data_ptr, d->data_len, d->payload_offset, d->payload_len);
        break;
    case WEBSOCKET_EVENT_DISCONNECTED: case WEBSOCKET_EVENT_ERROR: ESP_LOGW(TAG, "lost"); break;
    }
}
esp_websocket_client_config_t cfg = {
    .uri = "wss://api.example.com/ws",
    .crt_bundle_attach = esp_crt_bundle_attach,   /* needs MBEDTLS_CERTIFICATE_BUNDLE; include esp_crt_bundle.h */
    .reconnect_timeout_ms = 5000, .network_timeout_ms = 10000,
    .ping_interval_sec = 20, .pingpong_timeout_sec = 30,
    .headers = "Authorization: Bearer XYZ\r\n",    /* each header ends with CR LF */
    .buffer_size = 2048,
};
esp_websocket_client_handle_t c = esp_websocket_client_init(&cfg);
esp_websocket_register_events(c, WEBSOCKET_EVENT_ANY, ws_handler, NULL);
esp_websocket_client_start(c);
```

## Sending
```c
if (esp_websocket_client_is_connected(c))
    esp_websocket_client_send_text(c, json, strlen(json), pdMS_TO_TICKS(1000));
esp_websocket_client_send_bin(c, buf, len, portMAX_DELAY);
```
Both calls take a timeout in ticks, so avoid a long timeout inside the event handler.
`esp_websocket_client_send_text_partial`, `send_bin_partial` and `send_fin` send fragmented
messages.

## Large messages
A payload larger than `buffer_size` is posted through several DATA events: use
`payload_offset` (offset of this event's data) and `payload_len` (total length) to reassemble,
and check `fin` for the end of a fragmented message.

## Robustness
- Auto-reconnect is on unless `disable_auto_reconnect` is set; the delay is
  `reconnect_timeout_ms`. Resubscribe in CONNECTED, because server state is lost.
- Change headers with `esp_websocket_client_set_headers` (it replaces the old ones; stop the
  client first if it is connected).
- Close cleanly with `esp_websocket_client_close(c, timeout)`; stopping alone closes the TCP
  connection without sending close frames.

## Verify
- [ ] Server restart: client reconnects and resubscribes.
- [ ] A message much larger than the buffer reassembles correctly.
- [ ] TLS fails against a server with an untrusted cert.

## Checked
2026-10-31. Confirmed on the esp_websocket_client documentation: config fields
(`crt_bundle_attach`, `reconnect_timeout_ms`, `network_timeout_ms`, `ping_interval_sec`,
`pingpong_timeout_sec`, `headers`, `buffer_size`, `disable_auto_reconnect`), event data
fields, send/close/set_headers functions and their semantics, default auto-reconnect. Removed:
the `^1.2.0` version pin and the "IDF 5.x" claim, and the thread-safety statement.
Method: documentation only; no commands were run.
