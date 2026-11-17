---
id: computing-software.software-engineering.deno.supply-chain-trust-policy
name: supply-chain-trust-policy
category: computing-software
field: software-engineering
product: deno
tags: [supply-chain, minimum-dependency-age, trust-policy, no-downgrade, npmrc, provenance]
level: sme
status: docs-checked
description: "Delay fresh package versions with minimum dependency age (deno.json, flag, .npmrc) and block publishing-trust downgrades with trust-policy=no-downgrade."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/supply_chain.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Minimum dependency age: Deno refuses to install versions younger than a configured age; malicious versions are usually yanked within days. Since Deno 2.9 a 24-hour window is on by default; set age to `0` to disable. Configure in:

```jsonc title="deno.json"
{ "minimumDependencyAge": "P3D" }
```

```sh
deno install --minimum-dependency-age=P3D
```

```ini title=".npmrc"
min-release-age=3
```

(.npmrc needs Deno 2.8+ and accepts whole days only.) deno.json and the flag take an ISO-8601 duration (`P3D`, `PT72H`), integer minutes, an absolute date or RFC3339 timestamp, or `0`.

Publishing-trust policy refuses a version published by a weaker method than one you already locked. Signals from npm metadata: trusted publishing (OIDC), provenance attestation, staged publishing (2FA-approved). Ranking low to high: Plain, Provenance, Trusted publishing, Trusted publishing + provenance, Staged. Mirrors pnpm's `trustPolicy: no-downgrade`.

```ini title=".npmrc"
trust-policy=no-downgrade
```

Behaviour: Deno records the level as a `trust` field on each npm entry in `deno.lock` (omitted when plain); the highest recorded level is the baseline. With the policy on, it refuses candidates below the baseline and fetches the full packument. A first lock has no baseline. Off by default; any value other than `no-downgrade` leaves it off.

## Checked

2026-11-04. Confirmed against the Deno Supply chain management page: minimum dependency age settings and forms, the 24-hour default since Deno 2.9, `.npmrc` from Deno 2.8 with whole days, the three trust signals and ranking, `trust-policy=no-downgrade`, lockfile `trust` field behaviour. Nothing removed.

Method: documentation only; no commands were run.
