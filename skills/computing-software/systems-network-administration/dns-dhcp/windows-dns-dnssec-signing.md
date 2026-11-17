---
id: computing-software.systems-network-administration.dns-dhcp.windows-dns-dnssec-signing
name: windows-dns-dnssec-signing
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, windows-dns, windows-dnssec, dnssec, key-master, invoke-dnsserverzonesign]
level: practitioner
status: docs-checked
description: "Sign zones with DNSSEC on Windows Server DNS: key master role, signing keys, trust anchor distribution, DS export and unsigning, using the DnsServer PowerShell cmdlets."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/invoke-dnsserverzonesign
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/reset-dnsserverzonekeymasterrole
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverdnsseczonesetting
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserversigningkey
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/export-dnsserverdnssecpublickey
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/get-dnsservertrustanchor
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DNSSEC on Windows DNS

Windows DNS signs zones with a **Key Master**: any authoritative server that hosts a primary
copy of the zone can hold the role.

## Sign a zone
```powershell
Invoke-DnsServerZoneSign -ZoneName "corp.example.com" -SignWithDefault -Force
Get-DnsServerDnsSecZoneSetting -ZoneName "corp.example.com"
Get-DnsServerSigningKey -ZoneName "corp.example.com"
```
`-SignWithDefault` signs an unsigned zone with one ZSK and one KSK using default settings. On an
already-signed zone it removes the existing keys and re-signs with new defaults; use `-DoResign`
to re-sign without that reset. Read the defaults (algorithms, key lengths, rollover) back with the
two `Get-` cmdlets rather than assuming them.

Add a key: `Add-DnsServerSigningKey -ZoneName corp.example.com -Type KeySigningKey -CryptoAlgorithm ECDsaP256Sha256`.
`-CryptoAlgorithm` accepts RsaSha1, RsaSha256, RsaSha512, RsaSha1NSec3, ECDsaP256Sha256,
ECDsaP384Sha384. `-RolloverPeriod` takes a TimeSpan.

## Trust anchors
- `Set-DnsServerDnsSecZoneSetting -ZoneName corp.example.com -DistributeTrustAnchor DnsKey`
  distributes the trust anchor in Active Directory (accepted values: `None`, `DnsKey`). Servers
  do not distribute trust anchors by default; a non-DC DNS server only adds them to its local
  trust anchor store.
- `Get-DnsServerTrustAnchor` lists the trust anchors on a server.
- `Export-DnsServerDnsSecPublicKey` exports the DS and DNSKEY data of a signed zone to files
  (a `Dsset-<zone>` file for DS), for publishing at a parent zone or adding as a trust anchor
  elsewhere with `Add-DnsServerTrustAnchor`.

## Key master
`Reset-DnsServerZoneKeyMasterRole -ZoneName corp.example.com -KeyMasterServer dc2` transfers the
role. It first tries to connect to the current Key Master; if that is unreachable it makes no
change unless you add `-SeizeRole`.

## Unsigning
`Invoke-DnsServerZoneUnsign` removes DNSSEC signing from a zone.

## Checked
2026-11-01. Confirmed on the Microsoft Learn pages for Invoke-DnsServerZoneSign,
Reset-DnsServerZoneKeyMasterRole, Set-DnsServerDnsSecZoneSetting, Add-DnsServerSigningKey,
Export-DnsServerDnsSecPublicKey and Get-DnsServerTrustAnchor: SignWithDefault and DoResign
behaviour, key master transfer and SeizeRole, CryptoAlgorithm values, DistributeTrustAnchor
values and default, Dsset file naming. Removed: Windows Server version claim, default key sizes
and rollover periods, NSEC3 and large-response gotchas, NRPT client validation, the "Replicate
this private key" note, dynamic update behaviour, the unsign-order advice and the verify command,
none of which these pages state.
Method: documentation only; no commands were run.
