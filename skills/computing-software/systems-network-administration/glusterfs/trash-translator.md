---
id: computing-software.systems-network-administration.glusterfs.trash-translator
name: trash-translator
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, trash, trashcan, trash-max-filesize, recycle-bin]
level: practitioner
status: docs-checked
description: "Use the GlusterFS trash translator to keep deleted and truncated files in .trashcan: enable it, set the directory, max file size, excluded paths and internal ops."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Trash.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trash translator

```
gluster volume set <VOLNAME> features.trash <on/off>
gluster volume set <VOLNAME> features.trash-dir <name>
gluster volume set <VOLNAME> features.trash-max-filesize <size>
gluster volume set <VOLNAME> features.trash-eliminate-path <path1> [ , <path2> , . . . ]
gluster volume set <VOLNAME> features.trash-internal-op <on/off>
```

- `features.trash`: enables the translator (it is loaded at start but inert until on).
- `trash-dir`: default `.trashcan`; only changeable while trash is on.
- `trash-max-filesize`: default 5MB; larger files are deleted or truncated without being saved. Accepts KB, MB, GB suffixes (1024 based).
- `trash-eliminate-path`: files under listed paths skip the trash; each path must exist in the volume.
- `trash-internal-op`: default off; when on, also covers self-heal and rebalance, stored in an `internal_op` folder.

Caveats:

- Disabling trash does not remove the trash directory or its contents.
- The directory appears under the mount as soon as the volume starts.
- Trashed files get a timestamp appended to avoid name collisions.
- Known issue: AFR and DHT are unaware of the renames and truncates, so trashed files may stay hidden until a lookup uses the full path.

## Checked

2026-11-04: the five options with their defaults and units, timestamp suffix, internal_op folder, disable behaviour, directory visibility and the known issue were read against the glusterdocs page Trash. Nothing removed.

Method: documentation only; no commands were run.
