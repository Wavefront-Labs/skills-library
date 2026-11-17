---
id: computing-software.systems-network-administration.linux.network-bonding-and-teaming
name: network-bonding-and-teaming
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bonding, nic-teaming, lacp, 802.3ad, link-aggregation, bond0, active-backup, balance-rr, miimon, netplan, nmcli, high-availability, networking, sysadmin]
level: advanced
status: docs-checked
description: "Configure Linux NIC bonding modes (active-backup, LACP 802.3ad) for failover or throughput, and debug a bond that isn't aggregating."
sources:
  - https://docs.kernel.org/networking/bonding.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network bonding and teaming — one logical NIC from several physical ones

**Goal:** combine two or more physical NICs into one bond for failover or
aggregate throughput, pick the right mode for the switch config actually in
place, and recognize the single most common failure: a bond mode that needs
switch-side cooperation it isn't getting.

## 1. Pick the mode to match the switch — this decision comes first
| Mode | Number | Needs switch config | Behaviour |
|---|---|---|---|
| `active-backup` | 1 | No | One active slave; failover on link loss. Safest default, no switch changes. |
| `balance-xor` | 2 | Static EtherChannel (no LACP) | Hashes flows across slaves (see `xmit_hash_policy`); the kernel docs call modes 0 and 2 EtherChannel-compatible. |
| `broadcast` | 3 | No | Sends everything on every slave. Niche (fault tolerance testing). |
| `802.3ad` (LACP) | 4 | Yes — LACP enabled on switch | Dynamic link aggregation; negotiates with switch via LACPDU. Best throughput + failover when switch supports it. |
| `balance-tlb`/`balance-alb` | 5/6 | No | Adaptive transmit (and receive, for alb) load balancing, no switch config — software-only alternative to LACP. |

**A common failure**: mode 4 (802.3ad) configured on the host with the switch
ports left as plain access ports (no port-channel/LACP). The kernel documents
that 802.3ad needs a switch that supports IEEE 802.3ad and that most switches
need it enabled; without that the bond does not aggregate as intended. If you
don't control the switch or don't know its config, use `active-backup`.

## 2. Create a bond (NetworkManager / nmcli, the common current path)
```bash
nmcli con add type bond ifname bond0 bond.options "mode=802.3ad,lacp_rate=fast,miimon=100"
nmcli con add type ethernet ifname eth0 master bond0
nmcli con add type ethernet ifname eth1 master bond0
nmcli con up bond0
```
Classic `/etc/network/interfaces` (Debian ifupdown) or raw `ip link` +
`/sys/class/net/bond0/bonding/*` sysfs writes (documented in the kernel bonding guide; the bond must be down to change the mode) are alternatives; match whatever the distro's default network manager is
(NetworkManager, netplan/systemd-networkd, or ifupdown) rather than fighting it.

## 3. Verify what the bond is actually doing
```bash
cat /proc/net/bonding/bond0        # mode, MII status, which slave is active, LACP partner info for mode 4
ip link show bond0                 # UP/DOWN, master/slave relationships
ethtool eth0                       # confirm link speed/duplex per physical slave — a 1G slave bonded with a 100M slave bottlenecks silently
```
For 802.3ad specifically, `/proc/net/bonding/bond0` also reports the LACP
aggregator and partner details (exact fields vary by kernel); if they show no
partner, the switch is not aggregating even though the interface is up.

## 4. miimon and failover tuning
```
miimon=100          # ms between link-state polls; 0 disables MII monitoring (documented default 100 when arp_interval is unset)
updelay=200          # ms to wait after link recovery before enabling the slave; default 0, only valid with miimon
downdelay=200        # ms to wait after link failure before disabling the slave; default 0, only valid with miimon
```
`miimon` only detects *link* state (carrier), not "the switch is misbehaving
but the link light is green" scenarios — a bond can show both slaves up
while actual traffic through one is black-holed upstream (bad switch port,
misconfigured VLAN). ARP monitoring (`arp_interval`/`arp_ip_target`, at least
one target, up to 16) checks reachability of the targets instead; it should not
be used together with `miimon`.

## Gotchas
- Bonding and the kernel's own default route selection/ECMP (see
  `computing-software.systems-network-administration.linux.routing-tables-and-policy-routing`)
  solve different problems — bonding aggregates/failovers *link layer*
  interfaces that are meant to look like one NIC to IP; policy routing or
  ECMP spreads *IP-layer* routes across genuinely separate interfaces/subnets.
  Don't reach for bonding when the real need is two separate uplinks to two
  separate ISPs.
- `balance-rr` (mode 0, round-robin per packet) can reorder packets within a
  single TCP flow when the two links have different latency, hurting
  throughput for exactly the traffic you were trying to speed up — rarely
  the right choice outside specific UDP/multicast cases.
- Mismatched slave link speeds/duplex inside one bond is accepted by the
  kernel without complaint but silently caps effective throughput — check
  `ethtool` on every slave, not just that the bond interface shows "up."

## Verify
- [ ] `cat /proc/net/bonding/bond0` shows all intended slaves and the expected active/aggregating state.
- [ ] For LACP (mode 4): the partner/aggregator details in `/proc/net/bonding/bond0` show the switch is aggregating, not just link-up.
- [ ] `ethtool <slave>` shows matching speed/duplex across every slave in the bond.
- [ ] A physical/simulated link pull on the active slave results in failover within the configured `miimon`/`updelay` window, with no application-visible outage beyond that.
- [ ] Bond configuration survives a reboot (it's in the persistent network config, not a one-off `ip`/`nmcli` command).

## Checked

Date: 2026-10-25. Documentation release: Linux kernel Documentation/networking/bonding.rst (torvalds/linux master, read 2026-10-25) and NetworkManager settings reference text (NetworkManager main, read 2026-10-25).
Confirmed: mode numbers and switch requirements (modes 0 and 2 EtherChannel-compatible, 802.3ad needs a switch supporting it, tlb/alb need no special switch support); miimon, updelay and downdelay semantics and defaults; ARP monitoring (arp_ip_target, 16 targets, not with miimon); NetworkManager bond settings take a `bond.options` key/value dictionary, so the mode is passed there.
Removed as unconfirmed: the "Aggregator ID"/LACP "active" wording, the claim that cloud vNICs cannot be bonded, the "#1 support call" ranking. Source URL replaced by the current kernel docs page.

Method: documentation only; no commands were run.
