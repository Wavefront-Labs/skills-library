---
id: computing-software.systems-network-administration.pki-tls-administration.schannel-registry-hardening
name: schannel-registry-hardening
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [schannel-registry-hardening, pki-windows-tls, schannel, windows-tls, ssl-cipher-suite-order, iiscrypto, pki-tls-administration]
level: practitioner
status: draft
description: "Control Windows TLS versions and cipher suites with Schannel registry keys and Group Policy, and verify with scanners."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/tls/tls-registry-settings
  - https://learn.microsoft.com/en-us/powershell/module/tls/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schannel protocol and cipher hardening
Goal: the Windows TLS stack negotiates only approved protocols and suites.
Registry: `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server`
```powershell
$p = 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Server'
New-Item $p -Force | Out-Null
New-ItemProperty $p -Name Enabled -Value 0 -PropertyType DWord -Force
New-ItemProperty $p -Name DisabledByDefault -Value 1 -PropertyType DWord -Force
```
- Repeat for SSL 3.0, TLS 1.0, TLS 1.1 (Server and Client).
- Cipher suites: `Get-TlsCipherSuite`, `Disable-TlsCipherSuite -Name TLS_RSA_WITH_3DES_EDE_CBC_SHA`, or GPO "SSL Cipher Suite Order".
- TLS 1.3 server support: Windows Server 2022+ (confirm).
- .NET apps: set `SchUseStrongCrypto` and `SystemDefaultTlsVersions` in the .NET registry keys.
- Tool: IIS Crypto GUI applies a template.
- Reboot required.
Gotcha: disabling TLS 1.0 client-side breaks old SQL Server and RDP clients; test dependencies.
Verify:
- [ ] `nmap --script ssl-enum-ciphers -p 443 host` shows no TLS 1.0/1.1.
- [ ] Application event logs show no Schannel 36874/36888 errors after reboot.
