---
id: computing-software.software-engineering.deno.permissions-ffi-and-import
name: permissions-ffi-and-import
category: computing-software
field: software-engineering
product: deno
tags: [permissions, allow-ffi, allow-import, deny-import, napi, remote-imports]
level: advanced
status: docs-checked
description: "Gating native libraries with --allow-ffi and remote code with --allow-import, including the default trusted hosts, overriding them, and HTTPS-only rule."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/permissions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
FFI: `Deno.dlopen` and Node-API (NAPI) native addons need `--allow-ffi[=<PATH>...]`. Loaded libraries are not sandboxed, so use with extreme caution.

```sh
deno run --allow-ffi=./libfoo.so script.ts
deno run --allow-ffi --deny-ffi=./libfoo.so script.ts
```

Imports: `--allow-import[=<HOST>...]` governs importing code from `http:`/`https:` URLs, for static and dynamic imports and `new Worker()`.

```sh
deno run --allow-import=example.com main.ts
```

Default allowed hosts: `deno.land`, `jsr.io`, `esm.sh`, `raw.esm.sh`, `cdn.jsdelivr.net`, `raw.githubusercontent.com`, `gist.githubusercontent.com`. Only HTTPS is allowed.

The allow list applies by default to static imports, and to dynamic imports if `--allow-import` is specified. A bare `deno run --allow-import main.ts` permits dynamic imports from those defaults. Specifying a list overrides the default hosts.

Block hosts even when otherwise allowed (deny wins):

```sh
deno run --deny-import=esm.sh main.ts
```

A Web Worker loaded from an `https:` URL requires `--allow-import`; `data:` and `blob:` URLs need no permission.

## Checked

2026-11-04. Confirmed against docs runtime/reference/permissions.md: --allow-ffi for Deno.dlopen and NAPI, --allow-import semantics, default hosts, HTTPS-only, override and deny behaviour, Worker URL rules.

Method: documentation only; no commands were run.
