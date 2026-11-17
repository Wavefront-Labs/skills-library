---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcp-dns-update-credentials-and-dnsupdateproxy
name: windows-dhcp-dns-update-credentials-and-dnsupdateproxy
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, dnsupdateproxy, dynamic-dns, dns-credentials, record-ownership]
level: practitioner
status: draft
description: "Configure Windows DHCP dynamic DNS updates with a dedicated credential, understand DnsUpdateProxy group risks, and fix record ownership problems."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverdnscredential
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS dynamic update credentials and DnsUpdateProxy

When the DHCP server registers A/PTR records for clients in secure AD-integrated zones, the record's
ACL owner becomes whichever account created it. Ownership problems break later updates.

## Recommended setup
1. Create a dedicated low-privilege user (password not expiring, rotation process) e.g. `svc-dhcpdns`.
2. Set it on every DHCP server:
```powershell
$cred = Get-Credential corp\svc-dhcpdns
Set-DhcpServerDnsCredential -ComputerName dhcp1 -Credential $cred
Set-DhcpServerv4DnsSetting -ComputerName dhcp1 -DynamicUpdates Always -DeleteDnsRROnLeaseExpiry $true -UpdateDnsRRForOlderClients $true
```
Failover partners must use the same credential so either can update records the other created.

## DnsUpdateProxy group
Records created by members of DnsUpdateProxy have no owner security, so anyone can take them over
later. That fixes ownership between DHCP servers, but:
- Adding a DHCP server running on a DC to DnsUpdateProxy makes records created by the DC (including
  SRV records for AD) unsecured. Do not use it on DCs; use the dedicated credential instead.
- Records can be hijacked by any authenticated client.

## Fixing existing records
Stale records owned by an old DHCP server account or the client: delete and let DHCP re-register,
or grant the credential Full Control on the record (DNS Manager > record > Security).
`Get-DnsServerResourceRecord -ZoneName corp.example.com -Name host7 | Remove-DnsServerResourceRecord -ZoneName corp.example.com -Force`.

## Verify
- [ ] New leases create records owned by the dedicated account and lease expiry removes them; `Get-DhcpServerDnsCredential` matches on all servers.
