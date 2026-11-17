---
id: computing-software.cloud-infrastructure-engineering.zot.retention-policies
name: retention-policies
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, retention, keep-tags, delete-untagged, pulled-within, most-recently-pushed-count]
level: advanced
status: docs-checked
description: "Write Zot storage.retention policies: keepTags, keepUntagged, deleteUntagged, delay and dryRun, matching semantics, and the default-policy warning."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/retention.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policies go in `storage.retention.policies`. With none, untagged manifests are deleted unless an index or artifact references them, and all tags are kept.

Attributes: `dryRun` (default false), `delay` (defaults to `gcDelay`), and per policy `repositories` (globs; `*` first level, `**` recursive), `deleteReferrers` (false), `deleteUntagged` (true), `keepUntagged` (`mostRecentlyPushedCount`, `mostRecentlyPulledCount`, `pushedWithin`, `pulledWithin`) and `keepTags` (list with `patterns` regex, the same four counts and windows, for example `24h`).

Semantics:
- Runs per repository; the first matching policy applies; a repo matching none keeps all tags.
- If `keepTags` is defined, tags not matching are removed. An empty `keepTags` list retains all.
- Entries in `keepTags` combine with OR. Within one entry: `patterns` AND (any one of the activity rules). A regex alone retains all matches.
- `deleteUntagged` is the master switch; `keepUntagged` protects untagged manifests meeting one rule, useful for digest-only pull-through cache entries.
- Without metadata statistics, GC falls back to delay-based cleanup.
- Count ties break by tag name, then digest, ascending.
- From v2.1.23 removing a manifest's last tag keeps its activity statistics until pruned.

Warning: end with a default `keepTags` policy whose `patterns` match `.*`, or unmatched tags are deleted.

## Checked

2026-11-04. Read against the zot retention article; every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
