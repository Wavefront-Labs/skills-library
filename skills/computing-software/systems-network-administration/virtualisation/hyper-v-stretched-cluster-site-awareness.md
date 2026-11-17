---
id: computing-software.systems-network-administration.virtualisation.hyper-v-stretched-cluster-site-awareness
name: hyper-v-stretched-cluster-site-awareness
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [site-awareness, stretched-cluster, fault-domains, failover-cluster, hyper-v]
level: advanced
status: docs-checked
description: "Configure site awareness for stretched Hyper-V clusters: site fault domains, preferred sites, cross-site heartbeat, quorum witness placement and storage replication."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/fault-domains
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/stretch-cluster-replication-using-shared-storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stretched clusters and site awareness

**Goal:** a cluster spanning two sites that keeps VMs in their home site, fails over sensibly and survives a site loss.

## Define sites
```powershell
New-ClusterFaultDomain -Name 'SiteA' -Type Site -Location 'London'
New-ClusterFaultDomain -Name 'SiteB' -Type Site -Location 'Manchester'
Set-ClusterFaultDomain -Name hv01,hv02 -Parent SiteA
Set-ClusterFaultDomain -Name hv03,hv04 -Parent SiteB
Get-ClusterFaultDomain
```

## Placement
```powershell
(Get-Cluster).PreferredSite = 'SiteA'               # cluster-wide preferred site, as in Microsoft's stretch cluster example
```
Microsoft's stretch cluster page uses this to make the primary site own the source storage and VMs. Per-group preferred sites, failover ordering and heartbeat tuning (`CrossSiteDelay`, `CrossSiteThreshold`) are not covered by the cited pages; check the failover clustering documentation for your version before relying on them.

## Quorum
Configure a file share witness or cloud witness to provide quorum if a site goes down.

## Storage
- Shared SAN across sites with synchronous array replication (vendor-specific), or
- **Storage Replica** stretch cluster: asymmetric storage per site (each storage set visible to the servers of one site only, with Persistent Reservation support); synchronous replication wants an average of about 5 ms round-trip latency, asynchronous has no latency recommendation. The page states 2 to 64 nodes, and with only two servers (one per site) there is no intra-site failover.
- Keep VMs in the site that owns their primary replica to avoid cross-site I/O.

## Gotchas
- If nodes are in different subnets, create an IP address for the additional site using the OR dependency on the cluster name resource, and configure cluster networking and AD for faster DNS site failover (per the Storage Replica page).
- Expect storage errors in cluster validation because of the asymmetric storage.

## Verify
In a test, fail the inter-site link and confirm which site keeps quorum and where `Get-ClusterGroup` shows the VMs running; `Get-ClusterFaultDomain` lists the sites and their nodes.

## Checked

Checked 2026-10-26 against MicrosoftDocs/windowsserverdocs (Fault domain awareness, and Stretch cluster replication using shared storage; latest commit 2026-10-23). Confirmed: `New-ClusterFaultDomain -Type Site -Location`, `Set-ClusterFaultDomain -Parent`, `(Get-Cluster).PreferredSite`, witness advice, asymmetric storage, about 5 ms synchronous round-trip guidance, OR-dependency IP for multi-subnet. Wrong in the earlier draft: the parameter is `-Type`, not `-FaultDomainType`. Removed as undocumented: per-group PreferredSite, the "wins quorum ties" and failover/drain behaviour claims, `CrossSiteDelay`/`CrossSiteThreshold` defaults, `New-SRPartnership`, and the site-holding-the-witness survival rule.

Method: documentation only; no commands were run.
