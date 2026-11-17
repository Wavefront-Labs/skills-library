---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-certificate-validation-callbacks
name: dotnet-certificate-validation-callbacks
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, servercertificatecustomvalidationcallback, dotnet, csharp, httpclient, certificate-validation, custom-trust-store, x509chain, pinning]
level: practitioner
status: draft
description: "Replace dangerous ServerCertificateCustomValidationCallback code in .NET HttpClient with chain building against a custom root, pinning done right, and tests."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.net.http.httpclienthandler.servercertificatecustomvalidationcallback", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509chainpolicy", "https://learn.microsoft.com/en-us/dotnet/api/system.net.http.socketshttphandler.ssloptions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .NET certificate validation callbacks

## The anti-pattern
```csharp
handler.ServerCertificateCustomValidationCallback = (msg, cert, chain, errors) => true;          // accepts anything
handler.ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator;
```
Both disable TLS authentication. Search for them: `rg "ServerCertificateCustomValidationCallback|RemoteCertificateValidationCallback|DangerousAcceptAny"`.

## Private CA, done right (.NET 7+)
```csharp
var handler = new SocketsHttpHandler {
    SslOptions = new SslClientAuthenticationOptions {
        CertificateChainPolicy = new X509ChainPolicy {
            TrustMode = X509ChainTrustMode.CustomRootTrust,
            CustomTrustStore = { corpRoot },
            RevocationMode = X509RevocationMode.NoCheck,     // or Online if your CA publishes CRL/OCSP
        }
    }
};
var http = new HttpClient(handler);
```
Hostname validation still happens. No callback needed.

## If you must use a callback (older .NET)
```csharp
bool Validate(HttpRequestMessage m, X509Certificate2? cert, X509Chain? _, SslPolicyErrors errors) {
    if (cert is null) return false;
    if ((errors & ~SslPolicyErrors.RemoteCertificateChainErrors) != 0) return false;   // name mismatch etc.
    using var chain = new X509Chain();
    chain.ChainPolicy.TrustMode = X509ChainTrustMode.CustomRootTrust;
    chain.ChainPolicy.CustomTrustStore.Add(corpRoot);
    chain.ChainPolicy.RevocationMode = X509RevocationMode.NoCheck;
    return chain.Build(cert);
}
```
Never ignore `RemoteCertificateNameMismatch` or `RemoteCertificateNotAvailable`.

## Pinning
Pin the SPKI hash of an intermediate or your own key, in addition to (not instead of) chain validation, and ship a
backup pin. Compare `SHA256(cert.PublicKey.ExportSubjectPublicKeyInfo())`.

## Verify
- [ ] Test against a self-signed cert, wrong hostname, and expired cert: all fail.
- [ ] Code search finds no `=> true` validators.
