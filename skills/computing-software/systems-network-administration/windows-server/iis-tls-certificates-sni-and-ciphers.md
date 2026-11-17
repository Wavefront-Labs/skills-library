---
id: computing-software.systems-network-administration.windows-server.iis-tls-certificates-sni-and-ciphers
name: iis-tls-certificates-sni-and-ciphers
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, iis, iis-administration, iis-tls, sni, tls-hardening, schannel, cipher-suites, centralized-certificate-store, schannel-protocol-hardening]
level: advanced
status: docs-checked
description: "Secure IIS with TLS: SNI bindings, certificate renewal and rebinding, Centralized Certificate Store, disabling TLS 1.0/1.1 in SCHANNEL, cipher order and HSTS."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/tls/tls-registry-settings
  - https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-8/iis-80-server-name-indication-sni-ssl-scalability
  - https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-85/certificate-rebind-in-iis85
  - https://learn.microsoft.com/en-us/iis/get-started/whats-new-in-iis-8/iis-80-centralized-ssl-certificate-support-ssl-scalability-and-manageability
  - https://learn.microsoft.com/en-us/powershell/module/iisadministration/new-iissitebinding
  - https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/hsts
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IIS TLS certificates, SNI and cipher hardening

## SNI bindings
SNI (IIS 8.0 and later) lets many HTTPS sites share one IP and port, each binding `*:443:host` with the SNI flag.
Without SNI, one certificate per IP and port.

## Renew a certificate
Import the new PFX, then rebind:
```powershell
$new = Import-PfxCertificate -FilePath '<vol>:\certs\shop.pfx' -CertStoreLocation Cert:\LocalMachine\My -Password $pw
Remove-IISSiteBinding -Name shop -BindingInformation '*:443:shop.example.com' -Protocol https -Confirm:$false
New-IISSiteBinding -Name shop -BindingInformation '*:443:shop.example.com' -Protocol https -CertificateThumbPrint $new.Thumbprint -CertStoreLocation Cert:\LocalMachine\My -SslFlag Sni
```
Certificate Rebind (IIS 8.5 and later) rebinds a renewed certificate automatically; enable it for all HTTPS sites
on the server in the Server Certificates dialog in IIS Manager. Centralized SSL Certificate Support (IIS 8.0, an
optional component) loads certificates from a file share on demand, named `<CN>.pfx` (wildcards as `_.domain.pfx`),
which suits web farms: bind with `-SslFlag CentralCertStore`.

## Protocols (SCHANNEL registry)
Each protocol version has a subkey under
`HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\<version>\Server` (and `\Client`). Create
the DWORD `Enabled` = 0 to disable a version (1 to enable); `DisabledByDefault` controls the default state. Disabling
versions can break interoperability, and AcquireCredentialsHandle can fail if no version stays enabled. Test before
rolling out and check the Microsoft page for the exact semantics on your Windows version.
```powershell
foreach ($p in 'TLS 1.0','TLS 1.1') { foreach ($s in 'Server','Client') {
  $k="HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\$p\$s"
  New-Item $k -Force | Out-Null
  New-ItemProperty $k Enabled 0 -PropertyType DWord -Force | Out-Null
  New-ItemProperty $k DisabledByDefault 1 -PropertyType DWord -Force | Out-Null } }
```

## Ciphers
```powershell
Get-TlsCipherSuite | Select-Object Name
Disable-TlsCipherSuite -Name '<cipher-suite-name>'
```
Per-binding flags (`New-IISSiteBinding -SslFlag`) include DisableLegacyTLS, DisableTLS13, DisableHTTP2 and
DisableOCSPStp. OCSP stapling is on by default only for simple SSL/TLS bindings; check the Microsoft TLS page for
the binding types where it is not.

## HSTS (IIS 10.0 version 1709 and later)
Set per site in the `hsts` element (`enabled`, `max-age`, `includeSubDomains`, `preload`, `redirectHttpToHttps`),
for example `appcmd set config -section:system.applicationHost/sites "/[name='shop'].hsts.enabled:True" /commit:apphost`.

## Verify
- [ ] An external TLS scan shows only the protocol versions and suites you intend; the certificate chain is complete.

## Checked
Date 2026-10-27. Documentation: Windows Server TLS registry settings, IIS 8.0 SNI and Centralized SSL Certificate
pages, IIS 8.5 Certificate Rebind page, IISAdministration New-IISSiteBinding, Remove-IISSiteBinding, Tls
Get/Disable-TlsCipherSuite pages, IIS hsts reference. Confirmed: registry value names and meaning, SslFlag values,
CCS naming, rebind feature. TLS 1.3 defaults and .NET registry values are not stated here.
Method: documentation only; no commands were run.
