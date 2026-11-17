---
id: computing-software.systems-network-administration.linux.predictable-network-interface-names
name: predictable-network-interface-names
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, udev, predictable-interface-names, net-naming, systemd-networkd-link, link-file, net-ifnames, interface-rename, altname, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Understand and control NIC names: enoX/ensX/enpXsY schemes, naming-scheme versions, renaming with .link files or altnames, net.ifnames=0, and names that change after updates."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.net-naming-scheme.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.link.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-udevd.service.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predictable network interface names

**Goal:** interface names that don't change across reboots, hardware additions or OS updates,
and names you choose when the defaults are unhelpful.

## 1. The scheme
udev's `net_id` builtin derives names (first that applies):
`eno1` onboard (firmware index) → `ens3` PCIe hotplug slot → `enp3s0f1` PCI bus/slot/function →
`enx001122334455` MAC (not in the default NamePolicy) → kernel name. Prefixes include `en` Ethernet, `wl` WLAN, `ww` WWAN.
```bash
udevadm test-builtin net_id /sys/class/net/eth0    # candidates: ID_NET_NAME_ONBOARD/SLOT/PATH/MAC
ip -d link show | grep -E '^[0-9]|altname'                    # current names and alternative names
```

## 2. Naming-scheme versions
Newer systemd versions can take more device attributes into account, so names can change; distributions can pin an older scheme at build time.
After an upgrade a NIC can be renamed, breaking configs.
Pin explicitly on the kernel command line: `net.naming_scheme=v252` (or `latest`; identifiers are listed in `man systemd.net-naming-scheme`; the option is documented in systemd-udevd.service(8)). Pinning is not enough to fully stabilise names, because they derive from kernel driver attributes. `udevadm info /sys/class/net/<if>` shows the ID_NET_NAME_* properties.

## 3. Choose your own names (.link files)
```ini
# /etc/systemd/network/10-lan0.link
[Match]
MACAddress=52:54:00:12:34:56        # or Path=pci-0000:03:00.0, PermanentMACAddress=
[Link]
Name=lan0
AlternativeNamesPolicy=database onboard slot path
```
Works with NetworkManager too (.link files are applied by udev). Rebuild the initramfs with your distribution's tool if early boot must use the same names, then reboot.
Avoid `ethN` names for custom names — they collide with kernel names. The first matching .link file (alphanumeric order) is applied; later ones are ignored.

## 4. Turn it off (legacy)
Kernel argument `net.ifnames=0` disables predictable naming (kernel names `eth0`, `eth1` in probe order) — unstable with
multiple NICs. Only for single-NIC VMs/images where you want "eth0".

## 5. Alternative names
`ip link property add dev enp3s0f1 altname uplink` — usable anywhere a name is accepted,
doesn't change the primary name; not persistent unless set in a .link file (`AlternativeName=`).

## Gotchas
- Names pinned by MAC break when a clone gets a new MAC — match on `Path=` (a glob on the udev ID_PATH property) or don't pin.
- NetworkManager profiles bind to `interface-name`; rename = update profiles (`nmcli con mod … connection.interface-name lan0`).
- .link files are applied when the device is added (boot or driver reload), not to an interface that is already up.

## Verify
- [ ] `ip link` shows the intended names after reboot; configs (NM, networkd, firewall zones) reference them.
- [ ] `cat /proc/cmdline` shows `net.naming_scheme=` if you pinned one.

## Checked

Date: 2026-10-25. Documentation release: systemd main man sources (systemd.net-naming-scheme, systemd.link, systemd-udevd.service, udevadm) and network/99-default.link, docs/PREDICTABLE_INTERFACE_NAMES.md, read 2026-10-25; ip-link(8) for `ip link property add ... altname`.
Corrected: the kernel option is documented as `net.naming_scheme=` (underscore), not `net.naming-scheme=`.
Confirmed: ID_NET_NAME_ONBOARD/SLOT/PATH/MAC properties and prefixes en/wl/ww; the default NamePolicy (keep kernel database onboard slot path) so MAC-based names are not used by default; `[Match]` MACAddress, PermanentMACAddress and Path (glob on ID_PATH); `[Link]` Name, AlternativeNamesPolicy, AlternativeName; first matching .link file wins; `net.ifnames=0`; `net.naming_scheme` identifiers (v-numbers or latest) and its stability caveat; `udevadm test-builtin`.
Removed as unconfirmed: RHEL scheme identifiers, `prefixdevname`, `biosdevname=0`, dracut/update-initramfs command names, the Red Hat link.

Method: documentation only; no commands were run.
