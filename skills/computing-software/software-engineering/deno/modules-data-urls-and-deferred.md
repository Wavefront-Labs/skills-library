---
id: computing-software.software-engineering.deno.modules-data-urls-and-deferred
name: modules-data-urls-and-deferred
category: computing-software
field: software-engineering
product: deno
tags: [modules, data-url, import-defer, wasm-import, mock-modules, experimental]
level: advanced
status: docs-checked
description: "Generating modules from data: URLs (useful for test mocks), deferred module evaluation with import defer (Deno 2.8), and direct Wasm imports."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Data URL imports create modules on the fly, useful for tests, prototyping, mock modules and generated code. Pattern: `data:[<media type>][;base64],<data>`. Use `application/javascript`; `application/typescript` is also supported.

```ts
const plainModule = await import(
  "data:application/javascript,export function greet() { return 'Hi there!'; }"
);
console.log(plainModule.greet()); // Outputs: Hi there!

const textModule = await import(
  "data:text/plain,export default 'This is plain text'"
);
```

Deferred evaluation (Deno 2.8, TC39 Stage 3 proposal, so syntax may change): `import defer` loads a module and its dependencies but does not run top-level code until you first read a property from the namespace.

```ts title="main.ts"
import defer * as expensive from "./expensive.ts";

console.log("startup is fast: expensive.ts has not run yet");

// Touching any property triggers synchronous evaluation
console.log(expensive.value);
```

Use it for conditionally needed heavy modules, like error-path CLI code. Standard `import` remains the right default.

Wasm modules import directly; named exports mirror the Wasm exports and a `global` export resolves to its value:

```ts
import { add } from "./add.wasm";
```

## Checked

2026-11-04: confirmed against the Deno docs Modules page (Data URL imports, Deferred module evaluation, WebAssembly modules): data URL pattern and media types, import defer behaviour and 2.8 version, Stage 3 note, Wasm export mapping.

Method: documentation only; no commands were run.
