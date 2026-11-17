---
id: computing-software.systems-network-administration.active-directory.virtual-dc-placement-and-anti-affinity
name: virtual-dc-placement-and-anti-affinity
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, virtualized-dc, virtual-dc-placement, anti-affinity, hyper-v, failover-cluster]
level: practitioner
status: docs-checked
description: "Spread virtual domain controllers across hosts, clusters and storage so one failure cannot take all DCs: anti-affinity rules, startup order and a physical or cloud DC."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/cluster-affinity
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/new-clusteraffinityrule
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controllers-hyper-v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual DC placement

The point of two DCs is that one survives. Two DCs on one host, one cluster or one LUN is one DC.

## Rules
- At least two DCs per domain on **different hosts**, preferably different clusters and storage arrays.
- Keep one DC that does not depend on the infrastructure it authenticates, for example a DC on a standalone
  host or in another site.
- Don't store all DC disk files on storage that needs a DC to come online.

## Anti-affinity on Hyper-V failover clusters
```powershell
# class names keep roles apart; this is a soft block
(Get-ClusterGroup DC01).AntiAffinityClassNames = 'DomainControllers'
(Get-ClusterGroup DC02).AntiAffinityClassNames = 'DomainControllers'
# make the block hard cluster-wide
(Get-Cluster).ClusterEnforcedAntiAffinity = 1
# or an affinity rule (FailoverClusters cmdlets)
New-ClusterAffinityRule -Name DCsApart -RuleType DifferentNode
Add-ClusterGroupToAffinityRule -Groups DC01,DC02 -Name DCsApart
```
`AntiAffinityClassNames` is blank by default and is a soft block; `ClusterEnforcedAntiAffinity` value `1` makes it
a hard block (`0` disables enforcement). The affinity-rule cmdlets also support `SameNode`, `SameFaultDomain`
and `DifferentFaultDomain` rule types.

## Startup and availability
- Microsoft's guidance for time on a virtual DC is to disable host time synchronization for it (see
  virtual-dc-time-synchronization).
- Do not take or restore snapshots of a virtual DC (see virtual-dc-generation-id-safeguards).

## Verify
- [ ] `Get-ClusterGroup DC01 | fl AntiAffinityClassNames` (or `Get-ClusterAffinityRule`) shows every DC covered.
- [ ] Taking any single host or cluster out leaves at least one DC per domain running elsewhere.

## Checked

Documentation: Microsoft Learn Cluster Affinity page and the New-ClusterAffinityRule / Add-ClusterGroupToAffinityRule
cmdlet references (Windows Server 2025 module docs), from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: AntiAffinityClassNames (blank default, soft block), ClusterEnforcedAntiAffinity 0/1, RuleType values
including DifferentNode, `-Groups` parameter. Removed unconfirmed claims: version gates (2016+/2022+), VMware DRS
advice, automatic-start and cluster priority settings, and the claim about clusters starting without AD.

Method: documentation only; no commands were run.
