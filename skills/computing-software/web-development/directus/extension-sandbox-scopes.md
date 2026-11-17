---
id: computing-software.web-development.directus.extension-sandbox-scopes
name: extension-sandbox-scopes
category: computing-software
field: web-development
product: directus
tags: [extension-sandbox, requested-scopes, sandbox-request, sandbox-log]
level: advanced
status: docs-checked
description: "Run a Directus API extension in the isolated sandbox: enable it in package.json and request log, sleep and request scopes with URL allowlists."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/09.extensions/2.api-extensions/5.sandbox.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sandboxed API extensions run isolated and see only JavaScript standard built-ins, so `console` and `setTimeout` are unavailable. Extra capability comes from scopes through the `directus:api` module.

Enable in `package.json`:

```json
"directus:extension": {
  "type": "endpoint",
  "path": "dist/index.js",
  "source": "src/index.js",
  "sandbox": { "enabled": true, "requestedScopes": {} }
}
```

Scopes:
- `log`: `import { log } from 'directus:api'; log('Hello');` writes to the API logger. `"log": {}`
- `sleep`: `await sleep(1000)`, replaces `setTimeout`. `"sleep": {}`
- `request`: `await request(url, { method, headers, body })`; the result has `status`, `statusText`, `headers`, `data`.

```json
"requestedScopes": { "request": { "methods": ["GET", "POST"], "urls": ["https://directus.com/*"] } }
```

URLs support wildcards; `https://*` allows all and is for development only.

TypeScript: reference `@directus/extensions/api.d.ts` (or add it to `tsconfig.json`).

Each function needs its matching scope in `requestedScopes`: `log` and `sleep` take no options, `request` takes `methods` and `urls`.

## Checked

2026-11-04: sandbox isolation and missing console/setTimeout, package.json sandbox object, log, sleep and request scopes with their examples, response properties, URL wildcards and the TypeScript api.d.ts reference confirmed against the Directus Sandbox page. Replaced an unsupported failure claim and removed a Verify line.

Method: documentation only; no commands were run.
