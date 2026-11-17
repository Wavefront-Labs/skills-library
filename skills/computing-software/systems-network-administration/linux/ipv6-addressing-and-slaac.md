---
id: computing-software.systems-network-administration.linux.ipv6-addressing-and-slaac
name: ipv6-addressing-and-slaac
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ipv6, ipv6-configuration, slaac, router-advertisement, accept-ra, dhcpv6, privacy-extensions, link-local, ndp, ip-6, nmcli, networking, sysadmin]
level: practitioner
status: docs-checked
description: "Configure IPv6 on Linux hosts: link-local, SLAAC vs DHCPv6 vs static, router advertisements and accept_ra, privacy addresses, and verifying addresses, routes and neighbours."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4862
  - https://github.com/NetworkManager/NetworkManager/blob/main/src/libnm-core-public/nm-setting-ip6-config.h
  - https://docs.kernel.org/networking/ip-sysctl.html
  - https://networkmanager.dev/docs/api/latest/settings-ipv6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 addressing and SLAAC

**Goal:** hosts get correct global IPv6 addresses and a default route from the router
(SLAAC/DHCPv6) or static config, and you can prove where each address came from.

## 1. How a host gets IPv6
- **Link-local** `fe80::/64` always, on every up interface; needed for NDP and as the next hop of the default route.
- **SLAAC**: router sends RA with a /64 prefix and `A` flag → host builds its own address.
- **DHCPv6**: RA `M` flag (managed) → addresses from DHCPv6; `O` flag → only options (DNS) from DHCPv6.
- The default route is learned from Router Advertisements (`accept_ra_defrtr`, route metric `ra_defrtr_metric`); with RAs not accepted there is no learned default route unless configured statically.

## 2. Inspect
```bash
ip -6 addr show dev enp1s0       # address flags such as dynamic, mngtmpaddr, temporary
ip -6 route                       # learned default route shows its protocol (ra)
ip -6 neigh                       # NDP cache (IPv6 ARP)
sysctl net.ipv6.conf.enp1s0.accept_ra net.ipv6.conf.enp1s0.forwarding
```

## 3. Configure
NetworkManager:
```bash
nmcli con mod lan0 ipv6.method auto                       # RAs, DHCP or other automatic means
nmcli con mod lan0 ipv6.method manual ipv6.addresses 2001:db8:10::20/64 ipv6.gateway fe80::1
nmcli con mod lan0 ipv6.addr-gen-mode stable-privacy      # stable-privacy, or eui64 (derived from the hardware address)
nmcli con mod lan0 ipv6.ip6-privacy 2                     # RFC 4941 privacy extensions, prefer temporary addresses (0 off, 1 prefer public)
nmcli con mod lan0 ipv6.method disabled                   # IPv6 disabled for this connection
nmcli con up lan0
```
Raw sysctl (no NM):
```bash
sysctl -w net.ipv6.conf.enp1s0.accept_ra=2   # accept RAs even if forwarding is enabled (0 = never, 1 = only if forwarding is off)
sysctl -w net.ipv6.conf.enp1s0.use_tempaddr=2   # >1: privacy extensions, prefer temporary addresses
```

## Gotchas
- With forwarding enabled the functional default of `accept_ra` is off, so the kernel ignores RAs unless `accept_ra=2` — hosts can lose their IPv6 default route after enabling forwarding.
- Servers: prefer static addresses or DHCPv6 reservations; temporary privacy addresses change over time (default `temp_valid_lft` 2 days, `temp_prefered_lft` shorter), which breaks source-address ACLs. Set `ipv6.ip6-privacy 0` on servers.
- Disabling IPv6 for the whole system (`ipv6.disable=1`) stops all IPv6 sockets; disable per interface or per connection when only some interfaces should lose IPv6 (see the disable-ipv6 skill).
- Firewalls must allow ICMPv6 neighbour and router discovery and packet-too-big messages or IPv6 breaks in odd ways.

## Verify
- [ ] `ip -6 addr` shows a `scope global` address with the expected origin; `ip -6 route` has `default ... proto ra` (or your static gateway).
- [ ] `ping -6` to a known reachable IPv6 host succeeds.

## Checked

Date: 2026-10-25. Documentation release: Linux kernel Documentation/networking (torvalds/linux master)/ip-sysctl.rst (accept_ra, accept_ra_defrtr, ra_defrtr_metric, use_tempaddr, temp lifetimes, forwarding), NetworkManager settings reference text and libnm headers (NetworkManager main); nm-setting-ip6-config.h (methods auto, manual, disabled, ignore, dhcp, link-local, shared), read 2026-10-25.
Confirmed: `accept_ra` values 0/1/2 and the functional default depending on forwarding; `use_tempaddr` meanings; NetworkManager `ipv6.method`, `ipv6.addr-gen-mode` (eui64, stable-privacy, default), `ipv6.ip6-privacy` values -1/0/1/2; `ip -6` address flags (mngtmpaddr, temporary, tentative, dadfailed).
Removed as unconfirmed: the claim that DHCPv6 never supplies a default route, the stable-privacy "default" label, `rdisc6`, the global-disable side effects on `::1`, ICMPv6 type numbers, and the public-host connectivity checks.

Method: documentation only; no commands were run.
