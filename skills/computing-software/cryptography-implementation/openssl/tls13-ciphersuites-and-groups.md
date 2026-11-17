---
id: computing-software.cryptography-implementation.openssl.tls13-ciphersuites-and-groups
name: tls13-ciphersuites-and-groups
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, cipher-strings, tls13-ciphersuites, supported-groups, x25519mlkem768, ssl-ctx-set-ciphersuites, ssl-ctx-set1-groups-list, tls-1-3, key-share]
level: practitioner
status: docs-checked
description: "Configure TLS 1.3 ciphersuites and key exchange groups in OpenSSL: -ciphersuites vs -cipher, group lists incl. X25519MLKEM768, key share prediction, and server/app config keys."
sources: ["https://docs.openssl.org/master/man1/openssl-ciphers/", "https://docs.openssl.org/master/man3/SSL_CTX_set1_curves/", "https://docs.openssl.org/master/man3/SSL_CONF_cmd/", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://www.rfc-editor.org/rfc/rfc8446#appendix-B.4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 ciphersuites and groups

In TLS 1.3 the "cipher suite" only names the AEAD and hash; key exchange is
negotiated separately as a **group**. OpenSSL configures them with different
calls than TLS 1.2 cipher lists.

## Ciphersuites

OpenSSL's default TLS 1.3 list (from openssl-ciphers(1)) is:

```
TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256
```

Changing the default is rarely necessary; if you do, set it with the TLS 1.3 setting below, not the TLS 1.2 list.

| Where | TLS 1.3 setting | TLS 1.2 setting |
|---|---|---|
| C API | `SSL_CTX_set_ciphersuites` | `SSL_CTX_set_cipher_list` |
| CLI | `-ciphersuites` | `-cipher` |
| openssl.cnf | `Ciphersuites =` | `CipherString =` |
| nginx | `ssl_conf_command Ciphersuites ...` | `ssl_ciphers` |

nginx passes arbitrary OpenSSL configuration commands through `ssl_conf_command`; `ssl_ciphers` takes the TLS 1.2-and-below
cipher list format, and the two OpenSSL lists are combined.

## Groups (key exchange)

```bash
# OpenSSL 3.5+: hybrid post-quantum first, then classical
openssl s_server -groups X25519MLKEM768:X25519:secp256r1:secp384r1 ...
openssl s_client -groups X25519MLKEM768 -connect host:443   # look for the Peer Temp Key / Negotiated TLS1.3 group line
```

C API: `SSL_CTX_set1_groups_list(ctx, "X25519MLKEM768:X25519:P-256")`;
config file: `Groups = ...`. Since OpenSSL 3.5 X25519MLKEM768 is first in the default group list. In the simple
colon-separated form the first group is the sole predicted key share a client sends. The richer syntax uses a `*`
prefix to mark predicted key shares (ignored by servers), `/` to separate group tuples of comparable security, `?` to
ignore a group an implementation lacks, `-` to remove a group and `DEFAULT` for the built-in list.

## Key share and HelloRetryRequest

A TLS 1.3 client sends a group list and key shares for a predicted subset of those groups. A server that selects a group
outside the predicted subset costs an extra round trip (HelloRetryRequest). Choose server preferences so that the groups
clients predict are selected without it.

## Gotchas

- The default list predicts the X25519MLKEM768 key share; the larger ClientHello may no longer fit in one TCP segment and
  firewall software can disrupt the handshake in rare cases. Prepending `?X25519MLKEM768:` (without `*`) drops the
  prediction.
- Listing an unknown group name makes the list fail to parse (`SSL_CTX_set1_groups_list` returns 0) unless the name is
  prefixed with `?`; check the return value.

## Verify

- [ ] `openssl s_client -connect host:443 -tls1_3` shows the expected suite and group.
- [ ] TLS 1.3 restrictions applied via the TLS 1.3 setting, not the 1.2 list.
- [ ] Handshake error rates monitored after group changes.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-ciphers(1) (default TLS 1.3 list `TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256`, combination with the TLS 1.2 list), SSL_CTX_set1_groups(3) (key-share prediction, `*`, `/`, `?`, `-`, `DEFAULT`, the ClientHello size note, return values), SSL_CONF_cmd(3) (X25519MLKEM768 first in the default list from 3.5, the first group as the predicted share), the nginx ngx_http_ssl_module documentation for `ssl_conf_command` and `ssl_ciphers`, and the `Peer Temp Key` / `Negotiated TLS1.3 group` output in apps/lib/s_cb.c. Removed the unchecked statements about the five RFC suites, CCM_8, FIPS and ChaCha20, key-share byte sizes and the claim that nginx `ssl_ciphers` does not restrict TLS 1.3.

Method: documentation only; no commands were run.
