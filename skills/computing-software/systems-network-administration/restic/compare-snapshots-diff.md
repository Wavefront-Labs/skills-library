---
id: computing-software.systems-network-administration.restic.compare-snapshots-diff
name: compare-snapshots-diff
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, diff, snapshots, compare, metadata]
level: practitioner
status: docs-checked
description: "Compare two restic snapshots or subfolders with restic diff, including latest and the --metadata flag."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing snapshots

```
restic -r /srv/restic-repo diff <id1> <id2>
restic -r /srv/restic-repo diff latest <id>
```

`diff` lists files added, removed or modified between the two snapshots, so you can see what a backup actually picked up.

## Narrow the comparison

Use `<snapshot>:<subfolder>` on either side to compare directories inside snapshots:

```
restic diff 5e1a1b2c:/path/to/work latest:/path/to/work
```

## Metadata

`--metadata` includes metadata-only changes such as permissions and ownership; without it, you see content changes.

## Typical uses

- After changing exclude rules, diff the last snapshot against the one before it to confirm the intended files disappeared and nothing else did.
- In scripts, diff supports JSON output with `--json` (see the json-output-scripting skill).

`latest` selects the newest snapshot. Use `restic snapshots` to find IDs and to confirm both snapshots came from the same host and path.

## Checked

Checked 2026-11-08 against the restic Backing up page (040_backup) and Scripting page (075_scripting), both read in full. Confirmed: diff of two snapshot IDs, the snapshot:subfolder syntax with latest, --metadata, and diff JSON output. Removed: the restore-comparison use and the unique-prefix remark, which the pages do not state.

Method: documentation only; no commands were run.
