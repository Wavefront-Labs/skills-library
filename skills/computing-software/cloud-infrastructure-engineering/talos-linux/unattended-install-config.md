---
id: computing-software.cloud-infrastructure-engineering.talos-linux.unattended-install-config
name: unattended-install-config
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [unattendedinstallconfig, install, cel, disk-selector, image-factory, pxe, iso]
level: advanced
status: docs-checked
description: "Install Talos to disk from a multi-document machine config with UnattendedInstallConfig: CEL disk selector, installer image, wipe and reboot behaviour, status."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/lifecycle-management/unattended-install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`UnattendedInstallConfig` lets a node booted from ISO, PXE or iPXE install itself to a selected disk with no manual installer run. It replaces the deprecated `.machine.install` field.

```yaml
apiVersion: v1alpha1
kind: UnattendedInstallConfig
installer:
  image: factory.talos.dev/metal-installer/<schematic-id>:<talos-version>
provisioning:
  diskSelector:
    match: disk.dev_path == "/dev/sda"
  wipe: true
```

`diskSelector.match` is a CEL expression evaluated against discovered disks as `disk`. If several disks match, Talos logs a warning and uses the first. For production prefer `disk.serial`, `disk.wwid` or `disk.symlinks` over `/dev/sd*` names. Inspect disks first with `talosctl --nodes <NODE> get disks -o yaml`, then apply with `talosctl --nodes <NODE> patch mc --patch unattended-install.patch.yaml`.

Set `installer.image` to the Image Factory installer for the same schematic as the boot asset when extensions matter. If omitted, Talos derives it from the Image Factory boot entry, which works only when booted from an Image Factory asset.

Wiping defaults to on; `provisioning.wipe: false` keeps partition data the installer can reuse. `reboot` unset means reboot only if `installer.image` was set explicitly; `true` always reboots; `false` stays on the boot media.

Monitor with `talosctl --nodes <NODE> get unattendedinstallstatuses`. Phases: `pending` (no disk matches), `installing`, `installed`, `waiting-for-reboot`, `failed` (read the `error` field via `-o yaml`).

## Checked

Whole page read; fields, selector rules, reboot rules and phases confirmed.

Method: docs-checked 2026-11-09 against Talos v1.15 docs unattended-install.mdx (read in full).
