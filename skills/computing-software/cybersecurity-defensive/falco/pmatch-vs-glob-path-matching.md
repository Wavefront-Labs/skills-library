---
id: computing-software.cybersecurity-defensive.falco.pmatch-vs-glob-path-matching
name: pmatch-vs-glob-path-matching
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [pmatch, glob, path-prefix, fd-name, filesystem-rules]
level: practitioner
status: docs-checked
description: "Match file paths with pmatch prefix semantics instead of glob full-match, including wildcard behaviour and a prefix-boundary example."
sources:
  - https://falco.org/docs/concepts/rules/conditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pmatch` compares a path against a set of file or directory prefixes, for fields like `fd.name`, `evt.rawarg.path` or `fs.path.name`.

`fd.name pmatch (/var/run, /var/spool, /etc, /boot)` is true for `/var/spool/maillog` and false for `/opt/data/file.txt`. Prefixes respect path components: `fd.name pmatch (/tmp/hello)` is true for `/tmp/hello` and `/tmp/hello/world` but not `/tmp/hello_world`.

Internally `pmatch` builds a tree from the right-hand paths and walks the left-hand path components, returning true at the first matching leaf.
Wildcards are allowed and the match remains a prefix match: `fd.name pmatch (/var/*/*.txt, /etc, /boot)`. Wildcards do not cross directory separators.

The difference from `glob`: `glob` must match the whole string, `pmatch` succeeds if the path starts with a given prefix. So `fd.name pmatch (/var/*)` matches `/var/run/file.txt`, while `fd.name glob /var/*` does not.

Gotcha: `pmatch` prefixes are whole path components, so `/tmp/hello` does not cover `/tmp/hello_world`. List each directory or file prefix you need explicitly, or use `startswith` or `glob` for partial-name matching.

## Checked

2026-11-08. Read the cited conditions page in full. Fixed the glob example path and removed the unsupported scaling claim for pmatch versus startswith.

Method: documentation only; no commands were run.
