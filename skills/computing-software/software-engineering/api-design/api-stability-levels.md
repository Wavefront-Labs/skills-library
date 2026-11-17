---
id: computing-software.software-engineering.api-design.api-stability-levels
name: api-stability-levels
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-stability-levels, aip-181, alpha-beta-ga, api-lifecycle, preview-apis]
level: practitioner
status: docs-checked
description: "Label API components alpha, beta or stable (AIP-181), plus experimental, preview and GA versions, with the guarantees, deprecation and time-boxing each level implies."
sources: ["https://google.aip.dev/181"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alpha / beta / stable stability levels

Source: Google AIP-181. These levels roughly correspond to Google Cloud launch stages but are not identical.

## Component levels
| Level | Promise |
|---|---|
| Alpha | Rapid iteration with a curated, known set of users who tolerate change; breaking changes allowed and expected; no stability expectation |
| Beta | Complete and ready to be declared stable; public, not behind an allowlist; as stable as possible, but may change, with backwards-incompatible changes only after a deprecation period defined when marked beta |
| Stable | Fully supported for the life of the major version; no breaking changes, subject to the caveats below |

- Beta should be time-boxed and promoted to stable if no issues are found; the timeframe is set when marked beta
  (AIP-181 gives about 90 days as a rule of thumb).
- Stable, when breaking changes become necessary: create the next major version and start a deprecation clock on
  the old one. Turn-down needs a formal process, defined when marked stable, with a deprecation period.
- Isolated in-place breaking change in a stable API: an extreme course of action, treated with equal or greater
  gravity than a new major version; the component must still be supported for the normal turn-down period.
- Emergency changes (security, regulatory) may break any component regardless of level, with no promised
  deprecation.

## Interface-based (version) levels, linked to AIP-185
- Stability is judged on call-time compatibility (producer's responsibility) and upgrade compatibility (the
  consumer's, when moving versions).
- Experimental: no compatibility guarantee, no guaranteed lifetime, exempt from compatibility policies; directly
  communicate changes to the few consumers.
- Preview: time-boxed lifecycle communicated at inception; tries to keep call-time compatibility, gives no upgrade
  compatibility; not suitable for production. Expiry has phases (onboarding window closure, then final turn-down),
  with timing stated upfront.
- GA: long-term support, call-time compatibility, subject to discontinuation and deprecation policies; features
  facing deprecation or redesign may change incompatibly between consecutive GA versions after the producer has
  communicated and supported migration.

## Checked
Date: 2026-11-01. Confirmed on AIP-181 only. Removed: version-name examples, opt-in header and allow-list
mechanics, graduation checklist, vendor behaviours, and the Kubernetes comparison, which that page does not state.
Method: documentation only; no commands were run.
