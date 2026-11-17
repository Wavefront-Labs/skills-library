---
id: computing-software.systems-network-administration.virtualisation.proxmox-corosync-redundant-links
name: proxmox-corosync-redundant-links
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [corosync, corosync-link, knet, corosync-conf, link-priority, retransmit, proxmox-cluster, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Make Proxmox corosync resilient: multiple kronosnet links with priorities, editing corosync.conf safely (config_version), diagnosing retransmits and token timeouts."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
  - https://github.com/proxmox/pve-docs/blob/master/pvecm.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redundant corosync links (kronosnet)

**Goal:** cluster membership that survives a switch or NIC failure and is not disturbed by
storage or backup traffic.

## Design
- Redundancy comes from corosync's integrated **kronosnet (knet)** layer, enabled by giving more than one link address; corosync supports up to 8 links. Every link should be on its own physical network connection, for example link0 a dedicated NIC and link1 another network (shared networks only as a low-priority fallback).
- Latency matters more than bandwidth: storage or other heavy traffic on a shared link raises latency, and under HA a node without quorum is fenced.
- Links are used by priority (`knet_link_priority`, or `priority=` in `pvecm`); the link with the highest priority carries traffic, and equal priorities fall back to the lower link number.

## Edit corosync.conf safely
Never edit `/etc/corosync/corosync.conf` directly; edit the cluster copy:
```sh
cp /etc/pve/corosync.conf /etc/pve/corosync.conf.new
nano /etc/pve/corosync.conf.new     # add ring1_addr per node, an interface with linknumber 1 in totem, increment config_version
cp /etc/pve/corosync.conf /etc/pve/corosync.conf.bak   # backup of the working file
mv /etc/pve/corosync.conf.new /etc/pve/corosync.conf   # the change is picked up automatically
```
Example per node `ring0_addr: 10.99.0.11` / `ring1_addr: 10.98.0.11` (`ringX_addr` is a link address), and in `totem`:
```
interface {
  linknumber: 0
  knet_link_priority: 20
}
interface {
  linknumber: 1
  knet_link_priority: 10
}
```
Always increment `config_version`; omitting it can lead to problems. A new link is enabled when the file is replaced and a restart should not be necessary. Alternatively give the links when creating a cluster: `pvecm create NAME --link0 10.99.0.11,priority=20 --link1 10.98.0.11,priority=10`, or `--link1` on `pvecm add`.

## Diagnose
```sh
corosync-cfgtool -s          # status of the links on this node, with node status per link
corosync-cfgtool -n          # status of known nodes with their link status
journalctl -b -u corosync    # confirm corosync loaded the new link
pvecm status
```

## Gotchas
- Keep the backup copy so you can restore the last working file if the change fails to apply.
- Change only one link address at a time so recovery is easier; changing the cluster network can cause short quorum losses while nodes restart corosync.
- A single link backed by a bond can be problematic in some failure scenarios (asymmetric connectivity); active-backup avoids that case but the documentation still prefers separate knet links over bonds.
- If a corosync link address is a hostname, it is resolved when entered and only the resulting IP is saved; prefer plain IPs.

## Verify
`corosync-cfgtool -s` shows every link connected on every node. To test the new link, temporarily disconnect the old link on one node and check that its status stays online in `pvecm status`.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvecm.adoc, last pushed 2026-10-17) and corosync man pages (github.com/corosync/corosync, man/). Confirmed: kronosnet redundancy and the 8 link limit; link priority semantics (`knet_link_priority`, `priority=` in `pvecm create`, lower link number wins ties); the copy, `.new`, `.bak`, `mv` editing procedure and `config_version` rule; `--link0/--link1` options on `pvecm create` and `pvecm add`; `journalctl -b -u corosync`; the link test by disconnecting the old link; bond caveats; one-address-at-a-time advice. Removed: `passive mode` wording, the Retransmit and Token log-message interpretation, and the claim that a syntax error breaks all nodes (not documented).

Method: documentation only; no commands were run.
