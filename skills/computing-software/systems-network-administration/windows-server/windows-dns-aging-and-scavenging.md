---
id: computing-software.systems-network-administration.windows-server.windows-dns-aging-and-scavenging
name: windows-dns-aging-and-scavenging
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dns-scavenging, aging-and-scavenging, stale-records, no-refresh-interval, refresh-interval, set-dnsserverscavenging]
level: practitioner
status: docs-checked
description: "Configure Windows DNS aging and scavenging safely: intervals, per-zone and per-server switches, previewing deletions, DHCP lease alignment."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/aging-scavenging
  - https://learn.microsoft.com/en-us/windows-server/networking/dns/configure-aging-scavenging
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverscavenging
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverzoneaging
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverv4dnssetting
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Aging and scavenging of stale records

Dynamic records registered by clients carry a timestamp. Scavenging deletes records whose timestamp is older than **no-refresh + refresh** intervals. Without scavenging, stale records accumulate and point names at recycled IPs.

## The two intervals
- **No-refresh interval** (default 7 days): after a timestamp update, refreshes within this window are ignored (saves AD replication).
- **Refresh interval** (default 7 days): window, starting after the no-refresh interval ends, in which the server accepts a refresh; a record not refreshed by the end of it becomes stale. Clients re-register at start-up, when a DHCP lease renews and on `ipconfig /registerdns`.
- A record becomes stale after `no-refresh + refresh` (default 14 days) without refresh; the next scavenging run deletes it.
Rule: align the combined no-refresh and refresh intervals with your DHCP lease duration; a refresh interval shorter than the time clients need to re-register makes scavenging delete live records.

## Enable (three switches all required)
```powershell
# 1) Zone aging
Set-DnsServerZoneAging -Name corp.example.com -Aging $true -NoRefreshInterval 7.00:00:00 -RefreshInterval 7.00:00:00
# 2) Server scavenging, preferably limited to one DNS server per zone (see -ScavengeServers below)
Set-DnsServerScavenging -ComputerName dc01 -ScavengingState $true -ScavengingInterval 7.00:00:00 -ApplyOnAllZones:$false
# 3) Restrict which servers may scavenge a zone (by default every server hosting the zone can)
Set-DnsServerZoneAging -Name corp.example.com -ScavengeServers 10.0.0.10
Get-DnsServerZoneAging corp.example.com     # also shows AvailForScavengeTime: no deletions before this time
```
After enabling aging or changing its settings, the zone's available-for-scavenging time is the current server time (rounded down to the hour) plus the refresh interval; no scavenging of the zone happens before it - use that time to review.

## Before turning it on
- Static records: records added manually or from a text zone file have a timestamp of zero and are never scavenged. Dynamically registered records carry a timestamp; list them and review before enabling:
```powershell
Get-DnsServerResourceRecord -ZoneName corp.example.com -RRType A |
  Where-Object { $_.Timestamp -and $_.Timestamp -lt (Get-Date).AddDays(-14) } |
  Select HostName, Timestamp, @{n='IP';e={$_.RecordData.IPv4Address}}
```
Records with a nonzero timestamp are eligible for scavenging. To protect a dynamically registered record, clear "Delete this record when it becomes stale" in DNS Manager (this sets the timestamp to zero) or remove it and re-add it as a static record without `-AgeRecord`; no single cmdlet clears an existing timestamp, and re-adding changes the record's ownership and permissions.

## Operate
```powershell
Start-DnsServerScavenging -ComputerName dc01 -Force -Verbose      # manual run
Get-WinEvent -LogName 'DNS Server' | Where-Object Id -in 2501,2502 | Select -First 5   # scavenging summary events
```
Event 2501 reports records scavenged; 2502 means nothing was deleted.

## DHCP alignment
Configure DHCP to delete records on lease expiry (`Set-DhcpServerv4DnsSetting -DeleteDnsRROnLeaseExpiry`, valid only when dynamic updates are Always or OnClientRequest), and size the intervals against the lease duration so active leases are not scavenged.

## Verify
- [ ] Review list before the available-for-scavenging time contains no critical servers; scavenging restricted to one server per zone.
- [ ] Event 2501 shows deletions and no tickets about missing records afterwards.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DnsServer/DhcpServer/DnsClient modules) repositories, latest commit 2026-10-23. Confirmed: no-refresh and refresh defaults of 7 days; scavenging period default 7 days (minimum 1 hour); stale when timestamp plus both intervals is earlier than server time; available-for-scavenging time formula; zero timestamp means never scavenged and how to protect a record; events 2501 and 2502; `-ScavengeServers`, `-ApplyOnAllZones`, `Start-DnsServerScavenging -Force` and `-DeleteDnsRROnLeaseExpiry` parameters. Removed the claim that Windows clients refresh every 24 hours, which the checked pages do not state.

Method: documentation only; no commands were run.
