---
id: computing-software.database-administration.dragonfly.install-from-binary
name: install-from-binary
category: computing-software
field: database-administration
product: dragonfly
tags: [binary-install, dragonfly, tarball, helpfull]
level: intro
status: docs-checked
description: "Download a prebuilt Dragonfly release, unpack it, run it with flags, and discover the full flag list with --helpfull."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/getting-started/binary.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: a Linux OS (on Mac use Docker; Windows WSL works), network access, at least 4GB of RAM, 1 CPU core, Linux kernel 4.19 or higher.

1. Download a release (Aarch64 or X86-64 tarball, or ARM64/AMD64 Debian package) from the releases page of the dragonflydb/dragonfly repository.
2. Unpack and rename:

```
tar zxf {file_name}
mv {file_name} dragonfly
```

3. Run `./dragonfly --logtostderr`.

## Flags

`--help` lists supported flags and `--helpfull` lists all of them.

Example from the docs combining several options:

```
dragonfly --logtostderr --requirepass=youshallnotpass --cache_mode=true -dbnum 1 --bind localhost --port 6379  --snapshot_cron "*/30 * * * *" --maxmemory=12gb --keys_output_limit=12288 --dbfilename dump.rdb
```

## Flag files

`--flagfile <filename>` loads flags from a file with one flag per line. Key-value flags must use `--<flag_name>=<flag_value>` with an equals sign; a space does not work.

## Checked

2026-11-04: confirmed against the Install from Binary page (prerequisites, download variants, steps, example command, flag file rule). No unconfirmed claims found.
Method: documentation only; no commands were run.
