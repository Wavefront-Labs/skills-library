---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-selector-binaries
name: tetragon-selector-binaries
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [selector-binaries, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Filter Tetragon hooks by host PID, binary path and parent binary path, including followChildren and shebang script behaviour."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon matchPIDs, matchBinaries and matchParentBinaries

## matchPIDs

Filters on the host PID. Operators: `In`, `NotIn`. Set `followForks`; `isNamespacePID: true` compares the PID inside its namespace. Detect `kubectl exec` in a container, since those processes are not children of PID 1:

```yaml
- matchPIDs:
  - operator: NotIn
    followForks: false
    isNamespacePID: true
    values:
    - 1
```

## matchBinaries

Filters on the binary path. Operators: `In`, `NotIn`, `Prefix`, `NotPrefix`, `Postfix`, `NotPostfix`. `values` is a list of strings.

```yaml
- matchBinaries:
  - operator: "In"
    values:
    - "/usr/bin/cat"
    - "/usr/bin/tail"
```

`followChildren: true` also applies the filter to children of matching processes (e.g. `/usr/sbin/sshd`). Limits: children created before the policy was installed are not matched; at most 64 `matchBinaries` sections with `followChildren: true`; operator must be `In` or `NotIn`.

```yaml
- matchBinaries:
  - operator: "In"
    values:
    - "/usr/sbin/sshd"
    followChildren: true
```

### Scripts with shebangs

`matchBinaries` matches the interpreter, not the script path. Matching `/opt/scripts/my_script.py` will not work; match `/usr/bin/python3` instead.

## matchParentBinaries

Same shape and operators as `matchBinaries`, applied to the parent's binary. It needs the BPF map `parents_map` enabled with the option `--parents-map-enabled`, which adds memory overhead.

```yaml
- matchParentBinaries:
  - operator: "In"
    values:
    - "/usr/bin/bash"
    - "/usr/bin/sh"
    - "/usr/bin/zsh"
  matchBinaries:
  - operator: "In"
    values:
    - "/usr/bin/cat"
```

This matches `cat` run from an interactive shell. With `followChildren: true` any direct or transitive parent matches; again children created before install are not matched, at most 64 such sections, and only `In`/`NotIn` are supported.

## Checked

2026-11-08. Read the selectors page in full (raw docs markdown from cilium/tetragon). Checked matchPIDs, matchBinaries and matchParentBinaries sections against it; no claims removed.

Method: documentation only; no commands were run.
