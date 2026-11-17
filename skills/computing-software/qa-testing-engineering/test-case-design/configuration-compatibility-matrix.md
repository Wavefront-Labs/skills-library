---
id: computing-software.qa-testing-engineering.test-case-design.configuration-compatibility-matrix
name: configuration-compatibility-matrix
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [configuration-matrix, compatibility-matrix, combinatorial-testing, configuration-testing, environment-matrix]
level: practitioner
status: docs-checked
description: "Build a configuration test matrix (OS, browser, DB, device, settings) using usage data and pairwise reduction, and track which configurations each release covered."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
  - https://github.com/microsoft/pict/blob/main/doc/pict.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration and compatibility matrix

**Goal:** cover the configuration space that customers actually run, efficiently. PICT supports weighted, constrained pairwise generation (PICT documentation).

## Steps
1. **List dimensions**: OS/version, browser/version, DB engine/version, app server, device, screen size, locale, feature-flag/settings combinations, integrations enabled.
2. **Weight values** with telemetry/customer data (installed base per version) and contracts (supported platforms list).
3. **Generate** pairwise combinations with weights and constraints (`pict-pairwise-generation`); add must-have rows: most common config, newest versions, oldest supported versions.
4. **Assign tiers**: full regression on the top configs, smoke on the rest.
5. **Track** per release which configs were tested and results; rotate lower-tier configs across releases to spread coverage.

## Example matrix (excerpt; illustrative values only)
| # | OS | DB | Browser | SSO | Tier |
|---|---|---|---|---|---|
| 1 | Windows Server 2022 | SQL Server 2022 | Edge | SAML | full |
| 2 | RHEL 9 | PostgreSQL 16 | Chrome | OIDC | full |
| 3 | Ubuntu 22.04 | PostgreSQL 13 (oldest) | Firefox ESR | none | smoke |

## Automating
CI matrix jobs for automatable dimensions (OS x runtime x DB via containers); cloud device/browser grids for browsers/devices; feature-flag combos via config fixtures.

## Gotchas
- "Supported" lists grow but tests do not; prune support or test it.
- Settings combinations (feature flags) are configurations too and often the riskiest.

## Verify
Release report shows configuration coverage vs the matrix, and every supported configuration was tested within the last N releases.

## Checked

2026-10-28 Confirmed against: PICT documentation (constraint syntax); cross-reference to the library's pict-pairwise-generation skill exists. Removed or generalised: the ISTQB syllabus section number (page returned an error and could not be read). The example matrix rows are illustrative and not a support statement.

Method: documentation only; no commands were run.
