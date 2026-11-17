---
id: computing-software.cryptography-implementation.protocol-implementation.tls-exporters-and-channel-binding
name: tls-exporters-and-channel-binding
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-1-3, tls-exporter, channel-binding, rfc5705, rfc9266, keying-material-exporter]
level: advanced
status: docs-checked
description: "Derive keys and channel bindings from a TLS session with exporters: RFC 5705/8446 labels and context, tls-exporter binding (RFC 9266), SCRAM-PLUS, and API calls per library."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-7.5", "https://www.rfc-editor.org/rfc/rfc5705", "https://www.rfc-editor.org/rfc/rfc9266", "https://www.rfc-editor.org/rfc/rfc7627", "https://docs.openssl.org/3.0/man3/SSL_export_keying_material/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS exporters and channel binding

An exporter derives secret bytes both peers share, unique to this TLS connection. Use it to
bind an application-layer authentication (password, token, signature) to the channel so a
man-in-the-middle with a different TLS session cannot relay it.

## TLS 1.3 exporter (RFC 8446 7.5)
```
TLS-Exporter(label, context, length) =
  HKDF-Expand-Label(Derive-Secret(exporter_master_secret, label, ""),
                    "exporter", Hash(context_value), length)
```
- Labels must be registered or start with `EXPERIMENTAL`; choose a unique label per use.
- In 1.3, "no context" and "empty context" give the same output; in TLS 1.2 (RFC 5705) they
  differ, so always pass a context explicitly.
- TLS 1.2 exporters are only safe with Extended Master Secret (RFC 7627); without EMS the
  triple-handshake attack lets two sessions share a master secret. Require EMS or TLS 1.3.

## API calls
- OpenSSL: `SSL_export_keying_material(ssl, out, len, label, strlen(label), ctx, ctxlen, 1)`.
- Other stacks: look up the exporter call in your TLS library's reference; not all expose one.

## tls-exporter channel binding (RFC 9266)
For SASL SCRAM-*-PLUS and GSS-API: label `EXPORTER-Channel-Binding`, empty context, 32 bytes.
It replaces `tls-unique` for TLS 1.3, where `tls-unique` is not defined, and is
mandatory to implement if any channel binding is implemented for TLS 1.3. Use the
binding for one authentication exchange per connection, then close it, and never as a secret key.

## Patterns
- **Token binding to channel**: client signs `exporter(label="EXPERIMENTAL-myapp-auth", 32)` with
  its key; server recomputes and verifies. A relayed signature fails on the attacker's session.
- **Deriving app keys**: export a key for an inner protocol instead of running a second key exchange.
- Through TLS-terminating proxies the exporter belongs to the proxy's session; channel binding
  only works end to end.

## Verify
- [ ] Both sides compute identical exporter output in an integration test.
- [ ] TLS 1.2 connections without EMS are refused when exporters are used for security.
- [ ] Labels are unique per purpose and documented.

## Checked

2026-10-31. Confirmed in RFC 8446 7.5 (exporter formula, no context equals empty
context), RFC 5705 (EXPERIMENTAL labels), RFC 7627 (triple handshake, EMS), RFC 9266
(label, zero-length context, 32 bytes, tls-unique replacement, one use per connection)
and the OpenSSL SSL_export_keying_material man page (call signature). Removed: the Go,
rustls, Java, Node and Python API lines and the PostgreSQL, XMPP and IMAP claims.

Method: documentation only; no commands were run.
