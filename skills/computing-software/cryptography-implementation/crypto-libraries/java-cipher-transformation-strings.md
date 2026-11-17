---
id: computing-software.cryptography-implementation.crypto-libraries.java-cipher-transformation-strings
name: java-cipher-transformation-strings
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jca, jce, cipher-transformation, java-cryptography, rsa-oaep, aes-gcm, ecb-default]
level: practitioner
status: docs-checked
description: "Always pass full Java Cipher transformations: why 'AES' means ECB, explicit OAEP parameters, valid mode and padding names, and catching misuse in review."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/security/standard-names.html#cipher-algorithms", "https://docs.oracle.com/en/java/javase/21/security/java-cryptography-architecture-jca-reference-guide.html", "https://find-sec-bugs.github.io/bugs.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Explicit Cipher transformation strings (Java)

`Cipher.getInstance(String)` takes `"algorithm/mode/padding"`. Anything left out is filled in by
the provider's defaults; the JCA guide says SunJCE and SunPKCS11 default to ECB mode and PKCS5Padding for many
symmetric ciphers.

## The defaults you must never rely on
| You wrote | You get | Use instead |
|---|---|---|
| `"AES"` | ECB mode with PKCS5Padding (`AES/ECB/PKCS5Padding`) | `"AES/GCM/NoPadding"` |
| `"RSA/ECB/PKCS1Padding"` | PKCS#1 v1.5 padding (flagged by Find Security Bugs as `PADDING_ORACLE`) | `"RSA/ECB/OAEPWithSHA-256AndMGF1Padding"` + explicit spec |
| `"DES"`, `"DESede"` | flagged as insecure (`DES_USAGE`, `TDES_USAGE`) | AES-GCM |
| `"AES/CBC/PKCS5Padding"` | no integrity (`CIPHER_INTEGRITY`) | AES-GCM, or CBC + HMAC (encrypt-then-MAC) |

## The OAEP trap
The transformation string names only one digest. The standard-names page says that with `OAEPPadding` the
Cipher is initialised with a `javax.crypto.spec.OAEPParameterSpec` to supply the values. Always pass the digest
and the MGF1 digest explicitly, and test against the other language that reads the data:
```java
Cipher c = Cipher.getInstance("RSA/ECB/OAEPPadding");
c.init(Cipher.ENCRYPT_MODE, publicKey, new OAEPParameterSpec(
    "SHA-256", "MGF1", MGF1ParameterSpec.SHA256, PSource.PSpecified.DEFAULT));
```

## Good transformations
- `AES/GCM/NoPadding` with `GCMParameterSpec(128, iv12)` (see the GCM skill).
- `ChaCha20-Poly1305` (RFC 7539 AEAD) with `IvParameterSpec(nonce12)`.
- `AESWrap` / `AESWrapPad` (RFC 3394/5649, SP 800-38F) for wrapping keys; the standard-names page says they equal
  `AES` with KW or KWP mode and NoPadding.

## Engineering rules
- A `Cipher` holds init state (key, IV). Create one per operation or keep one per thread; never share a static
  instance.
- Centralise transformations in one class so reviews and migrations touch one place.
- Don't pass a provider name (`getInstance(t, "BC")`) unless you need that provider; it pins
  behaviour and breaks when the provider changes (see the providers skill).
- Catch `GeneralSecurityException` at the boundary and fail closed; don't log keys or plaintext.

## Find misuse
- SpotBugs + Find Security Bugs: `CIPHER_INTEGRITY`, `ECB_MODE`, `DES_USAGE`, `RSA_NO_PADDING`, `PADDING_ORACLE`.
- Grep: `getInstance\("(AES|RSA|DES)"\)` and `/ECB/` outside RSA.

## Verify
- [ ] No `Cipher.getInstance` call uses a bare algorithm name.
- [ ] Every OAEP use passes an explicit `OAEPParameterSpec`, tested against another language.
- [ ] No shared static `Cipher` instances.

## Checked
2026-10-28. Confirmed against the JDK 21 JCA Reference Guide, the Java Security Standard Algorithm Names page and
the Find Security Bugs pattern list: ECB and PKCS5Padding defaults for symmetric ciphers, OAEPPadding needs
OAEPParameterSpec, AESWrap/AESWrapPad equal KW/KWP with NoPadding, ChaCha20-Poly1305 RFC 7539, bug pattern names.
Removed: the claim that SunJCE uses SHA-1 for MGF1 (not on these pages), RSA default string, DES/DESede bit sizes,
PKCS5/PKCS7 note, JDK version gates, `Cipher` thread-safety wording and the CodeQL query ids.
Method: documentation only; no commands were run.
