---
id: computing-software.cryptography-implementation.crypto-libraries.using-platform-crypto-apis-safely
name: using-platform-crypto-apis-safely
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, web-crypto, subtle-crypto, javascript, nodejs, java, jca, jce, dotnet, csharp, aesgcm, golang, crypto-cipher, python, pyca-cryptography, aes-gcm, securerandom, csprng, getrandomvalues, pbkdf2, argon2, nonce, auth-tag, interoperability, ecb]
level: practitioner
status: gated
description: "Safe AES-GCM, randomness and KDF calls in Web Crypto, Java JCA, .NET, Go and Python cryptography, plus the interop traps: tag placement, nonce prefixing, encodings and ECB defaults."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto", "https://docs.oracle.com/en/java/javase/21/docs/specs/security/standard-names.html", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.aesgcm?view=net-9.0", "https://github.com/dotnet/dotnet-api-docs/tree/main/xml/System.Security.Cryptography", "https://pkg.go.dev/crypto/cipher", "https://cryptography.io/en/latest/hazmat/primitives/aead/", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using platform crypto APIs safely

**Goal:** encrypt with AES-256-GCM, generate randomness and derive keys correctly in
the standard library of each major platform, and make the ciphertext readable on
every other platform.

## The common contract (same everywhere)
- 32-byte key from a CSPRNG or KMS (see
  `computing-software.cryptography-implementation.key-management.key-lifecycle-and-envelope-encryption`).
- A **fresh 12-byte nonce per message** from the CSPRNG. Never reuse a nonce with the
  same key: in GCM that leaks the authentication key and XOR of plaintexts.
- A 16-byte (128-bit) tag. Never truncate it.
- AAD for context (record id, schema version).
- Wire format: `version(1) || nonce(12) || ciphertext || tag(16)`, then base64 if it
  must be text.

## Web Crypto (browsers, Deno, Node `globalThis.crypto`)
```js
const key = await crypto.subtle.generateKey({ name: "AES-GCM", length: 256 },
                                            false, ["encrypt", "decrypt"]); // extractable:false
const iv = crypto.getRandomValues(new Uint8Array(12));
const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv, additionalData: aad }, key, data);
// ct = ciphertext || 16-byte tag
```
Browsers only provide `crypto.subtle` in secure contexts (HTTPS or localhost).
`extractable: false` prevents script from exporting the key, but script can still
*use* it, so XSS remains fatal. `getRandomValues` fills at most 65,536 bytes per
call (Node 24.22: 65536 worked, 65537 threw `QuotaExceededError`). The classic Web Crypto spec has no Argon2; PBKDF2 is available
(`deriveKey`). Node 24.22 adds `crypto.argon2()`/`argon2Sync()` and an experimental `Argon2id` algorithm for `subtle.deriveBits`
(`importKey` format `raw-secret`; it emits an `ExperimentalWarning`), so check your runtime before relying on either statement.
In Node, `generateKey(..., false, ...)` made `exportKey` throw `key is not extractable`, and a 5-byte plaintext gave a 21-byte
`ct` (ciphertext plus 16-byte tag).

Node's own `crypto.createCipheriv("aes-256-gcm", key, iv)` returns the tag separately.
Call `cipher.getAuthTag()` after `final()`. When decrypting, call
`decipher.setAuthTag(tag)` before `final()` and pass `{ authTagLength: 16 }` so that
truncated tags are rejected.

## Java (JCA)
```java
SecureRandom rng = new SecureRandom();
byte[] iv = new byte[12]; rng.nextBytes(iv);
Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
c.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv)); // 128 = tag BITS
c.updateAAD(aad);
byte[] ct = c.doFinal(pt);   // tag appended
```
`Cipher.getInstance("AES")` means `AES/ECB/PKCS5Padding` in the default provider
(Java 8 run: two identical 16-byte plaintext blocks encrypted to identical ciphertext blocks, and 32 bytes in gave 48 out).
Never use the bare name. SunJCE refuses to reuse a key+IV pair for a second GCM
encryption (Java 8: re-`init` with the same key and IV threw `InvalidAlgorithmParameterException: Cannot reuse iv for GCM
encryption`, and a second `doFinal` on the same cipher threw `IllegalStateException: Must use either different key or iv`), so
create a new IV each time. During decryption SunJCE buffers the whole message until it has checked the tag (Java 8: `update` on
500 bytes of GCM ciphertext returned 0 bytes), so stream large files in chunks. Generate keys with `KeyGenerator.getInstance("AES")` and
`init(256)`. Don't seed `SecureRandom` yourself.

