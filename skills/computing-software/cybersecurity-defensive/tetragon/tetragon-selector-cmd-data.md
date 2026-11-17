---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-selector-cmd-data
name: tetragon-selector-cmd-data
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [selector-cmd-data, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Filter Tetragon events on process command-line arguments, current_task data fields and function return values."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon matchCmdArgs, matchData and matchReturnArgs

## Command-line arguments (matchCmdArgs)

Unlike `matchArgs` (hook arguments), this filters the arguments the current process was executed with. `index` is zero-based and excludes `argv[0]`: for `curl --output /tmp/result`, index 0 is `--output`.

```yaml
selectors:
- matchBinaries:
  - operator: In
    values:
    - "/usr/bin/curl"
  matchCmdArgs:
  - index: 0
    operator: Equal
    values:
    - "--output"
  - index: 1
    operator: Prefix
    values:
    - "/tmp/"
```

Operators: `Equal`, `NotEqual`, `Prefix`, `NotPrefix`, `Postfix`, `NotPostfix`. Up to five `matchCmdArgs` per selector, `index` 0 to 31, all must match. Only the first 256 bytes of arguments (including NUL separators) are cached; beyond that is truncated. Needs large BPF program support (normally Linux 5.3+). Arguments are user-controlled and can be reordered or obfuscated, so allow for alternate forms when enforcing.

## Data (matchData)

Filters on kernel data rather than function arguments. Each `data` entry has `index`, `source` (`current_task` or `pt_regs`), `resolve` (field of the source) and `type`. `matchData` refers to the entry by `index`. Operators are the same as for `matchArgs`, according to the data `type`.

Exclude pid 1:

```yaml
data:
- index: 0
  type: "int"
  source: "current_task"
  resolve: "pid"
selectors:
- matchData:
  - index: 0
    operator: "NotEqual"
    values:
    - "1"
```

Nested fields use `.` (e.g. `cred.uid.val`); the page filters with `GreaterThan` and `"1000"` at the LSM-called kprobe `security_bprm_committed_creds`. A string field works too (`comm` Equal `"cat"`).

## Return values (matchReturnArgs)

Filter on the call's result. Operators: `Equal`, `NotEqual`, `Prefix`, `Postfix`.

```yaml
matchReturnArgs:
- operator: "NotEqual"
  values:
  - 0
```

Use case: detect failed access to files such as `/etc/shadow`, where `openat` returns `-1` for an unprivileged user.

## Checked

2026-11-08. Read the selectors page in full (raw docs markdown from cilium/tetragon). Checked the matchCmdArgs, matchData and matchReturnArgs sections against it; no claims removed.

Method: documentation only; no commands were run.
