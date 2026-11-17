---
id: computing-software.qa-testing-engineering.test-case-design.system-integration-testing
name: system-integration-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [system-integration-testing, test-levels, end-to-end-integration, third-party-integration, sandbox-environments, interface-testing]
level: practitioner
status: draft
description: "Test integration with external systems (payment providers, ERPs, partner APIs): sandboxes, test agreements, data alignment, failure and timeout cases."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System integration testing (SIT)

**Goal:** prove the system works with the external systems and services it depends on. ISTQB CTFL v4.0 2.2.1.

## Preparation
1. **Inventory interfaces**: protocol, owner, direction, sync/async, environment available (sandbox, shared test env, none).
2. **Agree test windows and data** with each partner: test accounts, card numbers, matching master data (customer ids exist in both systems).
3. **Stub what you cannot get** (WireMock/Prism, see `wiremock-http-stubbing`) and record which tests ran against stubs vs real.

## Test conditions per interface
- Happy path end to end with real data mapping (field lengths, encodings, time zones, currencies).
- Partner returns errors (4xx/5xx, business rejections).
- Timeouts and retries; idempotency of retried requests (no double charge).
- Async: message ordering, duplicates, dead-letter handling.
- Reconciliation: totals in both systems match after a batch.

## Gotchas
- Sandboxes behave differently from production (instant settlement, relaxed validation). Note known differences.
- Shared integration environments get corrupted by other teams; schedule and reset.
- Clock/time zone differences cause off-by-one-day bugs on batches.

## Verify
An interface checklist shows every interface tested for success, error and timeout, with real or stubbed partner noted.
