---
id: computing-software.systems-network-administration.linux.backup-and-restore-rsync-borg-restic
name: backup-and-restore-rsync-borg-restic
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, backup, restore, rsync, borg, borgbackup, restic, deduplication, encrypted-backup, incremental-backup, snapshot-backup, lvm-snapshot-backup, pg-dump, mysqldump, retention, prune, 3-2-1, offsite, s3-backup, restore-test, systemd-timer-backup, lpic-2, sysadmin, link-dest, rsync-options, bare-metal-restore]
level: practitioner
status: gated
description: "Back up Linux hosts you can actually restore: rsync mirrors, borg and restic repos with retention, consistent DB and LVM-snapshot sources, systemd timers, and the restore drill."
sources:
  - https://borgbackup.readthedocs.io/en/stable/
  - https://restic.readthedocs.io/en/stable/
  - https://man7.org/linux/man-pages/man1/rsync.1.html
  - https://www.postgresql.org/docs/current/backup.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Backup and restore — rsync, borg, restic, and proving you can get it back

**Goal:** 3-2-1 (three copies, two media, one offsite) for the data that matters, with
consistent sources, bounded retention, alerts on failure, and a restore you've rehearsed.

## 0. What to back up, in order of regret
`/etc`, `/home`, `/root`, `/var/lib/<service>` (databases via dumps, see §3), `/srv`, `/var/mail`, (gated: unconfirmed, source is paywalled or blocked)
`/var/spool/cron`, `/var/log` (if compliance), package list (`dnf repoquery --userinstalled` /
`apt-mark showmanual`), LVM/partition layout (`lsblk -f`, `sfdisk -d`, `vgcfgbackup`). Skip
`/proc /sys /dev /run /tmp`, caches, container images (re-pullable). Don't back up an
unencrypted copy of secrets to a target the backup user can't protect.

## 1. rsync — mirrors and simple rotation
```bash
rsync -aHAX --numeric-ids --delete --delete-excluded --info=progress2 \
  --exclude-from=/etc/backup/excludes /srv/ backup@nas:/backups/web01/srv/
rsync -aHAX --link-dest=/backups/web01/2026-10-14 /srv/ /backups/web01/2026-10-15/   # hardlink snapshots (poor man's dedup)
rsync -n ...   # dry run first when --delete is involved
```
`-a` archive, `-H` hardlinks, `-A` ACLs, `-X` xattrs (SELinux labels, capabilities), `--numeric-ids`
when the target has different users. Trailing slash on the source = contents, not the dir.
rsync is a sync, not a backup: a deletion or ransomware encryption propagates on the next run.
Use it for mirrors and staging, pair it with snapshots or a real backup tool for history.

## 2. borg (SSH targets, local disks) and restic (S3/B2/Azure/SFTP/rest-server)
```bash
# borg
export BORG_REPO=ssh://backup@nas/./repos/web01 BORG_PASSCOMMAND='cat /etc/backup/borg.pass'
borg init --encryption=repokey-blake2
borg key export $BORG_REPO /etc/backup/web01.borgkey        # WITHOUT this + passphrase the repo is unreadable
borg create --stats --compression zstd,3 --exclude-caches --exclude-from /etc/backup/excludes \
  ::'{hostname}-{now:%Y-%m-%dT%H:%M}' /etc /home /root /srv /var/lib/backup-dumps
borg prune --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --glob-archives '{hostname}-*'
borg compact
borg list; borg info ::web01-2026-10-15T02:00; borg mount :: /mnt/borg   # FUSE browse
borg extract ::web01-2026-10-15T02:00 etc/nginx                         # relative paths, into cwd
borg check --verify-data   # monthly

# restic
export RESTIC_REPOSITORY=s3:https://s3.eu-west-1.amazonaws.com/backups-example/web01 RESTIC_PASSWORD_FILE=/etc/backup/restic.pass
# AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY from the env or a credentials file
restic init
restic backup --exclude-caches --exclude-file /etc/backup/excludes --tag daily /etc /home /root /srv /var/lib/backup-dumps
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
restic snapshots; restic ls latest /etc/nginx; restic restore latest --target /tmp/restore --include /etc/nginx
restic mount /mnt/restic; restic check --read-data-subset=10%   # monthly
```
- Both: client-side encryption, content-defined chunking dedup, so daily fulls cost
  only the delta. Both need the **key/passphrase stored outside the backup** (password
  manager + printed copy). Use one repo per host (restic with a
  rest-server in `--append-only` mode, borg with `borg serve --append-only` on the SSH key's
  `command=` to resist a compromised client deleting history).
