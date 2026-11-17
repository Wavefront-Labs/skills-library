---
id: computing-software.systems-network-administration.incus.cloud-init-user-data
name: cloud-init-user-data
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, cloud-init, user-data, vendor-data, cloud-images, nocloud, vm-agent]
level: practitioner
status: docs-checked
description: "Use cloud-init in Incus: cloud image variants, cloud-init.user-data/vendor-data (and legacy user.*), VM agent or disk, status check."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/cloud-init.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cloud-init user and vendor data

- Actions run only on first start, never on reboot. Create with `incus init`, add the config, then start.
- The image needs cloud-init. The `images:` remote has `/cloud` variants such as `images:debian/12/cloud` (larger).
- VMs need a working `incus-agent` or a data disk: `incus config device add INSTANCE cloud-init disk source=cloud-init:config`.
- Newer images read `cloud-init.vendor-data` / `cloud-init.user-data`; older ones read `user.vendor-data` / `user.user-data`.
- Put vendor-data in a profile for defaults, user-data on the instance; both may go either place and cloud-init merges them.
- Use a YAML `|` literal block, starting the data with `#cloud-config`:

```yaml
config:
  cloud-init.user-data: |
    #cloud-config
    package_upgrade: true
    packages:
      - package1
```

- Common keys: `package_upgrade`, `packages`, `timezone`, `runcmd`, `users`.
- Check inside the instance with `cloud-init status` (`running` or `done`) or `cloud-init status --wait`.

## Checked

2026-11-09. Confirmed against the Incus doc cloud-init.md: first-start-only behaviour, /cloud image variants, agent or cloud-init disk for VMs, cloud-init.* versus user.* options, vendor-data and user-data roles, YAML literal block, example keys and status check. Removed: nothing needed removing.

Method: documentation only; no commands were run.
