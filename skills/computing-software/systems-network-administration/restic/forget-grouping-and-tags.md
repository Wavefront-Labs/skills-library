---
id: computing-software.systems-network-administration.restic.forget-grouping-and-tags
name: forget-grouping-and-tags
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, forget, group-by, host, tag, unsafe-allow-remove-all]
level: advanced
status: docs-checked
description: "Scope restic forget by host, tag and --group-by, keep tagged snapshots, and remove every snapshot of a group deliberately."
sources:
  - https://restic.readthedocs.io/en/stable/060_forget.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scoping forget

A retention policy is applied separately to each group of snapshots. The default `--group-by` is host and paths, so each machine and directory set gets its own daily/weekly counts.

```
restic forget --group-by paths,tags --keep-daily 7
restic forget --group-by '' --keep-daily 7     # no grouping
```

The page notes that one would normally set `--group-by` on the `backup` command to the same value.

## Restricting what is considered

- `--host name` limits the policy to one host.
- `--tag foo --keep-last 1`: only snapshots tagged `foo`.
- `--tag foo --tag bar`: either tag (OR).
- `--tag foo,bar`: both tags (AND).
- `--tag ''`: untagged snapshots.

## Protecting snapshots

`--keep-tag` keeps snapshots that match at least one tag list; a snapshot only needs to match one `--keep-*` option to
be kept. Commas inside one `--keep-tag` mean all of those tags, repeated options are ORed, and `--keep-tag ''`
matches untagged snapshots only. forget exits with an error if all snapshots in a group would be removed because none
satisfy the tag policy.

## Removing everything on purpose

restic refuses to act on an empty policy (for example `--keep-last 0`). Since restic 0.17.0, `--unsafe-allow-remove-all`
deletes all snapshots for a host, tag or path, and must always be combined with a snapshot filter:

```
restic forget --tag example --unsafe-allow-remove-all
```

## Append-only caution

On an append-only repository an attacker who can add garbage snapshots with a slightly newer timestamp (backup's
`--time` option) can make a count-based policy such as three weekly snapshots delete the legitimate ones. The docs
recommend `--keep-within` for forget policies on append-only repositories, and running forget, prune and other
maintenance from a separate, well-secured client with full access.

## Checked
Compared with the "Removing backup snapshots" page: default grouping, `--group-by ''`, `--host`, `--tag` AND/OR rules,
`--keep-tag`, empty-policy refusal, `--unsafe-allow-remove-all` and its 0.17.0 gate, and the append-only security
section. Removed: the claim about parent detection disagreeing (not on the page).
Method: docs-only read of cited pages, 2026-11-08