## .NET
The C# block below was not compiled or run (no .NET SDK here); member names and signatures were read from the dotnet-api-docs
XML (the `AesGcm` constructor with `tagSizeInBytes`, the static `Rfc2898DeriveBytes.Pbkdf2`, `RandomNumberGenerator.GetBytes`,
`CryptographicOperations.FixedTimeEquals`) (gated: unconfirmed, source is paywalled or blocked).
```csharp
using var aes = new AesGcm(key, tagSizeInBytes: 16);   // .NET 8+ constructor
byte[] nonce = RandomNumberGenerator.GetBytes(12);
byte[] ct = new byte[pt.Length], tag = new byte[16];
aes.Encrypt(nonce, pt, ct, tag, aad);                  // tag is SEPARATE
byte[] k = Rfc2898DeriveBytes.Pbkdf2(pw, salt, 600_000, HashAlgorithmName.SHA256, 32);
```
`Aes` is the unauthenticated block-cipher class; authenticated GCM is the separate `AesGcm` class (see its docs), so don't use `Aes` modes
without a MAC for new designs. Compare MACs with `CryptographicOperations.FixedTimeEquals`. The one-argument
`AesGcm(key)` constructor is marked obsolete from .NET 8.

## Go
```go
block, _ := aes.NewCipher(key)              // 32-byte key = AES-256
aead, _ := cipher.NewGCM(block)
nonce := make([]byte, aead.NonceSize())
if _, err := rand.Read(nonce); err != nil { return err }   // crypto/rand, not math/rand
ct := aead.Seal(nonce, nonce, pt, aad)      // nonce prefix, tag appended
pt, err := aead.Open(nil, ct[:12], ct[12:], aad)
```
For passwords: `argon2.IDKey(pw, salt, 2, 19*1024, 1, 32)` from
`golang.org/x/crypto/argon2` (x/crypto v0.58.0 ran). The memory argument is in **KiB**; 19*1024 matches the OWASP Password Storage
Cheat Sheet minimum of Argon2id with 19 MiB, 2 iterations and 1 degree of parallelism (and PBKDF2-HMAC-SHA256 at 600,000
iterations where FIPS compliance is needed, which is the value used in the .NET block above). Go 1.24 added `crypto/hkdf`,
`crypto/pbkdf2`, `crypto/mlkem` and `cipher.NewGCMWithRandomNonce` to the standard library (go.dev/doc/go1.24 and the API file).

## Python (`cryptography`)
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)                      # or secrets.token_bytes(12); never random
ct = AESGCM(key).encrypt(nonce, pt, aad)    # tag appended; decrypt raises InvalidTag
```
`Fernet` is a complete, versioned format if you just need to encrypt a blob.

## Interop gotchas
- **Tag placement:** Web Crypto, Java, Go and Python append the tag; .NET `AesGcm`,
  Node `createCipheriv` and OpenSSL EVP return it separately (Web Crypto, Java 8, Node `createCipheriv` and Go were run; pyca `AESGCM`
  interop with Go was run). Concatenate or split explicitly.
- **Nonce:** Go's `Seal(nonce, ...)` prefixes it only because you passed it as the
  destination. Others don't. Document the layout.
- **Encodings:** UTF-8 for strings (Java `getBytes()` without a charset uses the
  platform default on old JDKs). Standard base64 and base64url are not
  interchangeable. Hex case can differ.
- **Units:** Java tag length is in bits (`GCMParameterSpec(128, iv)`), .NET `tagSizeInBytes` in bytes, Go's Argon2 memory in KiB.
- **AAD** must be byte-identical on both sides. Empty and absent behave the same in
  GCM, but not every API lets you pass empty.

## Verify
- [ ] No `"AES"`, `ECB`, `math/rand`, `Math.random` or `random` module anywhere near keys or nonces.
- [ ] Each encryption gets a new 12-byte nonce, and the tag is 16 bytes.
- [ ] A test vector encrypted on platform A decrypts on platform B, and fails after one bit flip.
- [ ] The wire format (version, nonce, tag position, encoding) is written down.
