---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-network-traffic-rules-and-throttling
name: veeam-network-traffic-rules-and-throttling
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, network-traffic-rules, throttling, encryption-in-transit, preferred-networks, backup-network]
level: practitioner
status: docs-checked
description: "Veeam network traffic throttling: how rules split bandwidth between jobs, when they apply, and which component pairs are throttled."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/setting_network_traffic_throttling.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Veeam network traffic throttling

**Goal:** limit the effect of Veeam jobs on network performance, mainly for off-site backup and replication over slow WAN links.

## Behaviour (from the Veeam guide)
- Throttling in a network rule prevents jobs using all available bandwidth.
- When several jobs matching the same rule run together, the throttled traffic is split equally between them (two jobs: half each). When one finishes the other can use the whole allowance.
- Throttling works only when the infrastructure components are on different servers with different IP addresses; if one server is both proxy and repository, the rules do not apply.
- Throttling is recommended for off-site backup or replication to a DR site over slow WAN links.
- For machine jobs the rules apply to virtual-disk transfer; you may see bandwidth peaks at the start of a job from other VM files.

## Where it applies
Between components with Veeam Data Movers, plus the capacity tier of a scale-out repository and object storage repositories. Examples from the guide: backup proxy and repository (Windows/Linux repository); proxy and gateway server (SMB/NFS shares, Data Domain, StoreOnce, or object storage via a gateway); proxy and object storage (direct mode); proxy and cloud gateway (Cloud Connect); source and target CDP proxies; source and target repositories, gateways or WAN accelerators (backup copy); source and target proxies or WAN accelerators (replication).

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center page "Enabling Traffic Throttling" (read in part; the component table was truncated in the fetched text).
Removed (not on the page): menu location, default Internet rule, AES-256 encryption, preferred-networks and multiple-upload-streams settings with their default of 5, NAT/LAN/restore gotchas, the Verify section.
Method: documentation only; no commands were run.
