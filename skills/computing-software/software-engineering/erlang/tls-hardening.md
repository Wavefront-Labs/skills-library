---
id: computing-software.software-engineering.erlang.tls-hardening
name: tls-hardening
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-security, tls-hardening]
level: sme
status: draft
description: "Hardening Erlang TLS: verify_peer, fail_if_no_peer_cert, TLS versions, TLS distribution with inet_tls and epmd exposure."
sources:
  - https://www.erlang.org/doc/apps/crypto/
  - https://www.erlang.org/doc/apps/ssl/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TLS server and distribution hardening
**Goal:** reduce the attack surface of listeners and clusters.

```erlang
ServerOpts = [{certfile, "cert.pem"}, {keyfile, "key.pem"},
              {versions, ['tlsv1.3', 'tlsv1.2']},
              {verify, verify_peer}, {fail_if_no_peer_cert, true}, {cacertfile, "ca.pem"}]
```
- Mutual TLS: set `verify_peer` and `fail_if_no_peer_cert` on the server and provide the CA that signs client certs.
- TLS for distribution: start with `-proto_dist inet_tls -ssl_dist_optfile <file>`; the optfile holds server and client option terms (file format in the "Using TLS for Erlang Distribution" guide).
- Bind epmd and the dist listener to private interfaces only; firewall 4369 and the dist port range.
- A leaked cookie equals remote code execution on that node, so treat it as a root credential and rotate it.
- Do not run `observer`, shells or `rpc` endpoints on public interfaces.

## Gotchas
- Default cookie file permissions matter; mode 400 owned by the service user.

## Self-check
Scan the host from outside: only the intended ports should answer.
