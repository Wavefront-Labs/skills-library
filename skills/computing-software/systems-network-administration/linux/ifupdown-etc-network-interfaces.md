---
id: computing-software.systems-network-administration.linux.ifupdown-etc-network-interfaces
name: ifupdown-etc-network-interfaces
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ifupdown, etc-network-interfaces, ifup, ifdown, ifupdown2, debian-networking]
level: practitioner
status: docs-checked
description: "Configure Debian-style networking with ifupdown and /etc/network/interfaces: static, DHCP, VLANs, bridges, hooks, ifupdown2 reloads, and coexisting with NetworkManager."
sources:
  - https://manpages.debian.org/bookworm/ifupdown/interfaces.5.en.html
  - https://manpages.debian.org/bookworm/ifupdown/ifup.8.en.html
  - https://manpages.debian.org/bookworm/ifupdown2/ifreload.8.en.html
  - https://networkmanager.dev/docs/api/latest/NetworkManager.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ifupdown and /etc/network/interfaces

**Goal:** predictable networking on Debian servers, Proxmox and minimal images that don't run NetworkManager or netplan.

## File layout
```
# /etc/network/interfaces
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto ens18
iface ens18 inet static
    address 192.0.2.10/24
    gateway 192.0.2.1
    dns-nameservers 192.0.2.53
    mtu 9000

allow-hotplug ens19
iface ens19 inet dhcp

iface ens18 inet6 static
    address 2001:db8::10/64
    gateway 2001:db8::1
```
- Comments must be on a line of their own; end-of-line comments are not supported in this file.
- Options such as `dns-nameservers`, `bridge-ports` and VLAN settings are extensions provided by helper packages (for example `resolvconf`/`openresolv`, `bridge-utils`, `vlan`); install the package that provides the option.
- `auto` brings the interface up when `ifup -a` runs (at boot); `allow-hotplug` brings it up when udev detects the device.
- Hooks: `pre-up`, `up`, `post-up`, `pre-down`, `down`, `post-down` run shell commands, e.g. `up ip route add 10.0.0.0/8 via 192.0.2.254`.

## VLAN and bridge
```
auto ens18.20
iface ens18.20 inet manual

auto vmbr0
iface vmbr0 inet static
    address 192.0.2.10/24
    gateway 192.0.2.1
    bridge-ports ens18
```

## Apply changes safely
```bash
ifquery --list; ifquery ens18          # parse and show config
ifup --no-act ens18                    # show what would run, change nothing
ifdown ens18 && ifup ens18             # classic ifupdown: drops the link, so run it from a console
ifreload -a                            # ifupdown2 only: reload all "auto" interfaces (-c: all that are currently up)
ifquery --state                        # which interfaces ifupdown believes are up
```
ifup and ifdown record which interfaces they brought up (see `ifquery --state` and `--state-dir`). Check that state before editing the file for an interface that is up, and take the interface down first if the change affects its addresses.

## Coexistence
- NetworkManager's ifupdown plugin manages interfaces listed in this file only when `[ifupdown] managed=true` is set in NetworkManager.conf. Do not define the same NIC in two tools.

## Verify
- [ ] After a reboot `ip -br addr` shows the expected addresses.
- [ ] `ifquery -a` parses without errors.

## Checked

Documentation check. Checked 2026-10-27 against Debian bookworm interfaces(5), ifup(8) and ifreload(8) (ifupdown2 3.0.0), and the NetworkManager.conf page (networkmanager.dev): that end-of-line comments are not supported (the old sample had inline comments, now removed), `auto` and `allow-hotplug` semantics, `source`, `address` with a prefix length, `gateway`, `mtu`, the `pre-up`/`up`/`post-up`/`pre-down`/`down`/`post-down` hooks, that `bridge-utils`, `resolvconf`, `openresolv` and `vlan` are extension packages, `ifquery --list` and `--state`, `--no-act`, `ifreload -a` and `-c`, and the `[ifupdown] managed` NetworkManager option. Removed the `bridge-stp` and `bridge-fd` lines, the `at` rollback line, the networking.service, netplan and NIC-renaming remarks, and the claim that ifdown uses the new stanza.
Method: documentation only; no commands were run.
