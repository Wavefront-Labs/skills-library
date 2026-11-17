---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-environment-variables-and-config
name: k6-environment-variables-and-config
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-env, k6, environment-variables, k6-options, config-files]
level: practitioner
status: verified
description: "Parameterise k6 tests: __ENV with -e and system env, --config JSON files, option precedence, per-environment profiles, and keeping secrets out of scripts."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/environment-variables/
  - https://grafana.com/docs/k6/latest/using-k6/k6-options/how-to/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment variables and config files (k6)

## __ENV
```js
const BASE = __ENV.BASE_URL || 'http://localhost:8080';
const PROFILE = __ENV.PROFILE || 'smoke';
```
```bash
k6 run -e BASE_URL=https://staging.example.test -e PROFILE=load script.js
BASE_URL=https://staging.example.test k6 run script.js        # system env is also visible in __ENV
k6 run --include-system-env-vars=false -e BASE_URL=... script.js   # only -e values (the default is true for `k6 run`, false for every other command: cloud run, archive, inspect)
```

## Profiles in the script
```js
const profiles = {
  smoke:  { vus: 1, duration: '1m' },
  load:   { stages: [{ duration: '5m', target: 100 }, { duration: '20m', target: 100 }, { duration: '5m', target: 0 }] },
  stress: { stages: [{ duration: '10m', target: 400 }, { duration: '10m', target: 0 }] },
};
export const options = {
  ...profiles[PROFILE],
  thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<500'] },
};
```

## Config files
```bash
k6 run --config configs/staging-load.json script.js
```
```json
{ "stages": [{ "duration": "5m", "target": 100 }], "thresholds": { "http_req_duration": ["p(95)<500"] }, "tags": { "env": "staging" } }
```
Precedence (lowest to highest): defaults < `--config` file < script `options` < `K6_*` env vars (e.g. `K6_VUS`, `K6_DURATION`) < CLI flags (`--vus`, `--duration`).
So script options override the config file; keep options either in files or script, not both.
Run on k6 2.3.0 with `--config` (`vus:3`), script `vus:5`, `K6_VUS=7` and `--vus 9`: effective VUs were 3, 5, 7 and 9 as each layer was added. System env `BASE_URL=sys` was visible in `__ENV` and disappeared with `--include-system-env-vars=false`; an `-e` value overrode the system one.

## Secrets
- Pass via env in CI (`-e API_TOKEN=$API_TOKEN`), never hard-code.
- `k6 run` prints options, not env values, but `console.log` can leak; avoid logging tokens.
- k6 has secret sources (`--secret-source`, read in scripts through `k6/secrets`); values are redacted from logs. Run: `k6 run --secret-source=mock=mysecret=hunter2value` and `console.log(await secrets.get('mysecret'))` printed `***SECRET_REDACTED***`. Built-in sources: `file`, `mock` (testing only), `url`, and `cloud` (for `k6 cloud run --local-execution`).

## Data per environment
Load environment-specific data files in init: `open(\`./data/${__ENV.ENV}/users.csv\`)`.

## Gotchas
- `__ENV` values are strings; `Number(__ENV.VUS)`.
- `K6_` env vars silently override script options in CI; check with `k6 run --verbose` (prints the effective scenario, e.g. `1 iterations for each of 1 VUs`) or print `exec.test.options` in setup.

## Verify
The same script runs smoke locally and load in CI by switching variables only, and no credentials are in the repository.
