---
id: computing-software.database-administration.valkey.tls-configuration
name: tls-configuration
category: computing-software
field: database-administration
product: valkey
tags: [tls, ssl, tls-port, mtls, tls-replication, tls-cluster, certificates]
level: practitioner
status: docs-checked
description: "Valkey TLS setup: tls-port, port 0, cert/key/CA files, mTLS and tls-auth-clients-user, auto reload, plus tls-replication, tls-cluster and Sentinel."
sources:
  - https://valkey.io/topics/tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TLS is optional and must be enabled at compile time.

Quick start server: `valkey-server --tls-port 6379 --port 0 --tls-cert-file server.crt --tls-key-file server.key --tls-ca-cert-file ca.crt`. Client: `valkey-cli --tls --cert client.crt --key client.key --cacert ca.crt`.

Ports: `tls-port` listens in addition to `port`, so TLS and plain TCP can coexist; `port 0` disables plain TCP.

Material: `tls-cert-file` and `tls-key-file` (server), `tls-ca-cert-file` or `tls-ca-cert-dir` (trusted CAs), and `tls-client-cert-file` / `tls-client-key-file` when Valkey acts as a TLS client (mTLS identity). `tls-auto-reload-interval` seconds (default 0, disabled) reloads in a background thread. Every load validates that files are non-empty and well formed, certificates match their keys, and dates are valid; any failure aborts the load.

Client auth: by default mTLS is required and the certificate must chain to your CAs; `tls-auth-clients no` disables it. A valid certificate alone does not log a client in as a user; clients still use `AUTH` or `HELLO`. Set `tls-auth-clients-user` to map a certificate field to an ACL user (no match leaves the `default` user); give such users no password, e.g. `ACL SETUSER client-user on allcommands allkeys`.

Other links: replicas need `tls-replication yes`; cluster bus needs `tls-cluster yes`; Sentinel follows `tls-replication` for both outgoing and its own TLS port. Protocol versions and ciphers are in `valkey.conf`. TLS lowers per-instance throughput.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/tls/ (page text read in full): Compile-time option, quick-start commands, tls-port with port 0, cert/key/CA/client file directives, tls-auto-reload-interval default 0, the three validation checks, tls-auth-clients, tls-auth-clients-user and the ACL SETUSER example, tls-replication, tls-cluster, Sentinel behaviour, throughput note.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
