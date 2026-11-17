---
id: computing-software.messaging-and-integration.nats.websocket-support
name: websocket-support
category: computing-software
field: messaging-and-integration
product: nats
tags: [websocket, websocket-config, allowed-connection-types, no-tls, browser-clients]
level: practitioner
status: docs-checked
description: "Enable the NATS websocket block, restrict users to WEBSOCKET connections, run it in Docker with no_tls, and allowed auth modes."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/websocket/websocket_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: allow browser and WebSocket clients to connect to nats-server.

Config block:
```
websocket {
  port: 443
  tls {
    cert_file: "/path/to/cert.pem"
    key_file: "/path/to/key.pem"
  }
}
```
Authentication options over WebSocket: username/password, token, NKeys, client certificates and JWTs (see the nats.ws client docs for usage).

Restricting connection types: add `allowed_connection_types` (aliases `connection_types`, `clients`) to a user, for example `{user: bar, password: <secret>, allowed_connection_types: ["WEBSOCKET"]}` so bar only works over WebSocket, or `["STANDARD", "WEBSOCKET"]` for both. Valid values: `STANDARD`, `WEBSOCKET`, `LEAFNODE`, `MQTT`. If the field is absent every connection type is allowed (default), so a user with no restriction can also connect through the WebSocket port.

Leaf nodes can use the WebSocket port instead of the leafnode port; see the leaf node configuration page.

Docker: WebSocket is not enabled by default in the container image, so supply a config file with at least:
```
websocket { port: 8080  no_tls: true }
```
and run it mapping the port, for example `docker run -it --rm -v /tmp:/container -p 8080:8080 nats -c /container/nats.conf`. `no_tls` is for local testing only; use TLS for real deployments.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
