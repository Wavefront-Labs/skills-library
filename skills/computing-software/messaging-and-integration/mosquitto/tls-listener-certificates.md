---
id: computing-software.messaging-and-integration.mosquitto.tls-listener-certificates
name: tls-listener-certificates
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [tls, certfile, keyfile, cafile, server-certificate]
level: practitioner
status: docs-checked
description: "Enable certificate based TLS on a Mosquitto listener with certfile, keyfile and cafile, and reload certificates on SIGHUP."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn on TLS for one listener.

The options are listener-level and are placed after the `listener` line:

```
listener 8883
cafile /path/to/ca.crt
certfile /path/to/server.crt
keyfile /path/to/server.key
```

- `certfile` is the path to the PEM encoded server certificate. Together with `keyfile` it must be present to enable certificate based TLS encryption.
- `keyfile` is the path to the PEM encoded server key (when `tls_keyform` is `pem`, the default; if it is `engine` the value is the engine handle).
- `cafile` is a file of PEM encoded CA certificates trusted when checking incoming client certificates.

Both the certificate and the private key are reloaded when Mosquitto receives a SIGHUP signal, which lets you load new certificates before the existing ones expire.

By default a TLS listener behaves like an https web server: the server has a certificate signed by a CA and the client verifies it. The aim is encryption of network traffic.

Unauthenticated encrypted support is provided by using just `certfile` and `keyfile`; add `require_certificate` for client certificates.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Claims unchanged; all match the certfile, keyfile, cafile, tls_keyform and Authentication text.
