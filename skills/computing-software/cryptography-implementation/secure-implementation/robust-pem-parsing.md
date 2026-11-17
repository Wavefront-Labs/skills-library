---
id: computing-software.cryptography-implementation.secure-implementation.robust-pem-parsing
name: robust-pem-parsing
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, pem-parsing, pem, rfc-7468, input-validation, private-key-formats, certificate-chains, parsing]
level: practitioner
status: gated
description: "Parse PEM safely per RFC 7468: labels and key formats, multiple blocks and chains, legacy encrypted headers, strict base64, size limits, and preferring library parsers."
sources: ["https://www.rfc-editor.org/rfc/rfc7468", "https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/", "https://docs.openssl.org/3.0/man3/PEM_read_bio_PrivateKey/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robust PEM parsing

## Labels and what they contain
| Label | Content |
|---|---|
| `CERTIFICATE` | X.509 certificate (DER) |
| `PRIVATE KEY` | PKCS#8 unencrypted (any algorithm) |
| `ENCRYPTED PRIVATE KEY` | PKCS#8 encrypted (PBES2) |
| `RSA PRIVATE KEY` (not an RFC 7468 label; legacy OpenSSL) | PKCS#1 RSA key; may carry legacy `Proc-Type: 4,ENCRYPTED` / `DEK-Info` headers |
| `EC PRIVATE KEY` | SEC 1 EC key |
| `PUBLIC KEY` | SubjectPublicKeyInfo |
| `CERTIFICATE REQUEST` | PKCS#10 CSR |
| `X509 CRL` | CRL |

## Rules (RFC 7468)
- Text before `-----BEGIN` and after `-----END` is allowed (explanatory text); parsers MUST NOT malfunction on it, so skip it.
- Generators MUST put the same label on BEGIN and END; parsers MAY disregard a mismatch, so decide yourself. pyca rejects a mismatch (run).
- Base64 body: the RFC says parsers SHOULD ignore whitespace and other non-base64 characters, and strict generators emit exactly 64-character lines. For untrusted input, still reject stray non-base64 characters: pyca rejected a body containing `!!!!` (run).
- Files may contain multiple blocks: certificate chains, key plus certificate. Decide explicitly what you accept.

## Common bugs
- Reading only the first certificate when a chain is expected (missing intermediates later).
- Accepting a private key where a public key was expected (and logging it).
- Unbounded input: a multi-megabyte "PEM" upload consumes memory; cap size (a few hundred KB for chains).
- Legacy encrypted PEM (`DEK-Info: DES-EDE3-CBC`) uses MD5-based key derivation; treat as weakly protected and
  convert to PKCS#8 with PBES2.

## Use library parsers
- pyca: `x509.load_pem_x509_certificates(data)` (all certs; `load_pem_x509_certificate` silently returns only the first of a chain, confirmed by run; both reject a PRIVATE KEY block), `serialization.load_pem_private_key(data, password)`.
- Go: loop `pem.Decode(rest)` until nil, check `block.Type`, ignore or reject unexpected types.
- OpenSSL: `PEM_read_bio_X509` in a loop; `OSSL_DECODER` for keys of any format.
- Java: no built-in PEM parser; Bouncy Castle `PEMParser` (gated: unconfirmed, source is paywalled or blocked) (Java not run here).

## Verify
- [ ] Parser tests: chain of 3, trailing text, wrong label, mismatched END, invalid base64, 10 MB input.
- [ ] Unexpected block types are rejected with a clear error, not ignored silently.
