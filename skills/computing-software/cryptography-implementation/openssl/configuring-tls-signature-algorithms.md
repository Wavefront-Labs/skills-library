---
id: computing-software.cryptography-implementation.openssl.configuring-tls-signature-algorithms
name: configuring-tls-signature-algorithms
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, sigalgs, signature-algorithms, openssl, tls-1-3, rsa-pss, ecdsa, ed25519, hsm, handshake-failure]
level: advanced
status: docs-checked
description: "Configure TLS signature algorithm lists in OpenSSL (-sigalgs, SignatureAlgorithms, SSL_CTX_set1_sigalgs_list) and debug no-shared-signature failures with HSM keys."
sources: ["https://docs.openssl.org/master/man3/SSL_CTX_set1_sigalgs/", "https://docs.openssl.org/master/man3/SSL_CONF_cmd/", "https://www.rfc-editor.org/rfc/rfc8446#section-4.2.3", "https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#tls-signaturescheme"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuring TLS signature algorithms

`signature_algorithms` tells the peer which schemes you accept for CertificateVerify (and, via
`signature_algorithms_cert`, for certificate signatures).

## Setting lists
```c
SSL_CTX_set1_sigalgs_list(ctx, "ecdsa_secp256r1_sha256:rsa_pss_rsae_sha256:rsa_pss_rsae_sha384:ed25519");
SSL_CTX_set1_client_sigalgs_list(ctx, "...");   /* what a server accepts from client certificates */
```
CLI: `openssl s_client -sigalgs "ecdsa_secp256r1_sha256:ed25519" ...` (and `-client_sigalgs`); config keys `SignatureAlgorithms` and `ClientSignatureAlgorithms`.
Two syntaxes: TLS 1.3 scheme names by their IETF names (`ecdsa_secp256r1_sha256`, `ed25519`, `rsa_pss_pss_sha256`; the
`_list` APIs accept them) or `ALGORITHM+HASH` pairs (`ECDSA+SHA256`, `RSA-PSS+SHA256`). Providers can add further schemes
via the TLS-SIGALG capability. If no list is set, everything the loaded providers support is permitted.

## Rules in TLS 1.3
- Entries that specify PKCS#1 v1.5 signatures (`RSA` as the algorithm, or `rsa_pkcs1_*`) are ignored in TLS 1.3 and are
  never negotiated, so an RSA key needs an RSA-PSS scheme there.
- ECDSA schemes are bound to a curve (`ecdsa_secp256r1_sha256` needs a P-256 key).

## Diagnosing "no shared signature algorithms" / handshake_failure
1. `openssl s_client -trace` (verbose protocol-message trace) and compare the ClientHello `signature_algorithms` list with your key type.
2. Common causes (check each against the trace):
   - Your configured list excludes every scheme the peer offers, or the peer's list excludes the scheme your key needs.
   - An RSA key that only supports PKCS#1 v1.5 signing (for example behind a token) cannot be used in TLS 1.3, since
     those schemes are ignored there.
3. Client certificates: the server's `CertificateRequest` sigalgs must include your client key's scheme.

## Verify
- [ ] The trace shows the signature scheme you expect (for example RSA-PSS or ECDSA) in the handshake messages.
- [ ] Interop tests pass with the strictest client in your fleet.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in SSL_CONF_cmd(3) and SSL_CTX_set1_sigalgs(3): `-sigalgs`/`-client_sigalgs` syntax, scheme-name and `ALGORITHM+HASH` forms, default when unset, PKCS#1 v1.5 entries ignored in TLS 1.3, `SignatureAlgorithms` config key, `s_client -trace`. Removed the unconfirmed `mldsa65` scheme name and the HSM, SHA-1 and curve-mismatch causes.

Method: documentation only; no commands were run.
