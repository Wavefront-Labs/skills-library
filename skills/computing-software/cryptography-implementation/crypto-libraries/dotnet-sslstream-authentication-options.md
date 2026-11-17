---
id: computing-software.cryptography-implementation.crypto-libraries.dotnet-sslstream-authentication-options
name: dotnet-sslstream-authentication-options
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, sslstream, dotnet, csharp, tls, sslclientauthenticationoptions, x509chainpolicy, alpn, mtls]
level: practitioner
status: draft
description: "Use .NET SslStream with SslClientAuthenticationOptions and SslServerAuthenticationOptions: OS-default protocols, ALPN, revocation, client certs and custom trust."
sources: ["https://learn.microsoft.com/en-us/dotnet/api/system.net.security.sslstream", "https://learn.microsoft.com/en-us/dotnet/api/system.net.security.sslclientauthenticationoptions", "https://learn.microsoft.com/en-us/dotnet/framework/network-programming/tls"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .NET SslStream authentication options

## Client
```csharp
using var tcp = new TcpClient();
await tcp.ConnectAsync("api.internal", 443);
using var ssl = new SslStream(tcp.GetStream(), leaveInnerStreamOpen: false);
await ssl.AuthenticateAsClientAsync(new SslClientAuthenticationOptions {
    TargetHost = "api.internal",                                    // SNI + hostname validation
    EnabledSslProtocols = SslProtocols.None,                        // let the OS choose (recommended)
    CertificateRevocationCheckMode = X509RevocationMode.Online,
    ApplicationProtocols = new() { SslApplicationProtocol.Http2, SslApplicationProtocol.Http11 },
    ClientCertificates = new X509CertificateCollection { clientCert },   // mTLS
    CertificateChainPolicy = new X509ChainPolicy {                  // .NET 7+: custom root without callbacks
        TrustMode = X509ChainTrustMode.CustomRootTrust,
        CustomTrustStore = { corpRoot },
        RevocationMode = X509RevocationMode.NoCheck,
    },
});
Console.WriteLine($"{ssl.SslProtocol} {ssl.NegotiatedCipherSuite} {ssl.NegotiatedApplicationProtocol}");
```

## Server
```csharp
var ctx = SslStreamCertificateContext.Create(serverCert, intermediates, offline: false);
await ssl.AuthenticateAsServerAsync(new SslServerAuthenticationOptions {
    ServerCertificateContext = ctx,              // sends the full chain, enables OCSP stapling where supported
    ClientCertificateRequired = true,
    RemoteCertificateValidationCallback = ValidateClient,
    EnabledSslProtocols = SslProtocols.None,
});
```
`ServerCertificateSelectionCallback` picks certificates per SNI name.

## Platform notes
- Windows uses SChannel, Linux uses OpenSSL, macOS uses Apple Security/Network framework; cipher suite control via
  `CipherSuitesPolicy` works on Linux/macOS only (Windows uses OS policy).
- `EnabledSslProtocols = SslProtocols.Tls12 | SslProtocols.Tls13` hard-codes versions and blocks future ones; prefer
  `None` and control versions at the OS.

## Verify
- [ ] Negotiated protocol and ALPN logged on first connection.
- [ ] Untrusted or wrong-host server certificate fails authentication.
