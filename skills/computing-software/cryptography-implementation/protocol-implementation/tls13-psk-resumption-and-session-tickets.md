---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-psk-resumption-and-session-tickets
name: tls13-psk-resumption-and-session-tickets
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, tls-1-3, psk-resumption, session-tickets, newsessionticket, psk-dhe-ke]
level: advanced
status: docs-checked
description: "Implement TLS 1.3 PSK resumption: NewSessionTicket contents, psk_dhe_ke vs psk_ke, binders, ticket lifetime and age obfuscation, single-use tickets and privacy."
sources: ["https://www.rfc-editor.org/rfc/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 PSK resumption and session tickets

## Flow
1. After a full handshake the server sends `NewSessionTicket` (post-handshake): `ticket_lifetime`
   (servers must not exceed 604800 seconds, 7 days), `ticket_age_add` (random 32-bit), `ticket_nonce`, opaque `ticket`, extensions
   (`early_data` max size).
2. Resumption PSK = `HKDF-Expand-Label(resumption_master_secret, "resumption", ticket_nonce, Hash.length)`.
3. Client sends `pre_shared_key` (identities + binders, must be the last extension) and
   `psk_key_exchange_modes`.
4. Server validates the binder, selects an identity, and the PSK seeds the Early Secret.

## psk_dhe_ke versus psk_ke
- `psk_dhe_ke`: PSK plus a fresh (EC)DHE. Forward secrecy if the ticket key later leaks. Use this.
- `psk_ke`: PSK only, no `key_share`. No forward secrecy: a stolen ticket-encryption key exposes every
  session resumed with it. Do not offer it unless you must.

## Binders
Binder = HMAC over the partial ClientHello transcript using `binder_key` from the PSK. It
proves the client holds the PSK and binds it to this ClientHello. Servers must verify the
binder for the selected identity before using the PSK; on failure abort with `decrypt_error`
(do not fall back silently).

## Ticket age
Client sends `obfuscated_ticket_age = (age_ms + ticket_age_add) mod 2^32`. Clients must not use tickets older
than `ticket_lifetime`. The server recovers the age by subtracting `ticket_age_add`; the age check also
narrows 0-RTT replay windows.

## Server-side ticket design
- Stateless tickets: AEAD-encrypt the session state under a rotating ticket key (see session
  ticket key rotation). Include creation time and the original SNI/ALPN; reject resumption with a
  different SNI.
- Stateful (session cache by ID): enables true single use, revocation, and works across key
  rotation, at the cost of shared storage.
- Re-check authorisation on resumption: the resumed session inherits the original client cert;
  if certs can be revoked, cap ticket lifetime accordingly.

## Client-side
- Use each ticket once (RFC 8446 C.4: clients SHOULD NOT reuse a ticket) so passive observers cannot
  link connections; servers should issue new tickets with every connection and enough of them for the
  connections a client may open.
- Scope cached tickets by server name and port, and drop them on certificate-validation policy
  changes.

## Verify
- [ ] Resumed handshakes use `psk_dhe_ke` (the `psk_key_exchange_modes` extension and a `key_share` in the ServerHello).
- [ ] Tampered binders and expired tickets cause full handshakes or `decrypt_error`, never acceptance.
- [ ] Ticket keys rotate and resumption still works across a fleet.

## Checked
Date: 2026-10-31. Confirmed in RFC 8446 (4.2.9, 4.2.11, 4.2.11.1, 4.2.11.2, 4.6.1, appendix C.4, alert
decrypt_error): 604800-second ticket cap, resumption PSK derivation, pre_shared_key last, psk_ke without key_share,
obfuscated_ticket_age formula, binder construction and abort on bad binder, client ticket reuse guidance.
Removed: OpenSSL SSL_OP_ALLOW_NO_DHE_KEX default claim and the "servers typically send 2 tickets" figure (not
confirmed). Corrected: the client, not the server, must not use over-age tickets.
Method: documentation only; no commands were run.
