---
id: computing-software.systems-network-administration.borg.borg-patterns-and-excludes
name: borg-patterns-and-excludes
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, exclude, patterns, patterns-from, pattern-styles, fnmatch, regex, exclude-caches, exclude-if-present]
level: practitioner
status: docs-checked
description: "Select what Borg backs up with exclude options and the pattern styles fm, sh, re, pp and pf, pattern files with R, P, plus, minus and bang prefixes, and tag-based excludes."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/help.html", "https://borgbackup.readthedocs.io/en/stable/usage/create.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg patterns and excludes

Selector styles: `fm:` (default for `--exclude`, shell wildcards), `sh:` (default for `--pattern`, like fm but `**/` matches zero or more levels), `re:` (Python regex, substring match so anchor with `^`/`$`), `pp:` (path prefix: directory and everything below), `pf:` (full-path match, fast hash lookup, ignores order).

Rules: archived paths never start with `/`, `.` or `..`. A directory pattern ending in a slash (`some/path/`) keeps the directory itself but excludes its contents; without the slash both are excluded. With `--pattern` the first match wins. Evaluation order: command-line `--pattern`/`--exclude` first, then `--patterns-from`, then `--exclude-from`.

Pattern files use line prefixes: `R path` (recursion root), `P style` (default style to end of file), `-` exclude, `!` exclude without recursing, `+` include.

```
borg create -e 'sh:**/steamapps/common/**' repo::a /
borg create --exclude 're:^home/[^/]+\.tmp/' repo::a /
borg create --pattern=+pics/2018/good --pattern=-pics/2018 repo::a pics
borg create --patterns-from patterns.lst repo::a
```

Tag excludes: `--exclude-if-present NAME` (with `--keep-exclude-tags` to keep the tag file), `--exclude-caches` (CACHEDIR.TAG), `--exclude-nodump`. Unlike tar, `--exclude '*/.bundler/gems'` is needed to match `foo/.bundler/gems`. Test with `borg create --list --dry-run`.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/help (patterns) and usage/create): pattern styles, defaults, pattern-file prefixes, evaluation order, tar difference. Removed: an imprecise trailing-slash claim, now reworded to match the page.

Method: documentation only; no commands were run.
