---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-importfrompem-for-rsa-and-ecdsa
name: dotnet-importfrompem-for-rsa-and-ecdsa
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, importfrompem, dotnet, rsa, ecdsa, pem, x509certificate2]
level: practitioner
status: draft
description: "Load PEM keys in .NET 5+ with RSA, ECDsa and X509Certificate2 ImportFromPem and ImportFromEncryptedPem: supported labels, CreateFromPemFile and Windows key quirks."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.asymmetricalgorithm.importfrompem", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509certificate2.createfrompemfile"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .NET ImportFromPem

## Keys
```csharp
using var rsa = RSA.Create();
rsa.ImportFromPem(File.ReadAllText("key.pem"));          // PRIVATE KEY, RSA PRIVATE KEY, PUBLIC KEY, RSA PUBLIC KEY

using var ec = ECDsa.Create();
ec.ImportFromEncryptedPem(File.ReadAllText("ec-enc.pem"), password);   // ENCRYPTED PRIVATE KEY (PKCS#8)
```
- Supported labels: `PRIVATE KEY`, `PUBLIC KEY`, `ENCRYPTED PRIVATE KEY`, plus algorithm specific (`RSA PRIVATE
  KEY`, `EC PRIVATE KEY`).
- A file with multiple PEM blocks throws `ArgumentException`; strip extra blocks first.
- Export: `rsa.ExportPkcs8PrivateKeyPem()`, `ExportSubjectPublicKeyInfoPem()` (.NET 7+).

## Certificates with keys
```csharp
var cert = X509Certificate2.CreateFromPemFile("tls.crt", "tls.key");
```
On Windows, the key is ephemeral; SslStream server auth may fail with
`No credentials are available in the security package`. Re-import through PKCS#12:
```csharp
cert = X509CertificateLoader.LoadPkcs12(cert.Export(X509ContentType.Pkcs12), null);  // .NET 9+
```
(older: `new X509Certificate2(cert.Export(X509ContentType.Pfx))`).

## Pitfalls
- Using `RSACryptoServiceProvider` (CAPI) on modern code; use `RSA.Create()`.
- `ImportFromPem` on a certificate file: use `X509Certificate2.CreateFromPem` instead.

## Verify
- [ ] Sign/verify round trip; on Windows test SslStream with the loaded cert.
