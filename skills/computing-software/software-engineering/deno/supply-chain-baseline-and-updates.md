---
id: computing-software.software-engineering.deno.supply-chain-baseline-and-updates
name: supply-chain-baseline-and-updates
category: computing-software
field: software-engineering
product: deno
tags: [supply-chain, lockfile, frozen, vendor, ci, intentional-updates, baseline]
level: advanced
status: docs-checked
description: "A Deno supply-chain baseline: pin versions, commit and freeze deno.lock, vendor, CI install flow, intentional update steps and frozen-lockfile troubleshooting."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/supply_chain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goals: determinism, security, controlled velocity, resilience. Core practices: pin deliberately (exact versions for apps, caret for libraries, avoid `*`); commit `deno.lock`; freeze it in CI/production (`--frozen` or `"lock": { "frozen": true }`); vendor for hermetic builds (complements, not replaces, the lockfile); centralise versions in `imports`; update on a cadence; set a minimum dependency age.

Recommended baseline:

```json title="deno.json"
{
  "imports": {/* centralize versions */},
  "vendor": true,
  "lock": { "frozen": true }
}
```

Commit `deno.json`, `deno.lock` and `vendor/`.

CI (Deno 2.8+): `deno ci`. Older, or manual:

```sh
deno install --frozen --entrypoint main.ts
deno run --cached-only main.ts
```

Intentional update: unfreeze (`--frozen=false` or `"frozen": false`), change versions (`deno add <specifier>@<newVersion>`), re-run `deno install --entrypoint main.ts` (optionally `--reload`), review the `deno.lock` and `vendor/` diff, re-freeze.

Frozen errors such as `The lockfile is frozen. Cannot add new entry for "jsr:@scope/pkg@1.3.0".` mean new or changed dependencies: unfreeze, run `deno install --entrypoint <entry>.ts`, commit. Lockfile is additive, so removed imports linger; regenerate only when necessary (back up, remove `deno.lock`, remove `vendor/` if used, reinstall, diff).

A scheduled CI job that unfreezes, runs `deno add --latest`, tests and opens a PR keeps patches flowing.

## Checked

2026-11-04. Confirmed against the Deno Supply chain management page: core practices, baseline config, `deno ci` from Deno 2.8, manual CI commands, update steps, frozen-lockfile errors, regeneration, weekly refresh tip. Nothing removed.

Method: documentation only; no commands were run.
