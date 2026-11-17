---
id: computing-software.messaging-and-integration.mosquitto.client-sessions-and-ids
name: client-sessions-and-ids
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [clean-session, session-expiry, client-id, persistent-session]
level: practitioner
status: docs-checked
description: "Create persistent client sessions with -c, -x, -i and -I in the Mosquitto client tools."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control session persistence and client identity.

- `-c, --disable-clean-session`: disable clean session, enable persistent client mode. The broker keeps subscriptions and queues later QoS 1 and 2 messages while the client is disconnected; on reconnect without cleaning, it receives them. A client id must be set manually with `-i` when using it.
- `-x session-expiry-interval`: sets the v5 session-expiry-interval and makes the client an MQTT v5 client. Values 0-4294967294 are seconds after disconnect; `-1`, `4294967295` or the infinity symbol mean never expire. Default is -1 if `-c` is given, else 0. A never-expiring session needs a client id.
- `-i, --id`: if not given, v3.1.1/v3.1 clients generate `mosq-XXXXXXXXXXXXXXXXXX` (random alphanumerics); v5 clients send a zero length id and the server generates one.
- `-I, --id-prefix`: builds the id from a prefix plus the process id; useful with the broker's `clientid_prefixes`; cannot be combined with `--id`.

```
mosquitto_sub -c -i logger1 -t sensors/# -q 1 -E
```

In mosquitto_sub, `-E` exits as soon as all subscriptions are acknowledged. With `-c` that initialises a durable session on the broker for later use without receiving messages.

Related broker limits: `persistent_client_expiration`, `allow_zero_length_clientid`.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
