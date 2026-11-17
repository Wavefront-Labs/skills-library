---
id: computing-software.systems-network-administration.powershell.tls-and-certificate-handling-web-requests
name: tls-and-certificate-handling-web-requests
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, invoke-restmethod, skipcertificatecheck, tls12, securityprotocol, client-certificates, certificate-validation, proxy]
level: practitioner
status: docs-checked
description: "Fix TLS and certificate errors in PowerShell web requests: TLS 1.2 on 5.1, -SkipCertificateCheck risks, trusting an internal CA, client certificate auth and proxies."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest
  - https://learn.microsoft.com/en-us/dotnet/framework/network-programming/tls
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS and certificate handling in web requests

## TLS errors in Windows PowerShell 5.1 (.NET Framework)
Per Microsoft's .NET Framework TLS guidance, two registry values control outgoing TLS behaviour for .NET Framework apps. They do not exist by default and must be added manually under `HKLM\SOFTWARE\[Wow6432Node\]Microsoft\.NETFramework\<VERSION>`, where `<VERSION>` is `v4.0.30319` (.NET Framework 4 and above) or `v2.0.50727` (3.5):
- `SchUseStrongCrypto` (DWORD): `1` uses strong cryptography (TLS 1.2 and 1.3, blocks insecure protocols). Defaults to 1 for apps targeting .NET 4.6+ and 0 for 4.5.2 or earlier.
- `SystemDefaultTlsVersions` (DWORD): `1` lets the operating system choose the protocol. Defaults to 1 for apps targeting .NET 4.7+ and 0 for 4.6.1 or earlier.
```powershell
foreach ($p in 'HKLM:\SOFTWARE\Microsoft\.NETFramework\v4.0.30319', 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319') {
  Set-ItemProperty $p -Name SchUseStrongCrypto -Value 1 -Type DWord
  Set-ItemProperty $p -Name SystemDefaultTlsVersions -Value 1 -Type DWord
}
```
Both keys have the same effect for HTTP (ServicePointManager) and TCP sockets (SslStream). Restart the process afterwards. Do not set `SchUseStrongCrypto` to 0 except to reach legacy services that cannot be upgraded.

`Invoke-RestMethod`/`Invoke-WebRequest -SslProtocol` (PowerShell 6.0+) limits the permitted protocols per call; by default all protocols supported by the system are allowed. Values combine as flags (array or comma-separated). `Tls13` is accepted from PowerShell 7.1.

## Certificate validation errors
Diagnose the failing certificate (name, expiry, chain) with your platform's certificate tools or the .NET `SslStream` documentation, then fix the cause in this order:
1. Use the name that is in the certificate's subject alternative names.
2. Trust the internal root CA in the OS trust store (or distribute it by GPO).
3. Renew an expired server certificate.

## -SkipCertificateCheck (PowerShell 6.0+): lab only
```powershell
Invoke-RestMethod -Uri https://10.0.0.5/api -SkipCertificateCheck
```
It skips all certificate validation (expiration, revocation, trusted root, and so on). Microsoft's warning: this is not secure and is intended only for known hosts with a self-signed certificate for testing. Never use it in production automation.

## Client certificate authentication
```powershell
$cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object { $_.Thumbprint -eq '<THUMBPRINT>' }
Invoke-RestMethod -Uri https://api.internal.example/v1/status -Certificate $cert
```
`-Certificate` takes an X509 client certificate; find one with `Get-PfxCertificate` or `Get-ChildItem` on the `Cert:` drive. The alternative `-CertificateThumbprint` maps only to local user accounts, not domain accounts.

## Proxies
```powershell
Invoke-RestMethod -Uri $u -Proxy 'http://proxy.example:8080' -ProxyUseDefaultCredentials
```
`-Proxy` takes a URI (PowerShell 6.0+). `-ProxyUseDefaultCredentials` works only together with `-Proxy` and cannot be combined with `-ProxyCredential`. From PowerShell 7.0, proxy settings from the `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` and `NO_PROXY` environment variables are supported.

## Verify
- [ ] Requests succeed without `-SkipCertificateCheck` in production scripts (search the repo).
- [ ] The two registry values above are set on 5.1 hosts that need them.

## Checked
Date: 2026-11-02. Confirmed against Microsoft Learn: .NET Framework TLS best practices (registry keys, paths, defaults), Invoke-RestMethod (SkipCertificateCheck, SslProtocol, Certificate, CertificateThumbprint, Proxy, ProxyUseDefaultCredentials, environment variables). Removed: the 5.1 per-session SecurityProtocol line, "PowerShell 7 uses OS defaults", the PSGallery claim, the SslStream diagnostic snippet and Import-Certificate command, private-key/EKU advice, WinINET and netsh winhttp proxy claims, 5.1 callback override claim.
Method: documentation only; no commands were run.
