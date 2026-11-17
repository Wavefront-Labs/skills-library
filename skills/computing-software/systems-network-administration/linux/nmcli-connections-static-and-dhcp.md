---
id: computing-software.systems-network-administration.linux.nmcli-connections-static-and-dhcp
name: nmcli-connections-static-and-dhcp
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, networkmanager, nmcli, nmcli-connection, nmcli-con-mod, static-ip, dhcp-client, dns-servers, ipv4-method, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Configure interfaces with nmcli connection add/modify/up: static IPv4 addressing, gateway and DNS, switching to DHCP, multiple addresses, and applying changes without losing SSH."
sources:
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/nmcli.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/nmcli-examples.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/src/libnmc-setting/settings-docs.h.in
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/NetworkManager.conf.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nmcli connections: static and DHCP

**Goal:** set an interface's addressing persistently with NetworkManager,
and change it remotely without cutting yourself off.

## 1. Look
```bash
nmcli device status                       # devices and which connection (profile) is active
nmcli connection show                     # profiles; a device can have several, one active
nmcli connection show "System eth0" | grep -E 'ipv4\.(method|addresses|gateway|dns)'
nmcli -f IP4 device show eth0             # what's actually applied
```
Connection (profile) ≠ device. Names with spaces need quotes; `nmcli c` and `nmcli d` abbreviations work.

## 2. Static IPv4
```bash
nmcli connection add type ethernet ifname eth0 con-name lan \
  ipv4.method manual ipv4.addresses 192.0.2.10/24 ipv4.gateway 192.0.2.1 \
  ipv4.dns "192.0.2.53 192.0.2.54" ipv4.dns-search example.com \
  ipv6.method auto connection.autoconnect yes
nmcli connection up lan
```
Modify an existing profile:
```bash
nmcli connection modify lan ipv4.addresses 192.0.2.11/24        # replaces the list
nmcli connection modify lan +ipv4.addresses 192.0.2.12/24       # add a secondary address
nmcli connection modify lan -ipv4.dns 192.0.2.54                # remove one value
nmcli connection modify lan ipv4.ignore-auto-dns yes            # with DHCP, use only your DNS
nmcli connection up lan                                         # or: nmcli device reapply eth0
```
`modify` only changes the stored profile; nothing happens until `up`/`reapply`.

## 3. Back to DHCP
```bash
nmcli connection modify lan ipv4.method auto ipv4.addresses "" ipv4.gateway ""
nmcli connection up lan
nmcli -f DHCP4 device show eth0           # lease options received
```
The DHCP client is chosen by the `dhcp` key in the `[main]` section of NetworkManager.conf (allowed values depend on the build; the internal client is built in, others need an external client installed).

## 4. Remote changes without lockout
```bash
nmcli connection modify lan ipv4.addresses 192.0.2.20/24
nmcli device reapply eth0        # update the device with the changes made to the active connection
```
`device reapply` is documented as updating the device with changes made to the currently active connection since it was last applied; `connection up` reactivates the profile. Changing the address you are connected through ends your SSH session either way, so keep console or out-of-band access and a way to restore the old profile.

## Gotchas
- Two profiles autoconnecting on one device → the wrong one may win; delete or set `autoconnect no` on extras.
- Set DNS in the profile (`ipv4.dns`, `ipv4.dns-search`, `ipv4.ignore-auto-dns`) rather than editing resolver files by hand; `ignore-auto-dns` only has an effect when `ipv4.method` is `auto`.
- nmcli only applies where NetworkManager manages the device.

## Verify
- [ ] `ip -4 addr show eth0`, `ip route`, `resolvectl status`/`cat /etc/resolv.conf` show the intended values.
- [ ] After reboot the same configuration is active (`nmcli -f IP4 device show eth0`).

## Checked
Checked 2026-10-25 against the NetworkManager source tree on GitHub (NetworkManager/NetworkManager main, last commit 2026-10-23): nmcli `connection add/modify/up/show`, `device show`, `device reapply`, `general reload`, the `+`/`-` prefixes for multi-value properties such as `ipv4.dns` and `ipv4.addresses`, an empty value resetting a property, `-f IP4`/`DHCP4` field selection, property semantics for `ipv4.addresses` (list, first is primary), `ipv4.gateway`, `ipv4.dns`, `ipv4.dns-search`, `ipv4.ignore-auto-dns`, `ipv4.method`, and NetworkManager.conf `[main] dhcp`. Removed unconfirmed claims: the background-subshell lockout trick, the /32 default for a bare address, resolv.conf handling, Ubuntu netplan note and the RHCSA remark.

Method: documentation only; no commands were run.
