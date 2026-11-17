---
id: computing-software.networking-hardware-and-wireless.strongswan.network-namespaces-multiple-instances
name: network-namespaces-multiple-instances
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, network-namespaces, netns, veth, piddir]
level: advanced
status: docs-checked
description: "Run strongSwan in Linux network namespaces: ip netns and veth basics, one daemon via ip netns exec, and several instances with per-netns config and a relocated piddir."
sources:
  - https://docs.strongswan.org/docs/latest/howtos/nameSpaces.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# network namespaces multiple instances
Network namespaces give separate instances of interfaces, routing tables and firewall rules. Manage them with `ip netns` (as root).

**Basics.**
- `ip netns add <name>`, `ip netns list`
- `ip link set <interface> netns <name>` moves an interface; list inside with `ip netns exec <name> ip link list`
- A veth pair (`ip link add <if1> type veth peer name <if2>`, needs CONFIG_VETH) acts like a bidirectional pipe; put one end inside the netns and keep the other outside, e.g. in a bridge or used by routing rules
- Interfaces moved into a netns are disabled: assign an address and bring them up with `ip netns exec <name> ip addr add ...` and `ip link set dev <if> up`
- Run routes and firewall rules in a netns with `ip netns exec <name> <command>`

**One instance.** Start the daemon inside the netns and run swanctl as `ip netns exec <name> swanctl <command>`.

**Several instances.** All netns share one file system. `ip netns exec` bind-mounts every file under `/etc/netns/<name>/` over its counterpart in `/etc/` (the file must exist there). Use this for per-instance config files and to move the piddir, where charon keeps its PID file and UNIX sockets (default `/var/run`, which would conflict).

Build with `--sysconfdir=/etc` and, for example, `--with-piddir=/etc/ipsec.d/run`. After install create the directories: `/etc/ipsec.d/run` and `/etc/netns/<netns name>/ipsec.d/run` for each namespace. Differing config files are modified copies placed under `/etc/netns/<name>/`.

## Checked
2026-11-04. Confirmed against the strongSwan network namespaces how-to: ip netns, ip link, veth and CONFIG_VETH, ip netns exec for swanctl, /etc/netns bind mounts, --sysconfdir and --with-piddir. Nothing removed.

Method: documentation only; no commands were run.
