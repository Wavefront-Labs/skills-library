---
id: computing-software.systems-network-administration.rclone.rclone-server-side-copy-and-shell-quoting
name: rclone-server-side-copy-and-shell-quoting
category: computing-software
field: systems-network-administration
product: rclone
tags: [server-side-copy, quoting, colon-in-filenames, aged-backups]
level: practitioner
status: docs-checked
description: "When rclone copies server-side, how to use it for aged backups, and how to handle shell quoting and colons in local names."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Server-side copy

Most remotes support server-side copy (the overview page lists exceptions). `rclone copy s3:oldbucket s3:newbucket` tells the server to copy objects in place instead of downloading and uploading. It applies to `sync` and `copy`, shows in the log with `-v`, and `move` may use a server-side copy plus delete when the backend lacks a native move. Remotes without support download and re-upload.

Server-side copies are attempted only when the remote names are the same. `--server-side-across-configs` allows server-side copy or move between two differently configured remotes of the same backend; it is off by default because rclone cannot easily tell whether it will work between arbitrary configurations.

This supports cheap aged backups:

```console
rclone sync --interactive remote:current-backup remote:previous-backup
rclone sync --interactive /path/to/files remote:current-backup
```

## Quoting and the shell

Shell metacharacters in remote paths must be quoted. Connection strings containing `:` and `,` need quotes: wrap in `"` and use `'` inside, which works on all operating systems. On Linux and macOS, `\`, `$` and `"` are still interpreted inside double quotes, so swap roles (single quotes outside, double inside); that form does not work on Windows.

## Colons in local names

Rclone uses `:` to mark a remote name, but it only searches for a `:` up to the first `/`. To act on a local directory called `sync:me`, give a path that has a slash before the colon, either `./sync:me` or the full absolute path.

```console
rclone sync --interactive ./sync:me remote:path
```

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
