---
id: computing-software.messaging-and-integration.mosquitto.pub-retain-qos-repeat
name: pub-retain-qos-repeat
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [retain, qos, repeat, repeat-delay]
level: intro
status: docs-checked
description: "Publish retained messages, set QoS, clear retained values and repeat messages with mosquitto_pub."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control delivery flags on published messages.

- `-q, --qos 0|1|2` (default 0).
- `-r, --retain` retains the message as a last known good value on the broker. Zero length payloads are never retained; a retained zero length payload clears any retained message on the topic.
- `--repeat count` publishes the message multiple times when in a single-message mode (`-m`, `-f` or `-s`). By default each repeat is published as soon as the previous one is delivered.
- `--repeat-delay seconds` waits that long after delivery before the next publish; it need not be an integer. It sets a minimum time between messages, not a guaranteed interval.

```
mosquitto_pub -r -t switches/kitchen_lights/status -m "on"
mosquitto_pub -r -t switches/kitchen_lights/status -n
mosquitto_pub -t sensors/temperature -m 32 --repeat 10 --repeat-delay 0.5
```

The page's own example retains the light status because there may be a long period between switch events.

On the broker side, `retain_available false` disconnects clients that send the retain bit.

mosquitto_sub can remove retained messages in bulk with `--remove-retained`.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Removed check_retain_source (not on the page).

Method: documentation only; no commands were run.
