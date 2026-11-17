---
id: computing-software.qa-testing-engineering.test-automation.shift-right-testing-in-production
name: shift-right-testing-in-production
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [shift-right, testing-in-production, canary-release, synthetic-monitoring, feature-flags, observability]
level: advanced
status: draft
description: "Test in production safely: canary and progressive delivery with automated analysis, synthetic monitoring, feature flags, dark launches and production-safe test data."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://sre.google/workbook/canarying-releases/
  - https://martinfowler.com/articles/feature-toggles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shift-right testing in production

**Goal:** catch what pre-production cannot (real traffic, data, scale, third-party behaviour) while limiting user impact.

## Techniques
- **Canary release:** route a small share of traffic (1-5%) to the new version; compare error rate, latency and business metrics with the baseline; automated promotion or rollback (Argo Rollouts analysis, Flagger, Spinnaker Kayenta).
- **Progressive delivery with feature flags:** enable for internal users, then a percentage, then all; kill switch tested before launch.
- **Dark launch / shadow traffic:** mirror real requests to the new service and compare responses without serving them (Istio mirroring, Diffy-style comparison).
- **Synthetic monitoring:** scripted journeys (Playwright, k6 browser, Checkly, Datadog Synthetics) every few minutes from several regions, alerting on failure.
- **Real user monitoring:** Core Web Vitals and JS errors from real browsers.
- **Chaos experiments** under SLO guardrails.
- **A/B tests** for product hypotheses (different purpose, same plumbing).

## Safety rules
- Production test accounts and data clearly marked and excluded from analytics, billing and emails (e.g. a `test_user` flag honoured downstream).
- Synthetic transactions must not trigger real payments or shipments: sandbox merchant, auto-cancel.
- Defined rollback triggers and owners before the canary starts.
- Observability in place first: you cannot test in prod what you cannot see.

## Canary analysis basics
Compare canary vs baseline (not vs last week), same time window, enough requests for significance; typical metrics: 5xx rate, p95/p99 latency, saturation, key business conversion.

## Verify
Releases go through a canary with recorded analysis results, synthetic journeys alert on failure within minutes, and test data never appears in business reports.
