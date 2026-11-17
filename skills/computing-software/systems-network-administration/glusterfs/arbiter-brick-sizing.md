---
id: computing-software.systems-network-administration.glusterfs.arbiter-brick-sizing
name: arbiter-brick-sizing
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, arbiter, brick-sizing, maxpct, inode]
level: advanced
status: docs-checked
description: "Size GlusterFS arbiter bricks: about 4KB per file, 512-byte inodes, and raising the XFS maxpct (for example 25%) on filesystems over 1TB."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/arbiter-volumes-and-quorum.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Split-brain-and-ways-to-deal-with-it.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arbiter brick sizing

Arbiter bricks store only file names, directory structure, extended attributes and the `.glusterfs` metadata, not file data.

- Estimate roughly 4KB multiplied by the number of files you expect.
- Use 512-byte inodes (the page recommends this).
- XFS limits the share of space usable for inodes by `maxpct` (default 5% for filesystems of 1TB to 50TB), which can cap inode capacity. For XFS filesystems larger than 1TB, set a higher value such as 25%; see the `mkfs.xfs` man page for the option.
- Enabling the arbiter feature sets client quorum to `auto`; leave it.

Failure behaviour:

- With two bricks up, one of them the arbiter, and the arbiter blaming the other up brick for a file, all writes to that file fail with ENOTCONN, because the only good copy is on the brick that is down.
- With two bricks up and the arbiter down, operations are allowed; with only one brick up, client quorum is not met and the volume returns ENOTCONN.

Create the volume with create-arbiter-volume.

## Checked

2026-11-04: metadata-only contents, the 4KB-per-file estimate, 512-byte inodes, XFS `maxpct` of 5% for 1TB to 50TB with 25% as the example, and the client-quorum auto note were read against the glusterdocs page arbiter-volumes-and-quorum. Corrected the one-brick-up behaviour from read-only (EROFS) to ENOTCONN and reworded the blame case to match the page.

Method: documentation only; no commands were run.
