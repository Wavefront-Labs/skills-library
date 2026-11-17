---
id: computing-software.cloud-infrastructure-engineering.ansible.selinux-mode-changes-and-reboots
name: selinux-mode-changes-and-reboots
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, firewall-selinux, selinux-reboot, enforcing, permissive, reboot-module]
level: practitioner
status: docs-checked
description: "Change SELinux mode and policy with ansible.posix.selinux, detect reboot_required, relabel safely when enabling from disabled, and avoid unbootable hosts."
sources: ["https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/selinux.py", "https://github.com/SELinuxProject/selinux/blob/main/policycoreutils/scripts/fixfiles.8", "https://github.com/SELinuxProject/selinux/blob/main/python/semanage/semanage-permissive.8", "https://github.com/linux-audit/audit-userspace/blob/master/docs/ausearch.8", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/reboot_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SELinux mode changes and reboots

```yaml
- name: Set SELinux to enforcing
  ansible.posix.selinux:
    policy: targeted
    state: enforcing
  register: se

- name: Reboot if the change needs it
  ansible.builtin.reboot:
    reboot_timeout: 900
  when: se.reboot_required
```

## What needs a reboot
| From → To | Runtime effect | Reboot |
|---|---|---|
| enforcing ↔ permissive | immediate (`setenforce`) | no |
| disabled → permissive/enforcing | none until boot | yes, plus full relabel |
| enabled → disabled | none until boot | yes |
| policy type change | written to the config file only; the module cannot change the running policy | take effect after a reboot |

The module writes `/etc/selinux/config` (`configfile`) and sets the runtime state when possible; the `reboot_required` result is true for the enable and disable transitions.

## Enabling from disabled safely
1. Set **permissive** first, `touch /.autorelabel` (the file `fixfiles onboot` uses; see fixfiles(8)), reboot (relabel can take a long time on large filesystems).
2. Check denials: `ausearch -m AVC -ts boot`.
3. Fix contexts/booleans, then switch to enforcing (no reboot needed).
Going straight from disabled to enforcing risks services failing because files are unlabelled.

## Kernel parameter
`update_kernel_param: true` also updates the kernel boot parameters when disabling or enabling SELinux; it needs `grubby` on the target. Prefer permissive mode, or per-domain permissive (`semanage permissive -a httpd_t`), over disabling.

## Gotchas
- `ansible.posix.selinux` needs the SELinux Python bindings (libselinux-python) on the target.
- A relabel can take a long time on large filesystems: give `reboot_timeout` enough room.

## Verify
```bash
ansible all -m ansible.builtin.command -a 'getenforce' -o
```

## Checked

Checked 2026-10-26 against the ansible.posix `selinux` module source (main) and the SELinux and audit manual pages on GitHub. Confirmed: `state` choices disabled, enforcing, permissive; `policy` required unless state is disabled; `configfile` default `/etc/selinux/config`; `update_kernel_param` (needs grubby); `reboot_required` is set for transitions that need a reboot (enabling from disabled, disabling) and not for enforcing/permissive changes; the running policy cannot be changed by the module; `semanage permissive -a`; `ausearch -ts boot`; the `/.autorelabel` file referenced by fixfiles. Removed the RHEL 9 `selinux=0` remark, which only the Red Hat documentation covers.

Method: documentation only; no commands were run.
