---
id: computing-software.systems-network-administration.rclone.rclone-combine-and-alias-remotes
name: rclone-combine-and-alias-remotes
category: computing-software
field: systems-network-administration
product: rclone
tags: [combine, alias, upstreams, synthetic-directories]
level: practitioner
status: docs-checked
description: "Build a synthetic directory tree from several remotes with combine, and give a remote a shorter name with alias."
sources: ["https://rclone.org/combine/", "https://rclone.org/alias/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## combine

The `combine` backend joins remotes into one directory tree. Its `upstreams` option is a space-separated list of `dir=remote:path` entries, where the part before `=` is the directory name in the combined tree and the part after is the remote.

```ini
[combined]
type = combine
upstreams = images=s3:imagesbucket files=drive:important/files
```

With that config `rclone tree combined:` shows `images` and `files` as top-level directories, each backed by a different provider. Quote entries with spaces: `"dir=remote:path with space"`. For Google Drive, `rclone backend -o config drives drive:` prints a combine config covering all the shared drives you have access to.

## alias

An `alias` remote gives a new name to another remote or local path, which may be as deep as required. If `backup` is an alias for `mydrive:private/backup`, then `rclone mkdir backup:desktop` is exactly `rclone mkdir mydrive:private/backup/desktop`. There is no special handling for `..` segments, so `backup:../desktop` becomes `mydrive:private/backup/../desktop`. An empty path is not allowed; to alias the current directory use `.`. The target can be a connection string.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off). Removed or corrected claims the pages did not confirm.

Method: documentation only; no commands were run.
