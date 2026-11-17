---
id: computing-software.cryptography-implementation.crypto-libraries.java-keygenerator-and-keypairgenerator
name: java-keygenerator-and-keypairgenerator
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, keypairgenerator, keygenerator, jca, java, key-generation]
level: practitioner
status: docs-checked
description: "Generate keys in Java with KeyGenerator and KeyPairGenerator: algorithm names, init with sizes or AlgorithmParameterSpec, SecureRandom choice, and provider pinning."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/KeyPairGenerator.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/KeyGenerator.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/security/standard-names.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeyGenerator and KeyPairGenerator

## Symmetric
```java
KeyGenerator kg = KeyGenerator.getInstance("AES");
kg.init(256);                                   // AES keys are 128, 192 or 256 bits
SecretKey k = kg.generateKey();
```

## Asymmetric
```java
KeyPairGenerator rsa = KeyPairGenerator.getInstance("RSA");
rsa.initialize(new RSAKeyGenParameterSpec(3072, RSAKeyGenParameterSpec.F4));
KeyPair kp = rsa.generateKeyPair();

KeyPairGenerator ec = KeyPairGenerator.getInstance("EC");
ec.initialize(new ECGenParameterSpec("secp256r1"));

KeyPair ed  = KeyPairGenerator.getInstance("Ed25519").generateKeyPair();   // RFC 8032 signatures
KeyPair x   = KeyPairGenerator.getInstance("X25519").generateKeyPair();    // RFC 7748 key agreement
```
The JDK 21 standard-names page lists `Ed25519` and `X25519` generators; check the standard-names page of your JDK
before using newer algorithm names (for example post-quantum ones).

## Gotchas
- Always initialize explicitly. Without parameters it is up to the provider what parameters to use, so defaults
  can differ between providers and JDK versions.
- `initialize(int)` uses a default parameter set for that size; prefer `ECGenParameterSpec` with a named curve.
- Pass a provider (`getInstance("EC", "SunEC")` or a Provider object) when HSM or FIPS providers are installed,
  so keys are created where intended.
- Do not seed `SecureRandom` manually. `initialize(int)` and the `AlgorithmParameterSpec` form without a
  `SecureRandom` use the SecureRandom of the highest-priority installed provider; pass your own
  `new SecureRandom()` only when you need to.

## Verify
- [ ] Key sizes/curves asserted in tests (`((RSAPublicKey) kp.getPublic()).getModulus().bitLength() == 3072`).

## Checked
2026-10-28. Confirmed against the JDK 21 KeyPairGenerator API page and Java Security Standard Algorithm Names page:
provider chooses parameters when none are given, `initialize(int)` default parameter set, `AlgorithmParameterSpec`
forms, SecureRandom source, `getInstance(algorithm, provider)`, AES key sizes, `Ed25519` and `X25519` generators.
Removed: ML-KEM and ML-DSA lines and Java version gates (not on the JDK 21 page), HmacSHA256 default size, the
RSA and EC default sizes. The Java code was not compiled or run.
Method: documentation only; no commands were run.
