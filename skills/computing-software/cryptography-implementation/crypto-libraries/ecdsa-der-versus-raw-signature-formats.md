---
id: computing-software.cryptography-implementation.crypto-libraries.ecdsa-der-versus-raw-signature-formats
name: ecdsa-der-versus-raw-signature-formats
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, interoperability, ecdsa-signature-format, ecdsa, der, ieee-p1363, jws]
level: practitioner
status: verified
description: "Convert ECDSA signatures between ASN.1 DER and raw r||s (IEEE P1363): which APIs emit which, fixed-width padding, JWS ES256 and KMS gotchas, and strict parsing."
sources: ["https://www.rfc-editor.org/rfc/rfc3279#section-2.2.3", "https://www.rfc-editor.org/rfc/rfc7518#section-3.4", "https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/sign", "https://nodejs.org/api/crypto.html#cryptosignalgorithm-data-key-callback", "https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ECDSA DER versus raw r||s signatures

An ECDSA signature is two integers, r and s. Two encodings exist:
- **DER** (`SEQUENCE { INTEGER r, INTEGER s }`, RFC 3279): variable length: typically 70-72 bytes for P-256 (2000 signatures gave 69 (2), 70, 71, 72; the maximum is 72).
- **Raw / IEEE P1363**: `r || s`, each left-padded to the curve size - 64 bytes (P-256),
  96 (P-384), 132 (P-521).

## Who emits what
| Emits DER | Emits raw r||s |
|---|---|
| OpenSSL (`dgst -sign`, EVP), Java `SHA256withECDSA`, Go `ecdsa.SignASN1`, pyca `sign`, .NET `SignData(..., DSASignatureFormat.Rfc3279DerSequence)`, Node default, AWS KMS `Sign` | Web Crypto, JWS/JWT ES256/384/512, COSE, Java `SHA256withECDSAinP1363Format`, .NET default `SignData`, Node `dsaEncoding: "ieee-p1363"`, Azure Key Vault `sign` |

Checked: `openssl dgst -sha256 -sign` on a P-256 key gave a 71-byte DER sequence (`asn1parse` shows two INTEGERs, one with a 0x00 sign byte); COSE ECDSA is the raw I2OSP(R, n) | I2OSP(S, n) form (RFC 9053); Node default 71 bytes (DER) and `ieee-p1363` 64 bytes; `crypto.subtle` P-256 64 bytes and P-521 132 bytes; Go `SignASN1` 70 bytes; pyca `sign` DER; MDN describes the Web Crypto format as r and s concatenated at curve width (IEEE P1363) and OpenSSL as the X.509 DER default; the .NET `ECDsa.SignData` remarks say the default is `IeeeP1363FixedFieldConcatenation`; the AWS KMS `Sign` reference says ECDSA output is DER (RFC 3279 section 2.2.3); Java 8 `SHA256withECDSA` gave DER lengths 70, 71 and 72 (200 signatures) and has no `SHA256withECDSAinP1363Format` (`NoSuchAlgorithmException`), while the Java 21 standard algorithm names list it (not run, no JDK 11+); the Azure Key Vault REST docs define ES256 etc. by RFC 7518, which uses the raw form (the AWS and Azure services were not called).

Azure Key Vault returns raw r||s; AWS KMS returns DER. A JWT signed with AWS KMS must be
converted to raw before base64url encoding, or every verifier rejects it.

## Converting
Python:
```python
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
r, s = decode_dss_signature(der)
raw = r.to_bytes(32, "big") + s.to_bytes(32, "big")       # 32 for P-256, 48 P-384, 66 P-521
der = encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
```
Node: `crypto.sign("sha256", data, {key, dsaEncoding: "ieee-p1363"})`.
Go: `golang.org/x/crypto/cryptobyte` to parse, or `ecdsa.VerifyASN1` vs `ecdsa.Verify(pub, h, r, s)`.
Java: switch algorithm names instead of converting (`SHA256withECDSAinP1363Format`).

## Pitfalls
- Width: always pad r and s to the curve byte length; P-521 is 66 bytes, not 65. Stripping
  leading zeros gives intermittent (1 in 256) verification failures.
- DER integers carry a 0x00 sign byte when the high bit is set; strip it when going to raw.
- Verifiers must reject non-canonical DER (extra leading zeros, trailing bytes, BER lengths).
  Lenient parsing caused signature malleability bugs (Bitcoin). Java CVE-2022-21449 ("psychic signatures", NVD: Oracle Java SE
  17.0.2 and 18) let a verifier accept a signature with r = s = 0. Check 0 < r, s < n (pyca raised `InvalidSignature` for r = s = 0
  and for trailing bytes; Go `ecdsa.Verify` returned false for r = s = 0).
- ECDSA signatures are malleable ((r, n-s) also verifies; checked with pyca on P-256); never use the signature bytes as a
  unique transaction ID.

## Verify
- [ ] Interop test signs in each producer and verifies in each consumer.
- [ ] Tests include signatures where r or s has a leading zero byte.
- [ ] Verifier rejects r = 0, s = 0 and trailing garbage.
