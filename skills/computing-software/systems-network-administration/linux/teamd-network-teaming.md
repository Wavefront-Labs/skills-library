---
id: computing-software.systems-network-administration.linux.teamd-network-teaming
name: teamd-network-teaming
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, teamd, team-driver, teamdctl, nic-teaming, runner, activebackup, lacp, link-watch, nmcli-team, rhel, networking, sysadmin]
level: practitioner
status: docs-checked
description: "Run or retire NIC teaming with teamd: runners and link watchers, nmcli team profiles, teamdctl state, and migrating team to bond because RHEL 9 deprecated and RHEL 10 removed teamd."
sources:
  - https://man.archlinux.org/man/teamd.conf.5
  - https://man.archlinux.org/man/teamdctl.8
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# teamd network teaming

**Goal:** operate existing team0 setups correctly, and know the kernel bonding equivalents
when a team has to be rebuilt as a bond (see the bonding skills).

## 1. Model
Kernel `team` driver + userspace `teamd` daemon (one per team). Behaviour = **runner**:
`activebackup`, `loadbalance`, `lacp`, `broadcast`, `roundrobin`, `random`.
Failure detection = **link_watch**: `ethtool` (libteam ethtool state changes), `arp_ping`, `nsna_ping` (IPv6 neighbour solicitation).

## 2. Create with NetworkManager
```bash
nmcli con add type team con-name team0 ifname team0 \
  team.runner activebackup team.link-watchers "name=ethtool" \
  ipv4.method manual ipv4.addresses 10.0.10.20/24 ipv4.gateway 10.0.10.1
nmcli con add type team-slave con-name team0-p1 ifname enp1s0 master team0
nmcli con add type team-slave con-name team0-p2 ifname enp2s0 master team0
nmcli con up team0
```
LACP: `team.runner lacp team.runner-tx-hash "eth,ipv4,ipv6,l4"` (hash fragments eth, vlan, ipv4, ipv6, ip, l3, tcp, udp, sctp, l4; default eth, ipv4, ipv6) — the switch ports must be an LACP port-channel.
Raw JSON equivalent (teamd.conf): `{"runner": {"name": "activebackup"}, "link_watch": {"name": "ethtool"}}`.

## 3. Inspect and operate
```bash
teamdctl team0 state                 # runner, active port, link state per port
teamdctl team0 config dump actual
teamnl team0 ports
teamdctl team0 state item set runner.active_port enp2s0    # manual failover
```

## 4. Rebuilding as a bond
There is no per-runner conversion table in the teamd or kernel docs; choose the bond mode from the
switch design (see `bonding-modes-and-xmit-hash-policy`): activebackup maps to `active-backup`,
lacp to `802.3ad`, roundrobin to `balance-rr`, an ethtool link watcher to `miimon`, an arp_ping
watcher to `arp_interval`/`arp_ip_target`. Do it from a console: the team profile and the bond
share the NICs. Check the result with `cat /proc/net/bonding/bond0`.

## Gotchas
- LACP runner with a non-LACP switch: ports stay unaggregated; read `teamdctl team0 state` for the per-port LACP state.
- Mixing team and bond config tools on the same NICs leaves stale profiles; delete old team-slave profiles after migration.

## Verify
- [ ] `teamdctl team0 state` shows both ports `up` and the expected active port; unplugging it fails over with ≤ 1 lost ping.
- [ ] After rebuilding as a bond, `/proc/net/bonding/bond0` shows the matching mode and both slaves `MII Status: up`.

## Checked

Date: 2026-10-25. Documentation release: libteam man pages teamd.conf(5), teamdctl(8), teamnl(8) (jpirko/libteam master, last commit 2026-10-13); NetworkManager settings reference (main).
Confirmed: runners (roundrobin, broadcast, random, activebackup, loadbalance, lacp), link watchers (ethtool, arp_ping, nsna_ping), `teamdctl` commands `state`, `config dump actual`, `state item set runner.active_port` (activebackup only), `teamnl ports`, and `runner.tx_hash` fragments and default; NetworkManager `team.runner`, `team.link-watchers` and `team.runner-tx-hash` properties.
Removed as unconfirmed: the `team2bond` tool and its flags, the RHEL 9/10 deprecation dates, the `dnf` package names and Red Hat link (Red Hat docs are not readable here), and the NetworkManager restart claim.

Method: documentation only; no commands were run.
