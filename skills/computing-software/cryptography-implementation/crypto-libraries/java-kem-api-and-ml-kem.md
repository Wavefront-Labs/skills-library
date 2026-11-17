---
id: computing-software.cryptography-implementation.crypto-libraries.java-kem-api-and-ml-kem
name: java-kem-api-and-ml-kem
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, java-kem, jca, java, ml-kem, kem, dhkem, jep-452, jep-496, post-quantum]
level: advanced
status: docs-checked
description: "Use the Java KEM API (JEP 452) for DHKEM and ML-KEM (JDK 24+): KeyPairGenerator names, Encapsulator and Decapsulator, deriving keys and provider support."
sources: ["https://openjdk.org/jeps/452", "https://openjdk.org/jeps/496", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/KEM.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java KEM API and ML-KEM

## API (javax.crypto.KEM, JDK 21+)
```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");          // JDK 24+
kpg.initialize(NamedParameterSpec.ML_KEM_768);
KeyPair kp = kpg.generateKeyPair();

KEM kem = KEM.getInstance("ML-KEM");
// sender
KEM.Encapsulator enc = kem.newEncapsulator(kp.getPublic());
KEM.Encapsulated e = enc.encapsulate();
SecretKey shared = e.key();                 // full shared secret as a SecretKey (algorithm name "Generic")
byte[] ciphertext = e.encapsulation();      // send this
// recipient
KEM.Decapsulator dec = kem.newDecapsulator(kp.getPrivate());
SecretKey shared2 = dec.decapsulate(ciphertext);
```
- `encapsulate(from, to, algorithm)` returns a slice of the secret as a key of the named algorithm (e.g.
  `encapsulate(0, 32, "AES")`).
- JDK 21 (JEP 452) includes the DHKEM defined in RFC 9180; ML-KEM arrived in JDK 24 (JEP 496) with parameter sets
  `ML-KEM-512`, `ML-KEM-768` and `ML-KEM-1024` (`NamedParameterSpec.ML_KEM_512` and so on). A `KeyPairGenerator` that
  is not initialized uses ML-KEM-768.

## Using the secret
Feed it through a KDF with context before using it as an AES key in a protocol, especially in hybrid designs where it must be combined with an ECDH secret.

## Key encoding
Public keys are X.509 encoded and private keys PKCS #8 (JEP 496). The ML-KEM encoding follows a draft IETF RFC that
the JDK tracks, so check that peer libraries agree on the format before exchanging keys.

## Verify
- [ ] Shared secrets match across Encapsulator and Decapsulator.

## Checked
2026-11-01. Confirmed in the OpenJDK source (javax.crypto.KEM, SunJCE, NamedParameterSpec) and JEP 452 / JEP 496: KEM
class since 21, getInstance/newEncapsulator/newDecapsulator/encapsulate(from,to,algorithm)/decapsulate, `Generic`
algorithm name, DHKEM in JDK 21, ML-KEM names and constants, default ML-KEM-768, X.509/PKCS #8 encodings. Removed:
the 32-byte secret size, curve list for DHKEM, Bouncy Castle and OpenSSL interop claims, KDF API wording.
Method: documentation only; no commands were run.
