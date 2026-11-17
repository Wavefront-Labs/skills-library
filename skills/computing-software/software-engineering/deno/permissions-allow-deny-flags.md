---
id: computing-software.software-engineering.deno.permissions-allow-deny-flags
name: permissions-allow-deny-flags
category: computing-software
field: software-engineering
product: deno
tags: [permissions, allow-flags, deny-flags, allow-all, no-prompt, sandbox]
level: intro
status: docs-checked
description: "How Deno's sandbox denies I/O by default, the --allow-*/--deny-* flag families, deny precedence, prompts and --no-prompt, and why -A disables the sandbox."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/permissions.md
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno code has no access to sensitive I/O unless granted. Flags: `--allow-read`, `--allow-write`, `--allow-net`, `--allow-env`, `--allow-run`, `--allow-sys`, `--allow-ffi`, `--allow-import`.

Most take a scoped list so a program gets only what it needs:

```sh
deno run --allow-net=example.com main.ts
```

A bare `--allow-net` grants the whole category.

`--deny-*` flags take precedence over allow flags, so grant broadly and carve out exceptions:

```sh
deno run --allow-read=/etc --deny-read=/etc/hosts script.ts
```

A deny flag with no value, such as `deno run --deny-read script.ts`, denies everything in the category and disables prompts for it.

A refused operation throws `Deno.errors.NotCapable`; catch it to handle missing permissions gracefully.

If stdout is a terminal and no flag was passed, Deno prompts (y/n/A). Prompts are not shown when stdout/stderr are not a TTY or when `--no-prompt` is passed.

`-A` / `--allow-all` grants everything, disables the sandbox entirely, and has the same security properties as Node.js (none). Use it sparingly.

Permissions can also be stored in deno.json (see the `permissions` section of the configuration reference).

## Checked

2026-11-04. Confirmed against docs runtime/reference/permissions.md and runtime/fundamentals/security.md: flag families, deny precedence, scoped vs bare flags, NotCapable, y/n/A prompt, --no-prompt and non-TTY, -A and --allow-all security note, permissions in deno.json.

Method: documentation only; no commands were run.
