---
id: computing-software.systems-network-administration.restic.files-from-lists
name: files-from-lists
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, files-from, files-from-raw, files-from-verbatim, include, find]
level: practitioner
status: docs-checked
description: "Back up an explicit list of paths with --files-from, --files-from-verbatim and --files-from-raw, including NUL-separated lists from find -print0."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Including files from a list

Three flags read the list of items to back up:

- `--files-from file`: lines are patterns. Special characters are expanded as in Go `filepath.Match`; blank lines and lines starting with `#` are ignored and surrounding whitespace is trimmed. UTF-8, or UTF-16 with BOM.
- `--files-from-verbatim file`: lines are literal paths, no expansion.
- `--files-from-raw file`: paths are NUL-terminated, matching `find -print0` output, so unusual file names (including newlines) are safe.

A `-` as the file name reads the list from stdin for all three.

```
restic -r /srv/restic-repo backup --files-from /tmp/files_to_backup /tmp/some_additional_file
find /path/to/data -name '*.conf' -print0 > /tmp/files_to_backup
restic -r /srv/restic-repo backup --files-from-raw /tmp/files_to_backup
```

You can mix a list with extra paths on the command line, as in the first example.

## When to pick which

- Hand-written lists with wildcards: `--files-from`.
- Generated lists where a path might contain `*`, `[` or leading spaces: `--files-from-verbatim` or, better, `--files-from-raw`.

Paths may be absolute or relative to the working directory. Pair a list with `--exclude` flags if some matches should be skipped, and check the result with `--dry-run`.

## Checked

Checked 2026-11-08 against the restic Backing up page (040_backup), read in full. Confirmed: the three flags and their parsing rules, UTF-8 or UTF-16 with BOM, - for stdin, find -print0 with --files-from-raw, mixing lists with extra paths, --dry-run and --exclude. Removed: the statement that ** is unsupported in --files-from and the environment-variable remark, which the page does not state.

Method: documentation only; no commands were run.
