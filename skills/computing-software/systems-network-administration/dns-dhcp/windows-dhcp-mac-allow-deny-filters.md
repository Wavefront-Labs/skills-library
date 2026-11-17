---
id: computing-software.systems-network-administration.dns-dhcp.windows-dhcp-mac-allow-deny-filters
name: windows-dhcp-mac-allow-deny-filters
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, windows-dhcp, mac-filter, link-layer-filter, access-control]
level: practitioner
status: docs-checked
description: "Use Windows DHCP Server allow and deny MAC filter lists with PowerShell: enable each list, add entries, bulk import from CSV, and treat it as hygiene rather than access control."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4filter
  - https://learn.microsoft.com/en-us/powershell/module/dhcpserver/set-dhcpserverv4filterlist
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allow/deny MAC filters

The Windows DHCP Server service keeps two MAC address filter lists, an allow list and a deny list. Each list has its own enabled state.

## Configure
```powershell
Set-DhcpServerv4FilterList -ComputerName dhcp1 -Allow $false -Deny $true     # enable deny list only
Add-DhcpServerv4Filter -ComputerName dhcp1 -List Deny -MacAddress 00-11-22-33-44-55 -Description "stolen laptop"
Add-DhcpServerv4Filter -List Allow -MacAddress "F0-DE-F1-7A-00-5E","F0-DE-F1-7A-00-5C"
Get-DhcpServerv4Filter -ComputerName dhcp1 -List Allow
```
- `Set-DhcpServerv4FilterList` sets the enabled state of the allow and deny lists (`-Allow`, `-Deny`, both Boolean).
- `Add-DhcpServerv4Filter` takes `-List` (Allow or Deny), one or more `-MacAddress` values and an optional `-Description`.
- The MS page lists `-MacAddress` as not supporting wildcards, so do not rely on a prefix or OUI wildcard entry.
- If a MAC is already in either list the cmdlet fails; `-Force` deletes the existing entries and creates the new ones (useful to move a MAC from Allow to Deny).

## Bulk load
```powershell
Import-Csv -Path MacAddressFilters.csv | Add-DhcpServerv4Filter -ComputerName dhcp1 -List Allow
```
CSV header is `MacAddress,Description`, for example `1a-1b-1c-1d-1e-1f,Computer1`.

## Per-server
The cmdlets act on the DHCP server named by `-ComputerName`. Run them against each server you operate (script a loop over servers); these pages say nothing about filters replicating.

## Limits
- MACs are trivially spoofed; this is hygiene, not security. Use 802.1X/NAC for access control.
- Randomised MACs (Windows, iOS, Android private addresses) will not match an allow list; use MDM or 802.1X for corporate Wi-Fi.

## Checked
Method: 2026-11-08 read both Microsoft Learn cmdlet pages in full. Kept: enabled-state cmdlet, Add/Get usage, -Force, CSV import. Removed as unsupported by the pages: wildcard entries, deny-over-allow precedence, drop-the-Discover behaviour, event IDs 20097-20100, failover non-replication (reworded to per-server). Spoofing and randomised-MAC limits are practitioner opinion, not from the pages.

## Verify
- [ ] `Get-DhcpServerv4FilterList` shows the intended list(s) enabled and a test client on the deny list receives no lease.
