---
id: computing-software.networking-hardware-and-wireless.haproxy.backend-tls-verification-and-sni
name: backend-tls-verification-and-sni
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, backend-tls, verifyhost, ssl-verify, crt-server-client-cert, sni-backend]
level: practitioner
status: docs-checked
description: "Re-encrypt to HAProxy backends with ssl, verify required, ca-file, verifyhost and sni, plus client certificates for mutual TLS to servers."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backend tls verification and sni
Encrypting the server side needs `ssl` on the `server` line. With OpenSSL support, `verify` on a server line defaults to `required` unless `ssl-server-verify none` is in the global section (or the `-dV` command-line option is used). `verify none` disables certificate checking and leaves the link open to trivial man-in-the-middle attacks.

```
global
    ssl-server-verify required
    ca-base /etc/ssl/certs
backend be_secure
    default-server ssl verify required ca-file ca-certificates.crt
    server app1 app1.internal:8443 check sni str(app1.internal) verifyhost app1.internal
    server app2 10.0.0.12:8443 check ssl crt /etc/haproxy/client.pem ca-file /etc/haproxy/internal-ca.pem verify required
```
The certificate is checked against CAs from `ca-file` (and optional `crl-file`), after its subject and subjectAlternateNames are matched to the name from `sni`, or if none, the static name from `verifyhost`. If neither is set, the certificate names are ignored, so without SNI always set `verifyhost`. `verifyhost` only takes effect with `verify required`, may contain wildcards in the certificate, and is also used for health checks. `sni <expression>` sets the SNI sent to the server; for HTTPS use `sni req.hdr(host)` so SNI matches the Host header (do not use `ssl_fc_sni` for HTTPS; it is meant for bridged TCP/SSL). `crt` on a server line presents a client certificate for mutual TLS. `ssl-min-ver` and `alpn` are also server-line settings.

`check-ssl` makes health checks use TLS and `check-sni <sni>` sets their SNI; without `check-ssl` checks go over plain TCP/HTTP even when traffic is `ssl`.

On verification failure the handshake is aborted.

## Checked
2026-11-03. Confirmed against configuration.html: global `ssl-server-verify` and `ca-base`, server keywords `verify`, `verifyhost`, `sni`, `check-ssl`, `check-sni`, `ca-file`, `crt`, `ssl-min-ver`, `alpn`. Fixed: the default for `verify` is `required` (the skill said no check without `ca-file`, with a "confirm" marker). Removed: `force-tlsv12` claim, the `openssl s_client` verify line and `L6OK` hint, and the garbled IP-with-verifyhost gotcha (replaced with the documented name-matching rule).
Method: documentation only; no commands were run.
