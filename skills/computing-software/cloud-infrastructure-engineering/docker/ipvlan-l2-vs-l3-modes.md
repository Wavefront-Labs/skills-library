---
id: computing-software.cloud-infrastructure-engineering.docker.ipvlan-l2-vs-l3-modes
name: ipvlan-l2-vs-l3-modes
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, ipvlan, ipvlan-l2, ipvlan-l3, ipvlan-mode, routed-container-network, upstream-routes, macvlan-alternative, docker-network-create]
level: advanced
status: docs-checked
description: "Choose and set up ipvlan L2 or L3 networks: shared parent MAC, when L2 beats macvlan, L3 routed subnets with upstream static routes, no broadcast, and host reachability."
sources: ["https://docs.docker.com/engine/network/drivers/ipvlan/", "https://docs.kernel.org/networking/ipvlan.html", "https://docs.docker.com/reference/cli/docker/network/create/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ipvlan L2 vs L3

ipvlan gives containers their own IPs while **sharing the parent interface's MAC**, so the network sees fewer MAC addresses than with macvlan. The kernel documentation suggests ipvlan when the switch allows only one MAC per port or when many MACs would push the NIC into promiscuous mode.

## L2 mode (default)
Containers sit in the parent's subnet; ARP and broadcast work; the upstream router sees
many IPs behind one MAC.
```bash
docker network create -d ipvlan \
  --subnet 192.168.1.0/24 --gateway 192.168.1.1 --ip-range 192.168.1.192/27 \
  -o parent=eth0 -o ipvlan_mode=l2 lan-l2
```
Use when: you want macvlan semantics but the port has a MAC limit. Limits:
- DHCP servers and anything keyed on MAC (static leases, NAC) see one MAC for all containers.
- The default (host) namespace is not reachable from the containers by design, and containers cannot ping the parent's addresses.

## L3 mode
The host acts as a router for container subnets. No ARP or broadcast/multicast across the
parent; containers in **different subnets** on the same parent can talk to each other
(routed by the host), and the outside world reaches them via routes you add upstream.
```bash
docker network create -d ipvlan \
  --subnet 10.200.1.0/24 --subnet 10.200.2.0/24 \
  -o parent=eth0 -o ipvlan_mode=l3 routed

docker run -d --network routed --ip 10.200.1.10 --name api myapi
```
- `--gateway` is ignored in L3; containers get a default route via their interface.
- Upstream router (or each LAN host) needs a static route:
  `ip route add 10.200.0.0/16 via <docker host LAN IP>`. Without it containers can send but
  replies never come back.
- `ipvlan_mode=l3s` is the same but traffic traverses the host's netfilter (iptables/nft
  rules and conntrack apply), useful when you need host-side filtering.
- No broadcast means no mDNS/DHCP/Wake-on-LAN for these containers.
- Kernel ≥ 4.2.

## Choosing
| Need | Pick |
|---|---|
| LAN presence, wired, multiple MACs allowed | macvlan |
| LAN presence, MAC-restricted port | ipvlan L2 |
| Large container address space, routable, many subnets, no L2 flooding | ipvlan L3 |
| Host must be able to filter traffic | ipvlan L3S or plain bridge |

## Extra options
- `-o ipvlan_flag=bridge|private|vepa` (bridge default): `private` blocks container-to-container
  on the same parent; `vepa` hairpins via the external switch.
- 802.1q sub-interfaces: `-o parent=eth0.30` (Docker creates them on the fly).

## Verify
```bash
docker exec api ip -d link show eth0          # "ipvlan mode l3"
docker exec api ip route                      # default dev eth0
# from another LAN host after adding the static route:
ping -c1 10.200.1.10
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the ipvlan driver page (options `ipvlan_mode` l2/l3/l3s, `ipvlan_flag` bridge/private/vepa, parent sub-interfaces, L3 drops broadcast/multicast, needs route distribution, no gateway in L3, kernel 4.2+, default namespace unreachable) and the kernel ipvlan documentation (L3S conntrack/iptables, flag semantics, when to choose ipvlan). Removed unconfirmed claims about Wi-Fi and cloud NICs and the host shim interface.

Method: documentation only; no commands were run.
