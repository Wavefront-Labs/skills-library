---
id: computing-software.systems-network-administration.proxmox-ve.firewall-enable-and-rules
name: firewall-enable-and-rules
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [firewall, pve-firewall, cluster-fw, ipset]
level: practitioner
status: docs-checked
description: "Enable the Proxmox VE firewall safely and write rules, IP sets, aliases and security groups in cluster.fw and VM fw files."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The firewall is disabled by default. Enable it cluster wide in `/etc/pve/firewall/cluster.fw`:

```
[OPTIONS]
enable: 1
```

Once enabled, traffic to all hosts is blocked by default, with exceptions for the local network reaching the web UI, SSH and other important services. Open an SSH session to a host before enabling, and add rules for remote administration: web GUI (port 8006), SSH (22) and SPICE (3128). An IPSet named `management` holding your remote IPs creates all those rules for you.

Per guest, the firewall must also be switched on for each network device, in addition to the general enable option. Guest rules live in `/etc/pve/firewall/<VMID>.fw`, host rules in `/etc/pve/nodes/<nodename>/host.fw`, where host level overrides datacenter level.

Rule syntax is `DIRECTION ACTION [OPTIONS]` or `DIRECTION MACRO(ACTION)`, and a leading `|` disables a rule:

```
[RULES]
IN SSH(ACCEPT) -i net0 -source +mynetgroup
|IN SSH(ACCEPT) -i net0
IN DROP
```

Use `+name` to reference an IP set. Security groups are defined at cluster level (`[group webserver]`) and applied in a guest with `GROUP webserver`. The `blacklist` IP set drops traffic from its members on every host and VM. `pve-firewall status` compiles the rules and shows warnings for config errors.

## Checked

2026-11-09. Compared with https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html: default-off behaviour, ports, management IP set, config file paths, rule syntax and standard IP sets match.

Method: documentation only; no commands were run.

