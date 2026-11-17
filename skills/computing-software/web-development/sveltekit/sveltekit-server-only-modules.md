---
id: computing-software.web-development.sveltekit.sveltekit-server-only-modules
name: sveltekit-server-only-modules
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, server-only-modules, secrets, security, imports, vitest]
level: intro
status: docs-checked
description: "Keep secrets out of browser bundles in SvelteKit by marking modules server-only via filename or a server directory, and understand the illegal-import error."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/50-server-only-modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit server-only modules

Goal: guarantee that sensitive code (API keys, secrets) cannot reach the browser.

## Built-in server-only modules

- `$app/env/private` can only be imported by server-only code such as `hooks.server.js` or `+page.server.js`.
- `$app/server` (which has `read` for reading assets from the filesystem) is likewise server-only.

## Making your own modules server-only

Either:

- add a `server` segment to the filename: `server.js` or `secrets.server.ts` (works anywhere in the project directory); or
- put it in a `server` directory anywhere in the project except inside `src/routes` or `static`, e.g. `src/lib/server/config.js` or `src/lib/data/server/user/profile.js`.

Legacy note from the docs: in SvelteKit 2, `server` directories were only recognised inside `src/lib`.

Modules outside your working directory and inside `node_modules` are not subject to these rules. To publish a package containing a server-only module, add `import '$app/server'` at the top of that file.

## How the check works

If public-facing code imports server-only code, directly or indirectly, SvelteKit errors, even if only a harmless export is used. Example chain: `src/routes/+page.svelte` imports `./utils.js`, which re-exports from `#lib/server/secrets.js`. The error reads:

```
Cannot import #lib/server/secrets.ts into code that runs in the browser, as this could leak sensitive information.

 src/routes/+page.svelte imports
  src/routes/utils.js imports
   #lib/server/secrets.ts

If you're only using the import as a type, change it to `import type`.
```

The page only uses `add`, not the secret export, but the secret code could end up in JavaScript the browser downloads, so the whole import chain is considered unsafe. Dynamic imports are checked too, even interpolated ones like `` await import(`./${foo}.js`) ``.

## Testing gotcha

Unit test frameworks such as Vitest do not distinguish server from public code, so illegal-import detection is disabled when `process.env.TEST === 'true'`.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/50-server-only-modules.md in full. One trim: removed advice to split the safe export into another module, which the page does not say; reworded to what the page states about the import chain.
