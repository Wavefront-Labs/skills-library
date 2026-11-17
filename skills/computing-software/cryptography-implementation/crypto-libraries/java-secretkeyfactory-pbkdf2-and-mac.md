---
id: computing-software.cryptography-implementation.crypto-libraries.java-secretkeyfactory-pbkdf2-and-mac
name: java-secretkeyfactory-pbkdf2-and-mac
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, secretkeyfactory, pbkdf2, javax-crypto-mac, hmac, jca, java]
level: practitioner
status: docs-checked
description: "Derive keys with Java SecretKeyFactory PBKDF2WithHmacSHA256 and use javax.crypto.Mac: iterations, salt, key length in bits, char[] passwords, and AES key conversion."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/SecretKeyFactory.html", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/Mac.html", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SecretKeyFactory PBKDF2 and Mac

## PBKDF2
```java
byte[] salt = new byte[16]; new SecureRandom().nextBytes(salt);
PBEKeySpec spec = new PBEKeySpec(password /* char[] */, salt, 600_000, 256);   // length in BITS
SecretKeyFactory f = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
byte[] raw = f.generateSecret(spec).getEncoded();
spec.clearPassword();
SecretKey aes = new SecretKeySpec(raw, "AES");
```
- The iteration count here is an example; take the current value from the OWASP Password Storage Cheat Sheet.
- Store salt and iteration count with the hash or ciphertext.
- `PBEKeySpec` takes `char[]` so callers can wipe it; the SunJCE implementation encodes as UTF-8.

## Mac
```java
Mac mac = Mac.getInstance("HmacSHA256");
mac.init(new SecretKeySpec(key, "HmacSHA256"));
byte[] tag = mac.doFinal(message);
boolean ok = MessageDigest.isEqual(tag, received);       // time depends only on the first array's length
```

## Pitfalls
- Comparing tags with `Arrays.equals` instead of `MessageDigest.isEqual`.
- Passing key length in bytes (32) instead of bits (256): 32-bit keys.

## Verify
- [ ] Known-answer PBKDF2-SHA256 test vectors reproduce.

## Checked
2026-11-01. Confirmed in the OpenJDK source: SunJCE registers `PBKDF2WithHmacSHA1` and `PBKDF2WithHmacSHA256`;
`PBEKeySpec(char[], byte[], int, int)` and `clearPassword()`; PBKDF2KeyImpl encodes the password as UTF-8 and takes the
key length in bits (divides by 8); `MessageDigest.isEqual` compares in time depending only on the first array's length.
Removed: OWASP figures, FIPS provider minimums, Mac thread-safety and Java-version claims, RFC vector references.
Method: documentation only; no commands were run.
