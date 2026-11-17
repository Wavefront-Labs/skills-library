---
id: computing-software.cybersecurity-defensive.falco.adaptive-syscall-selection
name: adaptive-syscall-selection
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [base-syscalls, custom-set, repair, syscall-selection, performance-tuning]
level: advanced
status: docs-checked
description: "Tune which syscalls Falco traces with base_syscalls.custom_set, repair and all, including recommended sets and exclusion notation."
sources:
  - https://falco.org/docs/concepts/event-sources/kernel/tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Falco traces syscalls required by enabled rules plus a fixed set that keeps its internal state engine correct:

```yaml
base_syscalls.custom_set: []
base_syscalls.repair: false
base_syscalls.all: false
```

Options:
- `base_syscalls.all: true` monitors every supported event, including normally ignored ones such as `write`. Costly in resources.
- `base_syscalls.custom_set` adds syscalls you list on top of rule-required ones. Misconfiguration can give incomplete events or break tracing. Negative notation `"!syscall_name"` excludes one.
- `base_syscalls.repair: true` lets Falco pick the minimal set of extra syscalls needed for state engine integrity. Recommended for most cases.

Recommended `custom_set` values:
- Process monitoring: `[clone, clone3, fork, vfork, execve, execveat, close]`
- Networking: add `socket, bind, getsockopt` to that set.
- Accurate UID/GID tracking: also add `[setresuid, setsid, setuid, setgid, setpgid, setresgid, capset, chdir, chroot, fchdir]`.

Commonly: `base_syscalls.repair: true`, `custom_set: []`, `all: false`.

Inspect what is ignored by default with `falco -i`. Events marked `EF_OLD_VERSION` are not generated live but may appear in `.scap` files.

Gotcha: the defaults do not suffice for spawned-process-only monitoring on constrained hosts; use `repair`.

## Checked

2026-11-08. Read the Advanced Performance Tuning page in full; claims match.

Method: documentation only; no commands were run.
