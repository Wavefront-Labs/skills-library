---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-loading-x509certificate2-and-private-keys
name: dotnet-loading-x509certificate2-and-private-keys
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, dotnet, csharp, x509certificate2, x509certificateloader, pkcs12, pem, key-storage-flags]
level: advanced
status: draft
description: "Load certificates and private keys in .NET: X509CertificateLoader in .NET 9+, PEM pairs, PFX key storage flags, Windows ephemeral key quirks, disposal and stores."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509certificateloader", "https://learn.microsoft.com/en-us/dotnet/fundamentals/syslib-diagnostics/syslib0057", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509certificate2.createfrompemfile"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loading X509Certificate2 and private keys (.NET)

## .NET 9+: X509CertificateLoader
The `X509Certificate2(byte[])` / `(string path, string password)` constructors are obsolete
(SYSLIB0057) because they guessed the format. Say what you are loading:
```csharp
using X509Certificate2 cert = X509CertificateLoader.LoadCertificateFromFile("leaf.cer"); // DER or PEM cert
using X509Certificate2 pfx  = X509CertificateLoader.LoadPkcs12FromFile(
    "api.pfx", password, X509KeyStorageFlags.EphemeralKeySet);
X509Certificate2Collection all = X509CertificateLoader.LoadPkcs12CollectionFromFile("api.pfx", password);
```
`Pkcs12LoaderLimits` caps iteration counts and sizes so a hostile PFX can't burn CPU; keep the
defaults for untrusted input.

## PEM certificate + key
```csharp
using var cert = X509Certificate2.CreateFromPemFile("fullchain.pem", "privkey.pem");
// encrypted key: CreateFromEncryptedPemFile(certPath, password, keyPath)
```
On Windows, `SslStream` can't use the resulting ephemeral key in some versions
(`The credentials supplied to the package were not recognized`). Workaround:
```csharp
using var usable = X509CertificateLoader.LoadPkcs12(cert.Export(X509ContentType.Pkcs12), null);
```

## Key storage flags (PFX)
| Flag | Effect |
|---|---|
| `EphemeralKeySet` | key kept in memory only; best default for services that load from files/secrets |
| `MachineKeySet` | key stored in the machine key store (services without a user profile) |
| `PersistKeySet` | key stays on disk after disposal; only when importing into a store |
| `Exportable` | key can be exported again; leave off |
| `UserKeySet` | current user's store (default) |
Loading PFX files repeatedly on Windows without `EphemeralKeySet` leaves key files behind in the
machine/user key directories until disposal or forever with `PersistKeySet`; long-running services
leak thousands of files. Always dispose certificates.

## Getting the key
```csharp
using RSA? rsa = cert.GetRSAPrivateKey();     // new object each call: dispose it
using ECDsa? ec = cert.GetECDsaPrivateKey();
if (!cert.HasPrivateKey) throw new InvalidOperationException("no private key");
```
Attach a key you loaded separately: `cert.CopyWithPrivateKey(ecKey)`.

## Stores
```csharp
using var store = new X509Store(StoreName.My, StoreLocation.LocalMachine);
store.Open(OpenFlags.ReadOnly);
var found = store.Certificates.Find(X509FindType.FindByThumbprint, thumbprint, validOnly: false);
```
`validOnly: true` runs chain validation and silently drops certs with untrusted roots, a common
"certificate not found" cause. On Linux, the `My` store is a per-user directory managed by .NET;
the `Root` store is read-only from the OpenSSL bundle.

## Verify
- [ ] No SYSLIB0057 warnings remain (treat as errors).
- [ ] Services load PFX with `EphemeralKeySet` (or from PEM) and dispose certificate objects.
- [ ] `HasPrivateKey` is checked at startup for server certificates.
