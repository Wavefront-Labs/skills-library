---
id: computing-software.systems-network-administration.linux.ip-link-and-ip-addr
name: ip-link-and-ip-addr
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, iproute2, ip-link, ip-addr, ip-neigh, mtu, link-state, ip-json, ifconfig-replacement, rhcsa, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Inspect and change interfaces at runtime with ip link and ip addr: state, MTU, MAC, addresses, neighbour table, statistics and JSON output, and why it isn't persistent."
sources:
  - https://man7.org/linux/man-pages/man8/ip-link.8.html
  - https://man7.org/linux/man-pages/man8/ip-address.8.html
  - https://man7.org/linux/man-pages/man8/ip-neighbour.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ip link and ip addr

**Goal:** read interface state at a glance and make temporary changes during troubleshooting.

## 1. Read
```bash
ip -br link                 # brief: name, state, MAC
ip -br addr                 # brief: name, state, addresses
ip -c addr show dev eth0    # colour, full detail (scope, flags, lifetimes)
ip -s -s link show eth0     # RX/TX bytes, packets, errors, dropped, overruns, carrier
ip -d link show eth0        # -d: more details (link type specifics)
ip -j addr                  # -j: JSON output for scripts
ip neigh show dev eth0      # ARP/NDP table; states include reachable, stale, failed (no answer suggests an L2 problem)
```

## 2. Change (runtime only)
```bash
ip link set eth0 up                            # or: down
ip link set eth0 mtu 9000
ip link set eth0 address 02:00:00:aa:bb:cc     # change the station address
ip link set eth0 promisc on
ip addr add 192.0.2.50/24 dev eth0             # secondary address
ip addr add 192.0.2.51/24 dev eth0 label eth0:1
ip addr del 192.0.2.50/24 dev eth0
ip addr flush dev eth0                         # remove all addresses (drops your SSH if it's that one!)
ip -6 addr add 2001:db8::50/64 dev eth0
ip neigh flush dev eth0; ip neigh add 192.0.2.1 lladdr 00:11:22:33:44:55 dev eth0 nud permanent
```

## 3. Persistence
None of the above survives reboot or a NetworkManager/networkd reapply — NM may even revert
it immediately. Persist through the network manager in use:
`nmcli con mod … +ipv4.addresses …`, netplan YAML, or `.network` files. Use `ip` to test, then
codify.

## 4. Troubleshooting patterns
- Errors/drops climbing in `ip -s link` point at the link or driver; compare with `ethtool` counters.
- MTU mismatch symptoms (SSH works, large transfers hang): `ping -M do -s 8972 host` for 9000 MTU.
- Duplicate IP: `arping -D -I eth0 192.0.2.50` before adding an address.
- Address "tentative"/"dadfailed" on IPv6 → duplicate address detection conflict.

## Gotchas
- `ip addr flush` / `ip link set down` on the management interface over SSH = lockout.
- Address `label` (such as `eth0:1`) is only a label; `ip addr` lists multiple addresses per interface.
- In a named network namespace use `ip -n <ns> addr` (equivalent to `ip netns exec <ns> ip addr`).

## Verify
- [ ] `ip -br addr` shows the intended addresses; `ip neigh` shows the gateway REACHABLE after traffic.
- [ ] Persistent config reproduces the same state after `nmcli con up`/reboot.

## Checked

Date: 2026-10-25. Documentation release: iproute2 man pages (iproute2/iproute2 mirror, last commit 2026-10-22) (ip(8), ip-link(8), ip-address(8), ip-neighbour(8)), ping(8) and arping(8) from iputils (iputils/iputils master), read 2026-10-25.
Confirmed: `-br`, `-c`, `-j`, `-d`, `-s` options; neighbour states; `ip link set ... mtu|address|promisc`; address `label`; `ip addr flush`; tentative and dadfailed flags; `ip -n NETNS`; `ping -M do -s`; `arping -D` duplicate address detection.
Removed as unconfirmed: the jq pipeline, NO-CARRIER/LOWER_UP interpretation, the interface-must-be-down claim, ethtool ring-buffer advice, nsenter, and the ifconfig deprecation remark.

Method: documentation only; no commands were run.