- Append-only / object lock on the target is what makes backups ransomware-resistant;
  `--delete` rights on the live host are the thing an attacker uses.
- Speed: restic `--read-concurrency`, borg `--files-cache=ctime,size` for huge trees; both
  use a local cache (`~/.cache/borg|restic`) — keep it on fast disk and don't back it up.
- `restic rewrite --exclude` drops secrets that were captured by accident.

## 3. Consistent sources
```bash
# databases: dump, don't copy files
pg_dumpall -U postgres | zstd > /var/lib/backup-dumps/pg-$(date +%F).sql.zst         # or pg_dump -Fc per DB
mariadb-dump --all-databases --single-transaction --routines --events | zstd > /var/lib/backup-dumps/mysql-$(date +%F).sql.zst
# or the tool's own PITR: pg_basebackup + WAL archiving (archive_command), mariabackup
# filesystems with live apps: LVM snapshot, back up the snapshot, drop it
lvcreate -s -L 5G -n srv_snap /dev/vg0/srv && mount -o ro,nouuid /dev/vg0/srv_snap /mnt/snap   # nouuid for XFS
borg create ::'{hostname}-srv-{now}' /mnt/snap; umount /mnt/snap; lvremove -f /dev/vg0/srv_snap
# btrfs/zfs: ro snapshot → backup the snapshot path (or zfs send | restic? no: send to another pool, restic for files)
```
VMs: `virsh domfsfreeze` via guest agent → `virsh snapshot-create-as --disk-only` → back up the
base → `blockcommit`. Containers: back up the volumes (`podman volume export`), not the container.

## 4. Scheduling and alerting
```ini
# /etc/systemd/system/backup.service
[Service]
Type=oneshot
ExecStart=/usr/local/sbin/backup.sh
Nice=19
IOSchedulingClass=idle
# /etc/systemd/system/backup.timer
[Timer]
OnCalendar=*-*-* 02:00
RandomizedDelaySec=30m
Persistent=true
[Install]
WantedBy=timers.target
```
`backup.sh` uses `set -euo pipefail`, dumps → backup → prune → check exit codes → pings a
dead-man's-switch (healthchecks.io-style URL or a Prometheus push). **Silence is not success**:
alert when the job *didn't* run. `OnFailure=status-email@%n.service` for the failure path.
`systemctl list-timers backup.timer`; `journalctl -u backup.service`.

## 5. The restore drill (quarterly, written down)
1. Bare-metal: boot rescue media, partition (`sfdisk /dev/sda < sda.dump`), recreate LVM, `mkfs`, mount
   under `/mnt`, `borg extract`/`restic restore` into it, `chroot` → reinstall bootloader
   (`grub2-install`, `dracut -f`), fix `fstab` UUIDs, `restorecon -R /` or `touch /.autorelabel`.
2. Single file: `restic restore latest --include <path> --target /tmp/r`; compare with `diff`.
3. Database: restore the dump into a scratch instance and run the app's smoke test.
Time it. If the RTO is wrong, the backup design is wrong, not the drill.

## Failure modes
- Backups "work" for a year, repo key lost with the dead host → unrecoverable. Export keys on day one.
- Retention never pruned → target full → silent failures. Prune + compact in the same job.
- Backing up live database files → corrupt restore. Dumps or snapshots only.
- Running as root to a target where the backup user can delete history → ransomware wins. Append-only.
- `rsync --delete` with a typo'd/empty source path → destination emptied. Dry-run, and quote variables.

## Verify
- [ ] `borg list`/`restic snapshots` shows a snapshot from last night and the timer's next run.
- [ ] A random file and the latest DB dump restore to a scratch location and match (`sha256sum`, app smoke test).
- [ ] The repo key/passphrase exists in two places outside the backed-up host; `borg check`/`restic check` passed within 30 days.

## Checked

2026-11-02

- Confirmed: The rsync(1) man page (man7.org), the BorgBackup and restic documentation indexes were fetched.
- Removed or gated: Borg and restic option names (--keep-*, --glob-archives, --read-data-subset, --verify-data) are not stated on the fetched index pages, and rsync -aHAX style bundles were not individually checked; gated, confirm in the current borg/restic references.

Method: documentation only; no commands were run.
