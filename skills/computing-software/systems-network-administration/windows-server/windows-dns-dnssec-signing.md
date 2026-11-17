---
id: computing-software.systems-network-administration.windows-server.windows-dns-dnssec-signing
name: windows-dns-dnssec-signing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-dns-server, dnsserver-module, dnssec, invoke-dnsserverzonesign, key-master, trust-anchors, nrpt, ksk-rollover]
level: advanced
status: docs-checked
description: "Sign zones with DNSSEC on Windows DNS Server: Invoke-DnsServerZoneSign, the key master, automatic rollover, trust anchor distribution, NRPT validation, and risks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/dnssec-overview
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/sign-dnssec-zone
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/validate-dnssec-responses
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/invoke-dnsserverzonesign
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserversigningkey
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNSSEC signing on Windows DNS Server

## Should you?
Signing internal AD zones protects against spoofing on the internal network but adds key
management and failure modes. Decide deliberately.

## Sign a zone
```powershell
Invoke-DnsServerZoneSign -ZoneName 'corp.example.com' -SignWithDefault -Force
Get-DnsServerDnsSecZoneSetting -ZoneName 'corp.example.com'
Get-DnsServerSigningKey -ZoneName 'corp.example.com'
```
`-SignWithDefault` signs with default parameters (a new KSK and ZSK; on an already signed zone it replaces the existing keys). The DNS Manager wizard defaults are RSA/SHA-256, KSK 2048 bits and ZSK 1024 bits, rollover enabled (KSK 755 days, ZSK 90 days), NSEC3 recommended; check the result with `Get-DnsServerSigningKey`. Supported `-CryptoAlgorithm` values: RsaSha1, RsaSha256, RsaSha512, RsaSha1NSec3, ECDsaP256Sha256, ECDsaP384Sha384. Custom keys:
`Add-DnsServerSigningKey -Type KeySigningKey -CryptoAlgorithm RsaSha256 -KeyLength 2048 ...`.

- **Key master**: one DNS server (default the one where you signed) owns keys and rollovers
  for AD-integrated zones; others load signed data via AD replication. If it dies, transfer:
  `Reset-DnsServerZoneKeyMasterRole -ZoneName corp.example.com -KeyMasterServer dns02 -SeizeRole`.
- For AD-integrated zones private signing keys replicate through AD; the wizard option "Replicate this private key to all DNS servers authoritative for this zone" is on by default.

## Trust anchors (for validating resolvers)
```powershell
Set-DnsServerDnsSecZoneSetting -ZoneName corp.example.com -DistributeTrustAnchor DnsKey -EnableRfc5011KeyRollover $true
Get-DnsServerTrustAnchor -Name corp.example.com
```
Internal resolvers validate only zones for which they have trust anchors (or that chain to the root).

## Client validation (NRPT)
A DNSSEC-aware client can be configured through the Name Resolution Policy Table (NRPT) to require that the DNS server performed validation for a namespace; `Get-DnsClientNrptPolicy` lists the rules. Test carefully: validation failure means no answer.

## Unsign
`Invoke-DnsServerZoneUnsign -ZoneName corp.example.com -Force` removes all DNSSEC records at once; if the zone is delegated, remove the DS record at the parent first so resolvers do not see a broken chain.

## Verify
- [ ] `Resolve-DnsName dc01.corp.example.com -DnssecOk -Server dns01` returns RRSIG records.
- [ ] Key rollover audit events (528 start, 529 end) appear in the DNS Server audit log.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DnsServer/DhcpServer/DnsClient modules) repositories, latest commit 2026-10-23. Confirmed: signing wizard defaults (RSA/SHA-256, KSK 2048, ZSK 1024, rollover 755 and 90 days) and the algorithm list; `-SignWithDefault` semantics; private-key replication for AD-integrated zones; NRPT validation requirement; `Reset-DnsServerZoneKeyMasterRole -SeizeRole`, `Set-DnsServerDnsSecZoneSetting -DistributeTrustAnchor/-EnableRfc5011KeyRollover`, `Invoke-DnsServerZoneUnsign -Force` parameters; audit events 528 and 529. Corrected the claim that `-SignWithDefault` uses ECDSA P-256 (the documented default algorithm is RSA/SHA-256) and removed the unsupported remarks about how rarely validation is enforced.

Method: documentation only; no commands were run.
