---
id: computing-software.systems-network-administration.linux.xfs-user-and-project-quotas
name: xfs-user-and-project-quotas
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, disk-quotas, xfs-quota, project-quota, directory-quota, uquota, pquota, xfs, lpic-1, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Limit space on XFS with xfs_quota: enable uquota/gquota/pquota at mount, set user limits, and cap individual directory trees with project quotas (projects/projid)."
sources:
  - https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/man/man8/xfs_quota.8
  - https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/xfs.rst
  - https://github.com/tytso/e2fsprogs/blob/master/misc/ext4.5.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XFS user and project quotas

**Goal:** per-user limits on XFS, and — XFS's speciality — per-**directory** limits
(project quotas) for shares, tenant directories or container volumes.

## 1. Enable (mount options; quota accounting is set at mount, not with quotaon)
```
/dev/vg0/srv  /srv  xfs  defaults,uquota,pquota  0 0
```
`uquota`/`usrquota`, `gquota`/`grpquota`, `pquota`/`prjquota`. For the **root** filesystem the quota mount flags must be passed with the `rootflags=` boot parameter (xfs_quota(8)).
Quota accounting must be turned on at mount time; limits cannot be set before quotas are on.
```bash
umount /srv && mount /srv
xfs_quota -x -c 'state' /srv          # accounting/enforcement ON for each type
```

## 2. User limits
```bash
xfs_quota -x -c 'limit bsoft=9g bhard=10g alice' /srv
xfs_quota -x -c 'limit isoft=50000 ihard=60000 alice' /srv
xfs_quota -x -c 'limit -g bhard=100g developers' /srv
xfs_quota -x -c 'timer -u -b 3days' /srv           # grace for soft limits
xfs_quota -x -c 'report -h' /srv                   # users (add -g / -p for groups / projects)
xfs_quota -c 'quota -h alice' /srv                 # non-expert mode, for the user
```

## 3. Project (directory) quotas
```bash
echo '42:/srv/projects/apollo' >> /etc/projects     # id:path
echo 'apollo:42' >> /etc/projid                      # name:id
xfs_quota -x -c 'project -s apollo' /srv             # tag directory tree with project id (sets inherit flag)
xfs_quota -x -c 'limit -p bsoft=900g bhard=1t apollo' /srv
xfs_quota -x -c 'report -p -h' /srv
```
Files created under the tree are accounted to the project. A hard link to a file in the tree only
succeeds if the project id matches the tree's (xfs_quota(8)).
Without /etc/projects you can use numeric ids directly: `project -s -p /srv/projects/apollo 42`.

## Gotchas
- Forgetting `pquota` in fstab: project accounting is off, and limits cannot be set before quotas are on.
- Reaching a hard limit gives `EDQUOT` ("Disk quota exceeded").
- `xfs_quota` commands need `-x` (expert mode) for limits/reports; without it only `quota`/`df` work.
- ext4 also supports project quotas (the `project` and `quota` features, ext4(5)) with the quota-tools commands instead.

## Verify
- [ ] `xfs_quota -x -c state` shows enforcement ON for the types you configured.
- [ ] Writing beyond the project hard limit fails inside the directory and succeeds outside it.
- [ ] `report -p -h` lists the project with correct usage.

## Checked
Checked 2026-10-26 against the xfs_quota man page (xfsprogs-dev master), the kernel XFS admin guide (Documentation/admin-guide/xfs.rst) and e2fsprogs ext4(5).
Confirmed: uquota/usrquota, gquota/grpquota, pquota/prjquota mount options; accounting must be set at mount; `rootflags=` for the root filesystem; `-x` expert mode; `limit bsoft/bhard/isoft/ihard`, `timer` with `3days`-style values, `report -h`, `quota`; `project -s`, `/etc/projects` and `/etc/projid`, numeric `project -s -p PATH ID`; hard links across project ids fail.
Removed as unconfirmed: V5-only coexistence of group and project quotas, the EXDEV-on-mv claim, the `df` project-size remark, the exact "project quota not enabled" error text and chattr project flags.
Method: documentation only; no commands were run.
