---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-pbkdf2-and-randomnumbergenerator
name: dotnet-pbkdf2-and-randomnumbergenerator
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, dotnet, csharp, rfc2898derivebytes, pbkdf2, randomnumbergenerator, password-hashing]
level: practitioner
status: docs-checked
description: "Use .NET's static Rfc2898DeriveBytes.Pbkdf2 with SHA-256 and modern iterations, avoid SHA-1 constructor defaults, and get random bytes and tokens from RandomNumberGenerator."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.rfc2898derivebytes.pbkdf2", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.randomnumbergenerator", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rfc2898DeriveBytes.Pbkdf2 and RandomNumberGenerator (.NET)

## PBKDF2: use the static method
```csharp
byte[] salt = RandomNumberGenerator.GetBytes(16);
byte[] hash = Rfc2898DeriveBytes.Pbkdf2(
    password: passwordUtf8,              // byte[] or ReadOnlySpan<char>
    salt: salt,
    iterations: 600_000,
    hashAlgorithm: HashAlgorithmName.SHA256,
    outputLength: 32);
```
- The static `Rfc2898DeriveBytes.Pbkdf2` takes the hash algorithm and iteration count explicitly; supported
  hashes are SHA1, SHA256, SHA384 and SHA512. Prefer it to the constructors, whose defaults you would otherwise
  have to look up.
- Iterations (OWASP Password Storage Cheat Sheet): PBKDF2-HMAC-SHA256 600,000; PBKDF2-HMAC-SHA512 220,000;
  HMAC-SHA1 is legacy only. Store algorithm, iterations, salt and hash together, e.g.
  `pbkdf2-sha256$600000$<salt b64>$<hash b64>`, so you can raise the cost.
- Compare hashes with a fixed-time comparison (`CryptographicOperations.FixedTimeEquals`), never `SequenceEqual`.
- OWASP prefers Argon2id (minimum 19 MiB memory, 2 iterations, 1 degree of parallelism); use PBKDF2 when FIPS-140
  compliance is required.

## Random numbers
```csharp
byte[] key   = RandomNumberGenerator.GetBytes(32);
RandomNumberGenerator.Fill(span);                       // fill an existing buffer
int    pick  = RandomNumberGenerator.GetInt32(0, 6);    // unbiased range [0, 6)
string token = Convert.ToBase64String(RandomNumberGenerator.GetBytes(32))
               .TrimEnd('=').Replace('+', '-').Replace('/', '_');   // URL-safe
string hex   = RandomNumberGenerator.GetHexString(32);
string code  = RandomNumberGenerator.GetString("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", 10);
```
- The static methods on `RandomNumberGenerator` are documented as cryptographically strong; `Create()` returns an
  instance of the default implementation, but the static methods are simpler. `Shuffle` and `GetItems` also use
  cryptographic randomness.
- `System.Random` is not documented as cryptographically strong: never use it for tokens, salts or IDs that grant
  access.
- Use `GetBytes(32)` for secrets rather than `Guid.NewGuid()`.

## Verify
- [ ] No `new Rfc2898DeriveBytes(` relying on default hash or iteration count.
- [ ] Password hashes record parameters and use fixed-time comparison.
- [ ] Grep finds no `new Random(` in security code.

## Checked
2026-10-28. Confirmed against the Microsoft Learn pages Rfc2898DeriveBytes.Pbkdf2 and RandomNumberGenerator and the
OWASP Password Storage Cheat Sheet: `Pbkdf2` overloads and supported hashes, OWASP iteration counts (600,000 SHA-256,
220,000 SHA-512), Argon2id minimums, PBKDF2 for FIPS, `GetBytes`, `Fill`, `GetInt32`, `GetHexString`, `GetString`,
`Create`, `Shuffle`. Corrected: SHA-512 iterations were 210,000 (OWASP says 220,000). Removed: constructor default
claims, SYSLIB ids, .NET version gates, PasswordHasher<T> details, library names, thread-safety and OS backend
claims, Guid bit count. The C# code was not compiled or run.
Method: documentation only; no commands were run.
