---
id: computing-software.systems-network-administration.linux.udevadm-info-monitor-and-test
name: udevadm-info-monitor-and-test
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, udev, udevadm, udevadm-monitor, udevadm-info, udevadm-test, udevadm-trigger, device-events, lpic-1, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Debug devices and udev rules with udevadm: info to read properties and the attribute chain, monitor to watch events, test to dry-run rules, trigger/settle to re-apply them."
sources:
  - https://github.com/systemd/systemd/blob/main/man/udevadm.xml
  - https://github.com/systemd/systemd/blob/main/man/udev.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# udevadm: info, monitor, test, trigger

**Goal:** find the exact properties/attributes to match a device, see what events fire when it
appears, and check that a rule does what you meant — before rebooting.

## 1. info
```bash
udevadm info /dev/sdb                        # properties: ID_SERIAL, ID_PATH, ID_FS_UUID, DEVLINKS …
udevadm info -q property -n /dev/sdb         # just KEY=value
udevadm info -a /dev/sdb | less              # attribute walk: device + every parent (KERNELS, SUBSYSTEMS, DRIVERS, ATTRS{})
udevadm info /sys/class/net/eth0
udevadm info --export-db | less              # whole udev database
```
Rule-writing rule: match keys from **one** parent block at a time in `-a` output (you can't mix
`ATTRS{}` from two different parents in one rule).

## 2. monitor
```bash
udevadm monitor --udev --property --subsystem-match=block   # udev events after rule processing, with properties
udevadm monitor --kernel                                    # kernel uevents
udevadm monitor -u -s usb
```
Plug the device and read the event sequence (add/change/remove/bind) — tells you which
ACTION and subsystem to match.

## 3. test
```bash
udevadm test /sys/class/block/sdb 2>&1 | less          # simulate a udev event run and print debug output
udevadm test-builtin path_id /sys/class/block/sdb
udevadm verify /etc/udev/rules.d/*.rules                # syntactic, semantic and stylistic check of rules files
```

## 4. Apply rules without reboot
```bash
udevadm control --reload                                # re-read rules files
udevadm trigger --action=change --subsystem-match=block # replay events for matching devices
udevadm trigger --sysname-match=sdb --action=add
udevadm settle --timeout=30                             # wait for the event queue to empty (scripts)
udevadm control --log-level=debug; journalctl -u systemd-udevd -f   # verbose rule processing
```

## Gotchas
- `ATTR{}` (this device) vs `ATTRS{}` (search parents) — the classic mistake.
- Rules in `/etc/udev/rules.d/` replace same-named files in `/usr/lib/udev/rules.d/` (files in /etc have the highest priority); files are processed in lexical order.
- Some properties only exist after a builtin/IMPORT has run — order your rule after it (higher number).

## Verify
- [ ] `udevadm test` output shows your rule file and the intended SYMLINK/OWNER/RUN.
- [ ] After `trigger`, `ls -l /dev/<symlink>` / permissions reflect the rule.

## Checked

2026-10-26. systemd main (udevadm.xml, udev.xml, commit of 2026-10): udevadm info -q, -n, -a, --export-db; monitor --kernel, --udev, --property, --subsystem-match; test (simulate an event run and print debug output); test-builtin; verify; control --reload and --log-level; trigger --action, --subsystem-match, --sysname-match; settle --timeout; same-name rules replacement and lexical processing. Removed the systemd 254 version gate, the claim about RUN listing in test and the network renaming gotcha, which were not confirmed.

Method: documentation only; no commands were run.
