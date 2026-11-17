---
id: computing-software.systems-network-administration.active-directory.rodc-dns-and-update-referrals
name: rodc-dns-and-update-referrals
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rodc, rodc-dns, read-only-dns, dns-update-referral, branch-office]
level: advanced
status: gated
description: "How DNS on an RODC works: read-only AD-integrated zones, dynamic update referrals to a writable DC, and the delay before a branch client's new record resolves."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/rodc/install-a-windows-server-2012-active-directory-read-only-domain-controller--rodc---level-200-
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/get-dnsserverzone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RODC DNS and update referrals

An RODC with the DNS role holds read-only copies of the AD-integrated zones (DomainDnsZones and ForestDnsZones,
if they are replicated to it). It answers queries locally but cannot accept writes.

## What happens on a dynamic update
1. A branch client sends a dynamic update to the RODC (its preferred DNS server) (gated: unconfirmed, source is paywalled or blocked).
2. The RODC returns a **referral** naming a writable DC that hosts the zone (gated: unconfirmed, source is paywalled or blocked).
3. The client sends the update to that writable DC over the WAN (gated: unconfirmed, source is paywalled or blocked).
4. The RODC then tries a single-object replication of that record from the writable DC so it resolves locally soon; if that fails it waits for normal inbound replication (gated: unconfirmed, source is paywalled or blocked).

So a new branch server can be unresolvable locally until the record replicates to the RODC.

## Check
```powershell
Get-DnsServerZone -ComputerName BR01-RODC
Get-DnsServerResourceRecord -ComputerName BR01-RODC -ZoneName ad.example.com -Name newsrv01
Resolve-DnsName newsrv01.ad.example.com -Server HQ-DC01
```
The zones on the RODC should be read-only copies. Update failures on clients point to the writable DC being unreachable.

## Design rules
- Writable DNS servers named in the zone must be reachable from the branch for updates.
- Clients should list the RODC first and a writable DC second.

## Verify
- [ ] Branch client registration succeeds (`ipconfig /registerdns`, event log clean).
- [ ] The new record resolves from the RODC within minutes, not hours.

## Checked
Checked 2026-10-27 against Microsoft Learn (Install an RODC, Windows Server 2012 article; Get-DnsServerZone and Resolve-DnsName references, Windows Server 2025).
- Confirmed: Get-DnsServerZone -ComputerName and Resolve-DnsName -Server exist; Install an RODC covers the DNS server role on an RODC only as an installation option.
- Gated: the referral and single-object replication sequence. Reason: the RODC DNS pages are previous-versions only and could not be read.
- Removed: the 180-minute figure, event 4015, the port list, the DirectoryPartitionName hint and the file-backed zone remark.

Method: documentation only; no commands were run.
