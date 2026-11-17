---
id: computing-software.systems-network-administration.rclone.rclone-config-file-and-locations
name: rclone-config-file-and-locations
category: computing-software
field: systems-network-administration
product: rclone
tags: [config, config-file, rclone-conf, portable-mode, token]
level: practitioner
status: docs-checked
description: "Where the rclone config file lives, its INI format, the lookup order and how to run with a portable or in-memory config."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Remotes are stored in a single INI file. Each remote is a `[section]` whose name is the remote name; the required `type` key names the backend (see `rclone help backends`). Other keys are the backend options without the `--backend-` prefix, lowercase, with `_` for `-` (so `--mega-hard-delete` becomes `hard_delete`). Comments start with `;` or `#`.

```ini
[megaremote]
type = mega
user = you@example.com
pass = PDPcQVVjVtzFY-GTdDFozqBhTdsPg3qH
```

Passwords in the file are obscured, not encrypted. Prefer the interactive `rclone config` over hand editing, particularly for token-based backends.

## Lookup order for an existing file

1. `rclone.conf` next to the rclone executable
2. `%APPDATA%/rclone/rclone.conf` (Windows only)
3. `$XDG_CONFIG_HOME/rclone/rclone.conf`
4. `~/.config/rclone/rclone.conf`
5. `~/.rclone.conf`

`rclone config file` prints the location in use and `rclone config touch` creates an empty file if none exists. Because a `rclone.conf` beside the executable always wins, portable mode is just an executable plus an empty `rclone.conf` in a writable directory.

Setting `--config ""`, `--config notfound` or the null device keeps the configuration in memory only, which also suppresses the "Config file not found" notice when you use only on-the-fly remotes.

## Write behaviour

The file must be writable when token backends are used, because refreshed tokens are written back. Rclone writes a temporary file, mirrors permissions on Unix, renames the old file to a backup name, renames the new file into place and deletes the backup. A symlinked config path is resolved and the real file is written. Keep the file readable only by its owner; rclone tries to enforce this when it writes.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
