---
id: computing-software.systems-network-administration.virtualisation.proxmox-firewall-rule-syntax-and-macros
name: proxmox-firewall-rule-syntax-and-macros
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-fw-rules, firewall-macro, pve-firewall, cluster-fw, ipset, proxmox]
level: practitioner
status: docs-checked
description: "Write Proxmox firewall rules directly in .fw files: section layout, rule syntax, macros, aliases, IP sets, security group references and validating with pve-firewall."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
  - https://pve.proxmox.com/pve-docs/pve-firewall.8.html
  - https://github.com/proxmox/pve-docs/blob/master/generated/pve-firewall-rules-opts.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox firewall rule syntax and macros

## Files
| Level | File |
|---|---|
| Datacenter | `/etc/pve/firewall/cluster.fw` |
| Host | `/etc/pve/nodes/<node>/host.fw` |
| VM/CT | `/etc/pve/firewall/<vmid>.fw` |
| SDN VNet (nftables backend only) | `/etc/pve/sdn/firewall/<vnet>.fw` |

## cluster.fw example
```ini
[OPTIONS]
enable: 1
policy_in: DROP
policy_out: ACCEPT

[ALIASES]
mgmt_net 10.0.5.0/24
monitoring 10.0.9.50

[IPSET admins]
mgmt_net
10.0.6.10

[RULES]
IN ACCEPT -source +admins -p tcp -dport 8006 -log nolog
IN SSH(ACCEPT) -source +admins
IN ACCEPT -source monitoring -p udp -dport 161
IN Ping(ACCEPT) -source mgmt_net

[group webserver]
IN HTTP(ACCEPT)
IN HTTPS(ACCEPT)
IN ACCEPT -p tcp -dport 8443 -source 10.0.0.0/8
```

## Rule syntax
`DIRECTION ACTION [options]`
- DIRECTION: `IN`, `OUT` or `FORWARD` (`FORWARD` is only honoured by the nftables backend). A line `GROUP <name>` references a security group.
- ACTION: `ACCEPT`, `DROP`, `REJECT`, or `Macro(ACTION)`.
- Options: `-source`, `-dest` (IP, CIDR, alias, `+ipset`, ranges `10.0.0.1-10.0.0.9`, comma lists; do not mix IPv4 and IPv6 in one list), `-p` protocol, `-dport`/`-sport` (service name or number, range `80:85`, comma list), `-i` interface (VM: `net0`), `-icmp-type` (only with icmp protocols), `-log <level>`.
- Disable a rule by prefixing with `|`.
- Macros include `SSH`, `HTTP`, `HTTPS`, `DNS`, `Ping`, `SMB`, `Ceph`, `RDP`, `SNMP`, `NTP`, `PostgreSQL`, `MySQL`; there is no `NFS` macro, so write the ports yourself. Full list: the Macro dropdown in the GUI rule editor or the macros table in the firewall chapter.

## VM file
```ini
[OPTIONS]
enable: 1
ipfilter: 1

[RULES]
GROUP webserver -i net0
IN SSH(ACCEPT) -source +admins
```
A `GROUP` line applies a datacenter-level security group to the guest.

## Validate and apply
```sh
pve-firewall compile | less    # compile and print the rules (for testing)
pve-firewall status            # reads and compiles all rules; warns about configuration errors
pve-firewall simulate --from outside --to host --dport 8006 --source 203.0.113.5
```

## Verify
`pve-firewall status` shows no warnings; `pve-firewall simulate` reports the expected verdict for an allowed and a denied flow.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, last pushed 2026-10-17). Confirmed: rule grammar (`DIRECTION ACTION`, `DIRECTION MACRO(ACTION)`, `|` to disable), IN/OUT/FORWARD, option semantics for source, dest, dport, iface, icmp-type, log, proto; the macro list (SSH, HTTP, HTTPS, DNS, Ping, SMB, Ceph, RDP, SNMP present; NFS absent); `GROUP name` rule line and `-i` on it as used in the docs; `pve-firewall compile`, `status`, `simulate`. Removed: `NFS` macro, `+dc/` and `+guest/` prefixes and the 8.3 VNet version (not documented), the claim about syntax errors and apply timing.

Method: documentation only; no commands were run.
