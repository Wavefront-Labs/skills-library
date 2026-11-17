---
id: computing-software.cryptography-implementation.crypto-libraries.aspnet-core-data-protection-key-management
name: aspnet-core-data-protection-key-management
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, dotnet, csharp, data-protection-api, key-ring, aspnet-core, cookie-encryption]
level: advanced
status: docs-checked
description: "Configure ASP.NET Core Data Protection for real deployments: shared persistent key ring, encryption of keys at rest, application name, purposes and key lifetime."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/security/data-protection/configuration/overview", "https://learn.microsoft.com/en-us/aspnet/core/security/data-protection/implementation/key-management", "https://learn.microsoft.com/en-us/aspnet/core/security/data-protection/consumer-apis/purpose-strings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ASP.NET Core Data Protection keys

Data Protection encrypts auth cookies, antiforgery tokens, TempData and anything you pass to
`IDataProtector.Protect`. Its default key storage suits a single developer machine and fails in
containers and farms.

## Symptom of a bad setup
After a deploy, restart or scale-out users get logged out and forms fail antiforgery validation because each
instance or container restart generated its own keys, or because instances do not share a key ring and
application name.

## Production configuration
```csharp
builder.Services.AddDataProtection()
    .SetApplicationName("contoso-web")                       // same on every instance that shares cookies
    .PersistKeysToAzureBlobStorage(blobUri, credential)      // or PersistKeysToDbContext / PersistKeysToFileSystem
    .ProtectKeysWithAzureKeyVault(keyIdentifier, credential) // or ProtectKeysWithCertificate
    .SetDefaultKeyLifetime(TimeSpan.FromDays(90));           // default is 90 days; minimum 7
```
- **Persist** the key ring somewhere shared and durable. `PersistKeysToFileSystem` accepts a UNC share.
- **Protect** keys at rest. If you change the persistence location the system no longer encrypts keys at rest
  automatically (it cannot know that DPAPI is appropriate). Call a `ProtectKeysWith*` API such as
  `ProtectKeysWithAzureKeyVault` or `ProtectKeysWithCertificate`.
- **Application name**: `SetApplicationName` sets the app's unique name and should match across deployments of
  the app. By default apps are isolated by content root path, even with a shared key repository, which also means
  different paths across hosts break sharing. With a shared repository, give apps that must share payloads the
  same name and apps that must not share payloads different names.

## Purposes
```csharp
var protector = provider.CreateProtector("Contoso.PasswordReset.v1");
string token = protector.Protect(userId);
```
The purpose string derives subkeys unique to the consumer, isolating it from all other consumers even when the
root keys are the same. It need not be secret, only unique. Appending a version (`.v1`) lets a later version use
a fully isolated purpose. Never let untrusted user input be the sole source of the purposes chain.

## Key lifecycle
- A new key gets an activation date of now + 2 days and an expiration of now + 90 days (the 2-day delay lets
  it propagate). If the default key expires within 2 days and no successor exists, a new key is persisted
  automatically. Created, active and expired keys can still unprotect payloads. The key ring is re-read about
  every 24 hours or when the default key expires.
- Revoked keys by default cannot unprotect payloads, so revoking logs users out. In a multi-instance deployment
  other instances learn of a revocation only at their next key-ring refresh; restart them if it must be immediate.
- Never delete a key from the ring (for example by deleting its file): everything it protected becomes permanently
  unreadable.
- Data Protection is for **short-lived** payloads. For long-term data at rest (database columns,
  files), use envelope encryption with a KMS-managed key; Data Protection keys can be lost, revoked
  or rotated in ways that make old data unreadable.

## Verify
- [ ] Restarting all instances doesn't log users out.
- [ ] Keys are encrypted at rest by an explicit `ProtectKeysWith*` call.
- [ ] Key storage location is backed up and access-controlled like a secret.

## Checked
2026-10-28. Confirmed against the Microsoft Learn ASP.NET Core Data Protection pages (Configuration overview, Key
management, Purpose strings): persistence and protection APIs, no automatic encryption after changing the
location, `SetApplicationName` and path-based isolation, 2-day activation delay, 90-day lifetime, 7-day minimum,
24-hour refresh, revoked and deleted key behaviour, multi-instance revocation caveat, purpose-string isolation.
Removed: log message texts, the Redis option, community AWS/GCP packages, the plain-XML-on-Linux statement,
time-limited protector, `RevokeAllKeys` method name (not on these pages). The C# code was not compiled or run.
Method: documentation only; no commands were run.
