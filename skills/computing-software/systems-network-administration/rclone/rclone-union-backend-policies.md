---
id: computing-software.systems-network-administration.rclone.rclone-union-backend-policies
name: rclone-union-backend-policies
category: computing-software
field: systems-network-administration
product: rclone
tags: [union, upstreams, create-policy, action-policy, search-policy, writeback, mergerfs]
level: advanced
status: docs-checked
description: "Merge remotes with the union backend: upstream tags, the action, create and search policy classes and writeback caching."
sources: ["https://rclone.org/union/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The union backend joins several remotes into one view. `upstreams` is a space-separated list of remotes or local paths, optionally with subpaths, and each can be tagged `:ro` (read only), `:nc` (no create) or `:writeback`. Quote entries containing spaces: `"upstreama:test/space:ro dir"`. Paths are passed through unchanged, so `union:desktop` equals `mydrive:private/backup/desktop` when that is the upstream.

## Policy classes

Behaviour follows three categories, each assigned a policy (inspired by mergerfs):

- action (default `epall`): changes to existing files: move, rmdir, delete, purge, and copy or sync as destination for existing files.
- create (default `epmfs`): new files: copy or sync to a destination where the file does not exist.
- search (default `ff`): ls, lsd, lsl, cat, md5sum, sha1sum, and copy or sync as source.

Policies starting with `ep` are path preserving: only upstreams where the relative path already exists are considered. Others create paths as needed. Policy names: `all`, `epall`, `epff`, `eplfs`, `eplus`, `eplno`, `epmfs`, `eprand`, `ff`, `lfs`, `lus`, `lno`, `mfs`, `newest`, `rand`. Policies using free space (lfs, mfs), used space (lus) or object counts (lno) need the upstream to report that quota field; check with `rclone about remote:`. `cache_time` (default 120 seconds) caches usage for path-preserving policies.

Action policies skip read-only upstreams; create policies skip read-only and no-create ones; if all are filtered you get an error. Using `rand` on delete with several copies gives odd results.

## Writeback

Tag one upstream `:writeback` to build a simple cache:

```ini
[union]
type = union
action_policy = all
create_policy = all
search_policy = ff
upstreams = /local:writeback remote:dir
```

Files read from `remote:dir` are first copied into `/local` (with `--multi-thread-streams` if set) and writes go to both. Use only one writeback tag. Rclone never expires or sizes the writeback remote; you must manage that.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
