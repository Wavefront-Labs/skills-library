---
id: computing-software.cybersecurity-defensive.nessus.agent-and-network-scan-asset-deduplication
name: agent-and-network-scan-asset-deduplication
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, asset-deduplication, tenable-vulnerability-management, nessus-agents, asset-merging, golden-image, scan-results]
level: advanced
status: draft
description: "Prevent and fix duplicate assets between Nessus agents and network scans: Tenable UUIDs, asset merge rules, agent and scanner identifiers, and cloned VM/golden image issues."
sources: ["https://docs.tenable.com/vulnerability-management/Content/Explore/Assets/AssetMerging.htm", "https://docs.tenable.com/nessus-agent/Content/AgentCloning.htm", "https://community.tenable.com/s/article/Tenable-io-Asset-Identification"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Duplicate assets between agents and network scans

Duplicates inflate counts and licences and split findings so neither record shows true state.

## How Tenable identifies assets
Tenable VM merges observations using identifiers in priority: Tenable UUID (agent UUID or host
tag written by credentialed network scans), BIOS/system UUID, MAC addresses, NetBIOS/FQDN, IP.
- Credentialed Nessus scans write a **host tag** (`Tenable` UUID) on Windows registry /
  `/etc/tenable_tag` on Linux; agents use the same tag. This is what lets agent and network scan
  results land on one asset.
- Uncredentialed scans can only match on IP/DNS/NetBIOS, so DHCP hosts duplicate.

## Common causes
1. **Golden images with agents linked or tags present**: clones share UUID, merging different hosts.
   Fix: before sealing images, `nessuscli agent unlink` and remove the host tag; or install agent with
   `NESSUS_KEY` at first boot. For cloned agents `nessuscli fix --reset` / `prepare-image` options.
2. **Disabled host tagging** in scan policy (Advanced: "Create unique identifier on hosts scanned
   using credentials") or no credentials.
3. **Cloud instances** with recycled IPs: use cloud connectors so instance IDs drive identity.

## Fixing existing duplicates
- Tenable VM asset merge (UI or `POST /api/v2/assets/bulk-jobs/merge`) moves findings to the target asset.
- Age-out settings delete assets not seen in N days per network object.
- Separate **networks** in Tenable VM for overlapping RFC1918 ranges so identical IPs in different
  sites are not merged.

## Gotchas
- Over-merging is worse than duplicates (two hosts' findings combined, one appears fixed). Check
  serial/BIOS UUID before merging.

## Verify
Count assets with both agent and Nessus scan sources vs agent-only + network-only for the same
hostnames; after fixes, duplicate hostname count trends to zero.
