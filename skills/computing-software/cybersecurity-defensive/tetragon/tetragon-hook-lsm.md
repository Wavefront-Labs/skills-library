---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-hook-lsm
name: tetragon-hook-lsm
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [hook-lsm, tetragon, tracing-policy]
level: practitioner
status: docs-checked
description: "Check that BPF LSM is available and enabled, then hook an LSM function with a Tetragon TracingPolicy lsmhooks entry."
sources:
  - "https://tetragon.io/docs/concepts/tracing-policy/hooks/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon LSM BPF hooks

Goal: instrument LSM hooks with eBPF so privileged users can implement system-wide MAC (Mandatory Access Control) and Audit policies. The hookable functions are listed in the kernel's `security/security.c`.

## Check kernel support

1. Is BPF LSM compiled in?

```shell
cat /boot/config-$(uname -r) | grep BPF_LSM
```

Supported output: `CONFIG_BPF_LSM=y`.

2. Is it enabled?

```shell
cat /sys/kernel/security/lsm
```

Example output: `bpf,lockdown,integrity,apparmor`. If `bpf` is missing, edit `/etc/default/grub`:

```
GRUB_CMDLINE_LINUX="lsm=lockdown,integrity,apparmor,bpf"
```

Then update the grub configuration and restart the system.

## Policy

Use the `lsmhooks` list with `hook` as the LSM function name, `args`, and `selectors`. This policy monitors access to `/etc/passwd` and `/etc/shadow` by the `/usr/bin/cat` executable:

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: "lsm-file-open"
spec:
  lsmhooks:
  - hook: "file_open"
    args:
      - index: 0
        type: "file"
    selectors:
    - matchBinaries:
      - operator: "In"
        values:
        - "/usr/bin/cat"
      matchArgs:
      - index: 0
        operator: "Equal"
        values:
        - "/etc/passwd"
        - "/etc/shadow"
```

Related: LSM hooks also support the `resolve` flag (kernel 5.7 and later).

## Checked

Date: 2026-11-07

Hook points page read in full (about 41 KB). Removed the Override with argError remark, which that page does not state.

Method: documentation only; no commands were run.
