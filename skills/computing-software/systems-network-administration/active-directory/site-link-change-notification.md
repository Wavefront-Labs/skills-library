---
id: computing-software.systems-network-administration.active-directory.site-link-change-notification
name: site-link-change-notification
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-replication, site-link-change-notification, urgent-replication, site-links, repadmin]
level: advanced
status: docs-checked
description: "Enable change notification on AD site links for near-real-time inter-site replication, understand urgent replication, and when it is worth the WAN cost."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adreplicationsitelink
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/determining-the-interval
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/modify-default-intra-site-dc-replication-interval
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742152(v=ws.11)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site link change notification and urgent replication

Within a site, a DC notifies its partners 15 seconds after a change by default. Between sites, replication follows the
site link **schedule and interval** (default 180 minutes) and is compressed, so a change at HQ can take hours to reach a branch.

## Enable change notification on a site link
Set the `options` attribute of the site link to 1 (the documented example for Set-ADReplicationSiteLink):
```powershell
Get-ADReplicationSiteLink 'HQ-BRANCH1' -Properties options     # check any existing value first
Set-ADReplicationSiteLink -Identity 'HQ-BRANCH1' -Replace @{'options'=1}
```
If `options` already holds other bits, keep them when you add this one. `repadmin /replicate ... /addref` also
enables change notification between a specific source and destination.

## When to do it
- Good: fast, reliable links (datacentre to datacentre, Azure ExpressRoute) where the sites exist only for
  client locality.
- Bad: slow or metered WAN; every change crosses the link right away.

## Verify
```powershell
Get-ADReplicationSiteLink 'HQ-BRANCH1' -Properties options
```
```cmd
repadmin /showrepl BR1-DC01
```
- [ ] `options` shows the expected value on the site link.
- [ ] A test object created at HQ reaches the branch without waiting for the schedule.

## Checked
2026-10-27, against the Set-ADReplicationSiteLink and New-ADReplicationSiteLink cmdlet pages, the repadmin /replicate and /showrepl pages (Learn previous-versions, Windows Server 2012 R2), the Determining the Interval page and the intra-site interval article. Confirmed: `-Replace @{'options'=1}` enables change notification on a site link; default inter-site interval 180 minutes; intra-site notification delay 15 seconds by default; intersite replication is scheduled and compressed; /replicate /addref enables change notification between a source and destination. Removed as unconfirmed: the urgent-replication list, the ADSI Edit path, the value-5 compression bit, the 15-minute minimum and repadmin /showconn output wording.

Method: documentation only; no commands were run.
