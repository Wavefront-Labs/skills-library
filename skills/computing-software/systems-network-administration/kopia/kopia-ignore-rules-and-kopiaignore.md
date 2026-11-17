---
id: computing-software.systems-network-administration.kopia.kopia-ignore-rules-and-kopiaignore
name: kopia-ignore-rules-and-kopiaignore
category: computing-software
field: systems-network-administration
product: kopia
tags: [kopiaignore, ignore-rules, exclusions, patterns, add-ignore]
level: practitioner
status: docs-checked
description: "Exclude files from Kopia snapshots with .kopiaignore files and policy ignore rules, including pattern operators and Windows slash rules."
sources: ["https://kopia.io/docs/advanced/kopiaignore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kopia uses pattern rules, one per line, to omit files and folders. A `.kopiaignore` file in a directory applies to that directory and below; rules can also live in the global or per-source policy (`kopia policy set --add-ignore ...`) or be read from a file path named in the policy. On Windows always use forward slashes in rules, such as `Documents/cache/*`, even in policies; backslashes copied from Windows paths are not supported.

## Operators

- `#` comment
- `!` negates a rule
- `*` zero or more characters, `**` zero or more directories
- `?` exactly one character
- `[0-9]`, `[a-z]`, `[A-Z]`, `[abc]` character sets
- a leading `/` anchors the rule to the root directory of that `.kopiaignore`

## Examples

```text
# ignore all .dat files
*.dat
# ignore everything in the root logs directory only
/logs/*
# ignore tmp.db wherever it is
tmp.db
```

`logs` matches every file or directory named logs at any depth, `/logs` only the one at the root, `*.db*` matches `.db` followed by anything (such as `tmp.dba`), `**/logs/**` all logs directories below, and `chapters/**/*.log` all `.log` files beneath `chapters`. A rule like `*.*` matches everything and `!*.*` matches nothing.

Mistyped rules silently produce incomplete snapshots, so test a new ignore file by taking a snapshot and checking what is present in it before relying on it.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Kopiaignore page (default file, policy rules, Windows forward-slash note, operator table, example rules, incomplete-snapshot warning).
Method: documentation only; no commands were run.
