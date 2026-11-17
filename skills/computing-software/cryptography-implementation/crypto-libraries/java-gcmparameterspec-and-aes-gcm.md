---
id: computing-software.cryptography-implementation.crypto-libraries.java-gcmparameterspec-and-aes-gcm
name: java-gcmparameterspec-and-aes-gcm
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, jca, jce, gcmparameterspec, aes-gcm, aead, java-cryptography, nonce-reuse]
level: practitioner
status: docs-checked
description: "Use AES-GCM correctly in Java: GCMParameterSpec tag bits, unique IVs, updateAAD order, IV-plus-ciphertext layout and tag failures."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/spec/GCMParameterSpec.html", "https://docs.oracle.com/en/java/javase/21/security/java-cryptography-architecture-jca-reference-guide.html", "https://csrc.nist.gov/pubs/sp/800/38/d/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCMParameterSpec and AES-GCM in Java

## Encrypt and decrypt
```java
static final SecureRandom RNG = new SecureRandom();
static final int IV_LEN = 12, TAG_BITS = 128;

static byte[] encrypt(SecretKey key, byte[] plaintext, byte[] aad) throws GeneralSecurityException {
    byte[] iv = new byte[IV_LEN];
    RNG.nextBytes(iv);
    Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
    c.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(TAG_BITS, iv));
    c.updateAAD(aad);                         // before any update()/doFinal() of data
    byte[] ct = c.doFinal(plaintext);         // ciphertext || 16-byte tag
    return ByteBuffer.allocate(IV_LEN + ct.length).put(iv).put(ct).array();
}

static byte[] decrypt(SecretKey key, byte[] blob, byte[] aad) throws GeneralSecurityException {
    if (blob.length < IV_LEN + TAG_BITS / 8) throw new GeneralSecurityException("short input");
    Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
    c.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(TAG_BITS, blob, 0, IV_LEN));
    c.updateAAD(aad);
    return c.doFinal(blob, IV_LEN, blob.length - IV_LEN);   // throws if the tag check fails
}
```

## Details that matter
- `GCMParameterSpec(tLen, iv)`: `tLen` is the tag length in **bits** (128). The GCM specification allows only
  128, 120, 112, 104 or 96 (and 64 or 32 for certain applications); other values may be accepted by the class but
  not by every provider. Keep 128.
- IV: never reuse a key and IV pair for encryption (JCA guide). The Cipher must be re-initialised with new
  parameters for every encryption. This example uses a fresh random 12-byte IV per message; SP 800-38D (under
  revision) governs IV construction and limits, so read it for your volume. Never derive the IV from the
  plaintext or a timestamp alone.
- Reuse across Cipher objects or processes cannot be detected by the library; your IV generation must prevent it.
- Output of `doFinal` here is `ciphertext || tag`. Fix your own wire format, e.g. `version || iv || ct || tag`,
  and test it against every other library that reads the data.
- AAD: bind context (record ID, tenant, version). AAD must be supplied before data (JCA guide), so call
  `updateAAD` first.

## Decryption behaviour
- A failed tag check means wrong key, wrong IV, wrong AAD or tampering. Treat them all the same: reject, don't
  return partial output, don't say which.
- For large files, chunk into independently authenticated segments (Tink streaming AEAD) instead of one giant
  GCM message.

## Keys
`KeyGenerator kg = KeyGenerator.getInstance("AES"); kg.init(256); SecretKey k = kg.generateKey();`
or a key from a KMS. Don't build keys from passwords with `new SecretKeySpec(pwd.getBytes(), "AES")`.

## Verify
- [ ] Round-trip test, plus tests that flipping one byte of IV, ciphertext, tag or AAD throws.
- [ ] IV is random per message (or a documented counter scheme) and stored with the ciphertext.
- [ ] Interop vector decrypts in the other languages that read the data.

## Checked
2026-10-28. Confirmed against the JDK 21 GCMParameterSpec API page and JCA Reference Guide (AES/GCM section):
tLen in bits and the permitted values, AAD before data, no key and IV reuse, re-initialise per encryption. The
NIST SP 800-38D page fetched is only the abstract (publication under revision). Removed: the 2^32 message budget,
the SunJCE `IllegalStateException` text, cross-library output layouts, `AEADBadTagException` wording, buffering
and `CipherInputStream` claims (not on these pages). The Java code was not compiled or run.
Method: documentation only; no commands were run.
