---
id: computing-software.systems-network-administration.incus.instance-devices
name: instance-devices
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, devices, config-device, hotplug, override, profiles, disk]
level: practitioner
status: docs-checked
description: "Add, set and remove Incus instance devices, hotplug rules, 64-character name limit, and how profile and instance devices override each other."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_configure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance devices

```
incus config device add my-container disk-storage-device disk source=/share/c1 path=/opt
incus config device set <instance> <device> <key>=<value>
incus config device remove <instance> <device>
```

- API: PATCH `/1.0/instances/<name>` using the `devices` field.
- Device names are unique per instance, at most 64 characters.
- Containers generally accept device changes while running; VMs hotplug only some device types.
- Override order: profile devices apply in the order profiles are assigned, then instance-level devices last. A later device with the same name replaces the earlier one entirely (no key merging).
- At creation, `--device` can override options of a device that a profile provides.
- `incus config show <name> --expanded` shows the merged result.

## Checked

2026-11-04: confirmed against the Incus configure-instances how-to (device add/set/remove, PATCH with `devices`, 64-character name limit, hotplug behaviour, override order, `--device` at creation, `--expanded`). Nothing removed.

Method: documentation only; no commands were run.
