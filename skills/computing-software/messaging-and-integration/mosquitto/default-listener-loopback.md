---
id: computing-software.messaging-and-integration.mosquitto.default-listener-loopback
name: default-listener-loopback
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [default-listener, loopback, port-1883, config-file]
level: intro
status: docs-checked
description: "Understand which interface and port Mosquitto 2.x binds without a config, and how -p and listener definitions interact."
sources:
  - https://mosquitto.org/man/mosquitto-8.html
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what the broker exposes when started with little or no configuration.

If `mosquitto` is started without `-c`, it listens on port 1883 bound to the loopback interface and uses the defaults documented in mosquitto.conf(5).

From version 2.0 onwards, listeners defined with `-p` are bound to the loopback interface only, so they can be reached only from the local machine. In 1.6.x and earlier, the listener from `-p` (or the default port 1883) was bound to all interfaces and could be combined with `-c`.

If both `-p` and a listener in a configuration file are used, the `-p` options are ignored. `-p` may be given up to 10 times to open multiple sockets on different ports.

Anonymous access follows the same safety rule: `allow_anonymous` defaults to false, unless no listeners are defined in the configuration file, in which case it is set to true but connections are only allowed from the local machine. In 1.6.x and earlier the option defaulted to true unless another security option was set.

To accept remote clients, define an explicit `listener port` in the configuration file and configure authentication for it.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
