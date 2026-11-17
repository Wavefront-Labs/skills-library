---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-aesgcm-and-chacha20poly1305
name: dotnet-aesgcm-and-chacha20poly1305
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, dotnet, csharp, dotnet-aesgcm, chacha20poly1305, aead, system-security-cryptography]
level: practitioner
status: docs-checked
description: "Use .NET AesGcm and ChaCha20Poly1305: the tag-size constructor, separate tag buffers, nonce generation, IsSupported checks and platform support."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.aesgcm", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.chacha20poly1305", "https://learn.microsoft.com/en-us/dotnet/standard/security/cross-platform-cryptography"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AesGcm and ChaCha20Poly1305 (.NET)

## Encrypt and decrypt with one self-describing blob
```csharp
const int NonceSize = 12, TagSize = 16;

static byte[] Encrypt(byte[] key, ReadOnlySpan<byte> plaintext, ReadOnlySpan<byte> aad)
{
    byte[] blob = new byte[NonceSize + plaintext.Length + TagSize];
    Span<byte> nonce = blob.AsSpan(0, NonceSize);
    Span<byte> ct    = blob.AsSpan(NonceSize, plaintext.Length);
    Span<byte> tag   = blob.AsSpan(NonceSize + plaintext.Length, TagSize);
    RandomNumberGenerator.Fill(nonce);
    using var aes = new AesGcm(key, TagSize);           // required tag size in bytes
    aes.Encrypt(nonce, plaintext, ct, tag, aad);
    return blob;                                         // nonce || ciphertext || tag
}

static byte[] Decrypt(byte[] key, ReadOnlySpan<byte> blob, ReadOnlySpan<byte> aad)
{
    if (blob.Length < NonceSize + TagSize) throw new CryptographicException("decrypt failed");
    var ct = blob.Slice(NonceSize, blob.Length - NonceSize - TagSize);
    byte[] pt = new byte[ct.Length];
    using var aes = new AesGcm(key, TagSize);
    aes.Decrypt(blob[..NonceSize], ct, blob[^TagSize..], pt, aad);   // throws on mismatch
    return pt;
}
```
The blob layout here is this skill's own convention. Fix your wire format and test it against every library that
reads the data.

## API details
- The `AesGcm(byte[])` constructor without a tag size is marked Obsolete; pass the required tag size.
  `Decrypt` writes plaintext only if the authentication tag can be validated, so treat any exception as a failed
  decrypt and never use the plaintext buffer after one. `Dispose` releases the instance's resources.
- `AesGcm.IsSupported` / `ChaCha20Poly1305.IsSupported` report platform support. The cross-platform cryptography
  page lists AES-GCM as unsupported in the browser, and ChaCha20Poly1305 as needing Windows 10 Build 20142+, OpenSSL
  1.1.0+ on Linux, or Android API level 28+; on iOS, tvOS and MacCatalyst support starts in .NET 9. Fail at startup
  if unsupported rather than falling back to CBC.
- Nonce and tag sizes: `AesGcm` supports only 96-bit (12-byte) nonces. Tags of 12 to 16 bytes work on Windows and
  Linux; Apple platforms allow only 16 bytes. Key sizes are 128, 192 or 256 bits.
- Nonces: 12 bytes from `RandomNumberGenerator.Fill`, never reused with a key.

## ChaCha20Poly1305
Same shape as AesGcm (key, then Encrypt/Decrypt with nonce, plaintext, ciphertext, tag and optional AAD). Check
`IsSupported` per target platform.

## Keys
`byte[] key = RandomNumberGenerator.GetBytes(32);` (GetBytes(Int32) returns a new array of cryptographically strong
random bytes) or a data key from KMS / Key Vault.

## Avoid
- `Aes.Create()` with `CipherMode.CBC`/`ECB` and no MAC.
- Building your own GCM from `AesCcm`/CTR primitives.

## Verify
- [ ] Unit tests flip bytes in nonce, ciphertext, tag and AAD and expect decryption to throw.
- [ ] Startup checks `IsSupported` on every target platform.
- [ ] Cross-language test vector decrypts.

## Checked
2026-10-28. Confirmed against the Microsoft Learn pages AesGcm, ChaCha20Poly1305, RandomNumberGenerator and
Cross-platform cryptography: constructors and the Obsolete tag-less one, `IsSupported`, platform support table
including ChaCha20Poly1305 minimums, 96-bit nonces, tag sizes, key sizes, `Decrypt` validates the tag, `GetBytes`
and `Fill`. Removed: SYSLIB id, `AuthenticationTagMismatchException` and .NET 8 gating, backend-library list,
2^32 nonce budget, cross-language layout claim, obsolete-class list, `CryptographicOperations.ZeroMemory` (page not
fetched). The C# code was not compiled or run.
Method: documentation only; no commands were run.
