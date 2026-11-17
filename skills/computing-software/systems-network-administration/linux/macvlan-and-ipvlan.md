---
id: computing-software.systems-network-administration.linux.macvlan-and-ipvlan
name: macvlan-and-ipvlan
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, macvlan, ipvlan, macvtap, l2, l3, container-networking, podman-macvlan, ip-link, networking, sysadmin]
level: advanced
status: gated
description: "Give containers or namespaces their own LAN presence with macvlan or ipvlan: mode choice, the host-cannot-reach-child trap and its shim fix, and when ipvlan beats macvlan."
sources:
  - https://man7.org/linux/man-pages/man8/ip-link.8.html
  - https://docs.kernel.org/networking/ipvlan.html
  - https://docs.podman.io/en/latest/markdown/podman-network-create.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macvlan and ipvlan

**Goal:** attach containers/namespaces directly to the physical network (own IP, no NAT,
no bridge) and avoid the classic "host can't talk to its own containers" outage.

## 1. Pick the driver
| Need | Use |
|---|---|
| Each child needs its own MAC (DHCP per child, MAC-based switch policy) | macvlan `bridge` mode |
| Upstream allows only one MAC per port, or many MACs would push the NIC into promiscuous mode | ipvlan `l2` (children share the parent MAC) |
| Routed design, no broadcast domain sharing | ipvlan `l3` (default ipvlan mode; slaves neither send nor receive multicast or broadcast) |
| ipvlan l3 but iptables connection tracking must work | ipvlan `l3s` |
| VM attach without a bridge | macvtap (libvirt `type='direct'`) |
macvlan modes: `bridge` (endpoints connected directly to each other), `vepa` (traffic between children goes out through the switch; the default macvlan mode, needs a hairpin-capable switch or a router), `private` (children cannot talk to each other), `passthru` (one child gets all traffic), `source` (match allowed source MACs). ipvlan flags: `bridge` (default), `private`, `vepa`.

## 2. Create
```bash
ip link add mv0 link enp1s0 type macvlan mode bridge     # without "mode" macvlan defaults to vepa
ip netns add app1; ip link set mv0 netns app1
ip -n app1 addr add 10.0.10.50/24 dev mv0; ip -n app1 link set mv0 up
ip -n app1 route add default via 10.0.10.1

ip link add ipv0 link enp1s0 type ipvlan mode l2
```
Podman: `podman network create -d macvlan -o parent=enp1s0 --subnet 10.0.10.0/24 --gateway 10.0.10.1 lan`
then `podman run --network lan --ip 10.0.10.51 ...` (`-o parent=` also works for ipvlan per the podman-network-create man page).

## 3. The host-to-child trap
The host usually cannot reach its own macvlan/ipvlan children through the parent interface (gated: unconfirmed, source is paywalled or blocked). The kernel and iproute2 documentation does not describe this. A common workaround is a host-side child (shim) with a route (gated: unconfirmed, source is paywalled or blocked):
```bash
ip link add mv-host link enp1s0 type macvlan mode bridge
ip addr add 10.0.10.49/32 dev mv-host; ip link set mv-host up
ip route add 10.0.10.48/28 dev mv-host        # the range your containers use
```
Persist with a networkd `.netdev` (`Kind=macvlan`) and `MACVLAN=mv-host` in the parent's `.network`, or a NetworkManager macvlan profile.

## Gotchas
- ipvlan is the documented alternative when the switch or router allows only one MAC per port, or when many virtual devices would exceed the NIC's MAC capacity and put it in promiscuous mode; it is also intended for untrusted network namespaces.
- ipvlan children use the parent's MAC address, so MAC-keyed DHCP leases cannot tell them apart.
- In ipvlan vepa mode, packets to an adjacent neighbour have identical source and destination MAC and make the switch or router send redirects.

## Verify
- [ ] From another LAN host, ping the child IP; `ip neigh` there shows the child's own MAC (macvlan) or the parent MAC (ipvlan).
- [ ] With a shim in place, `ping` from the host to a container succeeds (gated: unconfirmed, source is paywalled or blocked).

## Checked

Date: 2026-10-25. Documentation release: ip-link(8) macvlan and ipvlan sections (iproute2 mirror 2026-10-22), kernel Documentation/networking/ipvlan.rst, podman-network-create(1) (containers/podman main), read 2026-10-25.
Confirmed: macvlan modes private, vepa (default), bridge, passthru, source; macvtap; ipvlan modes l3 (default), l3s, l2 and flags bridge/private/vepa; l3 mode drops multicast/broadcast; ipvlan vs macvlan selection criteria; ipvlan vepa redirect note; podman `-d macvlan -o parent=`.
Gated: the host-to-child behaviour and the shim workaround are not described in the kernel, iproute2 or podman documentation read; they carry the gated marker.
Removed as unconfirmed: VMware vSwitch settings, cloud VPC and Wi-Fi limitations, DHCP client-id remark.

Method: documentation only; no commands were run.
