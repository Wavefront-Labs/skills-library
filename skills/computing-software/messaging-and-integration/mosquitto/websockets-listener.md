---
id: computing-software.messaging-and-integration.mosquitto.websockets-listener
name: websockets-listener
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [websockets, protocol, websockets-origin, ws]
level: practitioner
status: docs-checked
description: "Serve MQTT over WebSockets with protocol websockets and restrict browser origins with websockets_origin."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let browser clients connect over WebSockets.

Set the listener protocol:

```
listener 9001
protocol websockets
websockets_origin http://example.com:8080
```

`protocol value` can be `mqtt` (the default), `websockets` (MQTT tunnelled over WebSockets) or `http_api`.

- `websockets_origin` is compared to the http Origin header when a connection upgrades to WebSockets; only matching origins are allowed. Use the exact string the browser sends. It can be specified multiple times per listener. If not set, any origin is allowed. Requires libwebsockets 3.1.0 or later.
- `websockets_headers_size size` (the same option as `packet_buffer_size`) sets the buffer for reading the initial header; default 4096. Increase it if passing large header data such as cookies.
- `websockets_log_level level` is an integer mask for libwebsockets lws_log_levels (default 0); it is global, and `log_type websockets` must be enabled.

With the legacy libwebsockets support only a reduced TLS option set is available (`cafile`, `certfile`, `keyfile`, `ciphers`, `ciphers_tls1.3`), and `capath` is not supported. Legacy websockets support is not the default, and `http_dir` for websockets listeners will be removed in version 3.0. Websockets listeners can bind only to an IP address, not a hostname.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
