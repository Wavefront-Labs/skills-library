---
id: computing-software.software-engineering.deno.modules-dynamic-import-and-meta
name: modules-dynamic-import-and-meta
category: computing-software
field: software-engineering
product: deno
tags: [modules, dynamic-import, import-meta, import-meta-main, filename, dirname]
level: practitioner
status: docs-checked
description: "Dynamic import() with its permission rules, and import.meta fields (url, main, filename, dirname, resolve) including the import.meta.main entry-point guard."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`import()` loads a module on demand and returns a promise for its namespace:

```ts title="main.ts"
const { add } = await import("./calc.ts");
```

The specifier can be computed, useful for conditional loading:

```ts
if (Deno.args.includes("--greet")) {
  const { greet } = await import("./greet.ts");
  greet();
}
```

A string-literal specifier is part of the static module graph and needs no permissions. A computed one is checked at runtime: local paths need `--allow-read`, remote URLs need `--allow-import`.

`import.meta`:

```ts title="main.ts"
console.log(import.meta.url); // file:///path/to/main.ts
console.log(import.meta.main); // true if this is the entry module
console.log(import.meta.filename); // /path/to/main.ts (local modules only)
console.log(import.meta.dirname); // /path/to (local modules only)
console.log(import.meta.resolve("./data.json")); // resolves a specifier to a URL
```

`filename` and `dirname` are `undefined` for remote modules.

Use `import.meta.main` to make a file both an entry point and a library:

```ts title="server.ts"
export function createServer() {/* ... */}

// Only start the server when run directly, not when imported.
if (import.meta.main) {
  createServer();
}
```

## Checked

2026-11-04: confirmed against the Deno docs Modules page (Dynamic imports, Import metadata): import() promise, permission rules for computed specifiers, import.meta fields and local-only filename and dirname, import.meta.main guard.

Method: documentation only; no commands were run.
