---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-usecase-process-credentials
name: tetragon-usecase-process-credentials
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [usecase-creds, tetragon, process-credentials, privilege-escalation]
level: practitioner
status: docs-checked
description: "Monitor Linux process credential changes with Tetragon at the syscall layer or, preferably, the kernel commit_creds layer."
sources:
  - "https://tetragon.io/docs/use-cases/linux-process-credentials/"
  - "https://tetragon.io/docs/use-cases/linux-process-credentials/monitor-changes-at-kernel/"
  - "https://tetragon.io/docs/use-cases/linux-process-credentials/syscalls-monitoring/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor Linux process credentials with Tetragon

Goal: find programs running with, or gaining, high privileges (for example via sudo or a setuid binary). Credentials are UIDs/GIDs (real, effective, saved, fs), supplementary groups, capability sets (permitted, inheritable, effective, bounding), securebits and LSM state. Tetragon exposes them as a `process_credentials` object. Changes can be monitored at the syscall layer or at the kernel layer; the kernel layer is generally better.

## Kernel layer

Policy: `process-creds-installed.yaml` in `examples/tracingpolicy/process-credentials/`. It hooks when credentials are installed.

```shell
kubectl apply -f https://raw.githubusercontent.com/cilium/tetragon/main/examples/tracingpolicy/process-credentials/process-creds-installed.yaml
kubectl exec -it -n kube-system ds/tetragon -c tetragon -- tetra getevents
```

Answers: which process or container changes its own UIDs/GIDs or capabilities, and in which user namespace. Running a setuid binary as a non-root user gives a `process_kprobe` event with `function_name` `commit_creds` and `process_credentials_arg`: the new uid/gid/euid/egid/suid/sgid/fsuid/fsgid, `caps` (permitted, effective) and `user_ns`.

Advantages over syscall monitoring: not vulnerable to user space argument tampering, shows the full new credentials, has full context including the user namespace, and is a catch-all for every kernel path that manipulates credentials. Disadvantage: possibly many events, so filter.

## Syscall layer

Policy: `process.credentials.changes.at.syscalls.yaml` (same directory), hooking `setuid`, `setgid`, `setfsuid`, `setfsgid`, `setreuid`, `setregid`, `setresuid`, `setresgid`.

```shell
kubectl apply -f https://raw.githubusercontent.com/cilium/tetragon/main/examples/tracingpolicy/process-credentials/process.credentials.changes.at.syscalls.yaml
```

Running `su root` in the xwing pod gives events with `function_name` `__x64_sys_setgid` / `__x64_sys_setuid` and `int_arg` `0` (the requested id).

Disable either policy with `kubectl delete -f` on its URL.

## Checked

2026-11-08. Read the process credentials index and its two subpages (kernel layer, syscall layer) in full; added the subpages as sources because the policy details come from them. No claims removed.

Method: documentation only; no commands were run.
