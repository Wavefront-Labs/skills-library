---
id: computing-software.cryptography-implementation.protocol-implementation.tls13-certificateverify-and-signature-schemes
name: tls13-certificateverify-and-signature-schemes
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, certificateverify, tls-1-3, signature-schemes, rsa-pss, rfc-8446]
level: advanced
status: docs-checked
description: "Implement TLS 1.3 CertificateVerify: signed content with 64-space prefix and context string, transcript hash, allowed schemes (no PKCS#1 v1.5), and verification failures."
sources: ["https://www.rfc-editor.org/rfc/rfc8446"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS 1.3 CertificateVerify and signature schemes

## Signed content (RFC 8446 4.4.3)
```
0x20 repeated 64 times
|| "TLS 1.3, server CertificateVerify"   (or "TLS 1.3, client CertificateVerify")
|| 0x00
|| Transcript-Hash(Handshake Context, Certificate)
```
The octet-32 prefix, the context string and the 0 separator precede the transcript hash; the context string
separates client and server signatures.

## Schemes
- Allowed for CertificateVerify: `ecdsa_secp256r1_sha256` (0x0403), `ecdsa_secp384r1_sha384` (0x0503),
  `rsa_pss_rsae_*` (RSA key in a normal rsaEncryption certificate), `rsa_pss_pss_*` (certificate with an RSASSA-PSS
  key), `ed25519` (0x0807) and `ed448` (0x0808).
- `rsa_pkcs1_*` (and the SHA-1 legacy values) refer only to signatures in certificates, are not defined for signed
  handshake messages, and may appear in `signature_algorithms` only for TLS 1.2 backward compatibility.
- ECDSA scheme code points fix the curve and hash together, unlike TLS 1.2.

## Verifier checks
1. Scheme was offered in our `signature_algorithms`.
2. Scheme matches the certificate's key type and curve.
3. Signature verifies over the exact transcript hash at that point.
4. Failure sends a `decrypt_error` alert.

## Checked
2026-11-01: signed-content layout, scheme code points, legacy and RSA-PSS wording, and decrypt_error on a failed
signature confirmed against RFC 8446 sections 4.2.3 and 4.4.3. Removed: ML-DSA code points, the OpenSSL `-sigalgs`
debug line and its error string, and the tlsfuzzer test name (not confirmed).
Method: documentation only; no commands were run.
