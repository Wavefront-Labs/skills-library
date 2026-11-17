---
id: computing-software.cybersecurity-defensive.falco.syscall-events-and-args
name: syscall-events-and-args
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [syscall-events, evt-type, evt-dir, evt-arg, process-context]
level: advanced
status: docs-checked
description: "Write syscall conditions with evt.type, understand deprecated evt.dir, read arguments through evt.arg and rely on proc fields after execve."
sources:
  - https://falco.org/docs/concepts/rules/conditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Conditions on syscall events typically start with an `evt.type` expression or macro, since security rules focus on one syscall at a time. Each syscall has an entry event (`>`) and an exit event (`<`), formerly selected with `evt.dir`.

Deprecation: `evt.dir` and direction were deprecated in Falco 0.42.0. Until removal, `evt.dir='>'` matches nothing, `evt.dir='<'` matches everything, with a warning. Remove references now; after removal their presence will be a rules loading error.

Arguments are read as `evt.arg.<argname>`. Exit events carry the result, for example `openat(FD fd, FD dirfd, FSRELPATH name, FLAGS32 flags, UINT32 mode, UINT32 dev)`. To catch a process opening a file to overwrite it, check for `O_TRUNC`:
`evt.type in (open, openat) and evt.arg.flags contains O_TRUNC`

Arguments do not necessarily match raw kernel parameters; Falco parses them to make rules easier.

Context: the `proc` field class describes the process and thread behind a syscall (`proc.name`, `proc.pid`, and ancestors via `proc.aname[...]`). After `execve` returns, Falco updates the process context, so `proc.*` already refers to the newly spawned process. You do not need to check the `execve` arguments for this:
`evt.type = execve and container.id != host and proc.name = bash`

Container and Kubernetes metadata come from further field classes such as `container` and `k8s`.

## Checked

2026-11-08. Read the Condition Syntax page in full; claims match.

Method: documentation only; no commands were run.
