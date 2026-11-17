---
id: computing-software.systems-network-administration.virtualisation.proxmox-firewall-levels-and-rules
name: proxmox-firewall-levels-and-rules
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-firewall, pve-firewall-levels, cluster-fw, host-firewall, vm-firewall, input-policy, pve-firewall-compile, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Configure the Proxmox VE firewall at datacenter, node and VM/CT level: enable order, default policies, rule files in /etc/pve/firewall, macros, and compiling to check rules."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
  - https://pve.proxmox.com/pve-docs/pve-firewall.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox firewall levels and rules

**Goal:** host and guest filtering managed centrally, enabled in an order that never cuts
you off.

## Levels and files
| Level | File | Scope |
|---|---|---|
| Datacenter (cluster) | `/etc/pve/firewall/cluster.fw` | Global enable, default policies, security groups, IP sets, aliases, rules for host traffic |
| Node (host) | `/etc/pve/nodes/<node>/host.fw` | Node-specific host rules and options |
| VM/CT | `/etc/pve/firewall/<vmid>.fw` | Per-guest rules, enabled per NIC (`firewall=1`) |
Guest rules are enforced on the host (with the iptables backend through extra `fwbr` bridges), outside the guest. Rules at host level take precedence over datacenter-level rules.

## Enable in a safe order
1. Datacenter → Firewall → Options: the firewall is disabled by default (`enable: 0`); leave it off while you prepare the input policy (`policy_in: DROP`, `policy_out: ACCEPT`).
2. Prepare management access first. Hosts in the `management` IP set automatically reach 8006 (GUI), 22 (SSH), 5900-5999 (VNC console), 3128 (SPICE proxy) and 60000-60050 (migration); corosync UDP 5405-5412 is allowed in the cluster network. The local cluster network is added to `management` automatically (alias `cluster_network`). Open a separate SSH session before enabling. Other services (for example Ceph) need your own rules.
3. Enable at datacenter level. The host-level `enable` option defaults to 1, so nodes follow once the datacenter firewall is on.
4. For guests: VM → Firewall → Options → enable, set policy, and tick `firewall` on each NIC.

## Rules
```
[RULES]
IN ACCEPT -source +management -p tcp -dport 8006 -log nolog
IN SSH(ACCEPT) -source 10.0.0.0/24
IN ACCEPT -p icmp
```
Macros (SSH, HTTP, HTTPS, Ceph, DNS, ...) cover common services. A rule is `DIRECTION ACTION [OPTIONS]` or `DIRECTION MACRO(ACTION) [OPTIONS]`; prefix a line with `|` to disable it.

## Check before you trust
```sh
pve-firewall status
pve-firewall compile | less       # compile and print the rules (for testing)
pve-firewall localnet             # local network information
pve-firewall simulate --from outside --to host --dport 8006 --source 203.0.113.5   # simulate a flow
```

## Gotchas
- Enabling the datacenter firewall with DROP policy and no management rule locks you out
  of GUI and SSH on every node at once (see the lockout skill).
- Each guest NIC has its own firewall flag; it is required in addition to the guest and datacenter `enable` options.
- `FORWARD` rules (routed traffic, and VNet-level rules in `/etc/pve/sdn/firewall/<vnet>.fw`) are only honoured by the nftables-based `proxmox-firewall` (tech preview); the stock `pve-firewall` ignores them.
- After switching between `pve-firewall` and `proxmox-firewall`, restart running VMs and containers.

## Verify
`pve-firewall status` reports the firewall running (it also warns about configuration errors); GUI and SSH still work from the management network.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, last pushed 2026-10-17). Confirmed: file locations per level; firewall disabled by default and `enable` option; host `enable` default 1; `management` IP set and automatic allowances (8006, 5900-5999, 3128, 22, 60000-60050, corosync 5405-5412 UDP); `pve-firewall` subcommands `compile`, `localnet`, `simulate`, `status`, `start`, `stop`; rule syntax and `|` disable prefix; FORWARD and VNet rules need the nftables backend. Removed: the NIC hot-replug claim and the nmap verification (not documented); Ceph port list (not documented).

Method: documentation only; no commands were run.
