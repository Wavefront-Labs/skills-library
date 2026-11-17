---
id: computing-software.systems-network-administration.kopia.kopia-restore-and-mount
name: kopia-restore-and-mount
category: computing-software
field: systems-network-administration
product: kopia
tags: [restore, mount, snapshot-restore, fuse, point-in-time]
level: practitioner
status: docs-checked
description: "Restore from Kopia snapshots by mounting them, using snapshot restore or fetching single files."
sources: ["https://kopia.io/docs/mounting/", "https://kopia.io/docs/getting-started/", "https://kopia.io/docs/repository-server/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
There are three ways to get data back: mount a snapshot as a local drive and copy what you need, restore everything in a snapshot to a local or network location, or download individual files (for example in KopiaUI by browsing the snapshot). Mounting is described as the currently recommended way to restore.

```console
mkdir /tmp/mnt
kopia mount SNAPSHOT_ID /tmp/mnt &
ls -l /tmp/mnt
umount /tmp/mnt
```

Mounting works repository-wide or per content. The special path `all` mounts the whole repository with the latest snapshot version of each source:

```console
kopia mount all /tmp/mnt &
```

Mounted contents can be examined with ordinary file commands or a browser. For a full restore use `kopia snapshot restore` with a snapshot or object ID and a target directory.

Because files are content-addressed, `kopia show OBJECT_ID` works on the object identifier of any file or directory, such as one listed by `kopia ls -l`, and `kopia snapshot restore` can restore by snapshot or object ID. Under a repository server any user who knows a valid object ID can restore it, which is also how users can share files by exchanging IDs.

The most reliable validation of a backup is a real restore; when that is impractical use the verify options described in the consistency skill.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Mounting (recommended restore method, mount all, per-snapshot mount), Getting Started (three restore routes, show with object IDs) and Repository Server (object IDs allow restore and sharing). Removed or corrected: the `kopia restore OBJECT_ID` command, which the pages do not show; replaced with `kopia snapshot restore`.
Method: documentation only; no commands were run.
