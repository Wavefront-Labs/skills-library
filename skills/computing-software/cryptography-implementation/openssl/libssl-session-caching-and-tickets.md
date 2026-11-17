---
id: computing-software.cryptography-implementation.openssl.libssl-session-caching-and-tickets
name: libssl-session-caching-and-tickets
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, ssl-session-cache, libssl, session-resumption, session-tickets, ticket-key-rotation, tls-1-3, openssl]
level: advanced
status: docs-checked
description: "Configure libssl session resumption: server cache modes, session_id_context, TLS 1.3 tickets and SSL_CTX_set_num_tickets, ticket key rotation callback, client reuse."
sources: ["https://docs.openssl.org/master/man3/SSL_CTX_set_session_cache_mode/", "https://docs.openssl.org/master/man3/SSL_CTX_set_tlsext_ticket_key_cb/", "https://docs.openssl.org/master/man3/SSL_CTX_set_num_tickets/", "https://docs.openssl.org/master/man3/SSL_CTX_set_session_id_context/", "https://docs.openssl.org/master/man3/SSL_CTX_set_options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libssl session caching and tickets

## Server
```c
SSL_CTX_set_session_cache_mode(ctx, SSL_SESS_CACHE_SERVER);
SSL_CTX_set_session_id_context(ctx, (const unsigned char *)"orders-api", 10);   /* required with client certs */
SSL_CTX_set_num_tickets(ctx, 2);          /* TLS 1.3 tickets per full handshake (default 2); 0 sends no tickets at all */
SSL_CTX_set_timeout(ctx, 3600);           /* session lifetime in seconds */
```
- If the server has no `session_id_context` and client certificates are used, stored sessions are not reused and a fatal
  error is flagged so the handshake fails. Set it before any resumption can occur (sessions are created early in the handshake).
- Multiple processes or hosts: either share ticket keys (stateless) or use an external session cache
  (`SSL_CTX_sess_set_new_cb/get_cb/remove_cb`).
- `SSL_OP_NO_TICKET` stops stateless tickets: in TLS 1.2 and below no ticket is sent, but in TLS 1.3 a stateful ticket is still
  sent. To suppress all tickets in TLS 1.3 call `SSL_CTX_set_num_tickets(ctx, 0)` (or combine `SSL_OP_NO_TICKET` with
  `SSL_SESS_CACHE_OFF`). After a resumption at most one ticket is issued.

## Ticket key rotation
To control and share ticket keys across processes, install a callback:
```c
SSL_CTX_set_tlsext_ticket_key_evp_cb(ctx, ticket_cb);
/* ticket_cb(ssl, key_name[16], iv, EVP_CIPHER_CTX *ectx, EVP_MAC_CTX *hctx, int enc):
   enc=1: set an arbitrary 16-byte name, a random iv, and initialise ectx (cipher) and hctx (MAC key and digest via
          EVP_MAC_CTX_set_params); return 1
   enc=0: use key_name to find the key and initialise the same contexts; return 1 (ok), 2 (ok, ticket is in a renewal
          period and should be replaced), 0 (could not set up: session continues without resumption), <0 (error) */
```
Keep the current and previous keys so tickets issued just before a rotation still resume.

## Client
```c
SSL_CTX_set_session_cache_mode(cctx, SSL_SESS_CACHE_CLIENT | SSL_SESS_CACHE_NO_INTERNAL_STORE);
SSL_CTX_sess_set_new_cb(cctx, store_session);    /* TLS 1.3 tickets arrive after the handshake */
/* next connection */
SSL_set_session(ssl, saved_session);
/* after handshake */
if (SSL_session_reused(ssl)) { ... }
```
Store sessions per server name and port.

## Verify
- [ ] `openssl s_client -sess_out s.pem` then `-sess_in s.pem` reports the session as reused.
- [ ] Ticket keys rotate and old tickets still resume within the overlap window.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in SSL_CTX_set_num_tickets(3) (default 2, 0 issues no tickets, at most 1 after resumption), SSL_CTX_set_options(3) (`SSL_OP_NO_TICKET` behaviour in TLS 1.2 and 1.3, interaction with `SSL_SESS_CACHE_OFF`), SSL_CTX_set_session_id_context(3), SSL_CTX_set_tlsext_ticket_key_cb(3) (the `_evp_cb` signature, `enc` semantics and the 0, 1, 2 and negative return values), SSL_CTX_set_session_cache_mode(3) flags and `s_client -sess_out/-sess_in`. Fixed the claim that `num_tickets 0` only disables stateless tickets and the invented error text; removed unconfirmed claims about default key rotation, rotation interval and forward secrecy.

Method: documentation only; no commands were run.
