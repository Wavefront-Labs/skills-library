---
id: computing-software.systems-network-administration.linux.systemd-networkd-network-files
name: systemd-networkd-network-files
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd-networkd, networkd, network-file, networkd-network-file, netdev, link-file, networkctl, static-ip, dhcp, systemd-resolved, networking, sysadmin]
level: practitioner
status: docs-checked
description: "Configure interfaces with systemd-networkd .network, .netdev and .link files: match rules, static and DHCP addressing, routes, DNS hand-off to resolved, and networkctl checks."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.network.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.netdev.html
  - https://www.freedesktop.org/software/systemd/man/latest/networkctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd-networkd .network files

**Goal:** a minimal, dependency-free network stack for servers, containers and images,
configured by small INI files you can ship with config management.

## 1. File types and precedence
- `.network` — addresses, routes, DHCP for links that match `[Match]`.
- `.netdev` — create virtual devices (bond, bridge, vlan, wireguard, macvlan).
- `.link` — udev-time properties (name, MAC, MTU, offloads); applied by udev, not networkd.
- Files are read from `/usr/lib/systemd/network`, `/usr/local/lib/systemd/network`, `/run/systemd/network` and `/etc/systemd/network`, sorted together in alphanumeric order whatever the directory; files with identical names replace each other. The **first** `.network` file that matches a link is applied and later files are ignored, so prefix names with a number below 70 (`10-lan.network`) and keep catch-alls (`99-dhcp.network`) last.

## 2. Static and DHCP
```ini
# /etc/systemd/network/10-lan.network
[Match]
Name=enp1s0            # or MACAddress=52:54:00:12:34:56, Type=ether, Driver=virtio_net

[Network]
Address=10.0.10.20/24
Gateway=10.0.10.1
DNS=10.0.0.53
DNS=10.0.0.54
Domains=corp.example
IPv6AcceptRA=yes
LinkLocalAddressing=ipv6

[Route]
Destination=192.168.50.0/24
Gateway=10.0.10.254
Metric=50
```
```ini
# /etc/systemd/network/99-dhcp.network
[Match]
Type=ether
[Network]
DHCP=yes
[DHCPv4]
UseDNS=no              # keep your own resolvers
RouteMetric=200
```

## 3. Enable and inspect
```bash
systemctl enable --now systemd-networkd systemd-resolved
ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
networkctl list                           # SETUP column: configured / unmanaged / failed
networkctl status enp1s0                  # state, addresses, DNS
networkctl reload                         # re-read .netdev and .network files (v244+); reconfigure <link> applies them to one link
```

## Gotchas
- A link showing `unmanaged` matched no `.network` file — check `Name=` globs and the file suffix.
- `systemd-networkd-wait-online.service` blocks boot for 2 minutes if any managed link never
  comes up; mark optional links with `RequiredForOnline=no` in `[Link]`.
- `.link` files are applied by systemd-udevd (see `systemd.link`), not by systemd-networkd.
- Multiple `[Address]`/`[Route]` sections are allowed; repeating `Address=` in `[Network]` is equivalent.

## Verify
- [ ] `networkctl status <link>` shows the expected addresses and state `routable`.
- [ ] `ip route` has the default and static routes; `resolvectl dns` shows per-link servers.
- [ ] After reboot, `systemd-networkd-wait-online` finished without timing out (`systemd-analyze blame`).

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: file search directories, alphanumeric ordering, identical-name replacement and first-match rule (`systemd.network`); `networkctl reload` first appeared in v244 (NEWS); `RequiredForOnline=`, `LinkLocalAddressing=`, `IPv6AcceptRA=`, `DHCP=`, `[DHCPv4] UseDNS=`/`RouteMetric=` and `Domains=` exist as used; `systemd-networkd-wait-online` default timeout 120 s; `stub-resolv.conf` path (`systemd-resolved`); `unmanaged`/`configured` SETUP states (`networkctl`).

Method: documentation only; no commands were run.
