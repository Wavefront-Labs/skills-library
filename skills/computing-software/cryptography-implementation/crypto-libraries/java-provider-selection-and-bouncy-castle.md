---
id: computing-software.cryptography-implementation.crypto-libraries.java-provider-selection-and-bouncy-castle
name: java-provider-selection-and-bouncy-castle
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jca, jce, bouncy-castle, jca-providers, bc-fips, security-providers, java-pqc]
level: advanced
status: gated
description: "Choose and register Java security providers: provider order, when Bouncy Castle is needed, BC-FIPS, signed-jar pitfalls in fat jars, and JDK 24+ ML-KEM/ML-DSA."
sources: ["https://docs.oracle.com/en/java/javase/21/security/java-cryptography-architecture-jca-reference-guide.html", "https://www.bouncycastle.org/documentation/documentation-java/", "https://openjdk.org/jeps/496", "https://openjdk.org/jeps/497"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Provider selection and Bouncy Castle (Java)

JCA resolves `getInstance("X")` by walking registered providers in order and taking the first
that implements X. Provider choice changes behaviour, performance and compliance.

## See what you have
```java
for (Provider p : Security.getProviders()) System.out.println(p.getName() + " " + p.getVersionStr());
Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
System.out.println(c.getProvider().getName());     // who actually serves it
```
The list comes from the `security.provider.N` entries in the `java.security` file (location and format: see the JDK security docs) (gated: unconfirmed, source is paywalled or blocked).

## When the JDK is enough
Modern JDKs cover AES-GCM, ChaCha20-Poly1305, RSA-OAEP/PSS, ECDSA, EdDSA, X25519/X448, HKDF and PBKDF2 (first-release versions and KDF API status: confirm in the JDK docs) (gated: unconfirmed, source is paywalled or blocked), and ML-DSA (JEP 497, delivered in JDK 24); ML-KEM is JEP 496 (release: gated: unconfirmed, source is paywalled or blocked). Prefer the JDK when it has the algorithm: fewer dependencies, patched with
the JDK.

## When to add Bouncy Castle
- Formats and protocols: CMS/S-MIME, OpenPGP, PKCS#10 builders, X.509 certificate generation
  (`bcpkix`), OCSP/TSP clients.
- Algorithms missing from your JDK version (check the Bouncy Castle release notes for the current list) (gated: unconfirmed, source is paywalled or blocked).
- FIPS: Bouncy Castle publishes a separate Java FIPS line with its own documentation and roadmap; confirm module names and validation status there.

```java
Security.addProvider(new BouncyCastleProvider());                 // append: JDK stays first
Signature s = Signature.getInstance("<algorithm>", "BC");        // explicit only where needed
```
Avoid `Security.insertProviderAt(new BouncyCastleProvider(), 1)` unless you mean to change every
algorithm in the process to BC's implementation.

## Packaging pitfalls
- Bouncy Castle's documentation says to use its signed jar for the provider on JDK 1.4 and later. Shading `bcprov` into a fat/uber jar strips the signature, which can fail with `JCE cannot authenticate the provider BC` (error text gated: unconfirmed, source is paywalled or blocked). Keep BC as a separate jar.
- Artifact names on the Bouncy Castle docs page: `bcprov-jdk18on`, `bcpkix-jdk18on`, `bcpg-jdk18on`, `bctls-jdk18on`, `bcutil-jdk18on`; other lines exist for older JDKs (`jdk15to18`, `jdk14`). Don't mix versions of bcprov and bcpkix.
- Two copies of BC in one classloader hierarchy produce `ClassCastException` between
  identically named classes.

## FIPS deployments
Use either the OS-integrated provider or the Bouncy Castle FIPS module in its approved-only mode (property name: see the BC FIPS user guide) (gated: unconfirmed, source is paywalled or blocked); remove non-FIPS providers from the list so nothing falls through to them. FIPS suitability is a compliance question: confirm with your assessor and the module's current validation certificate.

## Verify
- [ ] Logs at startup list providers in the intended order.
- [ ] Each sensitive operation's `getProvider()` is the expected one (unit test).
- [ ] BC (if used) is the `jdk18on` line, current version, unshaded.

## Checked

2026-11-02. Checked against the Oracle JCA reference guide (provider preference order, getInstance search order, advice not to request specific providers), JEP 497 (ML-DSA, release 24, KeyPairGenerator/Signature/KeyFactory), and the Bouncy Castle Java documentation page (jdk18on artifact names, signed jar guidance, separate FIPS documentation). Removed or gated: first-release versions for EdDSA/X25519/HKDF, the Argon2/SLH-DSA/SM/GOST algorithm list, the unshaded-jar error text, jdk15on discontinued claim, BC-FIPS property and module names, java.security file path.

Method: documentation only; no commands were run.
