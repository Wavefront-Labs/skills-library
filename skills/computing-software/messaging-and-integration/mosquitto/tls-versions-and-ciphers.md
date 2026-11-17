---
id: computing-software.messaging-and-integration.mosquitto.tls-versions-and-ciphers
name: tls-versions-and-ciphers
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [tls-version, ciphers, tlsv1-3, ciphersuites]
level: advanced
status: docs-checked
description: "Set the minimum TLS version and cipher lists on a Mosquitto listener with tls_version, ciphers and ciphers_tls1.3."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control which TLS versions and ciphers a listener accepts.

- `tls_version tlsv1.3|tlsv1.2` sets the minimum TLS protocol version for the listener. If unset, TLS v1.3 and v1.2 are allowed. In Mosquitto 1.6.x and earlier this option set the only allowed version rather than the minimum.
- `ciphers cipher:list` is the list of allowed ciphers for TLS v1.2 and earlier only, separated by colons. List what is available with `openssl ciphers`.
- `ciphers_tls1.3 cipher:list` is the list of allowed ciphersuites for TLS v1.3, also colon separated.

```
listener 8883
tls_version tlsv1.2
ciphers_tls1.3 TLS_AES_256_GCM_SHA384
```

For PSK listeners, `ciphers` chooses from the available PSK ciphers, in the same format as the output of `openssl ciphers`.

The legacy libwebsockets-based websockets support offers a reduced TLS feature set, namely `cafile`, `certfile`, `keyfile`, `ciphers` and `ciphers_tls1.3`.

Bridges have their own equivalents: `bridge_tls_version` (default tlsv1.2), `bridge_ciphers` and `bridge_ciphers_tls1.3`; there the remote broker must support the same TLS version.

Clients such as mosquitto_pub use `--tls-version` with tlsv1.3 or tlsv1.2 (default tlsv1.2), which must match the broker.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
