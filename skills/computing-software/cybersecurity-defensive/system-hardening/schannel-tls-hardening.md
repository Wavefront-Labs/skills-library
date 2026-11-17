---
id: computing-software.cybersecurity-defensive.system-hardening.schannel-tls-hardening
name: schannel-tls-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [schannel-hardening, tls, windows-hardening, cipher-suites, tls-1-0-disable, dotnet-strong-crypto]
level: practitioner
status: docs-checked
description: "Harden Windows SCHANNEL: disable old SSL/TLS protocols via registry, set cipher suite order by GPO or the TLS PowerShell module, enable .NET strong crypto, and test impact."
sources: ["https://learn.microsoft.com/en-us/windows-server/security/tls/tls-registry-settings", "https://learn.microsoft.com/en-us/windows-server/security/tls/manage-tls", "https://learn.microsoft.com/en-us/dotnet/framework/network-programming/tls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCHANNEL TLS hardening

SCHANNEL is the Windows TLS/SSL provider (a Security Support Provider). Its settings are machine-wide and do not
affect third-party TLS libraries installed on the system.

## Protocols (registry)
Base key: `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\<Protocol> <Version>\{Server|Client}`
(for example `TLS 1.2\Server`, `SSL 3.0\Client`). A DWORD `Enabled` of 0 disables the version and 1 enables it,
overriding the system default; `DisabledByDefault` (0 or 1) is also read.
```powershell
foreach ($p in 'SSL 3.0','TLS 1.0','TLS 1.1') {
  foreach ($side in 'Server','Client') {
    $k = "HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\$p\$side"
    New-Item $k -Force | Out-Null
    New-ItemProperty $k -Name Enabled -Value 0 -PropertyType DWord -Force | Out-Null
    New-ItemProperty $k -Name DisabledByDefault -Value 1 -PropertyType DWord -Force | Out-Null
  }
}
```
Notes from Microsoft Learn:
- TLS 1.0 and 1.1 were deprecated by RFC 8996.
- Disabling versions can break callers and interoperability with remote peers. Changes take effect on credential
  handles acquired afterwards, so an application or service restart may be needed.
- Microsoft recommends system defaults for application callers and warns against creating Schannel registry
  settings the article does not document.

## Ciphers and suites
- Microsoft says cipher and hash algorithms should be controlled through the cipher suite order, not per-cipher
  registry keys.
- Group Policy: *Computer Configuration > Administrative Templates > Network > SSL Configuration Settings > SSL
  Cipher Suite Order* (enable it, edit the comma-separated list). Alternatives: the MDM Policy CSP
  `Cryptography/TLSCipherSuites`, or the TLS PowerShell module, which can list the ordered suites and enable or
  disable a suite.
- The suite list must be strictly comma delimited and is limited to 1,023 characters. Order changes take effect at
  the next boot; editing the default-priority registry values directly is unsupported.
- Remove weak suites (for example RC4, 3DES, NULL) from the list; check the Learn page "Cipher Suites in TLS/SSL
  (Schannel SSP)" for what each Windows version offers by default.

## .NET applications
.NET Framework apps that pin an older protocol keep it. To let the OS choose and to use strong crypto, set the
DWORDs `SchUseStrongCrypto=1` and `SystemDefaultTlsVersions=1` under
`HKLM\SOFTWARE\[Wow6432Node\]Microsoft\.NETFramework\v4.0.30319` (Learn gives the same for `v2.0.50727`).
Target .NET Framework 4.8 or later for TLS 1.3. Per the Learn page, Windows 11 defaults to TLS 1.3 and Windows 10
to TLS 1.2 when the app uses the OS default.

## Rollout
1. Inventory clients: set the `EventLogging` DWORD under `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL`
   (levels 0-7: bit values 1 = errors, 2 = warnings, 4 = informational and success; reboot required), or use
   network sensors, to see which TLS versions are in use.
2. Test dependent systems: databases, older Java clients, RDP clients, printers/scanners, monitoring agents.
3. Deploy by GPO or configuration management to rings.

## Verify
Use a TLS scanner against each service port (443, 3389, 636) to confirm only intended versions and suites are
offered; apps and RDP still connect; the TLS module's cipher listing shows the intended order.

## Checked
2026-10-31. Confirmed on Microsoft Learn "TLS registry settings", "Manage TLS" and ".NET TLS best practices":
Protocols key path and `Enabled` / `DisabledByDefault` values, restart caveat, EventLogging key and levels,
GPO path and 1,023-character limit, next-boot effect, TLS module capabilities, `SchUseStrongCrypto` and
`SystemDefaultTlsVersions` keys, .NET 4.8 for TLS 1.3, RFC 8996 note. Removed: claims that TLS 1.2/1.3 are enabled
by default on specific Windows Server releases, that recent releases disable TLS 1.0/1.1 by default, per-cipher
`Ciphers\<name>` registry instructions, IIS Crypto, the nmap script name and the SQL Server patch claim (not on the
cited pages).
Method: documentation only; no commands were run.
