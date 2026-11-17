---
id: computing-software.systems-network-administration.restic.mount-and-dump
name: mount-and-dump
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, mount, dump, fuse, tar, zip, stdout]
level: practitioner
status: docs-checked
description: "Browse snapshots with restic mount over FUSE and stream single files or archives to stdout with restic dump."
sources:
  - https://restic.readthedocs.io/en/stable/050_restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mount and dump

## Mount

```
mkdir /mnt/restic
restic -r /srv/restic-repo mount /mnt/restic
```

The repository is served as a filesystem via FUSE; browse it with normal tools and copy files out. Platform needs:

- Linux: the `fuse` module and `fusermount`
- macOS: FUSE-T or macOS FUSE
- FreeBSD: `kldload fuse`

The mountpoint must not overlap the repository directory; restic refuses it. Hard links need a tool such as `rsync --hard-links` to copy correctly. Mounting suits a few files; use `restore` for bulk restores.

## Dump to stdout

```
restic dump latest /path/in/snapshot/file.txt | less
restic dump <snapshot-id> /path/in/snapshot/file.txt
restic dump --path /path/to/data latest /path/in/snapshot/file.txt
restic dump -a zip latest /path/in/snapshot/dir > dir.zip
```

- A folder is written as an archive; `-a tar` is the default and `-a zip` the alternative.
- `latest:<subfolder> /` puts that folder's contents at the archive root.
- `--target <file>` writes to a file instead of stdout.

For example, `restic dump latest production.sql | mysql` streams a stored SQL dump straight back into a database; if `latest` is not the right snapshot, pass a snapshot ID or `--path`.

## Checked

Checked 2026-11-08 against the restic Restoring from backup page (050_restore), read in full. Confirmed: mount with FUSE on Linux, macOS and FreeBSD and the platform requirements, the mountpoint overlap refusal, rsync --hard-links, mount versus restore, dump with latest, snapshot ID and --path, tar default and -a zip, the snapshot:subfolder form and --target. Removed: the unsupported read-only claim.

Method: documentation only; no commands were run.
