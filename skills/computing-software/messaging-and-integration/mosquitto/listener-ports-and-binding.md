---
id: computing-software.messaging-and-integration.mosquitto.listener-ports-and-binding
name: listener-ports-and-binding
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [listener, ports, bind-address, unix-socket]
level: practitioner
status: docs-checked
description: "Open extra Mosquitto listeners with the listener option, bind them to an address or a Unix socket, and restrict IP family."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define which ports and interfaces the broker accepts connections on.

Syntax: `listener port [bind address/host/unix socket path]`. The option may be given multiple times. If `listener` is used and neither the global `bind_address` nor `port` is set, the implicit default listener is not started.

```
listener 1883 localhost
listener 8883 192.168.1.10
listener 0 /path/to/mosquitto.sock
```

For a Unix domain socket the port must be 0 and the socket path is given as the second argument. For websockets listeners only an IP address may be given as the bind value.

Related per-listener options:
- `bind_interface device` listens only on that interface; useful when an interface has several addresses or the address changes. It takes priority over a bind address and is not available on Windows and AIX.
- `socket_domain ipv4|ipv6` forces one IP family. By default a listener tries all supported families; omit the option for both.
- `listener_allow_anonymous`, `max_connections` and the TLS options also apply per listener.

The old `bind_address` and `port` options (default port 1883) are deprecated in favour of `listener`, and the docs recommend an explicit listener rather than relying on the implicit default one.

None of these options are reloaded on the reload signal, so changing a listener needs a broker restart.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
