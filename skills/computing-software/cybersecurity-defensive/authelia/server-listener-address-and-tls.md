---
id: computing-software.cybersecurity-defensive.authelia.server-listener-address-and-tls
name: server-listener-address-and-tls
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, server-address, listener, tls, unix-socket, mutual-tls]
level: practitioner
status: docs-checked
description: "Configure the Authelia main HTTP listener with server.address schemes (tcp, unix, fd), subpaths, TLS key and certificate, and client certificates."
sources:
  - https://www.authelia.com/configuration/miscellaneous/server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia's main listener is set with `server.address`, a URL whose scheme must be `unix`, `fd` or a `tcp` variant. The documented default is `tcp://:9091/`. It can set the host, port and path the listener responds to.

```yaml
server:
  address: 'tcp://127.0.0.1:9091/subpath'
  tls:
    key: '/path/to/server.key'
    certificate: '/path/to/server.crt'
    client_certificates: []
```

Behaviours worth knowing:

- If the path is anything other than `/`, requests are served on both `/` and the configured path. With `tcp://:9091/authelia`, both `/` and `/authelia/` answer.
- `unix:///var/run/authelia.sock` listens on a socket; `fd://3` takes a socket-activated file descriptor, for example from `systemd-socket-activate`.
- Authelia listens in plain text by design, because most deployments secure traffic at a lower layer. Setting both `tls.key` and `tls.certificate` switches it to TLS.
- The key must be PEM (DER base64) in PKCS#8, PKCS#1 or SECG1 form; the certificate must be PEM.
- `client_certificates` is a list of file paths to root or intermediate certificates used to authenticate clients. With no items, mutual TLS is disabled.
- `server.disable_healthcheck: true` stops Authelia checking for `/app/healthcheck.sh` and `/app/.healthcheck.env` at startup and writing to the latter. Use it on Kubernetes when security policies forbid writing to ephemeral storage.
- `asset_path` serves overridden static assets from a directory instead of the embedded filesystem.

The page notes that the Proxy Integration documentation has important notes on this option when integrating with a proxy.

Check: start Authelia and confirm the listening log line shows the expected address and TLS mode.

## Checked

2026-11-08. Read the full Authelia Server page. Corrected the default address to tcp://:9091/ (the draft said tcp://:/). Confirmed address schemes, subpath behaviour, unix and fd examples, TLS key and certificate formats, client_certificates and mutual TLS, disable_healthcheck and asset_path. Removed the unsourced proxy-forwarding remark.

Method: documentation only; no commands were run.
