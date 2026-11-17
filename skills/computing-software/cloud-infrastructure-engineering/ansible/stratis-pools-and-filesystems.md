---
id: computing-software.cloud-infrastructure-engineering.ansible.stratis-pools-and-filesystems
name: stratis-pools-and-filesystems
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, storage-filesystems, stratis, storage-role, filesystems]
level: practitioner
status: docs-checked
description: "Create Stratis pools and thin filesystems on RHEL with the storage system role or stratis CLI tasks, mount them with x-systemd.requires, and grow pools."
sources:
  - https://raw.githubusercontent.com/linux-system-roles/storage/main/README.md
  - https://raw.githubusercontent.com/stratis-storage/stratis-cli/master/docs/stratis.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Stratis pools and filesystems

Stratis creates a pool from one or more block devices and lets you create multiple filesystems from
the pool. Every Stratis filesystem holds an XFS filesystem.

## With the storage system role
```yaml
- hosts: db
  roles:
    - role: redhat.rhel_system_roles.storage
      vars:
        storage_pools:
          - name: datapool
            type: stratis
            disks: [sdb, sdc]
            volumes:
              - name: pgdata
                size: 50 GiB
                mount_point: /var/lib/pgsql
```
The storage role README lists Stratis pools as supported (with Stratis v3 and newer): `type: stratis`
in `storage_pools`, with nested `volumes`; new Stratis filesystems can be added to existing setups.
`size` takes human-readable values such as "50 GiB"; omitting it uses all available space. The role
manages the mount entry from `mount_point` and `mount_options`. For encrypted Stratis pools it
offers `encryption_clevis_pin` (`tang` or `tpm2`), `encryption_tang_url` and
`encryption_tang_thumbprint`. `storage_safe_mode` (default true) errors instead of removing or
formatting existing devices.

## Manually with the stratis CLI
```yaml
- name: Create pool
  ansible.builtin.command: stratis pool create datapool /dev/sdb
  when: "'datapool' not in pool_list.stdout"   # pool_list: register a prior `stratis pool list` (changed_when: false)
- name: Create filesystem
  ansible.builtin.command: stratis filesystem create datapool pgdata
  when: "'pgdata' not in fs_list.stdout"       # fs_list: register a prior `stratis filesystem list`
```
`stratis pool create <pool_name> <blockdev> [<blockdev>..]` and `stratis filesystem create <pool_name>
<fs_name>` are the documented forms (`--size` sets a size; `--size-limit` caps growth). The device
path to mount is shown in the `Device` column of `stratis filesystem list`; mount it with
`ansible.posix.mount` and check the systemd ordering your distribution documents for Stratis mounts.

## Growing
`stratis pool add-data <pool_name> <blockdev>` adds devices to enlarge the pool.
`stratis pool extend-data <pool_name>` uses space gained when a component device (for example a
RAID device) has expanded. Filesystems are grown by Stratis up to their size limit, or the maximum
possible if none is set. Pools allow overprovisioning by default; `stratis pool overprovision
<pool_name> no` (or `--no-overprovision` on create) stops the sum of filesystem sizes exceeding the pool, so
watch `stratis pool list` usage otherwise.

## Gotchas
- stratisd refuses to claim a block device that appears to be in use; any signature must be erased first, after carefully verifying the device.
- Encryption and a cache are mutually exclusive choices for a pool.
- Encryption on/off/reencrypt on an existing pool needs `--in-place`, runs for a time proportional to the pool size, and blocks adding devices meanwhile; back up first.

## Verify
- [ ] `stratis pool list` shows the pool, and `stratis filesystem list` shows the filesystem with its device path.
- [ ] The mount point from the play appears mounted after a reboot.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the linux-system-roles storage README (Stratis pool support, `storage_pools` keys, safe mode, Clevis options) and the stratis(8) man page source from stratis-cli (create, add-data, extend-data, overprovision, size limits, restrictions, notes). Removed as not confirmed: the RHEL 8+ and EX294 statements, the `x-systemd.requires=stratisd.service` mount option and boot-hang claim (the Red Hat guide returned 403), the `/dev/stratis/<pool>/<fs>` path and `creates:` guard, the claim that the role installs stratisd and writes systemd dependencies, the advice not to run `mkfs`/`xfs_growfs`, and `wipefs -a`.
