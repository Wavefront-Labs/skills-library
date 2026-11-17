---
id: computing-software.messaging-and-integration.mosquitto.bridge-tls-options
name: bridge-tls-options
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [bridge-cafile, bridge-capath, bridge-certfile, bridge-insecure]
level: advanced
status: docs-checked
description: "Secure a bridge with bridge_cafile, bridge_certfile and bridge_keyfile or PSK, and trust OS certificates."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure TLS for a bridge client connection.

At least one of `bridge_cafile`, `bridge_capath` or `bridge_tls_use_os_certs` must be provided to allow TLS.

```
bridge_cafile /path/to/ca.crt
bridge_certfile /path/to/bridge.crt
bridge_keyfile /path/to/bridge.key
```

- `bridge_cafile`: PEM CA certificates that signed the remote broker's certificate.
- `bridge_capath`: a directory of PEM CAs; files must end in `.crt` and `openssl rehash <path>` must be run after each change.
- `bridge_certfile` and `bridge_keyfile`: the client certificate and private key, if the remote broker requires them.
- `bridge_tls_use_os_certs true`: trust the default certificates provided by openssl (typically a large number). Default false.
- `bridge_insecure true`: disable verification that the remote certificate hostname matches the address connected to. The docs say it should always be false in production, since otherwise a third party could impersonate the server.
- `bridge_identity` and `bridge_psk` provide PSK instead (hex key, no 0x); only one of certificate and PSK on one bridge.
- `bridge_tls_version` tlsv1.3 or tlsv1.2 (default tlsv1.2), `bridge_ciphers`, `bridge_ciphers_tls1.3`.
- `bridge_require_ocsp true` requires OCSP on the connection.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
