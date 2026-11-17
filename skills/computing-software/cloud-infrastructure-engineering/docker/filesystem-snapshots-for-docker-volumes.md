---
id: computing-software.cloud-infrastructure-engineering.docker.filesystem-snapshots-for-docker-volumes
name: filesystem-snapshots-for-docker-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-backup, lvm-snapshot, zfs-snapshot, btrfs-snapshot, consistent-backup]
level: advanced
status: docs-checked
description: "Snapshot the filesystem under Docker volumes with LVM, ZFS or btrfs: where volume data lives, pausing containers, taking the snapshot, sizing LVM COW space, sending it elsewhere."
sources: ["https://man7.org/linux/man-pages/man8/lvcreate.8.html", "https://man7.org/linux/man-pages/man8/lvremove.8.html", "https://openzfs.github.io/openzfs-docs/man/master/8/zfs-snapshot.8.html", "https://openzfs.github.io/openzfs-docs/man/master/8/zfs-send.8.html", "https://btrfs.readthedocs.io/en/latest/btrfs-subvolume.html", "https://btrfs.readthedocs.io/en/latest/btrfs-send.html", "https://btrfs.readthedocs.io/en/latest/btrfs-receive.html", "https://docs.docker.com/engine/storage/volumes/", "https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/reference/cli/docker/container/pause/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filesystem snapshots for Docker volumes

Copying a large volume takes long. A snapshot gives a frozen image of a filesystem or logical
volume that you can copy from while the service keeps running.

## Layout first
Put volume data on its own snapshot-capable filesystem:
- The default `data-root` is `/var/lib/docker`, and it holds images, volumes and cluster
  state; it can be set with `--data-root` or `"data-root"` in `daemon.json`. A local-driver
  volume's mountpoint sits under it (for example `/var/lib/docker/volumes/my-vol/_data`),
  so put `data-root` on a dedicated LV / dataset / subvolume, or
- use bind mounts pointing at a directory on that filesystem.

## Pausing the application
`docker pause <container>` suspends all processes in the container using the freezer cgroup on
Linux; the processes cannot observe it, and `docker unpause` resumes them. Pausing before the
snapshot and resuming straight after keeps the window short. The cited pages do not describe
database-level backup modes, so check your database's own documentation if a paused container
is not enough.

## LVM
```bash
docker pause db
sudo lvcreate --snapshot --size 20G --name data-snap /dev/vg0/data
docker unpause db
```
Giving `--size` makes a copy-on-write snapshot; the size is the space available to store COW
blocks as writes occur to the origin or snapshot. The man page says the size should depend on
the writes you expect, "often 20% of the origin LV is enough", that COW space can be extended
with `lvextend`, that `lvs` shows how much is used, and that `--monitor` can extend it
automatically to avoid running out. A small part of the snapshot size is used to track COW
locations. Mount the snapshot LV read-only to copy from it, and remove it when done with
`lvremove` (it has `-y|--yes` to skip confirmation).

## ZFS
```bash
docker pause db; sudo zfs snapshot tank/docker@2026-11-07_0300; docker unpause db
sudo zfs send -i @prev tank/docker@2026-11-07_0300 | ssh backup zfs receive <dataset>
```
`zfs snapshot dataset@snapname` creates a snapshot atomically: a consistent image of the
dataset at one point in time, covering changes made by system calls that completed before it.
`-r` snapshots descendant datasets at the same time. The snapshot is mounted on demand under
the `.zfs/snapshot` directory at the root of the file system. `zfs send -i snapshot snapshot`
sends an incremental stream between two snapshots (the first may be given as just `@name`);
the receiving command is documented in zfs-receive(8), which was not read.

## btrfs
```bash
sudo btrfs subvolume snapshot -r /srv/data /srv/.snapshots/data-2026-11-07
sudo btrfs send /srv/.snapshots/data-2026-11-07 | ssh backup btrfs receive /pool
```
`-r` makes the snapshot read-only. Snapshots are read-write by default, and send requires
all snapshots involved to be read-only. A snapshot is not recursive: nested subvolumes are not
included and appear as empty stub subvolumes, so each nested subvolume needs its own snapshot.
The snapshot itself is instantaneous after dirty data is flushed. `btrfs send -p <parent>`
sends an incremental stream from a parent snapshot, and `btrfs receive <path>` stores the
received subvolume under `path`. The receive side must be protected from other writers until
the receive finishes.

## Gotchas
- A snapshot on the same disk is not a backup: send it elsewhere.
- Multiple volumes for one application on different filesystems need snapshots taken at the
  same moment (for example while the container is paused).
- Unmount and remove snapshots when finished; LVM COW snapshots hold space from the volume
  group while they exist.

## Checked
Date: 2026-11-07
Read in full: zfs-snapshot(8), btrfs-send, btrfs-receive, the docker container pause page. Read in part:
lvcreate(8) (snapshot option and size paragraph only; the rest of the 64 KB page searched, not read),
lvremove(8) (synopsis and `-y|--yes` only), btrfs-subvolume (snapshot/SUBVOLUME FLAGS/nested-subvolume
paragraphs), zfs-send(8) (synopsis and `-i`/`-I` options; the rest not read), dockerd page (`--data-root`
text only), Docker volumes page (mountpoint example and pre-populate paragraphs only).
Removed: `mount -o ro,nouuid` for xfs, `fsfreeze`, `pg_backup_start()`, restic, the claim that crash-consistent
snapshots are fine for databases, "a full snapshot becomes invalid" (the man page does not say that),
`zfs list -t snapshot`, "snapshots are read-only" for ZFS, EBS/PD/Azure disk snapshot paragraph (no cited page),
and "in-flight client requests time out" for docker pause. `zfs receive` arguments are left as a
placeholder because that man page was not read.
Method: documentation only; no commands were run.
