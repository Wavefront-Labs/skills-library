---
id: computing-software.systems-network-administration.active-directory.ad-replication-and-sites-topology
name: ad-replication-and-sites-topology
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, replication, sites-and-services, ad-sites, subnets, site-links, site-link-cost, replication-interval, kcc, istg, bridgehead, change-notification, intra-site, inter-site, dc-locator, nltest, repadmin, repadmin-syncall, repadmin-showobjmeta, usn-rollback, lingering-objects, strict-replication-consistency, tombstone-lifetime, event-1311, event-2042, metadata-cleanup, fsmo, branch-office, rodc, new-adreplicationsite, new-adreplicationsubnet, no-client-site, missing-subnets, bridgehead-server]
level: advanced
status: docs-checked
description: "Model AD sites, subnets and site links so clients find a local DC and replication follows the WAN: KCC, costs, intervals, lingering objects and USN rollback."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/designing-the-site-topology
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/determining-the-interval
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-adreplicationsitelink
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/diagnose-replication-failures
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/information-lingering-objects
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/detect-and-recover-from-usn-rollback
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/troubleshoot-event-id-1311-messages
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/modify-default-intra-site-dc-replication-interval
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# AD replication and sites topology — make AD's map match the network

**Goal:** describe the physical network to AD so clients authenticate against a nearby
DC and replication flows over sensible WAN paths, then repair the failure modes that
generic health checks (`repadmin /replsummary`, `dcdiag` — see
`computing-software.systems-network-administration.active-directory.ou-group-and-gpo-design`)
only reveal.

## 1. Sites and subnets: the part everyone skips
A **site** is a well-connected set of subnets. Clients pick a DC via DNS SRV records
scoped to *their* site, determined by **which subnet object contains their IP**.
```powershell
New-ADReplicationSite -Name 'BRANCH-LON'
New-ADReplicationSubnet -Name '10.20.0.0/16' -Site 'BRANCH-LON'
nltest /dsgetdc:<DOMAIN> /force         # which DC did I get?
```
- Missing subnets → clients fall back to *any* DC, often across the WAN. DCs log
  Netlogon warning event 5807 for clients whose IPs match no subnet — review it after every network change (new VPN
  pool, new VLAN, cloud VNet).
- Sites without a DC: enable/keep **automatic site coverage** so a DC in the cheapest
  linked site registers SRV records for them.

## 2. Site links: cost, interval, schedule
```powershell
New-ADReplicationSiteLink -Name 'HQ-LON' -SitesIncluded HQ,BRANCH-LON -Cost 100 -ReplicationFrequencyInMinutes 15
```
- **Cost** expresses preference, not bandwidth: lower cost path wins. Use a consistent
  scheme (e.g. 100 for primary WAN, 200 for backup).
- Default inter-site interval is **180 minutes**; the cmdlet documentation example uses 15.
  Intra-site replication uses change notification, by default 15 seconds after a change.
- Enable **change notification on a site link** (`options` attribute value `1`) when the
  WAN is good and you want near-real-time inter-site replication:
  `Set-ADReplicationSiteLink 'HQ-LON' -Replace @{options=1}`. Test first; every change
  then crosses the link immediately.

## 3. Let the KCC build connections
The **KCC** on each DC builds intra-site connections; one DC per site, the **ISTG**,
builds inter-site connections between **bridgehead** servers. Leave connection objects
automatic. Manual connections and preferred bridgeheads are the classic cause of
"replication stopped when that DC died". Microsoft strongly recommends not defining
preferred bridgehead servers.
```cmd
repadmin /kcc                            rem force topology recalculation
repadmin /showrepl <DC>
repadmin /syncall                        rem see repadmin /syncall /? for scope switches
repadmin /showobjmeta <DC> "<OBJECT_DN>" rem which DC changed which attribute, when
```

## 4. Failure modes that need real fixes
- **Event 1311 / 1865** (KCC can't build a spanning tree): a site isn't linked, a
  bridgehead is offline, or "Bridge all site links" was disabled without manual bridges.
- **Lingering objects** (event 1388/1988): a DC was offline longer than the tombstone
  lifetime (default 180 days on supported Windows Server versions; 60 on forests created on older versions) and holds objects deleted elsewhere. Ensure
  **Strict Replication Consistency = 1** (blocks inbound lingering objects), then
  remove them with `repadmin /removelingeringobjects <DC> <REF_DC_GUID> <NC> /advisory_mode`
  first, then without `/advisory_mode`. Microsoft's Lingering Object Liquidator
  automates this.
- **Event 2042** (replication blocked past tombstone lifetime): check for lingering objects
  and remove them before setting "Allow Replication With Divergent and Corrupt Partner"
  (see the replication error 8614 article), or demote and rebuild the stale DC.
- **USN rollback** (event 2095, NTDS paused, netlogon stopped): caused by restoring a DC
  from a snapshot/image outside AD-aware mechanisms. Fix = forcibly demote, clean up the
  metadata, then re-promote (see the USN rollback article in `sources`).
- **Dead DC**: seize roles if it held FSMOs (`Move-ADDirectoryServerOperationMasterRole
  -Force`), then remove its metadata and clean up its DNS records.

## 5. Design rules of thumb
- One site per location with a meaningful WAN boundary; a DC (or RODC for low-security
  branches) only where authentication must survive WAN loss.
- Global Catalog on every DC unless you have a specific reason not to.
- Cloud networks (Azure/AWS VNets with DCs) are sites too — give them subnets and links.

## Verify
- [ ] No recent Netlogon 5807 warnings on DCs.
- [ ] `nltest /dsgetdc` from a branch returns a local DC.
- [ ] `repadmin /replsummary` largest delta < link interval + margin; zero failures.
- [ ] No manual connection objects without documented reason.
- [ ] Strict Replication Consistency is 1 on all DCs; no events 1388/1988/2042/2095.

## Checked
2026-10-27, against Microsoft Learn (windowsserverdocs and SupportArticles-docs, current pages). Confirmed: default site-link interval 180 minutes; 15-second intra-site notification delay; `options=1` enables change notification (Set-ADReplicationSiteLink example); tombstone lifetime defaults (60 or 180 days, 180 for supported versions); Strict Replication Consistency and `repadmin /removelingeringobjects ... /advisory_mode`; event 2095 and USN rollback recovery; event 1311/1865 causes and the recommendation not to define preferred bridgeheads; Netlogon event 5807 for clients with no subnet match. Removed as unconfirmed: nltest /dsgetsite, netlogon.log path, urgent-replication list, compression effect, repadmin /bridgeheads and /syncall switch letters.

Method: documentation only; no commands were run.
