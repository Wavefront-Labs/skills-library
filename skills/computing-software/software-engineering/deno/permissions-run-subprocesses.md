---
id: computing-software.software-engineering.deno.permissions-run-subprocesses
name: permissions-run-subprocesses
category: computing-software
field: software-engineering
product: deno
tags: [permissions, allow-run, subprocess, privilege-escalation, ld-preload, allow-scripts]
level: advanced
status: docs-checked
description: "Scoping --allow-run to named executables, why it invalidates the sandbox, LD_* and DYLD_* env restrictions, self-signals, and npm post-install scripts."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/permissions.md
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Subprocesses are denied by default. Child processes run independently of the parent's permissions, so `--allow-run` essentially invalidates the sandbox. Limit it to named executables:

```sh
deno run --allow-run="curl,whoami" script.ts
deno run --allow-run --deny-run="whoami,ps" script.ts
```

Avoid `--allow-run=deno` unless the parent has `--allow-all`: a spawned `deno` can run with full permissions. Also avoid giving write access to directories holding allowed executables, since the binary could be overwritten.

Spawning with an environment variable starting `LD_` (e.g. `LD_PRELOAD`) or `DYLD_` requires the unscoped `--allow-run`; a scoped list like `--allow-run=curl` is not enough. Simplest fix: spawn with the variable unset.

```ts
new Deno.Command("echo", {
  args: ["hello"],
  env: { LD_PRELOAD: "/path/to/lib.so" },
}).outputSync();
```

Signalling your own process (`Deno.kill(Deno.pid, ...)`, `process.kill(process.pid, ...)`) needs no `--allow-run`.

npm packages' post-install scripts do not run by default (e.g. with `deno install`); `--allow-scripts` runs them as subprocesses.

## Checked

2026-11-04. Confirmed against docs runtime/reference/permissions.md and runtime/fundamentals/security.md: scoped --allow-run, sandbox bypass, --allow-run=deno warning, write-access-to-executables warning, LD_/DYLD_ rule, self-signal exemption, --allow-scripts.

Method: documentation only; no commands were run.
