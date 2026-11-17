---
id: computing-software.cryptography-implementation.secure-implementation.designing-misuse-resistant-crypto-apis
name: designing-misuse-resistant-crypto-apis
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, crypto-api-design, misuse-resistance, api-design, aead, key-handles, versioned-ciphertext, secure-defaults, tink, libsodium]
level: sme
status: draft
description: "Design internal crypto APIs that are hard to misuse: no caller-supplied nonces, typed key handles, versioned ciphertext, context binding, safe defaults, hazmat separation."
sources: ["https://www.usenix.org/conference/soups2017/technical-sessions/presentation/acar", "https://developers.google.com/tink/design", "https://doc.libsodium.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing misuse-resistant crypto APIs

Studies of developers using crypto libraries (Acar et al., SOUPS 2017) found that API design, not developer skill,
predicts correctness. Wrap primitives in an internal API that makes the secure path the only easy one.

## Principles
1. **No nonce/IV parameter.** Generate it internally (random 192-bit with XChaCha20-Poly1305, or AES-GCM-SIV) and
   embed it in the output.
2. **Authenticated encryption only.** No unauthenticated modes, no separate `mac()` that callers must remember.
3. **Typed key handles, not byte arrays.** `EncryptionKey`, `SigningKey`, `MacKey` types that cannot be swapped;
   keys carry their algorithm and version; serialisation is explicit and audited.
4. **Versioned, self-describing output.** `version || key_id || nonce || ciphertext || tag` so algorithms and keys
   can rotate without call-site changes.
5. **Mandatory context.** Require a purpose/context argument bound as associated data, preventing cross-context
   replay.
6. **Fail closed with exceptions.** Verification and decryption throw; there is no boolean to ignore and no partial
   plaintext on failure.
7. **No algorithm choice at call sites.** Algorithm selection lives in key metadata or configuration (like Tink
   keysets).
8. **Hazmat separation.** Low-level primitives live in a clearly named package (`hazmat`, `_unsafe`) that needs review
   to import.

## Shape
```python
class Envelope:
    def seal(self, plaintext: bytes, *, context: str) -> bytes: ...
    def open(self, blob: bytes, *, context: str) -> bytes: ...   # raises DecryptError
class Signer:
    def sign(self, message: bytes, *, context: str) -> bytes: ...
class Verifier:
    def verify(self, message: bytes, signature: bytes, *, context: str) -> None: ...  # raises
```

## Prior art to copy or wrap
Google Tink (keysets, primitives by purpose), libsodium (secretbox, box, secretstream), pyca Fernet, age, AWS
Encryption SDK. Wrapping one of these is usually better than building on raw primitives.

## Verify
- [ ] No call site in the codebase passes a nonce, IV or algorithm name.
- [ ] Static analysis forbids importing the hazmat layer outside the crypto package.
