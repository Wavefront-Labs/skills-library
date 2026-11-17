---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-hook-uprobes
name: tetragon-hook-uprobes
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [hook-uprobe, tetragon, tracing-policy]
level: advanced
status: docs-checked
description: "Hook user-space functions and USDT probes in a Tetragon TracingPolicy, with selectors and binary digest verification."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon uprobes and USDTs

Goal: hook any user-space function (uprobe) or a USDT probe. Uprobes are tied to the binary version, so may not be portable across versions or architectures.

## Uprobe

Give the executable or library `path` and the `symbols`. Find symbols with `objdump`, `nm` or `readelf`, e.g. `nm -D /bin/bash | grep readline` (type `T` means the text section).

```yaml
spec:
  uprobes:
  - path: "/bin/bash"
    symbols:
    - "readline"
```

Uprobes support the full set of selectors (`matchArgs`, `matchReturnArgs`, `matchBinaries`, `matchNamespaces`, `matchCapabilities`...). Report only `readline` returns starting with "sudo":

```yaml
  uprobes:
  - path: "/bin/bash"
    symbols:
    - "readline"
    return: true
    returnArg:
      index: 0
      type: "string"
    selectors:
    - matchBinaries:
      - operator: "In"
        values:
        - "/bin/bash"
        - "/usr/bin/bash"
      matchReturnArgs:
      - index: 0
        operator: "Prefix"
        values:
        - "sudo"
```

## Binary digest verification

Restrict a policy to specific builds with `binaryDigests` entries of form `<digest type>:<digest>`. Types: sha1, sha256, sha384, sha512, build-id (ELF `.note.gnu.build-id`). If no digest matches, Tetragon does not attach. With `ignore.digestVerificationFailure: true` the hook is skipped and the policy is partially loaded (state `TP_STATE_PARTIALLY_ENABLED`, per-hook status in `TracingPolicyStatus`); otherwise the whole policy is rejected.

The kernel tracks the target by inode. If a binary is updated in place (e.g. `cp`) the inode is kept and the uprobe keeps firing; installers should unlink first. To apply the policy to a new version after installation, reload the policy.

## USDT

List probes with `readelf -n <binary>` (stapsdt notes), or generate a policy: `tetra tracingpolicy generate usdts --binary <path>`. Each probe is defined by `path`, `provider` and `name` (under `spec.usdts`). Up to 5 arguments per probe (a Tetragon limitation), defined like other probe args.

## Checked

Date: 2026-11-07

Hook points page read in full (about 41 KB); every claim matched, no change.

Method: documentation only; no commands were run.
