---
id: computing-software.software-engineering.csharp-dotnet.aesgcm-password-hashing-and-key-vault
name: aesgcm-password-hashing-and-key-vault
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-security, aesgcm, password-hashing, azure-key-vault, pbkdf2, argon2, cryptography]
level: advanced
status: draft
description: "Correct .NET cryptography: AES-GCM authenticated encryption with unique nonces, password hashing (PBKDF2 or Argon2id) with constant-time compare, and secrets/keys from Azure Key Vault."
sources: ["https://learn.microsoft.com/en-us/dotnet/standard/security/cryptography-model", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.aesgcm", "https://learn.microsoft.com/en-us/azure/key-vault/general/developers-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AES-GCM, password hashing and Key Vault

## AES-GCM (authenticated encryption)
```csharp
static byte[] Encrypt(byte[] key, byte[] plain, byte[] aad)
{
    var nonce = RandomNumberGenerator.GetBytes(12);                       // 96-bit, UNIQUE per key; never reuse
    var cipher = new byte[plain.Length]; var tag = new byte[16];
    using var gcm = new AesGcm(key, tagSizeInBytes: 16);                  // key 32 bytes (AES-256)
    gcm.Encrypt(nonce, plain, cipher, tag, aad);
    return [.. nonce, .. tag, .. cipher];                                 // store nonce|tag|ciphertext
}
static byte[] Decrypt(byte[] key, byte[] blob, byte[] aad)
{
    var nonce = blob[..12]; var tag = blob[12..28]; var cipher = blob[28..]; var plain = new byte[cipher.Length];
    using var gcm = new AesGcm(key, 16);
    gcm.Decrypt(nonce, cipher, tag, plain, aad);                          // throws CryptographicException if tampered
    return plain;
}
```
Nonce reuse with the same key destroys confidentiality and authenticity: use random 96-bit nonces (safe for about 2^32 messages per key) then rotate keys. The `AesGcm(key, tagSize)` constructor is required from .NET 8 (the one-arg form is obsolete). Prefer `ChaCha20Poly1305` where AES hardware is absent. Never use ECB/CBC-without-MAC, or roll your own mode. Bind context via AAD (e.g., record id).

## Password hashing
```csharp
byte[] salt = RandomNumberGenerator.GetBytes(16);
byte[] hash = Rfc2898DeriveBytes.Pbkdf2(password, salt, iterations: 600_000, HashAlgorithmName.SHA256, 32);   // OWASP 2023 for SHA-256
bool ok = CryptographicOperations.FixedTimeEquals(hash, expected);                                            // constant-time
```
Store algorithm id, iterations, salt and hash together so parameters can be upgraded on login. PBKDF2 is built-in; **Argon2id** (Konscious.Security.Cryptography, Isopoh) is preferred for new systems (memory-hard). ASP.NET Identity's `PasswordHasher<T>` already does this correctly: use it for user passwords. Never SHA-256/MD5 plain, never store reversible passwords. Pepper (secret key) kept in Key Vault is optional hardening.

## Azure Key Vault
```csharp
var cred = new DefaultAzureCredential();                              // managed identity in Azure, dev login locally
var secrets = new SecretClient(new Uri("https://acme.vault.azure.net/"), cred);
KeyVaultSecret s = (await secrets.GetSecretAsync("Db--Password")).Value;
builder.Configuration.AddAzureKeyVault(new Uri("https://acme.vault.azure.net/"), cred);        // secrets as configuration; "--" maps to ":"
var crypto = new CryptographyClient(new Uri(keyId), cred);            // wrap/unwrap data keys, sign without exporting key material
```
Envelope encryption: generate a data key per record, encrypt data with AES-GCM, wrap the data key with a Key Vault key. Use RBAC (Key Vault Secrets User), soft delete and purge protection, private endpoints, and rotation with versioned secrets. Cache secrets; Key Vault throttles.

## Gotchas
- `Random` is not cryptographic: use `RandomNumberGenerator`.
- Compare MACs/hashes with `FixedTimeEquals`, not `SequenceEqual`.
- Keep keys out of source/logs; zero sensitive buffers (`CryptographicOperations.ZeroMemory`) where practical.
- Don't invent protocols: use libraries (Data Protection API for app-level cookies/tokens).

## Verify
Encrypt/decrypt round-trips; flipping one ciphertext byte throws; two encryptions of the same plaintext differ; password check passes for correct and fails for wrong with timing independent of input.
