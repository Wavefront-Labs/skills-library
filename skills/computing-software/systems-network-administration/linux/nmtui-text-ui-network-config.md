---
id: computing-software.systems-network-administration.linux.nmtui-text-ui-network-config
name: nmtui-text-ui-network-config
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nmtui, networkmanager, console, static-ip, hostname, network-profile, rhcsa, networking, sysadmin]
level: intro
status: docs-checked
description: "Use nmtui to edit NetworkManager profiles, activate connections and set the hostname from a console, and know what it writes so changes can be checked and scripted later."
sources:
  - https://networkmanager.dev/docs/api/latest/nmtui.html
  - https://networkmanager.dev/docs/api/latest/nmcli.html
  - https://networkmanager.dev/docs/api/latest/NetworkManager.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nmtui — NetworkManager from a text console

**Goal:** fix or set networking quickly from a server console (IPMI/VM console, no SSH yet)
without memorising nmcli property names, then confirm it stuck.

## 1. Entry points
```bash
nmtui              # menu
nmtui edit         # straight to the profile list; nmtui edit "System eth0" opens one profile
nmtui connect      # list connections; activate or deactivate them
nmtui hostname     # set the system hostname
```
The binaries `nmtui-edit`, `nmtui-connect` and `nmtui-hostname` skip the activity menu.

## 2. Setting a static address
1. Edit → select the profile (or Add → Ethernet, set Device to the interface name).
2. IPv4 CONFIGURATION: change Automatic → **Manual**, then `<Show>`.
3. Addresses: `10.0.10.20/24` — include the prefix length.
4. Gateway, DNS servers, Search domains; tick "Automatically connect".
5. OK → back to the main menu → Activate a connection → activate the profile (deactivate and
   reactivate it if it is already active).

## 3. What it writes
nmtui edits profiles through NetworkManager. NetworkManager stores keyfile profiles under
`/etc/NetworkManager/system-connections` unless the `path` option in the `[keyfile]` section of NetworkManager.conf says otherwise.
Check the result scriptably:
```bash
nmcli -f ipv4.method,ipv4.addresses,ipv4.gateway,ipv4.dns con show "System eth0"
nmcli device status
```

## Gotchas
- Profile name ≠ device name; editing an inactive duplicate profile changes nothing on the
  live interface. `nmcli con show --active` shows which one is in use.
- Over SSH, deactivating the profile you are connected through drops the session before you
  can reactivate it — do that step from the console.

## Verify
- [ ] `ip -br addr` and `ip route` match what was entered; `ping -c3 <gateway>` succeeds.
- [ ] `nmcli -g connection.autoconnect con show <profile>` is `yes`; a reboot keeps the address.

## Checked

Documentation check. Checked 2026-10-27 against the NetworkManager nmtui, nmcli and NetworkManager.conf manual sources (networkmanager.dev, main branch, 2026-10-27): the three activities `edit`, `connect` and `hostname` and the `nmtui-*` binaries, that `nmtui edit` takes a connection name or id, `nmcli -f`, `-g`, `con show --active`, `con mod ... connection.autoconnect`, `device status` and `con up`, and the keyfile `path` default. Removed the hostnamed, key bindings, package names, /32 behaviour, RHEL 8 ifcfg, atomic-swap and unsettable-property claims, which the pages do not state.
Method: documentation only; no commands were run.
