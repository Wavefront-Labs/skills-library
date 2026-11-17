---
id: computing-software.systems-network-administration.rclone.rclone-filtering-files-from-and-age-size
name: rclone-filtering-files-from-and-age-size
category: computing-software
field: systems-network-administration
product: rclone
tags: [files-from, min-size, max-age, min-age, exclude-if-present, directory-filters]
level: practitioner
status: docs-checked
description: "Filter by explicit file lists, age and size, directory rules and marker files, and how they interact with other filter flags."
sources: ["https://rclone.org/filtering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Directory rules

A rule ending in `/` is a directory rule, for example `/directory/subdirectory/`. Rclone infers directory rules from file rules (`/a/*.jpg` implies `/a/`) so it can skip recursion into excluded directories, which saves listing time. `rclone ls remote: --include /directory/` matches nothing, because `--include` implies `- **` and the directory pattern only prunes traversal. In a pattern list such as `{dir1/**,dir2/**}`, an item containing `/` or `**` stops rclone inferring directory rules, so with `--create-empty-src-dirs` an empty `dir3` would still be created; write `{dir1,dir2}/**` or two separate `--include` flags instead.

Recursion pruning applies when the source lacks `ListR` (local, sftp, OneDrive, WebDAV), or on `ListR` remotes when the command is not naturally recursive and `--fast-list` is not used. `ls`, `lsf -R` and `size` are naturally recursive; `sync`, `copy` and `move` are not.

`--exclude-if-present NAME` excludes any directory containing a file called NAME and takes precedence over other directory rules.

## File lists

`--files-from file` reads names one per line (use `-` for stdin), relative to the source root. Variants: `--files-from-raw` (no comment or whitespace processing) and `--files-from0` (NUL separated, for `find -print0`). Missing names do not cause errors. These flags override and cannot be combined with include, exclude or filter flags. With `--no-traverse` and a short list, rclone fetches each file directly rather than listing.

```console
find /path -print0 | rclone copy --files-from0 - / remote:path
```

## Age and size

`--min-size`, `--max-size`, `--min-age`, `--max-age` take suffixes (`50k`, `2d`) and apply to files only, not directories. For example `rclone ls remote: --max-age 2d` lists files modified within two days.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
