---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-selector-match-args
name: tetragon-selector-match-args
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [selector-match-args, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Filter Tetragon hook events on argument values with matchArgs, using index or args, operators and FileType filtering."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon matchArgs filter

Goal: emit or act on a hook only when an argument has a given value.

## Selector basics

Each hook holds up to 5 selectors. Filters in one selector are ANDed; with several selectors only the action of the first matching one applies. No action means the default `Post`.

## Pick the argument

- `index`: position within the function's arguments (zero-based).
- `args`: position within the spec's `args` list (zero-based); takes precedence over `index`. Only the `CapabilitiesGained` operator accepts more than one entry in `args`.
- `index` and `args` can be mixed.

Match files `/etc/passwd` or `/etc/shadow` on the second argument (type `file`, so paths match directly):

```yaml
selectors:
- matchArgs:
  - index: 1
    operator: "Equal"
    values:
    - "/etc/passwd"
    - "/etc/shadow"
```

Using `args` to select the second spec argument (which is function argument 0):

```yaml
- args:
  - index: 2
    type: "int"
    label: "arg0-index2"
  - index: 0
    type: "int"
    label: "arg1-index1"
  selectors:
  - matchArgs:
    - args: [1]
      operator: "Equal"
      values:
      - "0xcoffee"
```

## Operators

`Equal`, `NotEqual`, `Prefix`, `Postfix`, `Mask`, `FileType`, `NotFileType`. The `CelExpr` operator is deprecated; use `matchCEL`.

Several entries in one `matchArgs` are ANDed, e.g. fd equal to 3 and a path prefix `/etc`:

```yaml
- matchArgs:
  - index: 0
    operator: "Equal"
    values:
    - "3"
  - index: 1
    operator: "Prefix"
    values:
    - "/etc"
```

## File type filtering

`FileType` / `NotFileType` work only on `file` or `path` arguments. Values: `sock`/`socket`, `lnk`/`link`, `reg`/`regular`, `blk`/`block`, `dir`, `chr`/`char`, `fifo`/`pipe`.

```yaml
selectors:
- matchArgs:
  - index: 0
    operator: "FileType"
    values:
    - "reg"
```

## Checked

2026-11-08. Read the selectors page in full (raw docs markdown from cilium/tetragon). Checked the matchArgs section and selector basics against it; no claims removed.

Method: documentation only; no commands were run.
