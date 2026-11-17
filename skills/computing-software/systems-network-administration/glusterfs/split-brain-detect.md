---
id: computing-software.systems-network-administration.glusterfs.split-brain-detect
name: split-brain-detect
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, split-brain, gfid-split-brain, heal-info, detection]
level: practitioner
status: docs-checked
description: "Detect data, metadata, entry and GFID split-brain in a GlusterFS replicate volume using gluster volume heal info and heal info split-brain."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/resolving-splitbrain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detect split-brain

```
gluster volume heal <VOLNAME> info
gluster volume heal <VOLNAME> info split-brain
```

- `info` lists all entries needing heal; those in data or metadata split-brain are tagged "Is in split-brain".
- `info split-brain` shows only the split-brain subset.
- For GFID split-brain the parent directory is marked as split-brain and the file itself is listed as needing heal.
- GFID split-brain entries may not always show as split-brain in these outputs. For entry split-brain you may need `info split-brain` to find the directory, then `info` to list files beneath it.

For a GFID split-brain also inspect each brick copy:

```
getfattr -d -e hex -m. <path-to-file>
stat <path-to-file>
```

Type mismatches (a file on one brick, a directory on another) cannot be healed with the CLI policies.

Resolution options: split-brain-cli-resolution, split-brain-manual-xattr, split-brain-mount-choice.

## Checked

2026-11-04. Confirmed against the glusterdocs Resolving Split-brains page: heal info and heal info split-brain, the Is in split-brain tag, the GFID split-brain listing behaviour, the entry split-brain advice, getfattr and stat inspection, and the type-mismatch limitation. Removed: the prevention clause, which this page does not cover.

Method: documentation only; no commands were run.
