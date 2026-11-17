---
id: computing-software.devops-ci-cd.release-engineering.deprecation-policy-and-breaking-changes
name: deprecation-policy-and-breaking-changes
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, deprecation-policy, semver, changelog]
level: practitioner
status: docs-checked
description: "Run a deprecation policy for APIs and libraries: notice periods, Deprecation/Sunset headers, warnings in code, usage telemetry, migration guides and the removal release."
sources: ["https://semver.org/#how-should-i-deal-with-deprecating-functionality", "https://www.rfc-editor.org/rfc/rfc8594"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecation policy and breaking-change communication

## Policy (write it down)
- Minimum notice: publish a notice period for public APIs, and ship at least one minor release with the deprecation for libraries before removal in
  the next major.
- Channels: changelog "Deprecated" section, docs banner, email to API consumers, runtime warnings.
- Removal only in a major version (libraries) or after the sunset date (HTTP APIs).

## Signals in the artefact
- HTTP APIs: `Deprecation` header (RFC 9745) and `Sunset` header (RFC 8594):
  ```
  Deprecation: @1767225600
  Sunset: Wed, 30 Jun 2027 23:59:59 GMT
  Link: <https://api.example.com/docs/migrate-v2>; rel="deprecation"
  ```
- Libraries: use your language's deprecation marker or runtime warning mechanism.

## Telemetry
Measure who still uses deprecated paths (API key/client id per endpoint, library version
telemetry where acceptable). Contact top users directly before removal.

## Removal release
- Migration guide with before/after examples.
- Semver major bump; changelog "Removed" section links to the deprecation notice.
- Optional brownouts (scheduled short outages of the old endpoint) to flush out unknown consumers.

## Verify
- [ ] Deprecated endpoints return headers; usage dashboard trends to zero before the sunset date.

## Checked

2026-10-28. Confirmed: RFC 9745 defines the `Deprecation` header (example `Deprecation: @1688169599` form) and the `deprecation` link relation; RFC 8594 defines `Sunset`; semver.org says there should be at least one minor release containing the deprecation before removal in a new major release. Removed: the 6-month figure, the language marker examples (Java, Python, TypeScript, Rust) and the OpenAPI `deprecated: true` line, which were not checked against their docs.

Method: documentation only; no commands were run.
