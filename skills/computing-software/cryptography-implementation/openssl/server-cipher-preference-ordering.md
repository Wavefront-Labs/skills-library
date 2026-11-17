---
id: computing-software.cryptography-implementation.openssl.server-cipher-preference-ordering
name: server-cipher-preference-ordering
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, server-cipher-preference, cipher-order, openssl, nginx, chacha20]
level: practitioner
status: docs-checked
description: "Control server cipher preference in OpenSSL-based servers: SSL_OP_SERVER_PREFERENCE, nginx directives, and ChaCha20 prioritisation for mobile clients."
sources: ["https://docs.openssl.org/3.0/man3/SSL_CTX_set_options/", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html#ssl_prefer_server_ciphers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server cipher preference ordering

## Mechanism
When the option is not set, an OpenSSL server follows the client's preferences. With
`SSL_OP_SERVER_PREFERENCE` (older name `SSL_OP_CIPHER_SERVER_PREFERENCE`, discouraged since OpenSSL 3.6) it uses its own order for the
cipher, signature algorithm, TLS 1.2 curve or TLS 1.3 group.

- nginx: `ssl_prefer_server_ciphers on|off`
- C: `SSL_CTX_set_options(ctx, SSL_OP_SERVER_PREFERENCE)`
- Generic config: the `ServerPreference` command of `SSL_CONF_cmd`

Turn it on only when the list contains weaker suites that clients might prefer.

## ChaCha20 prioritisation
`SSL_OP_PRIORITIZE_CHACHA` (added in OpenSSL 1.1.1) works only with server preference set: if ChaCha20-Poly1305 is at
the top of the client's list, the server moves it to the top of its own list. This helps clients without AES hardware
(for example mobile) while other clients keep AES. nginx exposes it as `ssl_conf_command Options PrioritizeChaCha`.

## TLS 1.3
TLS 1.3 suites are set separately (`ssl_conf_command Ciphersuites ...`, `SSL_CTX_set_ciphersuites`);
`SSL_CTX_set_cipher_list` does not affect them.

## Verify
```sh
openssl s_client -connect h:443 -tls1_2 -cipher 'ECDHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256' </dev/null
```
- [ ] The negotiated cipher matches the intended policy (client-first or server-first).

## Checked

2026-11-01. Confirmed in the OpenSSL SSL_CTX_set_options, SSL_CONF_cmd and SSL_CTX_set_cipher_list man pages (server preference semantics, 3.6 rename, `SSL_OP_PRIORITIZE_CHACHA` behaviour and 1.1.1 version, `ServerPreference`, `PrioritizeChaCha`, `Ciphersuites`, cipher list does not affect TLS 1.3) and the nginx ssl module page (`ssl_prefer_server_ciphers`, `ssl_conf_command`). Removed: Apache, HAProxy and Mozilla guidance, which were not checked.
Method: documentation only; no commands were run.
