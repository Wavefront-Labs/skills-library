---
id: computing-software.systems-network-administration.virtualisation.proxmox-firewall-security-groups-ipsets
name: proxmox-firewall-security-groups-ipsets
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-security-group, pve-ipset, pve-firewall, aliases, ipfilter, ip-spoofing, micro-segmentation, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Reuse Proxmox firewall rules with security groups, IP sets and aliases; stop IP spoofing with ipfilter sets; build simple micro-segmentation between guest tiers."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
  - https://pve.proxmox.com/pve-docs/pve-firewall.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox firewall security groups, IP sets and aliases

**Goal:** write a rule once and apply it to many guests; keep guests from spoofing other
addresses.

## Aliases and IP sets
- **Alias:** a name for an IP address or network (`dbnet 10.0.30.0/24`); usable in IP set definitions and in the `source` and `dest` of rules. `local_network` is defined automatically.
- **IP set:** a named list referenced as `+name` in `source` and `dest`; standard sets are `management`, `blacklist` (dropped by every host and VM firewall) and `ipfilter-net*`.
```
# cluster.fw
[ALIASES]
monitoring 10.0.5.10
dbnet 10.0.30.0/24

[IPSET webservers]
10.0.20.21
10.0.20.22
```
Reference in rules as `-source +webservers` or `-dest dbnet`.

## Security groups
A named rule bundle defined at datacenter level, attached to any guest:
```
[group web-tier]
IN HTTPS(ACCEPT)
IN HTTP(ACCEPT)
IN ACCEPT -source monitoring -p tcp -dport 9100

[group db-tier]
IN ACCEPT -source +webservers -p tcp -dport 5432
```
Attach it in the guest's firewall rules with a `GROUP web-tier` line (or the GUI's Insert: Security Group).

## Anti-spoofing with ipfilter
A per-VM IP set named `ipfilter-net0` lists the IPs that NIC may use as source; outgoing traffic with another source IP is dropped. The VM option `ipfilter: 1` has the same effect as an empty `ipfilter-net<id>` set per interface, which implicitly contains the container's configured IPs and the MAC-derived IPv6 link-local address. `macfilter` defaults to 1.

## Micro-segmentation pattern
Guest policy IN DROP, OUT ACCEPT (or DROP with explicit allows) and one security group per tier. Log drops on rules being tuned (`-log info`) and read them in the GUI Firewall -> Log view.

## Verify
`pve-firewall compile` runs without errors and shows the group's rules for each guest that uses it.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, last pushed 2026-10-17). Confirmed: security group definition (`[group name]` at datacenter level) and `GROUP name` in a guest `[RULES]`; aliases usable in IP sets and rule source/dest; `+name` IP set syntax; standard sets `management`, `blacklist`, `ipfilter-net*` and their behaviour; `ipfilter` and `macfilter` (default 1) VM options. Removed: `!` exclusions, the `journalctl -u pvefw-logger` advice, the Ansible/Terraform remark and the spoofing test (not documented).

Method: documentation only; no commands were run.
