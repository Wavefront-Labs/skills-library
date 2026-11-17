---
id: computing-software.cryptography-implementation.secure-implementation.hardened-asn1-der-parsing
name: hardened-asn1-der-parsing
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, invalid-curve-attack, asn1-parsing, der, x509, parser-hardening]
level: advanced
status: gated
description: "Parse ASN.1/DER from untrusted input safely: strict DER not BER, memory-safe parsers, length and depth limits, re-encode checks, and the CVE patterns behind signature bypasses."
sources: ["https://www.itu.int/rec/T-REC-X.690", "https://pkg.go.dev/golang.org/x/crypto/cryptobyte", "https://boringssl.googlesource.com/boringssl/+/HEAD/include/openssl/bytestring.h", "https://www.rfc-editor.org/rfc/rfc5280", "https://github.com/google/wycheproof"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hardened ASN.1 and DER parsing

Certificates, keys, signatures (ECDSA DER, PKCS#1 DigestInfo), CMS and OCSP are all ASN.1.
Parser bugs here have produced RCEs (OpenSSL, NSS CVE-2021-43527 "BigSig", a heap overflow handling DER-encoded DSA or RSA-PSS signatures), signature forgeries
(Bleichenbacher 2006 e=3 DigestInfo parsing; python-rsa CVE-2016-1494 "BERserk"; node-forge CVE-2022-24771 lenient digest-structure checking) and DoS.

## Rules
1. **Use a maintained, memory-safe parser** - Go `cryptobyte` / `encoding/asn1`, BoringSSL `CBS`,
   Rust `der` / `x509-cert` / `rasn`, pyca `x509`, Bouncy Castle with strict mode (gated: unconfirmed, source is paywalled or blocked). Do not write
   a new TLV parser in C.
2. **Strict DER, never BER**, where a signature covers the encoding: definite lengths only,
   minimal length encoding, no leading zero octets on INTEGERs (except sign), no trailing data,
   SET OF sorted, BOOLEAN true = 0xFF (ITU-T X.690 DER rules, not re-read here (gated: unconfirmed, source is paywalled or blocked)). Reject anything else.
3. **Bounds**: each length checked against the remaining buffer before reading; reject lengths
   over a cap (certificates over 64 KiB, chains over ~10 certs).
4. **Depth**: limit nesting (e.g. 32) to stop stack exhaustion from deeply nested SEQUENCEs.
5. **Integers**: reject negative values where only positive are valid (serials, RSA moduli,
   ECDSA r and s), and bound size (a 100 KB INTEGER is an attack).
6. **OIDs**: reject overlong arc encodings and cap arc count; compare OIDs as decoded values.

## Signature verification specifics
- For PKCS#1 v1.5 signatures, do not parse the decrypted DigestInfo. Re-encode the expected
  `00 01 FF.. 00 || DigestInfo(hash)` and compare the whole block in constant time. Parsing
  with a lenient parser is how e=3 forgeries worked.
- For ECDSA, parse DER strictly or verifiers disagree on what was signed (malleability).
- Verify signatures over the exact received bytes (`tbsCertificate` raw), not over a re-encoding
  of your parsed structure.

## Re-encode check
A cheap guard where your library permits BER: parse, re-encode as DER, and reject if bytes differ.

## Testing
- Wycheproof vectors (ECDSA/RSA signature encodings) catch lenient parsers.
- Fuzz parsers with cargo-fuzz / libFuzzer / go-fuzz using real certs as seeds; run under ASan.
- Differential tests: the same input should parse identically in two libraries.

## Verify
- [ ] Parser is a vetted library with strict DER mode on.
- [ ] Wycheproof encoding tests pass; trailing-garbage and indefinite-length inputs are rejected.
- [ ] Size and depth caps exist and are tested.
