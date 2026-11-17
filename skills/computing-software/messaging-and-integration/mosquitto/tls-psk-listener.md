---
id: computing-software.messaging-and-integration.mosquitto.tls-psk-listener
name: tls-psk-listener
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [psk, psk-hint, psk-file, pre-shared-key]
level: advanced
status: docs-checked
description: "Enable TLS-PSK on a listener with psk_hint and psk_file and optionally use the PSK identity as the username."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate clients with pre-shared keys instead of certificates.

- `psk_hint hint` enables pre-shared-key support for the listener and also acts as its identifier. The hint is a free-form string sent to clients.
- `psk_file file path` defines the keys. Each line is `identity:key`, where the key is a hexadecimal string with no leading `0x`. The listener must have PSK enabled.

```
listener 8884
psk_hint broker1
psk_file /path/to/psk.txt
```

A client must provide a valid identity and key before any MQTT communication.

`use_identity_as_username true` makes the PSK identity the username for access control. The username is then checked as normal, so `password_file` or another authentication means must be used, and no password is used. If false, the client may still authenticate with MQTT username and password when `password_file` is set.

The `psk_file` is reloaded on the reload signal: identity and key data is freed and reloaded, and connected clients are not affected. With `per_listener_settings` true it applies to the current listener.

Both certificate and PSK encryption are configured per listener. A bridge can use `bridge_identity` and `bridge_psk` (key in hex, no 0x), but only one of certificate and PSK on one bridge. PSK listeners also accept a `ciphers` list chosen from the available PSK ciphers, and `tls_version` as the minimum version.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported client tool flags; added bridge_psk format, PSK ciphers and tls_version from the page.
