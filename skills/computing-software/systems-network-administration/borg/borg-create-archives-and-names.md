---
id: computing-software.systems-network-administration.borg.borg-create-archives-and-names
name: borg-create-archives-and-names
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-create, archive, placeholders, stdin, paths-from-stdin, slashdot, dry-run, stats]
level: practitioner
status: docs-checked
description: "Create Borg archives with borg create: naming and placeholders, the slashdot path hack, stdin input, external path lists, stats, listing and dry runs."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/create.html", "https://borgbackup.readthedocs.io/en/stable/usage/help.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg create

`borg create [options] REPO::ARCHIVE PATH...` stores every file found by recursing the paths. Paths are stored as given, so cd to the right directory for relative archives. Deduplication means a new archive costs almost nothing for data already stored.

Archive names must be unique and must not end in `.checkpoint` or `.checkpoint.N`. Placeholders: `{hostname}`, `{fqdn}`, `{user}`, `{now}`, `{utcnow}`, e.g. `{now:%Y-%m-%d_%H:%M:%S}`. Literal braces are doubled; in systemd units also double every `%`.

```
borg create /path/to/repo::{hostname}-{now:%Y-%m-%d} /path/to/Documents
borg create /path/to/repo::docs /mnt/disk/./docs     # stored as docs/...
find /path/to/home -size -1000k | borg create --paths-from-stdin /path/to/repo::small
```
Slashdot hack: `/./` marks the recursion root and strips the prefix before it.

Useful flags: `-n/--dry-run` (cannot combine with `--stats`), `-s/--stats` (the "This Archive" deduplicated size is the repo growth), `--list` with `--filter STATUSCHARS`, `--progress`, `--comment`, `--timestamp`. Item status flags: A added, M modified, U unchanged, C changed while backing up, E error, x excluded, - dry run.

Stdin: path `-` stores `stdin`; a failing producer can still leave a truncated archive, whereas `--content-from-command -- cmd` creates no archive on non-zero exit. Path lists: `--paths-from-stdin` or `--paths-from-command`, delimiter `--paths-delimiter`. Unreadable files give a warning and exit code 1, not a failure.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/create and usage/help (placeholders)): name rules, placeholders, slashdot hack, stdin versus --content-from-command, path-list options, status flags, error handling. Removed: nothing.

Method: documentation only; no commands were run.
