---
id: computing-software.software-engineering.deno.permissions-runtime-api
name: permissions-runtime-api
category: computing-software
field: software-engineering
product: deno
tags: [permissions, deno-permissions, query, request, revoke, not-capable]
level: practitioner
status: docs-checked
description: "Inspect and shrink a program's own permissions with Deno.permissions.query, request and revoke, and catch Deno.errors.NotCapable."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A program can inspect and tighten its own permissions through `Deno.permissions`:

- `Deno.permissions.query` reports whether a permission is granted.
- `Deno.permissions.request` prompts for one on demand.
- `Deno.permissions.revoke` downgrades a granted permission back to the prompt state.

Dropping permissions after startup shrinks the attack surface available to the rest of your code, including dependencies:

```ts
// Read a config file at startup, then give up read access.
const config = JSON.parse(await Deno.readTextFile("./config.json"));
await Deno.permissions.revoke({ name: "read" });

// Later reads now have to prompt again, and fail outright under --no-prompt.
```

Refused operations throw `NotCapable`; handle it gracefully:

```ts
try {
  await Deno.readTextFile("/etc/hosts");
} catch (err) {
  if (err instanceof Deno.errors.NotCapable) {
    console.error("Missing read permission, run again with --allow-read");
  }
}
```

## Checked

2026-11-04. Confirmed against docs runtime/fundamentals/security.md: Deno.permissions query/request/revoke, revoke example, NotCapable handling.

Method: documentation only; no commands were run.
