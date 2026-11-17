---
id: computing-software.systems-network-administration.syncthing.stignore-patterns
name: stignore-patterns
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, stignore, ignore-patterns, glob]
level: intro
status: docs-checked
description: "Write .stignore patterns for Syncthing, covering wildcards, rooted paths and first-match-wins ordering."
sources: ["https://docs.syncthing.net/users/ignoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .stignore pattern basics

## Where it lives
`.stignore` sits in the root of the synced folder, must be UTF-8, and is never synced itself. Files elsewhere are not applied. All patterns are relative to the folder root.

## Matching rules
The first matching pattern decides the outcome, so order matters.
- A plain name such as `foo` matches `foo`, `subdir/foo` and any directory called `foo`.
- `*` matches within one path segment and never crosses `/`.
- `**` also crosses directory separators.
- `?` matches one character that is not `/`.
- `[a-z]` is a character range and `{banana,pineapple}` is a set of alternatives.
- A leading `/` anchors the pattern to the folder root, so `/foo` does not match `subdir/foo`.
- Lines starting with `//` are comments. Leading and trailing spaces are trimmed.

```
// build output
/build
*.tmp
node_modules
```

## Directory trailing slash
A pattern ending with `/` matches the contents of a directory but not the directory itself. Leave the slash off to match both.

## Gotcha
Ignored files can stop an otherwise empty directory from being removed. Use the `(?d)` prefix for junk files you are happy to have deleted in that case.

## Checked

2026-11-09. Confirmed against the Syncthing Ignoring Files page (users/ignoring, raw rst from syncthing/docs): location and UTF-8 rule, never synced, first-match-wins, plain name, *, **, ?, [], {}, leading /, // comments, space trimming, trailing-slash note, (?d) deletion note. Removed: nothing.

Method: documentation only; no commands were run.
