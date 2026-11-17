---
id: computing-software.cryptography-implementation.crypto-libraries.java-signature-class-and-algorithms
name: java-signature-class-and-algorithms
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, java-signature, jca, java, ecdsa, rsa-pss, ed25519, ml-dsa, p1363, pssparameterspec]
level: practitioner
status: docs-checked
description: "Sign and verify with java.security.Signature: ECDSA DER vs P1363 formats, RSASSA-PSS parameter specs, Ed25519 and ML-DSA names and providers."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/Signature.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/security/standard-names.html#signature-algorithms", "https://openjdk.org/jeps/497"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# java.security.Signature

## Basic use
```java
Signature s = Signature.getInstance("SHA256withECDSA");
s.initSign(privateKey);
s.update(data);
byte[] sig = s.sign();                       // default (non-P1363) ECDSA encoding

Signature v = Signature.getInstance("SHA256withECDSA");
v.initVerify(publicKey);
v.update(data);
boolean ok = v.verify(sig);                  // false if not verified; SignatureException if badly encoded
```

## Algorithm names
| Need | Name | Notes |
|---|---|---|
| ECDSA, default encoding | `SHA256withECDSA` | ANSI X9.62 |
| ECDSA, r and s concatenated (IEEE P1363) | `SHA256withECDSAinP1363Format` | the format JOSE ES256 and WebCrypto expect |
| RSA-PSS | `RSASSA-PSS` + `setParameter(...)` | needs digest, salt length and MGF1 parameters before use |
| RSA PKCS#1 v1.5 | `SHA256withRSA` | RSASSA-PKCS1-v1_5 |
| Ed25519 / Ed448 | `Ed25519`, `Ed448` (or `EdDSA`) | RFC 8032 |
| ML-DSA | `ML-DSA` | JDK 24 (JEP 497); parameter sets ML-DSA-44, -65, -87 |

## RSA-PSS parameters
```java
Signature pss = Signature.getInstance("RSASSA-PSS");
pss.setParameter(new PSSParameterSpec("SHA-256", "MGF1", MGF1ParameterSpec.SHA256, 32, 1));
```
Digest, MGF1 and salt length must match the peer on both sides.

## Gotchas
- `Signature` is stateful (init, update, sign or verify); create one per operation rather than sharing.
- `verify` returning false versus throwing: treat both as invalid; do not leak which happened.
- Prehashed input: `NONEwithECDSA` signs data without digesting it; use only when the other side signs digests
  (HSMs, KMS DIGEST mode).
- Provider selection: `Signature.getInstance(alg, "BC")` pins that provider; without a provider argument the
  installed providers are searched in preference order.

## Verify
- [ ] Signatures verify in the other library that reads them (cross-library test).
- [ ] PSS parameters match the peer (check with a cross-library test).

## Checked
2026-10-28. Confirmed against the JDK 21 Signature API page, the Java Security Standard Algorithm Names page and
JEP 497: sign/verify behaviour, `SHA256withECDSA`, `...inP1363Format` (r and s concatenated), `NONEwithECDSA`,
`RSASSA-PSS` needs parameters, Ed25519/Ed448/EdDSA names, ML-DSA in JDK 24 with the 44/65/87 parameter sets.
Removed: JDK 9 and 15 version gates, SunEC attribution, the DER wording, salt-length-32 advice, thread-safety
wording and the OpenSSL check (not on these pages). The Java code was not compiled or run.
Method: documentation only; no commands were run.
