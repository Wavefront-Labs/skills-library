---
id: computing-software.cloud-infrastructure-engineering.kubespray.upgrade-with-system-package-updates
name: upgrade-with-system-package-updates
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [upgrade, system-upgrade, reboot, apt, yum]
level: practitioner
status: docs-checked
description: "Patch OS packages during upgrade-cluster.yml with system_upgrade, control reboots with system_upgrade_reboot and clean apt caches with system_upgrade_autoclean."
sources:
  - https://kubespray.io/docs/operations/upgrades.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To upgrade APT or YUM packages while nodes are cordoned, enable the system upgrade in the graceful playbook:

```ShellSession
ansible-playbook upgrade-cluster.yml -b -i inventory/sample/inventory.ini -e '{"system_upgrade": true}'
```

Reboots are controlled by `system_upgrade_reboot`. The default is `on-upgrade`, so nodes are rebooted when package upgrades happened. It can be set to `always` or `never`.

Downloads happen twice unless `system_upgrade_reboot` is `never`.

For Debian-based nodes, `system_upgrade_autoclean: true` cleans packages to reduce disk usage.

Also from the same page: migrating a cluster from docker to containerd is not officially supported. Since Kubespray 2.18.0 containerd is the default container engine, and the safer route is to reset and redeploy with the new engine.

## Checked

2026-11-04. The system_upgrade variables were confirmed on the System upgrade section of the Upgrading page; the containerd remark is from the Migrate from Docker to Containerd section. Removed an unsupported remark about combining with the pause variables.

Method: documentation only; no commands were run.
