---
id: computing-software.systems-network-administration.virtualisation.proxmox-datacenter-manager
name: proxmox-datacenter-manager
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [proxmox-datacenter-manager, pdm, proxmox, multi-cluster]
level: practitioner
status: docs-checked
description: "Use Proxmox Datacenter Manager to view and operate multiple Proxmox VE clusters: adding remotes with tokens, central status, updates and cross-cluster migration."
sources:
  - https://pdm.proxmox.com/docs/introduction.html
  - https://pdm.proxmox.com/docs/web-ui.html
  - https://pdm.proxmox.com/docs/remotes.html
  - https://pdm.proxmox.com/docs/guests.html
  - https://pdm.proxmox.com/docs/access-control.html
  - https://pdm.proxmox.com/docs/command-syntax.html
  - https://pve.proxmox.com/pve-docs/qm.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Proxmox Datacenter Manager

**Goal:** one place to see and act on many independent Proxmox VE clusters and nodes.

## What it is
A central management platform for Proxmox VE and Proxmox Backup Server instances in separate locations. Each connected node or cluster is a **remote**. It is a control plane with an "escape hatch" to each remote's own web interface, loosely coupled so it is not a bottleneck or single point of failure for the remotes. It is free and open source (AGPL v3), installs from its own ISO or on top of Debian, and needs a 64-bit CPU. The web interface is on port 8443 (`https://<ip>:8443`).

## Add a remote
Web interface: Remotes -> Configuration lists remotes and lets you configure new ones. CLI:
```bash
proxmox-datacenter-manager-client remote add pve <remote-id> --authid <user@realm!tokenname> --nodes <node-address> --token <secret>
```
`--create-token <name>` creates the token on the remote and uses it instead. API token permissions are the intersection of the token's own ACLs and its user's permissions, so tokens can never do more than their user; new users and tokens have no permissions by default. A dedicated account for PDM makes tokens easier to audit and revoke.

## Daily use
- Dashboard: state of all remotes and resources, running and stopped guests, datastores, running tasks, CPU and memory use, SDN zones and subscription status.
- Search bar in the header to find remotes and resources; the Guests page filters with `tag:`, `remote:`, `node:`, `status:` and `type:` qualifiers.
- Remotes -> Updates: update and package overview across remotes; Remotes -> Tasks and Firewall tabs also exist.
- Guest actions: start, resume, shutdown, snapshots (take, edit description, rollback, delete), migrate, and open in the PVE UI.
- SDN: EVPN zones and VNets can be configured across multiple remotes.
- Ceph: read-only monitoring of the Ceph clusters of hyper-converged PVE remotes.

## Cross-cluster migration
PDM supports live migration of guests between nodes of one remote and between independent remotes (Guests -> Migrate). The Proxmox VE CLI equivalent is `qm remote-migrate <vmid> [<target-vmid>] <target-endpoint> --target-bridge <map> --target-storage <map>`, where the endpoint is `apitoken=<PVEAPIToken=user@realm!token=SECRET>,host=<address>[,fingerprint=<fp>][,port=<port>]`. The bridge and storage options map source IDs to target IDs (a single ID maps all; `1` maps each to itself). In `qm`, the feature is marked experimental, and the original VM is kept stopped on the source cluster unless `--delete` is given. Add `--online` for live migration of a running VM.

## Gotchas
- PDM validates a remote's TLS certificate against the system store; for self-signed certificates it pins the fingerprint you accepted. After the remote renews its certificate, every connection fails until you re-probe: web UI "Check Certificate", or `proxmox-datacenter-manager-client remote probe-certificate <remote> <node>` then `remote set-fingerprint <remote> <node> <fingerprint>` (omit the fingerprint to clear the pin). Confirm the new certificate over a trusted channel first, since an unexpected change can be a man-in-the-middle.
- Every action runs against the backing remote, where that remote's own privileges apply.
- PDM is a rolling release on Debian: use `apt full-upgrade` rather than `apt upgrade`. A separate subscription is not sold; a Basic or higher subscription on your PVE or PBS remotes covers PDM's enterprise repository and support.

## Verify
All remotes show as up on the dashboard; a test VM migrates between clusters and starts with the mapped network.

## Checked
Date: 2026-11-08. Confirmed against the Proxmox Datacenter Manager documentation (introduction, installation FAQ, web interface, remotes, guests, access control, command syntax) and the `qm` manual page for `remote-migrate`. Corrected: the migrated source VM is kept stopped by default (it is not removed after success), and the add-remote flow is documented through the Remotes menu and `remote add`. Removed: the unsupported claims about the leftover-token failure on re-add, migration-port requirements, refusal of guests with local-only devices, PDM/PVE version compatibility and the domain-controller comparison.
Method: documentation only; no commands were run.
