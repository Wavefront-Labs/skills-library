---
id: computing-software.systems-network-administration.windows-server.windows-dns-ad-integrated-zones
name: windows-dns-ad-integrated-zones
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-integrated-zone, secure-dynamic-updates, dns-application-partitions, zone-replication-scope, dnsupdateproxy, add-dnsserverprimaryzone]
level: practitioner
status: docs-checked
description: "Manage Active Directory-integrated DNS zones: replication scopes, secure dynamic updates, DHCP update credentials, conversion and troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/zone-types
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/dynamic-update
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/active-directory-integrated-dns-zones
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/add-dnsserverprimaryzone
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverprimaryzone
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/convertto-dnsserverprimaryzone
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dcdiag
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AD-integrated zones

AD-integrated zones store DNS records as objects in Active Directory, so every DNS server on a domain controller in the replication scope is a writable primary (multi-master) and zone data replicates with AD.

## Create and configure
```powershell
Add-DnsServerPrimaryZone -Name corp.example.com -ReplicationScope Forest -DynamicUpdate Secure
Add-DnsServerPrimaryZone -NetworkId 10.20.0.0/16 -ReplicationScope Domain -DynamicUpdate Secure   # reverse zone
Get-DnsServerZone | Select ZoneName, ZoneType, IsDsIntegrated, ReplicationScope, DynamicUpdate
Set-DnsServerPrimaryZone -Name corp.example.com -ReplicationScope Domain
Set-DnsServerPrimaryZone -Name legacy.example.com -ReplicationScope Forest -PassThru   # file-backed primary -> AD-integrated
```

## Replication scopes
| Scope | Stored in | Replicates to |
|---|---|---|
| Forest | `ForestDnsZones` application partition | all DCs running DNS in the forest |
| Domain | `DomainDnsZones` partition | all DCs running DNS in the domain |
| Legacy | a legacy directory partition | see the cmdlet help for `-ReplicationScope` |
| Custom | a custom application partition (`-DirectoryPartitionName`) | DCs you enlist |
- The cmdlets accept the four values Custom, Domain, Forest and Legacy for `-ReplicationScope`.
- `ConvertTo-DnsServerPrimaryZone` converts a zone (for example a secondary) to a primary zone; add `-ReplicationScope` to make the result AD-integrated.

## Secure dynamic updates
- `Secure` only accepts updates from authenticated clients and restricts which computers can update which names, so other machines cannot overwrite an existing name.
- `NonsecureAndSecure` accepts unauthenticated updates - avoid.
- DHCP servers registering records on behalf of clients: configure DNS update credentials on DHCP (a dedicated low-privilege user) so records aren't owned by the DHCP server's computer account:
```powershell
Set-DhcpServerDnsCredential -Credential (Get-Credential corp\svc-dhcpdns) -ComputerName dhcp01
Set-DhcpServerv4DnsSetting -ComputerName dhcp01 -DynamicUpdates Always -DeleteDnsRROnLeaseExpiry $true
```
- Members of the `DnsUpdateProxy` group do not secure the names they register, so do not use that group in an AD-integrated zone that allows only secure updates; use the dedicated DHCP credentials instead. A DHCP server on a domain controller inherits the DC's authority over secure records.

## Troubleshooting
```powershell
Get-DnsServerResourceRecord -ZoneName corp.example.com -Name app01
dcdiag /test:dns /v /e
Get-ADObject -SearchBase "DC=corp.example.com,CN=MicrosoftDNS,DC=DomainDnsZones,DC=corp,DC=example,DC=com" -Filter "name -eq 'app01'" -Properties *
```
- Record differs between DCs: AD replication latency or failure, not DNS.
- Duplicate zone in both Forest and Domain partitions (conflict after a misconfigured move): decide which copy is current before deleting the other.
- Client can't update its record: the record is owned by another account (check the record's Security tab in DNS Manager), or the client is not domain-authenticated.

## Verify
- [ ] All AD-integrated zones use Secure updates and the intended scope; `_msdcs` is forest-wide.
- [ ] `dcdiag /test:dns` passes on every DC; a new record appears on all DNS DCs after replication.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DnsServer/DhcpServer/DnsClient modules) repositories, latest commit 2026-10-23. Confirmed: `-ReplicationScope` accepts Custom, Domain, Forest and Legacy (Add-/Set-DnsServerPrimaryZone, ConvertTo-DnsServerPrimaryZone parameters); ConvertTo-DnsServerPrimaryZone converts a zone to a primary zone, while Set-DnsServerPrimaryZone changes the scope of an existing primary; ForestDnsZones and DomainDnsZones partitions; the DnsUpdateProxy and dedicated DHCP credential guidance in the Dynamic Update article; Set-DhcpServerDnsCredential and Set-DhcpServerv4DnsSetting parameters. `dcdiag /test:dns` with `/v` and `/e` per the dcdiag reference. Removed the repadmin line (reference not available in the repositories), the Legacy-scope replication detail, the _msdcs rule, event 4515 and the ACL-ownership wording because the checked pages do not state them.

Method: documentation only; no commands were run.
