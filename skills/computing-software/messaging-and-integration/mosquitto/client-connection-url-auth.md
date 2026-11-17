---
id: computing-software.messaging-and-integration.mosquitto.client-connection-url-auth
name: client-connection-url-auth
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-pub, url, username, password, connection]
level: practitioner
status: docs-checked
description: "Connect mosquitto_pub and mosquitto_sub by host, port, unix socket or one -L URL, with credentials and SRV lookup."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: specify where and as whom a client connects.

Options common to the client tools:
- `-h, --host` (default localhost), `-p, --port` (default 1883, or 8883 for TLS), `--unix socket path`, `-A` bind address, `-S` SRV lookup.
- `-u, --username` and `-P, --pw`. A password without a username is invalid with MQTT v3.1/v3.1.1.
- `-L, --url` sets user, password, host, port and topic at once:

```
mqtt(s)://[username[:password]@]host[:port]/topic
ws(s)://[username[:password]@]host[:port]/path
```

Default ports by scheme: `mqtt://` 1883, `mqtts://` 8883, `ws://` 80, `wss://` 443.

```
mosquitto_pub -L mqtts://user:pass@broker.example.com/sensors/temp -m 21
```

- `--proxy socks5h://[username[:password]@]host[:port]` connects via a SOCKS5 proxy; `socks5h` means the proxy resolves hostnames. The port defaults to 1080, and %25, %3A and %40 in the credentials are URL-decoded to %, : and @. IPv6 hosts need square brackets and the URL may need quoting in the shell.
- `--ws` uses WebSockets, `--nodelay` disables Nagle's algorithm.

Putting credentials in a client config file (below) avoids showing them on the command line.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
