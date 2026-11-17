---
id: computing-software.systems-network-administration.linux.vlan-interfaces-8021q
name: vlan-interfaces-8021q
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vlan, vlan-interface, 8021q, vlan-tagging, trunk-port, nmcli, ip-link, systemd-networkd, netplan, networking, sysadmin, rhcsa]
level: practitioner
status: docs-checked
description: "Create 802.1Q VLAN sub-interfaces on Linux with ip, nmcli, networkd or netplan: tagging on a trunk, VLANs on bonds, MTU, and confirming tags on the wire."
sources:
  - https://man7.org/linux/man-pages/man8/ip-link.8.html
  - https://networkmanager.dev/docs/api/latest/settings-vlan.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.netdev.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 802.1Q VLAN interfaces

**Goal:** put a host on several VLANs over one trunk link (or a bond), each with its own
addressing, persistently.

## 1. Prerequisites
- Switch port configured as a trunk carrying those VLAN IDs (and a native/untagged VLAN if the parent also needs an IP).

## 2. Runtime test with ip
```bash
ip link add link enp1s0 name enp1s0.20 type vlan id 20
ip addr add 10.0.20.5/24 dev enp1s0.20
ip link set enp1s0.20 up
ip -d link show enp1s0.20           # shows the vlan protocol and id
```

## 3. Persistent
NetworkManager:
```bash
nmcli con add type vlan con-name vlan20 ifname enp1s0.20 dev enp1s0 id 20 \
  ipv4.method manual ipv4.addresses 10.0.20.5/24
# parent with no IP of its own (pure trunk):
nmcli con mod enp1s0 ipv4.method disabled ipv6.method disabled
```
systemd-networkd:
```ini
# 10-enp1s0.network
[Match]
Name=enp1s0
[Network]
VLAN=vlan20
LinkLocalAddressing=no

# 20-vlan20.netdev
[NetDev]
Name=vlan20
Kind=vlan
[VLAN]
Id=20

# 21-vlan20.network
[Match]
Name=vlan20
[Network]
Address=10.0.20.5/24
```
netplan:
```yaml
network:
  version: 2
  ethernets: {enp1s0: {}}
  vlans:
    vlan20: {id: 20, link: enp1s0, addresses: [10.0.20.5/24]}
```
VLAN on a bond: same, with `dev bond0` / `link: bond0` — create the bond first.

## 4. Confirm tags on the wire
```bash
tcpdump -eni enp1s0 vlan 20 -c5      # -e prints the link-level header
```
Capture on the parent interface to see the tags.

## Gotchas
- Only one default gateway: give it to one VLAN; others get static routes or policy routing.
- Wrong VLAN ID on either side gives "link up, no ARP replies"; check the switch trunk allowed list.

## Verify
- [ ] `ip -d link show <vlan>` shows the right ID and parent; address present; ping the VLAN gateway.
- [ ] `tcpdump -eni <parent> vlan <id>` shows tagged traffic; reboot keeps the VLAN.

## Checked

Date: 2026-10-25. Documentation release: iproute2 man pages ip-link(8), bridge(8) (iproute2/iproute2 mirror, last commit 2026-10-22); NetworkManager settings reference text (NetworkManager main); systemd.network(5)/systemd.netdev(5) man sources (systemd/systemd main); tcpdump(1)/pcap-filter(7), read 2026-10-25.
Confirmed: `ip link add link DEV name NAME type vlan id N` (with `protocol`, default 802.1Q); NetworkManager VLAN settings (parent, id range 0-4094); systemd `[Network] VLAN=`, `[NetDev] Kind=vlan`, `[VLAN] Id=`, `LinkLocalAddressing=`; netplan `vlans` with `id` and `link`; tcpdump `-e`, `-n`, `-i`, `-c` and the `vlan` filter primitive.
Removed as unconfirmed: 8021q module auto-load, `/proc/net/vlan/config`, MTU and rxvlan offload gotchas, tcpdump output text. (The kernel 802.1Q documentation page is no longer in the kernel docs tree.)

Method: documentation only; no commands were run.
