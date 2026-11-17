---
id: computing-software.software-engineering.deno.security-model-principles
name: security-model-principles
category: computing-software
field: software-engineering
product: deno
tags: [security, threat-model, sandbox, static-module-graph, eval, privilege]
level: intro
status: docs-checked
description: "The principles of Deno's security model: no I/O by default, shared privilege per thread, no silent escalation, and the static module graph exemption."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno is secure by default; unlike Node, dependencies do not automatically get full I/O access. Key principles:

- No access to I/O by default (files, network, env vars, subprocesses).
- No limits on executing code at the same privilege level: `eval`, `new Function`, dynamic imports and web workers run with the caller's privilege, wherever the code comes from.
- All code on the same thread shares one privilege level; modules cannot have different levels in one thread.
- Code cannot escalate privileges without user consent (prompt or invocation flag).
- Multiple invocations of the same app can share data via caching and KV; different apps cannot see each other's data.
- The initial static module graph (static `import`s and `import()` with a string literal; local, npm, jsr, URLs) loads without consulting permissions. No `--allow-read` or `--allow-net` is needed to load it. This applies only to loading: once code runs it goes through permissions, and `import(someVariable)` is checked against `--allow-read` / `--allow-import` at runtime.

The model is enforced by the Deno runtime, not the operating system.

Evaluation can use code hosted on the network, in a local file (if read is granted), or in a string.

## Checked

2026-11-04. Confirmed against docs runtime/fundamentals/security.md: all six key principles, static graph exemption and its runtime caveat.

Method: documentation only; no commands were run.
