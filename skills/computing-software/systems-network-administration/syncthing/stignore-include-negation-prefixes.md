---
id: computing-software.systems-network-administration.syncthing.stignore-include-negation-prefixes
name: stignore-include-negation-prefixes
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, stignore, negation, include]
level: practitioner
status: docs-checked
description: "Use .stignore #include, ! negation and the (?i) and (?d) prefixes correctly, including the scan cost of negated patterns."
sources: ["https://docs.syncthing.net/users/ignoring.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# .stignore include, negation and prefixes

## Include
`#include more-patterns.txt` loads patterns from another file. It is an error if the file is missing or included twice. Patterns inside stay relative to the folder root. Nested `#include` paths are relative to the directory of the loaded file. The included file can be one that syncs between devices, even though `.stignore` itself does not.

## Negation
`!pattern` re-includes matches that a later, more general pattern would ignore. Because the first match wins, put it before the general rule:

```
!frobble
!quuz
foo
*2
qu*
```

## Scan cost
Negated patterns that could match below the folder root force Syncthing to traverse otherwise ignored directories, and the watcher will watch them. Directories ignored before the first negation are skipped safely. Top-level rooted negations such as `!/baz` followed by `*` do not cause this.

## Prefixes
- `(?i)` makes matching case-insensitive, for example `(?i)my pictures`. On macOS and Windows matching is always case-insensitive.
- `(?d)` allows removal of matching files when they block deleting a directory, for example `(?d).DS_Store`.
- Prefixes combine in any order, such as `(?d)(?i)`, but not inside one pair like `(?di)`.

## Defaults
Default patterns can be configured (since 1.19.0). They are written to a new `.stignore` when a folder is auto-accepted from a remote device and none exists yet.

## Checked

2026-11-09. Confirmed against the Syncthing Ignoring Files page (users/ignoring, raw rst from syncthing/docs): #include errors and relative-path rules, ! negation and first-match ordering, traversal cost and the rooted-pattern exception, (?i) and (?d) behaviour and combining rule, the example pattern set, default patterns (1.19.0). Removed: nothing; added the 1.19.0 version and the "none exists yet" condition from the page.

Method: documentation only; no commands were run.
