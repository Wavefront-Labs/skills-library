---
id: computing-software.firmware-embedded-development.iot-protocols.mqtt-over-websockets
name: mqtt-over-websockets
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mqtt-over-websockets, mqtt-client-practice, mqtt, websockets, subprotocol, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT over WebSockets: Connect browsers and proxied environments to MQTT."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html
  - https://mosquitto.org/man/mosquitto-conf-5.html
  - https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT over WebSockets

**Goal:** Connect browsers and proxied environments to MQTT.

## Steps
1. Open ws:// or wss:// and offer the WebSocket subprotocol `mqtt`; the server must select `mqtt`, and the URI has no effect on MQTT itself
2. MQTT packets travel in binary data frames (other frame types make the receiver close the connection); one frame can hold several packets or part of one, so do not assume packet and frame boundaries align
3. Mosquitto: a separate `listener <port>` with `protocol websockets`; websockets_origin restricts allowed browser origins
4. EMQX default ports: 8083 for ws and 8084 for wss, with path `/mqtt`, for example `wss://host:8084/mqtt`
5. With the legacy libwebsockets listener only cafile, certfile, keyfile, ciphers and ciphers_tls1.3 are available for TLS in Mosquitto

## Gotcha
A proxy in the path may close idle WebSockets; check its idle timeout and keep the MQTT keep alive interval comfortably shorter.

## Verify
- [ ] Browser client subscribes via wss
- [ ] Idle connection survives the proxy timeout
- [ ] websockets_origin set to the expected site origins

## Checked

2026-11-03. Confirmed in OASIS MQTT 3.1.1 chapter 6 (binary frames, frame alignment, `mqtt` subprotocol offered by client and returned by server), the mosquitto.conf(5) man page (protocol websockets, websockets_origin, reduced TLS options for libwebsockets) and the EMQX WebSocket article (ports 8083 and 8084, `/mqtt` path). Removed: the `mqttv3.1` legacy subprotocol, browser client-certificate and token-in-password claims, the https/wss rule, and proxy Upgrade-header advice (not covered by these pages).
Method: documentation only; no commands were run.
