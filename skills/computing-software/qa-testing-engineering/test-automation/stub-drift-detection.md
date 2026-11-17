---
id: computing-software.qa-testing-engineering.test-automation.stub-drift-detection
name: stub-drift-detection
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [stub-drift, service-virtualization, contract-testing, mock-drift, record-replay]
level: advanced
status: draft
description: "Keep stubs and mocks in sync with real services: contract-backed stubs, scheduled live comparison, schema validation of stubs, re-recording and ownership."
sources:
  - https://wiremock.org/docs/
  - https://docs.pact.io/
  - https://docs.hoverfly.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keeping stubs in sync with real services

**Goal:** prevent green tests built on stubs that no longer behave like the real service, the main risk of service virtualisation.

## Detection techniques
- **Validate stubs against the provider's OpenAPI spec:** run each stub response through a schema validator in CI (WireMock mappings parsed and validated with ajv/openapi-core); any stub that does not conform fails.
- **Contract-backed stubs:** generate stubs from Pact contracts the provider verifies (Pact stub server: `pact-stub-server -f pacts/`), so a stub only exists for interactions the provider proved it supports.
- **Scheduled live comparison:** a nightly job sends the stubbed requests to the real sandbox and compares responses with the stubs (status, schema, key fields). Hoverfly diff mode does this for captured simulations.
- **Record/replay refresh:** periodically re-record cassettes (VCR, WireMock record, Hoverfly capture) against the sandbox and review the diff in a PR.
- **Provider change feeds:** subscribe to partner changelogs, API version deprecation headers (`Sunset`, `Deprecation`).

## Practice
- Each stub set has an owner and a "last verified" date; stale beyond N weeks triggers re-verification.
- Keep a small set of live integration tests against the real sandbox, run on schedule, not in the PR gate.
- Prefer stubs with minimal hand-written behaviour; complex fake logic drifts fastest.
- Tag stubs with the provider version they were captured from.

## Verify
CI rejects stubs that violate the provider schema, the nightly live comparison reports zero unexplained diffs, and every stub set has a recent verification date.
