---
id: computing-software.cryptography-implementation.openssl.quic-client-testing-with-openssl-35
name: quic-client-testing-with-openssl-35
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, openssl-quic, quic, http3, openssl-s-client, alpn]
level: advanced
status: docs-checked
description: "Test QUIC endpoints with OpenSSL's s_client -quic: required ALPN, keylog and qlog debugging, and limits of a handshake-only check."
sources: ["https://docs.openssl.org/3.5/man7/openssl-quic/", "https://docs.openssl.org/3.5/man1/openssl-s_client/", "https://www.rfc-editor.org/rfc/rfc9000"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# QUIC client testing with OpenSSL

OpenSSL 3.2 added QUIC client support (and the `-quic` option of `s_client`); 3.5 added server side support.
`s_client` can open a QUIC connection to inspect the TLS 1.3 handshake carried inside QUIC.

## Commands
```sh
openssl s_client -quic -alpn h3 -connect host:443 -servername host </dev/null
openssl s_client -quic -alpn h3 -connect host:443 -servername host -brief -msg </dev/null
```
- `-alpn` must be given together with `-quic`; HTTP/3 uses `h3`.
- Output shows the negotiated protocol, ciphersuite and the certificate chain as with TCP.

## Debug
- `-keylogfile keys.log` writes TLS secrets that Wireshark can use to decrypt packets.
- qlog tracing (added in OpenSSL 3.3) writes into the directory named by the `QLOGDIR` environment variable (see the openssl-qlog man page for the build and filter setup).
- A firewall dropping UDP on the port is a common failure; test from another network.

## Limits
- `s_client` checks the handshake and certificates, not HTTP/3 semantics or performance; use an HTTP/3 capable client for that.

## Verify
- [ ] The handshake succeeds with the expected certificate over QUIC.

## Checked

2026-11-01. Confirmed in the OpenSSL s_client man page (`-quic` requires `-alpn`; `-brief`, `-keylogfile`), openssl-quic man page (QUIC from 3.2, client and server), CHANGES.md (`-quic` added to s_client in 3.2, qlog in 3.3, server side support in 3.5) and openssl-qlog/openssl-env (`QLOGDIR`). Removed: curl `--http3-only` details, Alt-Svc and `nc` advice, specific output fields.
Method: documentation only; no commands were run.
