---
id: computing-software.systems-network-administration.linux.gre-ipip-vxlan-tunnels-with-ip-link
name: gre-ipip-vxlan-tunnels-with-ip-link
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, gre-tunnel, vxlan, ipip, ip-link, overlay-network, mtu, tunnels]
level: advanced
status: docs-checked
description: "Build point-to-point and overlay tunnels with iproute2: GRE/GRETAP, IPIP, VXLAN with static or multicast peers, MTU math, firewalling and persistence."
sources:
  - https://man7.org/linux/man-pages/man8/ip-link.8.html
  - https://docs.kernel.org/networking/vxlan.html
  - https://man7.org/linux/man-pages/man8/ip-tunnel.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GRE, IPIP and VXLAN tunnels

## GRE (L3, any protocol, IP proto 47)
```bash
# host A 203.0.113.1 <-> host B 198.51.100.2
ip tunnel add gre1 mode gre local 203.0.113.1 remote 198.51.100.2 ttl 64
ip addr add 10.255.0.1/30 dev gre1 && ip link set gre1 up mtu 1476
ip route add 10.20.0.0/16 via 10.255.0.2
```
Mirror on B. GRE itself provides no encryption. L2 variant: `ip link add gretap1 type gretap local ... remote ...` (link type listed in ip-link(8); a gretap interface can be added to a bridge).

## IPIP (IPv4-in-IPv4 only, smallest overhead)
`ip tunnel add ipip1 mode ipip local A remote B` — inner MTU 1480 on a 1500 underlay (20-byte outer IPv4 header).

## VXLAN (L2 over UDP 4789)
```bash
ip link add vxlan100 type vxlan id 100 dstport 4789 local 192.0.2.11 dev eth0 nolearning
bridge fdb add to 00:17:42:8a:b4:05 dev vxlan100 dst 192.0.2.12     # static forwarding entry: remote MAC -> remote VTEP
ip link set vxlan100 up mtu 1450
ip link add br100 type bridge && ip link set vxlan100 master br100 && ip link set br100 up
```
Multicast instead: `group 239.1.1.100 dev eth0` handles traffic with no forwarding-table entry (kernel vxlan docs). The kernel's default destination port predates the IANA-assigned 4789, so always set `dstport 4789` explicitly. Show the table with `bridge fdb show dev vxlan100`.

## MTU math
Outer 1500: GRE −24 (20 IPv4 + 4 GRE) → 1476; IPIP −20 → 1480; VXLAN −50 (20 IPv4 + 8 UDP + 8 VXLAN + 14 inner Ethernet) → 1450 (IPv4 underlay). Set the inner MTU or clamp MSS, for example with iptables:
`iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`.

## Firewall
Allow IP protocol 47 (GRE), IP protocol 4 (IPIP) or UDP port 4789 (VXLAN) between the tunnel endpoints only.

## Persist
`nmcli con add type ip-tunnel mode gre ifname gre1 remote 198.51.100.2 local 203.0.113.1 ip4 10.255.0.1/30` (NetworkManager `ip-tunnel` modes include ipip, gre, gretap), `nmcli con add type vxlan ifname vxlan100 id 100 remote ...`; or systemd-networkd `.netdev` `Kind=gre` or `Kind=vxlan`.

## Verify
- [ ] `ping -M do -s <mtu-28> <peer-inner-ip>` succeeds (`-M do` sets the DF flag; 28 = 20 IP + 8 ICMP header bytes); `tcpdump -ni eth0 udp port 4789` shows VXLAN traffic.

## Checked

Date: 2026-10-25. Documentation release: ip-link(8), ip-tunnel(8), bridge(8) (iproute2 mirror, 2026-10-22), kernel Documentation/networking/vxlan.rst, NetworkManager settings text, systemd.netdev(5), iptables-extensions(8) (TCPMSS), ping(8) (iputils), read 2026-10-25.
Confirmed: `ip tunnel add ... mode gre|ipip ... local remote ttl`; gre, gretap, ipip and vxlan link types; vxlan `id`, `group`, `dev`, `dstport`, `[no]learning`; `bridge fdb add to MAC dst IP dev vxlan0` and `bridge fdb show`; UDP 4789 as the IANA port with a different historical kernel default; `--clamp-mss-to-pmtu` rule form; `ping -M do`; NetworkManager `ip-tunnel` mode list and `vxlan` id/remote settings; systemd `Kind=` gre and vxlan. Header overheads are arithmetic (IPv4 underlay).
Removed as unconfirmed: the all-zero-MAC head-end replication entries, EVPN/FRR statement, the nft maxseg and ip protocol rules, the Red Hat blog link.

Method: documentation only; no commands were run.
