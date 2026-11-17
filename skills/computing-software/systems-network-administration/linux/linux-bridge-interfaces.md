---
id: computing-software.systems-network-administration.linux.linux-bridge-interfaces
name: linux-bridge-interfaces
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bridge, bridge-interface, bridge-utils, br0, ip-link-bridge, bridge-fdb, nmcli-bridge, kvm-bridge, br-netfilter, networking, sysadmin]
level: practitioner
status: docs-checked
description: "Build a Linux bridge (br0) so VMs and containers share the LAN: moving the host IP to the bridge, nmcli/networkd config, the bridge command, br_netfilter and remote-cutover safety."
sources:
  - https://man7.org/linux/man-pages/man8/bridge.8.html
  - https://networkmanager.dev/docs/api/latest/settings-bridge.html
  - https://docs.kernel.org/networking/bridge.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux bridge interfaces

**Goal:** a software switch (`br0`) with the physical NIC as a port, so VMs/containers get
addresses on the real LAN, while the host keeps its own IP — on the bridge, not the NIC.

## 1. The rule that trips everyone
Once a NIC is a bridge port, configure the host address on the bridge (`br0`), not on the port. Doing this over SSH on that NIC disconnects you mid-change —
use a console, a second NIC, or a single atomic nmcli/netplan apply.

## 2. Runtime (testing)
```bash
ip link add br0 type bridge
ip link set enp1s0 master br0
ip addr flush dev enp1s0
ip addr add 10.0.10.20/24 dev br0; ip link set br0 up; ip route add default via 10.0.10.1
bridge link                 # ports and their STP state
bridge fdb show br br0      # learned MACs per port
```
Use `bridge` and `ip link` (iproute2) as above.

## 3. Persistent with NetworkManager
```bash
nmcli con add type bridge con-name br0 ifname br0 \
  ipv4.method manual ipv4.addresses 10.0.10.20/24 ipv4.gateway 10.0.10.1 ipv4.dns 10.0.0.53 \
  bridge.stp no
nmcli con add type bridge-slave con-name br0-port1 ifname enp1s0 master br0
nmcli con down "Wired connection 1"; nmcli con up br0     # run as one line over SSH
```
systemd-networkd: `br0.netdev` (`Kind=bridge`), NIC `.network` with `Bridge=br0`, and
`br0.network` with the address. Netplan: `bridges: {br0: {interfaces: [enp1s0], addresses: [...]}}`.

## 4. Tuning
- With STP enabled, ports spend `forward_delay` in listening and again in learning before forwarding, which can make DHCP in guests time out; on a single-uplink host bridge `bridge.stp no` avoids that.
- `bridge.mac-address` pins the bridge MAC; if unset, NetworkManager derives it from `ethernet.cloned-mac-address`, so pin it when DHCP reservations must not change.

## Gotchas

## Verify
- [ ] `ip -br addr`: the address is on `br0`, none on the port; `bridge link` shows the port `forwarding`.
- [ ] A VM attached to `br0` gets a LAN DHCP address; `bridge fdb show br br0` lists its MAC.

## Checked

Date: 2026-10-25. Documentation release: iproute2 man pages ip-link(8), bridge(8) (iproute2/iproute2 mirror, last commit 2026-10-22); kernel bridge.rst; NetworkManager settings reference text (NetworkManager main); systemd.network(5)/systemd.netdev(5) man sources (systemd/systemd main), read 2026-10-25.
Confirmed: `ip link add ... type bridge`, `ip link set ... master`, `bridge link`, `bridge fdb show br br0`; NetworkManager `bridge.stp`, `bridge.forward-delay`, `bridge.mac-address` behaviour; systemd `Bridge=` in the port `.network`; netplan `bridges` with `interfaces` and `addresses`; STP states and forward delay.
Removed as unconfirmed: the brctl deprecation, br_netfilter advice, Wi-Fi bridge limitation, libvirt virbr0 and macvtap sentences, and the "address on the enslaved NIC stops working" wording.

Method: documentation only; no commands were run.
