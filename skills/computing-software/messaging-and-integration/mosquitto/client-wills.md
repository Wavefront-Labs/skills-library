---
id: computing-software.messaging-and-integration.mosquitto.client-wills
name: client-wills
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [will, last-will, will-topic, will-retain]
level: practitioner
status: docs-checked
description: "Register a Last Will message from mosquitto_pub or mosquitto_sub with the --will-* options."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have the broker publish a message when the client vanishes.

A will is stored by the broker and sent out if the client disconnects unexpectedly.

Options (identical in mosquitto_pub, mosquitto_sub and mosquitto_rr):
- `--will-topic topic`: the only required one; alone it produces a non-retained, zero length message at QoS 0.
- `--will-payload payload`: the message body; requires `--will-topic`.
- `--will-qos qos`: defaults to 0; requires `--will-topic`.
- `--will-retain`: send the will as a retained message; requires `--will-topic`.

```
mosquitto_sub -t sensors/# --will-topic status/sub1 --will-payload offline --will-retain
```

For MQTT v5 the will can carry properties via `-D WILL identifier value`: content-type, correlation-data, message-expiry-interval, payload-format-indicator, response-topic, user-property and will-delay-interval.

In mosquitto_pub the will options combine with the normal publish options (synopsis: `--will-topic topic [--will-payload payload] [--will-qos qos] [--will-retain]`), and the will is only sent when the client disconnects unexpectedly.

Bridges use the same feature: `notifications true` publishes connection state through the Last Will and Testament mechanism, to `$SYS/broker/connection/<remote_clientid>/state` (1 active, 0 failed).

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
