---
id: computing-software.cloud-infrastructure-engineering.ansible.software-raid-with-mdadm
name: software-raid-with-mdadm
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, storage-filesystems, mdadm, raid, mdadm-conf, storage-role]
level: advanced
status: docs-checked
description: "Create Linux software RAID arrays from Ansible safely: guarded mdadm commands or the RHEL storage role, mdadm.conf persistence, initramfs update and health checks."
sources:
  - https://man7.org/linux/man-pages/man8/mdadm.8.html
  - https://raw.githubusercontent.com/md-raid-utilities/mdadm/main/mdadm.conf.5.in
  - https://raw.githubusercontent.com/linux-system-roles/storage/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Software RAID with mdadm

Two options: the storage system role (declarative, preferred) or guarded `mdadm` commands.

## 1. The storage system role (declarative)
```yaml
- hosts: db
  roles:
    - role: redhat.rhel_system_roles.storage      # or fedora.linux_system_roles.storage
      vars:
        storage_safe_mode: true                   # error instead of removing or formatting existing data
        storage_volumes:
          - name: data
            type: raid
            disks: [sdb, sdc, sdd, sde]
            raid_level: raid10
            raid_chunk_size: 512 KiB
            fs_type: xfs
            mount_point: /data
```
The README lists MD RAID as supported and the role manages file systems and mount entries.
For `type: raid` volumes the options are `raid_level` (`linear`, `raid0`, `raid1`, `raid4`, `raid5`,
`raid6`, `raid10`), `raid_device_count`, `raid_spare_count`, `raid_metadata_version` and
`raid_chunk_size` (a multiple of 4 KiB). `storage_safe_mode` defaults to true. Changing
`raid_level` on an existing volume is destructive (data lost) and RAID reshaping is not supported.
Pools of `type: lvm` can also set `raid_level` for a volume group on an mdraid array.

## 2. Guarded commands
```yaml
- name: Create RAID1 if not present
  ansible.builtin.command: >
    mdadm --create /dev/md0 --level=1 --raid-devices=2 --metadata=1.2
    --name=data --run /dev/sdb /dev/sdc
  args:
    creates: /dev/md0

- name: Show the array definition to put in the config file
  ansible.builtin.command: mdadm --detail --scan
  register: scan
  changed_when: false
```
`--metadata` defaults to 1.2 for `--create`. `mdadm --detail --scan` prints lines in
`mdadm.conf` form; the config file is `/etc/mdadm.conf` (or `/etc/mdadm/mdadm.conf`; also
`mdadm.conf.d`). Append the array line with `ansible.builtin.lineinfile` so reruns do not duplicate
it. Then use `community.general.filesystem` and `ansible.posix.mount` on `/dev/md0`.

## Monitoring
`MAILADDR` in `mdadm.conf` sets where monitor mail goes (for example `MAILADDR root@mydomain.tld`
is the man page's example). Under systemd the page says `mdmonitor.service` should be present and
runs the monitor. `/proc/mdstat` lists all md arrays and shows resync progress.

## Gotchas
- `--run` insists on running the array even if some devices look like they belong to another array; old metadata is removed with `--zero-superblock`, which the man page warns to use carefully. Both are destructive: only on new disks, behind a flag.
- Do not rely on array device names unless they are in the config file; check the names after a reboot.
- Initial resync runs in the background; progress is in `/proc/mdstat`.

## Verify
- [ ] `mdadm --detail /dev/md0` lists the array state and all member devices.
- [ ] After a reboot `/dev/md0` exists with the same name.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the mdadm(8) man page (flags `--create`, `--level`, `--raid-devices`, `--metadata`, `--name`, `--run`, `--zero-superblock`, `--detail --scan`, config file paths, mdmonitor.service, /proc/mdstat), the mdadm.conf(5) source (MAILADDR) and the linux-system-roles storage README (RAID options, safe mode). Removed as not in these sources: "no mdadm module exists", the claim that the storage role writes mdadm.conf, the grep-based persistence script, the update-initramfs and dracut tasks and their distro mapping, the `/dev/md127` rename claim, the `[U_]` degraded check, the `State : clean` output claim and the Red Hat guide citation (page blocked, not read).
