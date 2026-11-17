---
id: computing-software.cryptography-implementation.crypto-libraries.java-securerandom-instances-and-blocking
name: java-securerandom-instances-and-blocking
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jca, jce, securerandom-strong, securerandom, drbg, entropy-blocking, java-cryptography]
level: practitioner
status: docs-checked
description: "Pick the right Java SecureRandom: new SecureRandom() vs getInstanceStrong() blocking, DRBG parameters and the setSeed trap."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/SecureRandom.html", "https://docs.oracle.com/en/java/javase/21/security/oracle-providers.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/DrbgParameters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SecureRandom instances and blocking (Java)

## Default choice
```java
private static final SecureRandom RNG = new SecureRandom();   // one shared instance
byte[] key = new byte[32]; RNG.nextBytes(key);
```
The default preference order in the JDK 21 SUN provider is `NativePRNG` first on Linux and macOS, and `DRBG`
first on Windows (there is no NativePRNG on Windows; `Windows-PRNG` comes from SunMSCAPI). Use the default for
keys, IVs, tokens and salts.

## getInstanceStrong() is usually wrong for servers
`SecureRandom.getInstanceStrong()` returns the algorithm and provider named in the
`securerandom.strongAlgorithms` Security property. The API docs warn that `generateSeed`, `reseed` and
`nextBytes` may block while entropy is gathered, for example when the source is `/dev/random`, so a strong
instance on a request path can stall. Use it only for long-term key generation where a stall is acceptable.

## DRBG with explicit parameters
```java
SecureRandom drbg = SecureRandom.getInstance("DRBG",
    DrbgParameters.instantiation(256, DrbgParameters.Capability.PR_AND_RESEED, "app-v1".getBytes()));
```
The mechanism and algorithm come from the `securerandom.drbg.config` Security property (default Hash_DRBG
with SHA-256); without a `DrbgParameters.Instantiation` the default is 128-bit strength, no prediction
resistance and no personalization string. Entropy comes from `securerandom.source`.

## The setSeed trap
```java
SecureRandom r = SecureRandom.getInstance("SHA1PRNG");
r.setSeed(42L);           // before first nextBytes(): no self-seeding
```
Per the API docs, a PRNG `SecureRandom` will not seed itself automatically if `setSeed` is called before any
`nextBytes` or `reseed` call, and the caller must supply enough entropy. A constant or guessable seed makes the
output guessable. Never call `setSeed` with a fixed or low-entropy value on a security RNG; if you see it,
treat derived keys as compromised. Use `reseed` to add entropy from the source.

## Other rules
- Don't use `java.util.Random` or `Math.random()` for anything secret.

## Verify
- [ ] Grep finds no `setSeed(` on SecureRandom and no `java.util.Random` in security code.
- [ ] No `getInstanceStrong()` on request paths.
- [ ] One shared SecureRandom per class, not one per call.

## Checked
2026-10-28. Confirmed against the JDK 21 SecureRandom and DrbgParameters API pages and the Oracle JDK Providers
Guide (default SecureRandom order per OS): default order, `securerandom.strongAlgorithms`, possible blocking,
setSeed non-self-seeding, `securerandom.drbg.config` default, DRBG instantiation defaults, `securerandom.source`.
Removed: kernel-version blocking claim, the egd/virtio-rng section, UUID bit count, nextInt bias claim,
ThreadLocalRandom, JDK 9 version gate and NativePRNG internals (not on these pages).
Method: documentation only; no commands were run.
