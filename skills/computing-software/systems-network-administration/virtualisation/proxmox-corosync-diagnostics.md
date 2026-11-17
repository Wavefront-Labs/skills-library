---
id: computing-software.systems-network-administration.virtualisation.proxmox-corosync-diagnostics
name: proxmox-corosync-diagnostics
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [corosync-cfgtool, corosync, pvecm, proxmox-cluster, knet, quorum, proxmox]
level: advanced
status: docs-checked
description: "Diagnose Proxmox cluster communication with pvecm status, corosync-cfgtool link status, corosync-quorumtool and journal patterns like retransmit lists and token timeouts."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvecm.html
  - https://github.com/proxmox/pve-docs/blob/master/pvecm.adoc
  - https://github.com/corosync/corosync/blob/main/man/corosync-cfgtool.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Corosync diagnostics on Proxmox VE

## Quick health
```sh
pvecm status            # cluster information, quorum information and membership
pvecm nodes             # membership list
corosync-cfgtool -s     # status of the links on this node, with node status per link (knet)
corosync-cfgtool -n     # status of known nodes with their link status
corosync-quorumtool -s  # quorum status; -l lists nodes
```
Healthy: every link is connected to every peer and the cluster is quorate.

## Logs
```sh
journalctl -b -u corosync
systemctl status corosync
```
Read the corosync journal on every node for the same time window and compare link and membership messages.

## Typical causes
- Corosync needs consistent low latency but little bandwidth. Sharing its network with storage or other heavy traffic raises latency; with HA a node that loses quorum with active services is fenced after the 60 second watchdog timeout. Give corosync its own physical network (a dedicated 1 Gbit NIC is enough) and a second link on a different physical network; shared networks are acceptable only as a low-priority fallback.
- Nodes must reach each other on UDP ports 5405-5412 (corosync) and TCP 22 (SSH); check firewalls.
- A bond as the only corosync link can fail asymmetrically: LACP bonds should use `bond-lacp-rate fast` on both the node and the switch, and balance-rr, balance-xor, balance-tlb and balance-alb are advised against.
- Hostnames used as link addresses can change what they resolve to; prefer static IPs.

## Measure latency
Requirement: latency under 5 ms between all nodes. Higher latency may work in small clusters, but the documentation calls it unlikely to stay stable with more than three nodes and latencies above around 10 ms. Test with `ping` between the nodes on the cluster network, also while the network is busy.

Token timeout and consensus timeout derive from the token coefficient. Check the live values:
```sh
corosync-cmapctl | grep -Ew 'runtime.config.totem.token|runtime.config.totem.consensus'
```
Default formulas: `token = 3000 + (number_of_nodes - 2) * token_coefficient` ms and `consensus = 1.2 * token`. The token coefficient defaults to 650 ms; clusters created since Proxmox VE 9.2 set `token_coefficient: 125` explicitly. The documentation suggests lowering the coefficient when token plus consensus exceeds 30 s, and with HA that sum must stay below 45 s so a new membership forms before the 60 s watchdog fires.

## Gotchas
- Editing corosync.conf: work on a copy of `/etc/pve/corosync.conf` (changes there propagate to the local file, not vice versa), **increment `config_version`**, then move the copy into place.
- `pvecm expected 1` makes a non-quorate node quorate so you can fix configuration; use it only if you understand what you are doing.

## Verify
After fixes, `corosync-cfgtool -s` shows all links connected, `pvecm status` stays quorate under load, and there is no unexpected HA fencing.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvecm.adoc, last pushed 2026-10-17) and corosync man pages (github.com/corosync/corosync, man/). Confirmed: `pvecm status|nodes|expected`; `corosync-cfgtool -s|-n` and `corosync-quorumtool -s|-l` options; network requirements (UDP 5405-5412, TCP 22, latency under 5 ms, dedicated 1 Gbit NIC); bond caveats; token and consensus formulas, 650 ms default, 125 ms for new clusters from 9.2, 30 s and 45 s limits, the 60 s watchdog; `corosync-cmapctl` command; corosync.conf editing rules. Removed: the log-pattern table, the pmxcfs `cpg_send_message` entry, the IGMP/multicast claim, storm-control and MTU causes and the ping flags (not documented).

Method: documentation only; no commands were run.
