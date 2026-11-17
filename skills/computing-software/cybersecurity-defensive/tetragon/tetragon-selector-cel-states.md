---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-selector-cel-states
name: tetragon-selector-cel-states
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [selector-cel-states, tetragon, tracing-policy]
level: advanced
status: docs-checked
description: "Use Tetragon matchWorkloads, matchCEL, matchUserCallers and matchStates to filter by Kubernetes workload, expression, caller or state."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/selectors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon workloads, matchCEL, user callers and states

## matchWorkloads

Takes `hostSelector`, `podSelector` and `containerSelector`, like the global `spec.*Selector` fields. Fails to load outside Kubernetes.

```yaml
matchWorkloads:
  hostSelector: {}
  podSelector:
    matchExpressions:
    - key: "k8s:io.kubernetes.pod.namespace"
      operator: In
      values:
      - "kube-system"
```

## matchCEL

CEL expressions evaluated in-kernel. Arguments from `args:` are `argX` (X = array position) and `data:` items are `dataX`.

```yaml
selectors:
- matchActions:
  - action: Post
  MatchCel:
    expr: "arg1 == int32(-1) && data0 == arg0 + int32(42)"
```

Supported: `+ - * /`, `&& || !`, `== != < <= > >=`, `int32()`, `uint32()`, bitwise `and() or() xor() not() lsh() rsh()`. Shift amounts are reduced modulo the operand bit width.

## matchUserCallers (uprobes only)

Match on the user-space callstack:

```yaml
selectors:
- matchUserCallers:
  - depth: "2"
    symbol: "main"
```

`depth` is 1 to 15 or `"any"`. Instead of `symbol` use `startRange` and `endRange` offsets (mutually exclusive); `path` names the caller binary if different. Up to 5 entries, all must match. Binaries and libraries must have frame pointers. Immediate caller matching needs kernel >= 6.12 commit `cfa7f3d2c526` on amd64 and is unsupported with depth 1 on arm64; kernel >= 5.9 for binaries without buildID in their first note section.

## matchStates

Pair with the `UpdateState` action. Declare states in `spec.state` first. A missing state matches only `NotEqual`-style operators. Operators: `Equal`, `NotEqual`; `value` is a u64 integer.

```yaml
spec:
  state:
  - name: "canary"
  kprobes:
  - call: "security_file_open"
    syscall: false
    args:
    - index: 0
      type: "file"
    selectors:
    - matchArgs:
      - index: 0
        operator: Equal
        values:
        - "/run/secrets/decoy-key"
      matchActions:
      - action: UpdateState
        state:
          name: "canary"
          operator: Set
          value: "1"
  - call: "sys_connect"
    syscall: true
    selectors:
    - matchStates:
      - name: "canary"
        operator: Equal
        value: "1"
      matchActions:
      - action: Override
        argError: -1
```

The page calls this example not production-ready.

## Checked

2026-11-08. Read the selectors page in full (raw docs markdown from cilium/tetragon). Checked matchWorkloads, matchCEL, matchUserCallers and matchStates against it; no claims removed.

Method: documentation only; no commands were run.
