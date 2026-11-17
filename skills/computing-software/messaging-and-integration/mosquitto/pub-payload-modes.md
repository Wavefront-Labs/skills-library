---
id: computing-software.messaging-and-integration.mosquitto.pub-payload-modes
name: pub-payload-modes
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-pub, payload, stdin, null-message]
level: intro
status: docs-checked
description: "Publish with mosquitto_pub using exactly one payload mode: -m, -f, -s, -l or -n."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send a message from the command line.

`mosquitto_pub [options] -t topic {payload-options}`. It is a simple MQTT v5/3.1.1 client that publishes a single message and exits. Exactly one payload option is used:

- `-m, --message`: a single message from the command line.
- `-f, --file`: send the contents of a file as the message.
- `-s, --stdin-file`: read the entire stdin as one message.
- `-l, --stdin-line`: read stdin line by line, each line a separate message.
- `-n, --null-message`: send a zero length message.

Examples from the page:
```
mosquitto_pub -t sensors/temperature -m 32 -q 1
mosquitto_pub -t my/topic -f ./data
mosquitto_pub -t my/topic -s < ./data
read_cc128.pl | mosquitto_pub -t sensors/cc128 -l
mosquitto_pub -t zigbee2mqtt/power-microwave/set -m '{"state":"ON"}'
```

Defaults: host localhost, port 1883 (8883 for TLS), QoS 0, MQTT protocol 3.1.1 (`-V` accepts 5, 311, 31), keepalive 60 seconds (`-k`).

`-d` enables debug messages and `--quiet` suppresses runtime errors (not invalid-input errors).

Other connection helpers: `-A` binds to a local address, `--nodelay` disables Nagle's algorithm, `-S` uses SRV lookups of `_mqtt._tcp.<host>`, `--ws` connects over WebSockets, and `--unix` connects over a Unix domain socket instead of `-h`/`-L`.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
