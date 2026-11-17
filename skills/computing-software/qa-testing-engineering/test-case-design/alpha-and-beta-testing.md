---
id: computing-software.qa-testing-engineering.test-case-design.alpha-and-beta-testing
name: alpha-and-beta-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [alpha-testing, beta-testing, test-levels, acceptance-testing, early-access, feedback-programme, feature-flags]
level: practitioner
status: draft
description: "Run alpha (in-house) and beta (real users in their environment) programmes: recruit, instrument, collect structured feedback and decide exit."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alpha and beta testing

**Goal:** get feedback from potential users in realistic conditions before general release. ISTQB CTFL v4.0 2.2.1.

## Alpha
- Done at the developer's site by internal users outside the team (dogfooding) or invited customers.
- Use for: workflow fit, obvious usability problems, early stability. Collect via an in-app feedback button and short structured interviews.

## Beta
- Done by real users in their own environments: catches device, network, data and configuration diversity you cannot reproduce.
- **Recruit** for diversity: OS/browser/device mix, light and heavy users, regions/locales.
- **Distribute**: TestFlight / Play Console closed testing tracks, feature flags with a beta cohort, early-access opt-in.
- **Instrument**: crash reporting (Sentry/Crashlytics), analytics funnels, version tagging so beta data is separable.
- **Structure feedback**: short survey at fixed points, in-app bug report that attaches logs and device info.
- **Exit criteria**: crash-free sessions >= target (e.g. 99.5%), no open critical issues, key funnel completion rates at or above baseline.

## Gotchas
- Beta users rarely write good bug reports; rely on telemetry and attach diagnostics automatically.
- An open beta with no feedback channel is just an early release.
- Respect consent and privacy for collected data.

## Verify
Beta dashboard shows crash-free rate, top issues by user count, and all exit criteria evaluated at the go/no-go.
