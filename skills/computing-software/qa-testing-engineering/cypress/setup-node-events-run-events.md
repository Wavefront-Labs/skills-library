---
id: computing-software.qa-testing-engineering.cypress.setup-node-events-run-events
name: setup-node-events-run-events
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [cypress-run-events, setupnodeevents, before-run, after-spec, cypress-plugins]
level: practitioner
status: verified
description: "Hook into Cypress run lifecycle events in setupNodeEvents (before:run, after:spec, after:run, after:screenshot) to clean artifacts, upload results or notify."
sources:
  - https://docs.cypress.io/api/node-events/overview
  - https://docs.cypress.io/api/node-events/after-spec-api
  - https://docs.cypress.io/api/node-events/before-run-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# setupNodeEvents and run events

`setupNodeEvents(on, config)` runs in Node (not the browser). Besides `task`, it can subscribe to run events.

```js
// cypress.config.js
const fs = require('fs');
module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      on('before:run', (details) => { console.log(`Run on ${details.browser.name}, ${details.specs.length} specs`); });
      on('after:spec', (spec, results) => {
        // keep videos only for failed specs
        if (results && results.video && !results.tests.some(t => t.attempts.some(a => a.state === 'failed'))) {
          fs.unlinkSync(results.video);
        }
      });
      on('after:run', async (results) => { if (results.totalFailed) await notifySlack(results); });  // notifySlack: your own helper
      on('after:screenshot', (details) => {   // move the file yourself, then report the new path
        const to = details.path.replace(/\.png$/, '-ci.png');
        fs.renameSync(details.path, to);
        return { path: to };
      });
      return config;  // return modified config if changed
    },
  },
});
```

## Event reference
| Event | When | Typical use |
|---|---|---|
| `before:run` | once before specs (run mode; open mode with `experimentalInteractiveRunEvents`) | seed, start services |
| `before:spec` / `after:spec` | each spec | per-spec cleanup, video pruning |
| `after:run` | end of run | aggregate results, notify |
| `after:screenshot` | each screenshot | rename, move, upload |
| `before:browser:launch` | browser start | flags, extensions |
| `file:preprocessor` | bundling specs | custom webpack/esbuild |

## Config modification
`setupNodeEvents` can return a changed `config` (e.g. load `config.env` from a secrets file per `config.env.environment`).

## Gotchas
- Registering the same event twice: only the last handler ran (`before:run` and `after:spec` each printed just the second handler in a 16.2.0 run); plugins competing for one event need `cypress-on-fix` (exists on npm) or manual chaining.
- `before:run` details keys: `browser`, `config`, `cypressVersion`, `parallel`, `specs`, `specPattern`, `system`. `after:spec` results keys: `error`, `reporter`, `reporterStats`, `screenshots`, `spec`, `stats`, `tests`, `video`. `after:run` results have `totalFailed`, `totalPassed`, `runs` and so on but no `status` field.
- With Electron each spec launched its own browser, so `before:browser:launch` fired once per spec.
- Run events don't fire in `cypress open` unless `experimentalInteractiveRunEvents` is on (the config key exists, default false; open mode itself was not run here).
- Async handlers must return a promise; otherwise Cypress won't wait.

## Verify
Run on Cypress 16.2.0 with all five run events plus `after:screenshot` and `before:browser:launch` (`preferences.width = 1500` was applied: the page saw an outer width of 1500). After a run, videos exist only for failing specs and the notification fires on failure.
