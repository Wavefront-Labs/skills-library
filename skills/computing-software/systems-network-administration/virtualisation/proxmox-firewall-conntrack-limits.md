---
id: computing-software.systems-network-administration.virtualisation.proxmox-firewall-conntrack-limits
name: proxmox-firewall-conntrack-limits
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [nf-conntrack, conntrack, proxmox, firewall, netfilter]
level: advanced
status: docs-checked
description: "Size and tune netfilter connection tracking on Proxmox VE hosts with the firewall enabled: nf_conntrack_max, timeouts, invalid packet handling and table-full symptoms."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
  - https://pve.proxmox.com/pve-docs/pve-firewall.8.html
  - https://github.com/proxmox/pve-docs/blob/master/generated/pve-firewall-host-opts.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection tracking limits

**Goal:** the PVE firewall never drops traffic because the conntrack table is full.

## Symptoms
- `dmesg` shows the kernel message that the conntrack table is full and packets are being dropped.
- Random new connections fail to busy guests (web, DNS, NAT gateways) while established ones work.

## Check
```bash
cat /proc/sys/net/netfilter/nf_conntrack_count
cat /proc/sys/net/netfilter/nf_conntrack_max
```

## Tune (host firewall options)
Node -> Firewall -> Options, or `/etc/pve/nodes/<node>/host.fw`:
```
[OPTIONS]
nf_conntrack_max: 1048576
nf_conntrack_tcp_timeout_established: 86400
nf_conntrack_tcp_timeout_syn_recv: 60
nf_conntrack_allow_invalid: 0
nf_conntrack_helpers: ftp
```
- Defaults per the host options reference: `nf_conntrack_max` 262144 (minimum 32768), `nf_conntrack_tcp_timeout_established` 432000 s (5 days; minimum 7875), `nf_conntrack_tcp_timeout_syn_recv` 60 (range 30-60), `nf_conntrack_allow_invalid` 0.
- Lower the established timeout on hosts carrying many short-lived flows.
- `nf_conntrack_allow_invalid: 1` accepts packets conntrack marks invalid; prefer fixing the cause (for example asymmetric routing).
- `nf_conntrack_helpers` enables conntrack helpers for named protocols; supported: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp.
- `log_nf_conntrack: 1` (default 0) logs conntrack information in the firewall log.

## Gotchas
- The conntrack table is a single limit per node, so one busy guest can exhaust it for every guest on that node.
- With the nftables backend (`proxmox-firewall`, tech preview) guest firewall rules are evaluated even for connections that already have conntrack entries.

## Verify
After the change, `/proc/sys/net/netfilter/nf_conntrack_max` reports the new value and `nf_conntrack_count` stays below it under load.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, last pushed 2026-10-17). Confirmed: host option names `nf_conntrack_max`, `nf_conntrack_tcp_timeout_established`, `nf_conntrack_tcp_timeout_syn_recv`, `nf_conntrack_allow_invalid`, `nf_conntrack_helpers`, `log_nf_conntrack`; their defaults and ranges; the supported helper list; the nftables note that guest rules apply even with conntrack entries. Removed: per-entry memory figure, the `conntrack` tool and awk pipeline, the claim that `firewall=0` removes a NIC from conntrack (none documented).

Method: documentation only; no commands were run.
