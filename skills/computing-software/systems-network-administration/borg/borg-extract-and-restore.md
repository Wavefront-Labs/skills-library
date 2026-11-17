---
id: computing-software.systems-network-administration.borg.borg-extract-and-restore
name: borg-extract-and-restore
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-extract, restore, strip-components, dry-run, stdout, sparse, numeric-ids]
level: practitioner
status: docs-checked
description: "Restore from Borg with borg extract: whole archive or paths, pattern styles, dry-run verification, strip-components, stdout for raw devices, and metadata flags."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/extract.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg extract

`borg extract [options] REPO::ARCHIVE [PATH...]` always writes into the current working directory, so cd to the target first. With no PATH the whole archive is restored. PATH arguments default to literal prefix matches (`pp:`); use `sh:` or `fm:` for wildcards. Archive paths are relative, e.g. `home/user/docs`.

```
cd /path/to/restore
borg extract --list /path/to/repo::archive
borg extract /path/to/repo::archive home/user/docs
borg extract /path/to/repo::archive 'sh:**/*.c'
borg extract --dry-run --list /path/to/repo::archive
borg extract --stdout /path/to/repo::raw-disk | dd of=/dev/sdX bs=10M
```

`--dry-run` does everything except write: it reads, verifies hashes and MACs, decrypts and decompresses, so it is a practical restore test. Other options: `--strip-components N` (shorter paths are silently skipped), `-e/--exclude`, `--pattern`, `--numeric-ids`, `--noflags`, `--noacls`, `--noxattrs`, `--sparse` (holes for all-zero chunks), `--stdout`. If parent directories are not extracted, their owner, group and permissions cannot be restored. `--progress` makes an extra metadata pass and can be slower. The raw device must not be in use or mounted.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/extract): pp: default path matching, current-directory behaviour, --dry-run scope, option list, parent metadata caveat. Removed: nothing.

Method: documentation only; no commands were run.
