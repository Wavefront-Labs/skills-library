---
id: computing-software.systems-network-administration.linux.routing-tables-and-policy-routing
name: routing-tables-and-policy-routing
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, routing, iproute2, ip-route, ip-rule, policy-routing, multi-homed, multipath, route-metrics, source-routing, rt-tables, fwmark, sysadmin, networking, default-gateway]
level: advanced
status: docs-checked
description: "Read and shape Linux routing: the main table, multiple routing tables, ip rule policy routing, and route metrics on multi-homed hosts."
sources:
  - https://man7.org/linux/man-pages/man8/ip-route.8.html
  - https://man7.org/linux/man-pages/man8/ip-rule.8.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Routing tables and policy routing — more than one path out of the box

**Goal:** understand why a packet with two possible exits goes out one
interface and not the other, and build routing that chooses by *source*
address, mark, or policy — not just destination.

## 1. The ordinary case: one routing table
```bash
ip route show                       # main table (table 254) — what most hosts have
ip route get 8.8.8.8                # which route/interface/src a destination actually uses
ip -s link show                     # per-interface packet counters, sanity-check which NIC is busy
```
Default route selection is destination-based: the kernel walks the table for
the most specific match (longest prefix) to the *destination* address. A
single-homed host never needs more than this.

## 2. Multiple routing tables
```bash
cat /etc/iproute2/rt_tables         # name-to-ID map; table IDs 0, 253, 254, 255 are reserved (default, main, local)
echo "100 isp2" >> /etc/iproute2/rt_tables   # the etc copy takes precedence over the vendor copy if it exists
ip route add default via 203.0.113.1 table isp2
ip route show table isp2
```
A second table is inert until something tells the kernel when to consult it
— that's `ip rule`'s job. Creating routes in table 100 with no matching rule
pointing packets at it does nothing; this is the most common "policy
routing isn't working" mistake.

## 3. `ip rule` — policy routing by source, not just destination
```bash
ip rule show                        # default: 0 (local), 32766 (main), 32767 (default) — priority order, lowest first
ip rule add from 203.0.113.5 table isp2 priority 100
```
Classic use case: a host with two WAN uplinks. Traffic *sourced from* ISP2's
assigned address must egress via ISP2's gateway, or the return path hairpins
through the wrong link and the remote end's reply never routes back (asymmetric
routing dropped by the ISP or a stateful firewall upstream). The fix is
exactly the rule above: match on `from`, not `to`.

`fwmark`-based rules combine with `nftables`/`iptables` marking for policy
routing driven by richer match criteria than source address alone:
```bash
nft add rule inet filter mangle meta mark set 0x1 ...     # or: iptables -t mangle -j MARK --set-mark 1
ip rule add fwmark 1 table isp2
```

## 4. Route metrics and multipath
```bash
ip route add default via 10.0.0.1 dev eth0 metric 100
ip route add default via 10.0.1.1 dev eth1 metric 200    # backup; only used if eth0's route disappears
ip route add default scope global nexthop via 10.0.0.1 dev eth0 weight 1 \
                                   nexthop via 10.0.1.1 dev eth1 weight 1   # ECMP load-share
```
Lower `metric` wins when multiple routes to the same destination exist —
this is how a routing daemon (or DHCP client) can implement primary/backup
uplinks without policy routing. A multipath route (`nexthop ... weight`) is a different thing from failover; test what happens when one nexthop dies rather than assuming the route is withdrawn.

## 5. Diagnosing "why did this packet go there"
```bash
ip route get <dst> from <src>        # exact lookup the kernel would do, table and all
ip rule show                          # rules are scanned in priority order, lowest number first
traceroute -n <dst>                   # confirm what the box ACTUALLY does, not just what tables say
```
Order of operations: the rule database is scanned in priority order (lowest number first); a matching rule's action selects a table and, if that lookup yields a route, the search ends, otherwise it continues
with the next rule (ip-rule(8)). A rule with the wrong priority can shadow the policy
route you just added by matching the `main` table (default priority 32766) first.

## Gotchas
- Policy routing survives a reboot only if it's in config files the distro
  actually loads (`/etc/iproute2/rt_tables` plus a script or
  NetworkManager/netplan dispatcher hook) — commands typed at a shell vanish
  on reboot like any other `ip` command.
- `ip route` changes are immediate and have no undo/rollback primitive;
  misconfigure the default route on a remote box over SSH and the session
  (and everything else) may become unreachable. Test additive rules first,
  keep an out-of-band console path before touching default routes remotely.
- Reverse path filtering (`net.ipv4.conf.*.rp_filter`: 0 off, 1 strict, 2 loose per the kernel docs) can discard
  asymmetric-routed packets even when the routing table itself is correct — a multi-homed/policy-routing
  setup may need loose mode (2) on the relevant interfaces, not just the routes themselves. See
  `computing-software.systems-network-administration.linux.kernel-tuning-with-sysctl`.
- Container and VPN interfaces add their own routes and can win a longest-prefix match you didn't expect — run `ip route show` after bringing one up, not just before.

## Verify
- [ ] `ip route get <dst> from <src>` returns the interface and nexthop you intend for that source/destination pair.
- [ ] `ip rule show` lists policy rules in the priority order intended, with no unexpected rule shadowing them.
- [ ] Policy routing and custom tables survive a reboot (config file, not just shell history).
- [ ] For multi-homed hosts, `rp_filter` is set deliberately (loose or off) on interfaces that legitimately see asymmetric return traffic.
- [ ] A live failover/ECMP path is tested by actually killing one link, not just inspecting the route table.

## Checked

Date: 2026-10-25. Documentation release: iproute2 man pages (iproute2/iproute2 mirror, last commit 2026-10-22) (ip-route(8), ip-rule(8)), Linux kernel Documentation/networking (torvalds/linux master)/ip-sysctl.rst, read 2026-10-25.
Confirmed: default rules at priorities 0 (local, table 255), 32766 (main, 254) and 32767 (default, 253); rule scanning order and fall-through to the next rule when a lookup fails; `ip rule add from ... table ... priority`, `fwmark` selector; `nexthop via ... dev ... weight` syntax; `metric`; table names from rt_tables with the etc copy taking precedence and reserved IDs 0, 253, 254, 255; `ip route get ... from ... iif`; rp_filter values 0/1/2.
Removed as unconfirmed: the route-cache flush comment, the claim that the kernel never withdraws dead nexthops, the "strict by default on many distros" statement, and the "first matching rule wins" wording (rules fall through when the lookup fails).

Method: documentation only; no commands were run.
