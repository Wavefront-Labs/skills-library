---
id: computing-software.systems-network-administration.virtualisation.proxmox-nftables-firewall
name: proxmox-nftables-firewall
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [proxmox-firewall-nftables, nftables, pve-firewall, proxmox-firewall, forward-rules, vnet-firewall, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Switch Proxmox VE to the nftables-based proxmox-firewall: enabling per node, differences from iptables pve-firewall, forward/vnet rules, checking the ruleset, and rollback."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The nftables-based proxmox-firewall

**Goal:** move to the newer nftables firewall implementation where its features are
needed, with a clean rollback.

## What changes
- `proxmox-firewall` (package of the same name) generates an **nftables** ruleset from the same configuration files and format the iptables-based `pve-firewall` uses.
- Adds **forward** direction rules (routed traffic) and VNet-level rules in `/etc/pve/sdn/firewall/<vnet>.fw`; the stock `pve-firewall` ignores both.
- Opt-in per node via the `nftables` host option (default 0). The documentation calls it tech preview and not suited for production use; check whether that still applies to your release.

## Enable
Install the package (`apt install proxmox-firewall`), then Host → Firewall → Options → **nftables**: yes. Or in `host.fw`:
```
[OPTIONS]
nftables: 1
```
The `proxmox-firewall` service takes over; check that `pve-firewall` no longer generates iptables rules. After enabling or disabling it, restart all running VMs and containers.
```sh
systemctl status proxmox-firewall
nft list ruleset | less
```
The service manages two tables, `proxmox-firewall` and `proxmox-firewall-guests`; your own custom tables are left untouched.

## Differences to watch
- With Linux bridges no extra `fwbrX` firewall bridges are created (guests on OVS bridges still get them).
- `REJECT` is not possible for guest traffic; it is dropped instead.
- The `NDP`, `Router Advertisement` and `DHCP` options always create firewall rules regardless of the default policy.
- Guest rules are evaluated even for connections that have conntrack entries.

## Rollback
Set the value back to 0 / No; the old firewall resumes (restart running guests). `systemctl stop proxmox-firewall` removes all rules the service generated. Keep console access during the switch.

## Verify
`systemctl status proxmox-firewall` is active, `nft list ruleset` contains the expected host and guest chains, and management access still works.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, last pushed 2026-10-17). Confirmed: tech-preview warning; same configuration files; the list of differences (no fwbr on Linux bridges, no REJECT for guests, NDP/RA/DHCP options, conntrack behaviour); forward and VNet rules need the nftables backend; install command, `nftables` option (default 0), required VM/CT restart, `systemctl` control, the two table names, rollback by setting the value back. Removed: Rust and version claims, the logging statement, the `nft flush table` command and the `inet` table family (not documented).

Method: documentation only; no commands were run.
