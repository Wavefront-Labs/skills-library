---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-modules-and-jslib
name: k6-modules-and-jslib
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-modules, jslib, remote-modules, k6-bundling, es-modules]
level: practitioner
status: verified
description: "Structure k6 scripts with local ES modules, remote modules and jslib.k6.io helpers, know the k6 built-in modules, and bundle npm dependencies with esbuild or webpack."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/modules/
  - https://grafana.com/docs/k6/latest/javascript-api/jslib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modules, remote modules and jslib

## Built-in modules
`k6`, `k6/http`, `k6/metrics`, `k6/data`, `k6/execution`, `k6/crypto` (hashing only; prefer the global WebCrypto `crypto`), `k6/encoding`, `k6/ws`, `k6/websockets`, `k6/net/grpc`, `k6/browser`, `k6/timers`, `k6/secrets`. All of these imported cleanly on k6 2.3.0. `k6/experimental/webcrypto` no longer imports (error: it "has been graduated and it's now globally available"; remove the import). `k6/experimental/csv`, `fs` and `streams` still import (the docs list only those three under `k6/experimental`); `k6/experimental/redis` was removed in v2.0.0.

## Local modules
```js
// lib/auth.js
import http from 'k6/http';
export function login(user) { return http.post(`${__ENV.BASE}/login`, JSON.stringify(user)).json('token'); }
// script.js
import { login } from './lib/auth.js';
```
Relative imports need the `.js` extension (run: `import './lib/auth'` fails with `The moduleSpecifier "./lib/auth" couldn't be found`). Keep scenario files thin; share flows in `lib/`.

## Remote modules and jslib
```js
import { uuidv4, randomIntBetween, randomItem } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.1.0/index.js';
import { URL, URLSearchParams } from 'https://jslib.k6.io/url/1.0.0/index.js';
import { expect } from 'https://jslib.k6.io/k6-testing/0.5.0/index.js';
```
Always pin versions in the URL. Remote modules are fetched at start; for air-gapped CI vendor them locally. All four URLs above resolve and ran on k6 2.3.0; newer releases exist on jslib.k6.io (k6-utils up to 1.6.0, k6-testing up to 0.6.1; url has only 1.0.0), so bump deliberately.

## npm packages
k6 is not Node: no `fs`, `net`, Node globals. Pure-JS npm packages can be bundled:
```bash
npx esbuild src/test.js --bundle --format=esm --platform=neutral --main-fields=module,main --external:k6* --outfile=dist/test.js
k6 run dist/test.js
```
With `--platform=neutral` esbuild ignores a package's `main` field, so a CommonJS package fails with `Could not resolve` unless you add `--main-fields=module,main` (run with esbuild 0.25.0; `--platform=browser` also worked). The bundle then ran under k6 2.3.0. Keep `k6`/`k6/*` imports external. (Grafana's `k6-template-es6`/`k6-template-typescript` show webpack/esbuild setups.)

## k6 archive
`k6 archive -O out.tar script.js` creates a tar with all local and remote modules resolved (the tar for the script above held 15 jslib entries) and `k6 run out.tar` runs it, for reproducible runs on other machines or the cloud.

## Gotchas
- Large bundles inflate init time and memory per VU.
- Modules execute once per VU in init context; heavy top-level work multiplies by VUs.

## Verify
`k6 inspect script.js` resolves imports and prints the options as JSON; `k6 archive` produces a tar that `k6 run` accepts (`k6 archive --help`: "a fully self-contained test run"); confirm air-gapped behaviour on your own CI runner.
