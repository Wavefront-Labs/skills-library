---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-one-shot-hashdata-and-hmac
name: dotnet-one-shot-hashdata-and-hmac
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, hashdata, dotnet, sha256, hmac, one-shot-api]
level: practitioner
status: draft
description: "Use .NET one-shot static hashing APIs: SHA256.HashData, HMACSHA256.HashData, stream overloads, Span destinations, and why they beat instance Create patterns."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.sha256.hashdata", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.hmacsha256.hashdata"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .NET one-shot HashData and HMAC

## APIs (.NET 5+ for hash, .NET 6+ for HMAC)
```csharp
byte[] h  = SHA256.HashData(data);
byte[] h2 = SHA512.HashData(File.OpenRead("big.iso"));        // Stream overload, .NET 7+
byte[] t  = HMACSHA256.HashData(key, message);
Span<byte> dest = stackalloc byte[SHA256.HashSizeInBytes];
SHA256.HashData(data, dest);                                   // no allocation
byte[] s3 = SHA3_256.HashData(data);                           // .NET 8+, check SHA3_256.IsSupported
string hex = Convert.ToHexStringLower(h);                      // .NET 9+, ToHexString earlier
```
- `CryptographicOperations.HashData(HashAlgorithmName.SHA256, data)` (.NET 8+) picks by name.
- `IncrementalHash.CreateHMAC(HashAlgorithmName.SHA256, key)` for multi-part input.

## Why prefer them
- Thread-safe, no `IDisposable` to forget, fewer allocations.
- Instance objects (`SHA256.Create()`) are not thread-safe; sharing one across requests corrupts output.

## Pitfalls
- `SHA3_256.IsSupported` is false on older OS crypto libraries (Windows before 11 build 25324, older OpenSSL).
- `HMACSHA256.HashData` with an empty key is valid; validate key length yourself (>= 32 bytes).
- MD5/SHA1 one-shots exist; flag them in review unless used for non-security checksums.

## Verify
- [ ] Hash of "abc" equals the FIPS 180-4 test value in unit tests.
