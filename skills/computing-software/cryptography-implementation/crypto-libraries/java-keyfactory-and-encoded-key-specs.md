---
id: computing-software.cryptography-implementation.crypto-libraries.java-keyfactory-and-encoded-key-specs
name: java-keyfactory-and-encoded-key-specs
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, keyfactory, jca, java, pkcs8, x509-encoded-key-spec, key-import]
level: practitioner
status: docs-checked
description: "Load and convert Java keys with KeyFactory: X509EncodedKeySpec and PKCS8EncodedKeySpec from DER/PEM, RSA and EC component specs, and common InvalidKeySpecException causes."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/KeyFactory.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/spec/PKCS8EncodedKeySpec.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KeyFactory and encoded key specs

## PEM to keys
```java
static byte[] pemBody(String pem) {
  return Base64.getMimeDecoder().decode(pem.replaceAll("-----(BEGIN|END) [A-Z ]+-----", ""));
}
PublicKey pub  = KeyFactory.getInstance("RSA").generatePublic(new X509EncodedKeySpec(pemBody(pubPem)));
PrivateKey prv = KeyFactory.getInstance("EC").generatePrivate(new PKCS8EncodedKeySpec(pemBody(keyPem)));
```

## Formats Java accepts
- Public: SubjectPublicKeyInfo DER (`BEGIN PUBLIC KEY`).
- Private: unencrypted PKCS#8 DER (`BEGIN PRIVATE KEY`).
- `PKCS8EncodedKeySpec` and `X509EncodedKeySpec` take only those two ASN.1 structures, so convert PKCS#1
  (`BEGIN RSA PRIVATE KEY`), SEC1 (`BEGIN EC PRIVATE KEY`) and OpenSSH keys to PKCS#8 / SubjectPublicKeyInfo first.

## Components
```java
RSAPublicKeySpec spec = new RSAPublicKeySpec(modulus, publicExponent);
KeyFactory.getInstance("RSA").generatePublic(spec);
ECPublicKeySpec ecs = kf.getKeySpec(pub, ECPublicKeySpec.class);   // extract W (x, y)
```

## Common errors
- `InvalidKeySpecException` from PKCS#1 or SEC1 input; convert to PKCS#8.
- Wrong algorithm name for the key type (EC key with `KeyFactory("RSA")`).
- Base64 decoder choking on newlines; use `getMimeDecoder()`.

## Verify
- [ ] Round-trip `getEncoded()` equals the original DER; signature test with loaded key pair passes.

## Checked
2026-11-01. Confirmed in the OpenJDK source: `PKCS8EncodedKeySpec` is the ASN.1 OneAsymmetricKey (PKCS#8) encoding with
format "PKCS#8"; `X509EncodedKeySpec` is SubjectPublicKeyInfo; `ECPublicKeySpec.getW()`; `KeyFactory.getKeySpec`.
Removed: EdDSA/XDH version claim, PEMDecoder preview claim, openssl and Bouncy Castle conversion commands, exact
error text.
Method: documentation only; no commands were run.
