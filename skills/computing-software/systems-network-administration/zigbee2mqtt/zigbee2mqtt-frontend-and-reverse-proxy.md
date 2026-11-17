---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-frontend-and-reverse-proxy
name: zigbee2mqtt-frontend-and-reverse-proxy
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, frontend, windfront, auth-token, https, base-url, websocket, unix-socket, reverse-proxy]
level: practitioner
status: docs-checked
description: "Configure the Zigbee2MQTT web frontend: port, host binding, auth_token, HTTPS, subpath base_url, notification filters, the windfront package and running behind a reverse proxy."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/frontend.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT frontend

```yaml
frontend:
    enabled: true
    port: 8080
    host: 127.0.0.1                    # or a unix socket path
    auth_token: '!secret.yaml auth_token'
    ssl_cert: /path/to/fullchain.pem
    ssl_key: /path/to/privkey.pem
    base_url: /zigbee2mqtt
    url: 'https://zigbee2mqtt.example.org'
    package: zigbee2mqtt-windfront
    notification_filter:
        - 'z2m: Failed to ping.*'
    disable_ui_serving: false
```

- Default is all interfaces, IPv4 and IPv6. `host` may be a unix socket path such as `/run/zigbee2mqtt/zigbee2mqtt.sock` to avoid network exposure. In Docker and the Home Assistant add-on do not set `host` unless the address exists inside the container.
- `auth_token` is cleartext, not hashed; keep it in `secret.yaml`. Anyone reaching the frontend has the same control as MQTT.
- HTTPS needs both `ssl_cert` and `ssl_key`; alternatively terminate TLS in Nginx or Apache.
- `base_url` is for serving from a subpath behind a proxy; `url` is currently used for the Home Assistant device configuration link.
- `package` chooses `zigbee2mqtt-frontend` (legacy) or `zigbee2mqtt-windfront` (rewrite, also usable standalone with multiple instances); changing it requires a restart and the feature set differs.
- `notification_filter` takes regexes to hide toast notifications, for example failed pings.
- `disable_ui_serving: true` keeps only the WebSocket if you serve a UI yourself.
- Home Assistant add-on forces port 8099 for Ingress.
- WebKit bug 80362 stops basic auth on WebSockets, which breaks the frontend in Safari and all iOS browsers when a proxy applies HTTP basic auth.

## Checked

2026-11-03. Confirmed against the Frontend page: options and defaults, host binding and unix socket, Docker/add-on host caveat, cleartext auth_token and secret.yaml, ssl_cert plus ssl_key, base_url, url, package values and restart requirement, windfront standalone, notification_filter, disable_ui_serving, add-on port 8099, WebKit bug 80362. Nothing removed.
Method: documentation only; no commands were run.
