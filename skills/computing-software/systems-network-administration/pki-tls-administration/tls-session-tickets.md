---
id: computing-software.systems-network-administration.pki-tls-administration.tls-session-tickets
name: tls-session-tickets
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [tls-session-tickets, pki-session, tls-session-resumption, session-tickets, ticket-keys, psk, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Understand TLS 1.3 session resumption with NewSessionTicket and PSKs: lifetime limits, forward secrecy and multi-node ticket handling."
sources:
  - https://www.rfc-editor.org/rfc/rfc8446
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session tickets and resumption
Goal: faster repeat connections without weakening forward secrecy. Source: RFC 8446 (TLS 1.3).
- In TLS 1.3 resumption uses a PSK identity (the ticket) derived from the initial handshake (section 2.2). TLS 1.2 and below used session IDs and RFC 5077 tickets; RFC 8446 says both mechanisms are obsoleted in TLS 1.3.
- After the client Finished, the server MAY send a `NewSessionTicket` (section 4.6.1). It may send several tickets, which helps clients opening parallel connections or racing across address families.
- `ticket_lifetime` is in seconds and servers MUST NOT use a value above 604800 (7 days). Zero means discard immediately. Clients MUST NOT cache tickets longer than 7 days, and a server MAY treat a ticket as valid for less than the stated lifetime.
- The `ticket` is an opaque label: either a database lookup key or a self-encrypted and self-authenticated value. `ticket_age_add` is a fresh random 32-bit value per ticket.
- A ticket may only be resumed with a cipher suite that has the same KDF hash as the original connection. A client MUST only resume if the new SNI is valid for the original server certificate, and SHOULD only resume when it matches the original SNI.
- Forward secrecy (section 2.2): PSKs can be combined with (EC)DHE for forward secrecy, or used alone at the cost of forward secrecy for the application data. A client offering resumption SHOULD also send `key_share` so the server can decline and fall back to a full handshake.
- Single-use tickets (section 8.1): if tickets are database keys and the PSKs are deleted when used, resumed connections have forward secrecy. Sharing that database between nodes makes high PSK success rates harder than with self-encrypted tickets; self-encrypted tickets resume without consistent storage.
- Where 0-RTT is allowed, tickets still require consistent storage across servers for anti-replay (section 8.1). The RFC gives no ticket-key rotation interval.
- The server `NewSessionTicket` may carry an `early_data` extension with `max_early_data_size` (see the zero-rtt-early-data skill).
Verify:
- [ ] A second connection from the same client shows resumption in your TLS client or server logs.
- [ ] Ticket key distribution and rotation across nodes is documented and monitored; consult your server's own documentation for the setting names and rotation interval.

## Checked
Confirmed 2026-11-08 against RFC 8446 sections 2.2, 4.6.1 and 8.1. Removed: nginx and HAProxy directives, the daily-rotation recommendation, the Mozilla "intermediate keeps tickets off" claim, the TLS 1.2 key-compromise risk statement and the `openssl s_client -reconnect` commands (none are on the cited page).
Method: docs-only read of cited pages, 2026-11-08
