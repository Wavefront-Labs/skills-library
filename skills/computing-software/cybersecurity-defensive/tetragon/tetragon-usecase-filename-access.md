---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-usecase-filename-access
name: tetragon-usecase-filename-access
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [usecase-filename, tetragon, file-access, kprobe]
level: practitioner
status: docs-checked
description: "Monitor file reads, writes, mmaps and truncations by filename with Tetragon kprobes, filtered in-kernel, incl. the Linux 6.2 truncate change."
sources:
  - "https://tetragon.io/docs/use-cases/filename-access/"
  - "https://raw.githubusercontent.com/cilium/tetragon/main/examples/tracingpolicy/filename_monitoring.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon filename access monitoring

Goal: report file access by name with kernel-side filtering instead of post-filtering events.

## Hooks

- `security_file_permission`: common point for read, write, `copy_file_range`, `sendfile`, `aio` and `io_uring` calls.
- `security_mmap_file`: when a file is mapped into the address space.
- `security_path_truncate`: truncate-family calls. From Linux 6.2 it is replaced by `security_file_truncate`.

## Filtering

Declare the argument types, then match in `selectors`. Operators include `Equal` and `Prefix`:

```yaml
  - call: "security_file_permission"
    syscall: false
    args:
    - index: 0
      type: "file"
    - index: 1
      type: "int" # 0x04 is MAY_READ, 0x02 is MAY_WRITE
    selectors:
    - matchArgs:
      - index: 0
        operator: "Equal"
        values:
        - "/etc/passwd"
      - index: 1
        operator: "Equal"
        values:
        - "2"
```

The example policy `filename_monitoring.yaml` (`TracingPolicy` `file-monitoring`) hooks `security_file_permission`, `security_mmap_file` (arg 2 type `nop`) and `security_path_truncate` (arg type `path`), each with `return: true`, `returnArg` int, and `Prefix` match on `/etc/`.

## Try it

```bash
kubectl apply -f https://raw.githubusercontent.com/cilium/tetragon/main/examples/tracingpolicy/filename_monitoring.yaml
kubectl run --rm -it file-access -n default --image=busybox --restart=Never
kubectl exec -it -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact --namespace default --pod file-access
```

Running `vi /etc/passwd` gives process, read, write, truncate and exit events. In `process_kprobe` JSON, `file_arg.path` is the path, `int_arg` the operation (2 write, 4 read), and `return.int_arg` is 0 if allowed.

## Kernel 6.2+

If a policy names a hook missing from the kernel, the whole policy fails to load. Replace `security_path_truncate` with `security_file_truncate` (arg type `file`, not `path`), or list both with `ignore: callNotFound: true`. Check with `grep security_file_truncate /sys/kernel/tracing/available_filter_functions`.

## Limitation

Matching is on the filename used by the application. Access through a hard link or a different bind mount generates no event.

## Checked

2026-11-08. Read the filename access page in full and the filename_monitoring.yaml example policy; added the example policy as a source for the per-hook policy details. No claims removed.

Method: documentation only; no commands were run.
