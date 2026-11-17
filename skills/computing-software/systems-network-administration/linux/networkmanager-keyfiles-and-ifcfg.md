---
id: computing-software.systems-network-administration.linux.networkmanager-keyfiles-and-ifcfg
name: networkmanager-keyfiles-and-ifcfg
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, networkmanager, nm-keyfile, nmconnection, ifcfg, ifcfg-rh, network-scripts, nmcli-migrate, profile-storage, rhel, networking, sysadmin]
level: practitioner
status: docs-checked
description: "Read, write and migrate NetworkManager profile files: .nmconnection keyfiles, legacy ifcfg-rh files, permissions, reload, and nmcli connection migrate on RHEL 9/10."
sources:
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/nm-settings-keyfile.xsl
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/NetworkManager.conf.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/man/nmcli.xml
  - https://github.com/NetworkManager/NetworkManager/blob/main/src/libnm-core-impl/nm-keyfile.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetworkManager keyfiles and ifcfg files

**Goal:** know where a profile is stored, edit or template it as a file safely, and move
legacy `ifcfg-*` profiles to keyfiles.

## 1. Which plugin owns a profile
```bash
nmcli -f NAME,UUID,FILENAME con show
NetworkManager --print-config | grep -A2 '\[main\]'    # shows the plugins key
```
- Keyfile (the generic plugin, always enabled): `.nmconnection` files in `/etc/NetworkManager/system-connections/`, `/usr/lib/NetworkManager/system-connections/` and `/run/NetworkManager/system-connections/` (the last holds runtime-only profiles).
- In current upstream NetworkManager the `ifcfg-rh`, `ifcfg-suse` and `ifnet` plugins are deprecated and selecting them has no effect; `ifupdown` (Debian and Ubuntu) reads `/etc/network/interfaces` read-only. Which plugins your distribution still ships is distribution-specific; check its documentation.

## 2. Keyfile format
```ini
[connection]
id=lan0
uuid=4f1c2b7e-0000-4000-8000-000000000001
type=ethernet
interface-name=enp1s0
autoconnect=true

[ipv4]
method=manual
address1=10.0.10.20/24,10.0.10.1
dns=10.0.0.53;10.0.0.54;
dns-search=corp.example;

[ipv6]
method=auto
```
Rules: the plugin ignores files that are readable or writable by anyone other than root (use mode 0600, owner root); lists are separated by `;` (the reader also accepts `,`); addresses, routes and routing rules use one numbered key per entry (`address1`, `address2`, ...) in the form `address/prefix,gateway`. Every profile needs its own UUID (for example from `uuidgen`).

## 3. ifcfg (legacy)
Old `ifcfg-*` files are the format of the deprecated ifcfg-rh plugin; migrate them to keyfiles (section 5) rather than writing new ones.

## 4. After hand edits
```bash
nmcli con reload                 # re-read all files (or: nmcli con load <file>)
nmcli con up lan0                # apply to the device
```
Editing a file does nothing until NetworkManager is told (`nmcli con reload`, or `nmcli con load <file>`) and the profile is activated; `nmcli con mod` writes the file for you.

## 5. Migrate ifcfg → keyfile
```bash
nmcli connection migrate                 # all profiles to keyfile
nmcli connection migrate lan0            # one profile (by name, UUID or D-Bus path)
nmcli -f NAME,FILENAME con show          # confirm the new file locations
```
`keyfile` is the only supported migration target (and the default `--plugin`). Check your distribution's upgrade notes for any ifcfg-related upgrade blockers.

## Gotchas
- Every profile needs a unique `uuid`; do not copy a keyfile to a second profile on the same host without changing it.
- Secrets (Wi-Fi PSK, 802.1X passwords) are stored in plain text in the keyfile unless the property's secret flags say otherwise (the NM sample with an always-ask secret uses `password-flags=2`); see "Secret flag types" in nm-settings-nmcli.

## Verify
- [ ] `nmcli -f NAME,FILENAME con show` points every profile at a `.nmconnection` path.
- [ ] Each keyfile is owned by root and not accessible to others (mode 600); `nmcli con up` succeeds after a `reload`.

## Checked
Checked 2026-10-25 against the NetworkManager source tree on GitHub (NetworkManager/NetworkManager main, last commit 2026-10-23): keyfile directories, root-only permission rule, ini-style format with `;` lists and numbered `address1`-style keys, `address/plen,gateway` grammar (nm-keyfile.c), `type=ethernet` style aliases, `nmcli connection reload/load/migrate` (migrate target keyfile only), NetworkManager.conf plugin notes (ifcfg-rh, ifcfg-suse and ifnet deprecated with no effect; ifupdown read-only). Fixed: the skill presented ifcfg-rh as a live plugin on RHEL 9; upstream documents it as deprecated with no effect. Removed unconfirmed claims: RHEL 9/10 plugin availability, the Leapp blocker, the ifcfg example, duplicate-id behaviour and `psk-flags=1` meaning. The nm-settings-ifcfg-rh page is no longer part of the docs source tree.

Method: documentation only; no commands were run.
