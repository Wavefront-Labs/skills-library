---
id: computing-software.systems-network-administration.linux.user-disk-quotas-ext4
name: user-disk-quotas-ext4
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, disk-quotas, quota-setup, quotacheck, edquota, setquota, repquota, grace-period, soft-hard-limits, usrquota, grpquota, ext4, lpic-1, sysadmin]
level: practitioner
status: docs-checked
description: "Set up user and group quotas on ext4: enable with tune2fs or usrquota/grpquota plus quotacheck, set soft/hard limits and grace with edquota/setquota, report with repquota."
sources:
  - https://sourceforge.net/p/linuxquota/code/ci/master/tree/quotacheck.8?format=raw
  - https://sourceforge.net/p/linuxquota/code/ci/master/tree/edquota.8?format=raw
  - https://sourceforge.net/p/linuxquota/code/ci/master/tree/setquota.8?format=raw
  - https://sourceforge.net/p/linuxquota/code/ci/master/tree/repquota.8?format=raw
  - https://sourceforge.net/p/linuxquota/code/ci/master/tree/quotaon.8?format=raw
  - https://sourceforge.net/p/linuxquota/code/ci/master/tree/warnquota.8?format=raw
  - https://github.com/tytso/e2fsprogs/blob/master/misc/tune2fs.8.in
  - https://github.com/tytso/e2fsprogs/blob/master/misc/ext4.5.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User/group quotas on ext4

**Goal:** stop one user filling `/home` or a shared volume, with a warning window before the
hard stop, and a report of who uses what.

## 1. Enable
Modern way (journaled quota stored in hidden inodes, no aquota files):
```bash
umount /home
tune2fs -O quota /dev/vg0/home          # quota feature: hidden quota inodes (-Q usrquota,grpquota,prjquota to choose)
mount /home                              # ext4(5): quotas are enabled automatically at mount
quotaon -p /home                         # print quota state
```
Classic way (quota files):
```
/dev/vg0/home  /home  ext4  defaults,usrquota,grpquota  0 2
```
```bash
mount -o remount /home
quotacheck -cugm /home       # create aquota.user/aquota.group by scanning (-m: don't remount ro)
quotaon -v /home
```

## 2. Limits
Blocks are in 1 KiB units; inodes = number of files.
```bash
setquota -u alice 9G 10G 0 0 /home                      # soft 9G, hard 10G, no inode limit
setquota -g students 50G 55G 200000 220000 /home
edquota -u alice                                        # editor view of the same
edquota -p alice bob carol                              # copy alice's limits to others
quota -vs alice                                         # what alice sees (also `quota` as the user)
```

## 3. Soft, hard and grace
- **Hard** limit: writes fail immediately beyond it (`Disk quota exceeded`, EDQUOT).
- **Soft** limit: may be exceeded for the **grace period**; after it expires soft acts as hard.
```bash
edquota -t                         # filesystem-wide grace times
setquota -t 259200 259200 /home    # 3 days block and inode grace, in seconds
edquota -T alice                   # per-user grace override (only while over soft)
```
Warn users: `warnquota` (cron) mails over-soft users using `/etc/warnquota.conf`.

## 4. Reporting
```bash
repquota -s /home                  # all users: used, soft, hard, grace; "+-" flags over-limit
repquota -gs /home                 # groups
repquota -as                       # all quota-enabled filesystems
```

## Gotchas
- Quotas are per filesystem; `/home` on `/` means quota on the root fs.
- Files count against the **owner**; `chown` moves usage. Group quotas count by file group.
- XFS uses different tooling (`xfs_quota`) — see the XFS quota skill.

## Verify
- [ ] `repquota -s /home` lists users with the intended limits.
- [ ] As a test user, `fallocate -l 11G ~/big` fails with "Disk quota exceeded".
- [ ] `quotaon -p /home` reports user and group quota on after reboot.

## Checked
Checked 2026-10-26 against the quota-tools man pages (setquota, edquota, quotacheck, quotaon, repquota, warnquota, quota; linuxquota master) and e2fsprogs tune2fs(8) and ext4(5).
Confirmed: blocks are 1 KiB units with K/M/G/T suffixes and inode limits literal; `setquota -t` grace form; `edquota -p`, `-t`, `-T`; `quotacheck -c -u -g -m`; `quotaon -v` and `-p` (print state); `repquota -s -a -g`; warnquota mail from cron with `/etc/warnquota.conf`; `tune2fs -O quota` and `-Q usrquota,grpquota,prjquota`; the ext4 quota feature enables quotas at mount.
Removed as unconfirmed: the 7-day default grace, the post-crash quotacheck rule and the root-bypass remark.
Method: documentation only; no commands were run.
