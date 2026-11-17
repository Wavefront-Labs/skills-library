---
id: computing-software.software-engineering.deno.permissions-file-system
name: permissions-file-system
category: computing-software
field: software-engineering
product: deno
tags: [permissions, allow-read, allow-write, symlinks, file-system, module-loading]
level: practitioner
status: docs-checked
description: "Scoping --allow-read and --allow-write, which reads are allowed by default during module loading, APIs that touch disk without permission, and symlink rules."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/permissions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--allow-read[=<PATH>...]` (`-R`) and `--allow-write[=<PATH>...]` (`-W`) accept comma-separated paths covering files or directories and their subdirectories. Double a comma to include it in a path.

```sh
deno run --allow-read=foo.txt,bar.txt script.ts
deno run --allow-write=./ --deny-write=./secrets script.ts
```

Allowed without read permission during loading: files imported in a statically analyzable way (static `import`, or `import()` with a string literal), and files inside `node_modules/`. `deno info <entrypoint>` prints the full list. Dynamic imports that cannot be analyzed, and local-file Web Worker scripts, need `--allow-read`.

`localStorage`, Deno KV, `caches` and `Blob` use disk without read/write permission, so they can still consume storage. Deno's module and transpile cache also uses disk.

Symlinks: permissions are checked on the symlink's location, not its target. But links resolving into `/proc`, `/dev`, `/sys` need `--allow-all`; `/proc/**/environ` needs `--allow-env`; `/dev/null`, `/dev/zero`, `/dev/random`, `/dev/urandom` are always accessible.

Creating a symlink with `Deno.symlink()` requires unscoped `--allow-read` and `--allow-write`.

## Checked

2026-11-04. Confirmed against docs runtime/reference/permissions.md: -R/-W, comma doubling, default reads at module load, Worker and node_modules rules, APIs that use disk, symlink rules and Deno.symlink requirement.

Method: documentation only; no commands were run.
