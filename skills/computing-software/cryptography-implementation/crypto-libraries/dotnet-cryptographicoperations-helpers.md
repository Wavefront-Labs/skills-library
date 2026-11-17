---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-cryptographicoperations-helpers
name: dotnet-cryptographicoperations-helpers
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, fixedtimeequals, zeromemory, dotnet, constant-time-compare, secure-memory]
level: practitioner
status: docs-checked
description: "Use .NET CryptographicOperations.FixedTimeEquals and ZeroMemory: constant-time tag comparison, wiping spans, limits with managed strings."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.cryptographicoperations", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.cryptographicoperations.zeromemory"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CryptographicOperations helpers

## FixedTimeEquals
```csharp
byte[] expected = CryptographicOperations.HmacData(HashAlgorithmName.SHA256, key, body);
if (!CryptographicOperations.FixedTimeEquals(expected, receivedTag)) return Unauthorized();
```
- Compares two byte sequences in time that depends on their length, not their values.
- Replace `SequenceEqual`, `==` on strings, and `Convert.ToBase64String(a) == b` comparisons.
- Decode the received hex/base64 tag to bytes first, then compare bytes.

## ZeroMemory
```csharp
byte[] key = new byte[32];
// fill key from a CSPRNG
try { /* use key */ }
finally { CryptographicOperations.ZeroMemory(key); }

Span<byte> tmp = stackalloc byte[32];
// ... use tmp ...
CryptographicOperations.ZeroMemory(tmp);
```
The docs say `ZeroMemory` exists to guard against runtime optimizations that could drop writes not followed by reads,
though none are planned for .NET.

## Limits
- `string` secrets are immutable and may be interned or copied; keep secrets in `byte[]`/`char[]`.

## Verify
- [ ] grep finds no `SequenceEqual`/`==` comparisons on tags, tokens or hashes.

## Checked
2026-11-01. Confirmed on the Microsoft Learn CryptographicOperations pages: `FixedTimeEquals(ReadOnlySpan<byte>,
ReadOnlySpan<byte>)` (time depends on length, not values), `HmacData(HashAlgorithmName, byte[], byte[])`, and
`ZeroMemory(Span<byte>)` with its remark on future-proofing against write-eliminating optimizations. Removed: GC
pinning, Array.Clear comparison and platform-key claims.
Method: documentation only; no commands were run.
