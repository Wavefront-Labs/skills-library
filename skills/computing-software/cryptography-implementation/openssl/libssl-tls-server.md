---
id: computing-software.cryptography-implementation.openssl.libssl-tls-server
name: libssl-tls-server
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, libssl, ssl-ctx, libssl-server, certificate-chain, sni-callback, session-tickets, client-authentication, openssl-3, c-api]
level: advanced
status: docs-checked
description: "Set up a TLS server with OpenSSL 3 libssl: loading chain and key, checking they match, protocol floor, ALPN, SNI callback for multiple certs, tickets, and optional client certs."
sources: ["https://docs.openssl.org/3.0/man3/SSL_CTX_use_certificate/", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_tlsext_servername_callback/", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_options/", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_tlsext_ticket_key_cb/", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_alpn_select_cb/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A TLS server with libssl

```c
SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);
if (SSL_CTX_use_certificate_chain_file(ctx, "fullchain.pem") <= 0) goto err; /* leaf then intermediates */
if (SSL_CTX_use_PrivateKey_file(ctx, "key.pem", SSL_FILETYPE_PEM) <= 0) goto err;
if (!SSL_CTX_check_private_key(ctx)) goto err;                 /* key matches leaf */
SSL_CTX_set_options(ctx, SSL_OP_NO_RENEGOTIATION | SSL_OP_CIPHER_SERVER_PREFERENCE);
SSL_CTX_set_alpn_select_cb(ctx, alpn_cb, NULL);                 /* if serving h2/http1.1 */
/* accept loop: */
SSL *ssl = SSL_new(ctx); SSL_set_fd(ssl, client_fd);
if (SSL_accept(ssl) <= 0) { ERR_print_errors_fp(stderr); SSL_free(ssl); continue; }
```

## Certificates

- `SSL_CTX_use_certificate_chain_file` loads a PEM chain that must be sorted leaf first,
  then intermediates, ending at the highest-level CA.
  `SSL_CTX_use_certificate_file` loads only the first certificate in the file (the man page
  NOTES explain why the chain-file call is preferred).
- A new certificate replaces any existing certificate of the same type, and
  `SSL_CTX_check_private_key` checks only the last pair installed for a type, so
  call `SSL_CTX_check_private_key` after each cert/key pair.
- Multiple hostnames on one listener: register
  `SSL_CTX_set_tlsext_servername_callback` and `SSL_set_SSL_CTX(ssl, ctx_for_name)`
  inside it. The man page says the ClientHello callback (`SSL_CTX_set_client_hello_cb`)
  mostly supersedes it, but the servername callback is still needed to acknowledge
  the requested servername.
- Reload certificates on renewal without restart: build a new `SSL_CTX` and
  swap the pointer atomically for new connections.

## Sessions and tickets

By default OpenSSL issues stateless session tickets. In a multi-process or
multi-node deployment, either share ticket keys with
`SSL_CTX_set_tlsext_ticket_key_evp_cb` (rotated keys from a secure store) or
accept lower resumption rates. `SSL_OP_NO_TICKET` stops stateless tickets (TLS 1.3
then sends stateful ones); `SSL_CTX_set_num_tickets` can suppress all TLS 1.3
tickets. Rotate ticket keys often.

## Client certificates (mTLS)

```c
SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL);
SSL_CTX_load_verify_locations(ctx, "client-ca.pem", NULL);
```

After the handshake, authorise from `SSL_get0_peer_certificate(ssl)` (subject/SAN),
not from the mere fact that verification passed.

## Verify

- [ ] `openssl s_client -connect host:port -servername name -showcerts` shows the full chain.
- [ ] `testssl.sh host:port` reports no TLS 1.0/1.1, no weak ciphers.
- [ ] Certificate reload tested without dropping existing connections.

## Checked

2026-10-31. Confirmed against the OpenSSL 3.0 pages SSL_CTX_use_certificate (chain-file ordering, `SSL_CTX_check_private_key`, replacement of same-type certificates), SSL_CTX_set_tlsext_servername_callback (`SSL_set_SSL_CTX`, ClientHello callback), SSL_CTX_set_options (`SSL_OP_NO_RENEGOTIATION`, `SSL_OP_CIPHER_SERVER_PREFERENCE`, `SSL_OP_NO_TICKET`, `SSL_CTX_set_num_tickets`, stateless tickets by default), SSL_CTX_set_tlsext_ticket_key_cb (`SSL_CTX_set_tlsext_ticket_key_evp_cb`), SSL_CTX_set_alpn_select_cb, SSL_CTX_set_verify (`SSL_VERIFY_FAIL_IF_NO_PEER_CERT` in server mode) and SSL_get_peer_certificate (`SSL_get0_peer_certificate`). The local `openssl s_client` help lists `-connect`, `-servername` and `-showcerts`.
Removed: the 3.2 server guide source (page returns 404), the AIA and "most API clients fail" claims, the dual-certificate selection claim, the `SSL_load_client_CA_file` line, the 1.1.1 version note and the forward-secrecy assertion about long-lived ticket keys.
Method: documentation only; no commands were run, apart from reading the local `openssl s_client -help`.
