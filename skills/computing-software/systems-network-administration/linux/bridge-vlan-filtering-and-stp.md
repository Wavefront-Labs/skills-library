---
id: computing-software.systems-network-administration.linux.bridge-vlan-filtering-and-stp
name: bridge-vlan-filtering-and-stp
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bridge, bridge-vlan-filtering, bridge-stp, vlan-aware-bridge, pvid, untagged, rstp, mstpd, bridge-vlan, kvm-networking, networking, sysadmin]
level: advanced
status: docs-checked
description: "Run one VLAN-aware Linux bridge instead of a bridge per VLAN: vlan_filtering, per-port PVID and tagged VLANs, guest access ports, and STP settings that avoid loops and slow links."
sources:
  - https://man7.org/linux/man-pages/man8/bridge.8.html
  - https://docs.kernel.org/networking/bridge.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bridge VLAN filtering and STP

**Goal:** one `br0` that behaves like a managed switch — trunk uplink, guests on access
VLANs or trunks — and spanning tree configured so it neither loops nor stalls.

## 1. VLAN-aware bridge
```bash
ip link add br0 type bridge vlan_filtering 1 vlan_default_pvid 0
ip link set enp1s0 master br0                       # uplink trunk
bridge vlan add dev enp1s0 vid 10                   # tagged
bridge vlan add dev enp1s0 vid 20
ip link set vnet0 master br0                        # a VM tap
bridge vlan add dev vnet0 vid 20 pvid untagged      # access port on VLAN 20
# host IP on VLAN 10 via the bridge itself:
bridge vlan add dev br0 vid 10 self
ip link add link br0 name br0.10 type vlan id 10
ip addr add 10.0.10.20/24 dev br0.10
bridge vlan show                                    # per-port VIDs, PVID, Egress Untagged
```
`vlan_default_pvid` sets the default PVID (native/untagged VLAN ID) of the bridge; run `bridge vlan show` after changing it to see which VLAN each port carries untagged.

## 2. Persistent
NetworkManager: `nmcli con add type bridge ifname br0 bridge.vlan-filtering yes bridge.vlan-default-pvid 0`,
ports with `bridge-port.vlans "10, 20"` (tagged) or `"20 pvid untagged"`.
systemd-networkd: `[Bridge] VLANFiltering=yes` in the `.netdev`; per port `.network`:
```ini
[BridgeVLAN]
VLAN=10
[BridgeVLAN]
VLAN=20
```
and `PVID=20` + `EgressUntagged=20` for access ports.

## 3. STP
```bash
ip link set br0 type bridge stp_state 1 priority 32768
bridge -d link show                # per-port STP state
ip -d link show br0                # bridge options as set (forward_delay, hello_time, max_age, priority)
```
- Ports pass through blocking, listening, learning and forwarding states; `forward_delay` is the time spent in listening and in learning, and only matters when STP is enabled (man page range 2 to 30, `hello_time` 1 to 10, `max_age` 6 to 40; check units with `ip -d link show`).
- Single-uplink host bridge with no other bridge attached: STP can be left off (`stp_state 0`) so ports forward without the listening and learning delay.
- Host with two uplinks into the same L2 domain: STP on, or bond the uplinks instead.
- `stp_mode` chooses who runs STP: `auto` (default) hands the bridge to the `/sbin/bridge-stp` helper for a userspace STP daemon (initial network namespace only), `user` enables userspace STP directly, `kernel` uses the kernel STP. It can only be changed while STP is disabled and may be set in the same command as `stp_state`. `mst_enabled` turns on multiple spanning tree support.
- The bridge with the lowest priority value and bridge ID becomes root (kernel docs example default 32768): give the host bridge a numerically high `priority` so it does not win the election.

## Gotchas
- Enabling `vlan_filtering` on a live bridge changes which frames each port accepts: add the VIDs first or work from the console.
- Switch side must trunk the same VLANs; mismatched native VLAN = traffic in the wrong VLAN.

## Verify
- [ ] `bridge vlan show` matches the design; a guest on an access port gets an address from that VLAN's DHCP.
- [ ] `tcpdump -eni enp1s0 vlan` (link-level headers, numeric, `vlan` filter) shows guest frames tagged with the right VID; `bridge -d link` shows ports `forwarding`.

## Checked

Date: 2026-10-25. Documentation release: iproute2 man pages ip-link(8), bridge(8) (iproute2/iproute2 mirror, last commit 2026-10-22); kernel Documentation/networking/bridge.rst (torvalds/linux master); NetworkManager settings reference text (NetworkManager main); systemd.network(5)/systemd.netdev(5) man sources (systemd/systemd main); tcpdump(1) and pcap-filter(7), read 2026-10-25.
Confirmed: `vlan_filtering`, `vlan_default_pvid`, `stp_state` (any value above 0 enables STP), `stp_mode` auto/user/kernel and its constraints, `mst_enabled`, `priority` (16-bit, lower wins root election), `forward_delay`/`hello_time`/`max_age` meanings and ranges; `bridge vlan add dev X vid N [pvid] [untagged] [self]`, `bridge link`; STP port states; NetworkManager `bridge.vlan-filtering`, `bridge.vlan-default-pvid`, `bridge-port.vlans` syntax; systemd `VLANFiltering=`, `[BridgeVLAN]` `VLAN=`, `PVID=`, `EgressUntagged=`.
Removed as unconfirmed: the stp_state 2 / mstpd statements, 30-50 s convergence figure, the numeric forward_delay and hello_time example values (the man page gives seconds while the kernel interface units differ, so verify on your host), the sysfs root_id read (kernel docs call sysfs deprecated), the switchdev and libvirt sentences, and the priority 61440 figure.

Method: documentation only; no commands were run.
