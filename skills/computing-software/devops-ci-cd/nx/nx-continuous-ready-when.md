---
id: computing-software.devops-ci-cd.nx.nx-continuous-ready-when
name: nx-continuous-ready-when
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, continuous, readywhen, waitfor, e2e, dev-server]
level: advanced
status: docs-checked
description: "Model long-running Nx tasks: continuous:true, dependsOn waitFor ready, and readyWhen checks (url, port, command, logMatches, signal) with timeout and interval."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let an `e2e` task depend on a `serve` task that never exits, and start only when the server is up. (Nx 21+)

```json
// apps/myapp/project.json
"serve": { "continuous": true, "readyWhen": { "url": "http://localhost:4200" } }
// apps/myapp-e2e/project.json
"e2e": { "dependsOn": [ { "projects": "myapp", "target": "serve", "waitFor": "ready" } ] }
```
`continuous: true` stops dependents waiting for the task to complete. Without `waitFor: "ready"` a dependent starts as soon as the server process started. A continuous target with no `readyWhen` counts as ready once started.

`readyWhen` takes exactly one of:
- `url`: ready when HTTP(S) GET returns 200-403 (redirects not followed; a 404 at root is retried at `/index.html`).
- `port` (+ optional `host`): TCP connect succeeds. `port: 0` or `"auto"` runs no check (ready once started).
- `command`: shell command at workspace root exits 0; gets `NX_TASK_OPTIONS` as JSON.
- `logMatches`: string or array of strings that must all appear in task output (colors stripped; order irrelevant).
- `signal: true`: the task reports readiness itself (nx-ready-signal).
Extra keys: `timeout` ms (default `600000`), `interval` ms (default `250`; not for `signal`).
Placeholders: `{workspaceRoot}`, `{projectRoot}`, `{projectName}`, `{options.*}`, `{env.*}`, fallbacks with `??`, e.g. `"http://localhost:{options.port ?? env.PORT ?? 4200}"`.

On timeout the task fails and waiting tasks are skipped. A `readyWhen` in `targetDefaults` replaces a plugin-inferred one; project config replaces both; `null` disables it; `{ "...": true, "timeout": 1200000 }` extends. This is unrelated to the `readyWhen` option of `nx:run-commands`.

Hashing: an `e2e` task also hashes its continuous dependency's inputs. Use `"inputs": false` on that `dependsOn` entry to hash only its own. A server with no declared inputs contributes its whole project.

To inspect: `nx show target` shows a target's `readyWhen` with the timeout and where the check came from.

## Checked

2026-11-07. Confirmed: continuous, waitFor ready, the readyWhen check types, timeout 600000 and interval 250 defaults, and placeholders against Project configuration; the "inputs": false hashing note against Inputs. Removed: an invented Verify step (replaced by the page's nx show target statement) and the unconfirmed "blocks dependents forever" wording.

Method: documentation only; no commands were run.
