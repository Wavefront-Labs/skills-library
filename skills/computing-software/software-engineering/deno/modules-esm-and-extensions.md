---
id: computing-software.software-engineering.deno.modules-esm-and-extensions
name: modules-esm-and-extensions
category: computing-software
field: software-engineering
product: deno
tags: [modules, esm, commonjs, import-specifiers, file-extension, jsr, npm]
level: intro
status: docs-checked
description: "Deno's ES module system: how it picks ESM or CommonJS, mandatory file extensions on local imports, and importing jsr: and npm: packages."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno uses ECMAScript modules as its primary module system, with no bundler or build step. CommonJS also runs, but ESM is recommended for new code.

Detection: `.mjs` is always ESM, `.cjs` is always CommonJS, and `.js`/`.ts` are ESM unless a `package.json` sets `"type": "commonjs"`.

Local import specifiers must include the full file extension:

```ts title="example.ts"
// WRONG: missing file extension
import { add } from "./calc";

// CORRECT: includes file extension
import { add } from "./calc.ts";
```

Run with `deno run main.ts`.

Third-party modules use the same `import` syntax, typically starting with `jsr:` or `npm:`:

```ts title="main.ts"
import { camelCase } from "jsr:@luca/cases@1.0.0";
import { say } from "npm:cowsay@1.6.0";
```

Deno recommends JSR for third-party modules, including the Deno Standard Library. To avoid retyping versions, centralise them in the `imports` field of deno.json (the import map).

To update versions: `deno outdated` lists dependencies with newer versions and `deno outdated --update` updates them; `deno bump-version patch` increments your own package version.

## Checked

2026-11-04: confirmed against the Deno docs Modules page: ES modules as primary system, extension and package.json type detection, mandatory local file extensions, jsr: and npm: imports, JSR recommendation, imports field, deno outdated and deno bump-version.

Method: documentation only; no commands were run.
