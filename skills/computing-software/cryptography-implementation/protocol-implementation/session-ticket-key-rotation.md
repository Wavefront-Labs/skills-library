---
id: computing-software.cryptography-implementation.protocol-implementation.session-ticket-key-rotation
name: session-ticket-key-rotation
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-configuration, session-ticket-keys, session-resumption, forward-secrecy, ssl-session-ticket-key, stek, load-balancer]
level: advanced
status: docs-checked
description: "Rotate TLS session ticket encryption keys (STEKs) across a fleet: why static ticket keys break forward secrecy, rotation, nginx key files, and disabling tickets."
sources: ["https://datatracker.ietf.org/doc/html/rfc8446", "https://datatracker.ietf.org/doc/html/rfc5077", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session ticket key rotation

TLS session tickets let clients resume without a full handshake: the server
encrypts session state with a session ticket encryption key (STEK) and hands
it to the client. Anyone with the STEK can decrypt ticket contents, which
include the resumption secret. In TLS 1.2, that means **all traffic of
resumed sessions** (and, with RFC 5077 tickets, often the original session)
can be decrypted later - static STEKs silently cancel forward secrecy.
TLS 1.3 resumption with `psk_dhe_ke` mixes in fresh ECDHE, limiting the damage,
but 0-RTT data and `psk_ke`-only resumption still depend on the STEK.

## Policy

- Rotate STEKs on a fixed schedule; keep the previous key for decryption
  only, so tickets issued just before rotation still resume.
- Ticket lifetime should not exceed the rotation window.
- Generate keys from a CSPRNG, distribute over an authenticated channel, never in images or config repos.

## Single server

nginx uses its `ssl_session_cache shared:...` zone to automatically generate, store and periodically
rotate ticket keys (since 1.23.2) unless you set `ssl_session_ticket_key` explicitly. Provide rotated key files when a fleet must share keys.

## Fleet behind a load balancer

Without a shared STEK, clients landing on another node cannot resume
(acceptable, just slower). With a shared STEK, rotate it centrally:

```nginx
ssl_session_tickets on;
ssl_session_ticket_key /run/tls/ticket.current;   # first key encrypts new tickets
ssl_session_ticket_key /run/tls/ticket.prev;      # older key, still accepted
```

```bash
openssl rand 80 > /run/tls/ticket.new     # nginx file must hold 80 or 48 bytes of random data
# rotate: prev <- current, current <- new, then reload on all nodes
```

## Or disable

If you cannot rotate safely, set `ssl_session_tickets off` and accept the cost of full handshakes or cache-based resumption.

## Verify

- [ ] Ticket key age monitored; rotation job runs on all nodes.
- [ ] Resumption works before rotation, and old tickets stop working once their key is dropped.
- [ ] STEK files are access-restricted and absent from backups.

## Checked
2026-11-01. Confirmed against the nginx ssl module page (first ssl_session_ticket_key encrypts; 80 or 48 byte key file; automatic key rotation from the shared cache since 1.23.2) and RFC 8446 (psk_ke and psk_dhe_ke modes; 0-RTT replay). Removed: daily rotation figure, HAProxy/Go/BoringSSL APIs, OpenSSL per-process key claim, tmpfs 0600, s_client resumption commands, ECDSA claim.
Method: documentation only; no commands were run.
