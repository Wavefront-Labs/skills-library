---
id: computing-software.cryptography-implementation.openssl.testing-mutual-tls-with-s-client
name: testing-mutual-tls-with-s-client
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, s-client-client-cert, s-client, mutual-tls, mtls, client-certificate, post-handshake-auth, tls-testing]
level: practitioner
status: docs-checked
description: "Test client-certificate TLS with openssl s_client: -cert/-key/-cert_chain, reading acceptable CA names and sigalgs, TLS 1.3 post-handshake auth and failure alerts."
sources: ["https://docs.openssl.org/master/man1/openssl-s_client/", "https://docs.openssl.org/master/man1/openssl-s_server/", "https://github.com/openssl/openssl/blob/master/crypto/err/openssl.txt", "https://www.rfc-editor.org/rfc/rfc8446#section-4.6.2"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Testing mutual TLS with s_client

## Connect with a client certificate
```
openssl s_client -connect api.internal:443 -servername api.internal \
  -cert client.pem -key client.key -cert_chain client-intermediate.pem \
  -CAfile server-ca.pem -verify_return_error </dev/null
```
Key in an HSM or TPM: `-key "pkcs11:token=...;object=client" -provider pkcs11 -provider default`.

## Read what the server asks for
In the output:
- `Acceptable client certificate CA names` - DNs of CAs the server trusts for client auth. Your certificate must chain
  to one of them (clients use this list to pick a certificate).
- `Requested Signature Algorithms` / `Shared Requested Signature Algorithms` - your key must sign with one of them.
- `Client Certificate Types` (TLS 1.2).

## TLS 1.3 post-handshake authentication
For servers that ask for a client certificate after the handshake in TLS 1.3, add `-enable_pha`: it sends the
Post-Handshake Authentication extension (TLS 1.3 only), whether or not `-cert` was given.

## Failure signatures
| Alert / message | Likely cause |
|---|---|
| `alert certificate required` (116) | TLS 1.3 server requires a certificate and you sent none |
| `alert unknown ca` (48) | Your chain does not lead to a CA the server trusts; missing intermediate |
| `alert bad certificate` (42) / `certificate unknown` (46) / `unsupported certificate` (43) | The server rejected the certificate (expired, revoked, unsuitable type or purpose); read the server log, since servers choose different alerts |
| `alert handshake failure` (40) | No shared signature algorithm for your key |
| `alert decrypt error` (51) | Signature by the client key failed (wrong key for the cert) |

## Verify
- [ ] Handshake completes and the application receives the client identity (check server logs).
- [ ] Removing `-cert` produces the expected rejection alert.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-s_client(1): `-cert`, `-key` (file or URI), `-cert_chain`, `-requestCAfile`, `-enable_pha` (TLS 1.3 only, sent whether or not a certificate is given), `-verify_return_error`; the printed headings `Acceptable client certificate CA names`, `Requested Signature Algorithms`, `Shared Requested Signature Algorithms` and `Client Certificate Types` in apps/lib/s_cb.c; and the alert numbers (reason code minus 1000) for certificate required 116, unknown ca 48, bad certificate 42, certificate unknown 46, unsupported certificate 43, handshake failure 40 and decrypt error 51 in crypto/err/openssl.txt. Removed the nginx and Apache references and the version-specific observations about how an OpenSSL server answers.

Method: documentation only; no commands were run.
