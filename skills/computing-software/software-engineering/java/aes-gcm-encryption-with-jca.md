---
id: computing-software.software-engineering.java.aes-gcm-encryption-with-jca
name: aes-gcm-encryption-with-jca
category: computing-software
field: software-engineering
product: java
tags: [java, java-security, aes-gcm-jca, aes-gcm, authenticated-encryption, nonce, cipher]
level: advanced
status: docs-checked
description: "Encrypt data in Java with AES-GCM via javax.crypto.Cipher using AES/GCM/NoPadding: random nonce per message, AAD, key storage, DEK/KEK and rotation."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/security/standard-names.html#cipher-algorithms", "https://csrc.nist.gov/pubs/sp/800/38/d/final", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AES-GCM with the JCA

The transformation string is `AES/GCM/NoPadding`; the JCA standard-names list marks it as one every Java platform implementation must support (key size 128), and `GCMParameterSpec` is the parameter type for GCM. GCM is defined in NIST SP 800-38D.

```java
private static final SecureRandom RNG = new SecureRandom();

static byte[] encrypt(SecretKey key, byte[] plain, byte[] aad) throws GeneralSecurityException {
    byte[] iv = new byte[12];                       // fresh random nonce per message
    RNG.nextBytes(iv);
    Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
    c.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));    // 128-bit tag
    if (aad != null) c.updateAAD(aad);              // authenticated but unencrypted context (e.g. record id)
    byte[] ct = c.doFinal(plain);                   // ciphertext with tag appended
    return ByteBuffer.allocate(iv.length + ct.length).put(iv).put(ct).array();
}

static byte[] decrypt(SecretKey key, byte[] blob, byte[] aad) throws GeneralSecurityException {
    Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
    c.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(128, blob, 0, 12));
    if (aad != null) c.updateAAD(aad);
    return c.doFinal(blob, 12, blob.length - 12);   // fails if the data was tampered with or the key is wrong
}
```

## Rules (OWASP Cryptographic Storage Cheat Sheet)
1. Use AES with a key of at least 128 bits, ideally 256, and an authenticated mode: GCM or CCM are the first preference. If neither is available use CTR or CBC with separate authentication (encrypt-then-MAC). ECB should not be used outside very specific circumstances.
2. Never reuse an IV with the same key. Rotate keys before reaching the mode's limits on message size, operation count and IV uniqueness; the cheat sheet points to NIST SP 800-38D sections 5.2.1.1 and 8 for the GCM input-length and IV-construction rules. Read those sections of the standard (not read here) before choosing nonce size, tag size and per-key message limits.
3. Generate keys and IVs with a CSPRNG: `java.security.SecureRandom`, never `java.util.Random` or `Math.random()`.
4. Keep keys in a key vault, HSM or secrets manager, not in source, version control or environment variables. Store keys apart from the data.
5. Envelope encryption: a data encryption key (DEK) encrypts the data and a key encryption key (KEK), stored separately and at least as strong, encrypts the DEK. Mark each item with the id of the key used so old data stays decryptable while keys rotate.
6. Rotate keys when compromise is suspected, after the cryptoperiod, before usage limits, or when an attack on the algorithm is announced. Have the rotation code and process ready before it is needed.
7. A KDF can derive a KEK from a passphrase, so the passphrase can change without re-encrypting data.
8. Do not rely on encryption alone: add access control around the stored data.

## Gotchas
- Do not log keys or plaintext.
- Treat any decryption failure as tampering: fail closed and release no partial plaintext.

## Verify
Round-trip test; flip one byte of the blob and assert decryption fails; encrypt the same plaintext twice and assert the outputs differ.

## Checked

Date: 2026-11-08

Read in full: the OWASP Cryptographic Storage Cheat Sheet and the NIST SP 800-38D landing page (abstract only; the standard itself was not read). Confirmed in the JCA standard names page by searching it (about 90 KB, not read in full): the `AES/GCM/NoPadding` transformation, the GCM parameter and mode entries. Removed because none of these pages state them: the 96-bit nonce and 2^32-message figures, the PBKDF2 iteration count and Argon2, the `AEADBadTagException` name, `KeyGenerator` usage, the chunked-framing advice and the Tink recommendation.

Method: documentation only; no commands were run.
