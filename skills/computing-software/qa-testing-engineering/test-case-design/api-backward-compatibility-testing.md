---
id: computing-software.qa-testing-engineering.test-case-design.api-backward-compatibility-testing
name: api-backward-compatibility-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [backward-compatibility, compatibility-testing, interoperability-testing, api-versioning, oasdiff, breaking-changes, schema-evolution]
level: practitioner
status: docs-checked
description: "Prevent breaking API consumers: diff OpenAPI specs for breaking changes, run old-client tests against new servers, and test schema evolution for events and messages."
sources:
  - https://github.com/oasdiff/oasdiff
  - https://docs.pact.io/
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API backward compatibility testing

**Goal:** a new provider version does not break existing consumers.

## Breaking changes to look for
Removed endpoint/field, renamed field, type change, new required request field, narrowed enum or validation, changed status codes or error format, changed default sort/pagination, auth scope changes.
Usually safe: new optional request field, new response field (if clients ignore unknown fields), new endpoint.

## Techniques
1. **Spec diff in CI**:
   Run oasdiff against the base and head specs and fail the build on breaking changes; see the
   oasdiff README for the command and exit-code options.
2. **Consumer contract tests** (Pact): provider verifies the contracts its consumers have published, see `pact-provider-states-verification`.
3. **Old-client regression**: keep the previous SDK/mobile app version's API tests and run them against the new server; mobile apps stay in the field for months.
4. **Event schemas**: schema registry compatibility types (Backward, Forward, Full) define which schema changes are allowed and are checked when a new schema version is registered; test consumers with old and new messages.
5. **Tolerant reader check**: clients ignore unknown fields and enum values (test by injecting extra fields via a stub).

## Gotchas
- Behavioural breaks (same schema, different semantics, e.g. amounts now in cents) pass every schema check; cover with contract examples.
- Deprecations need a timeline and usage telemetry before removal.

## Verify
CI blocks a PR that removes a response field, and the previous client version's test suite passes against the release candidate.

## Checked

- Date: 2026-10-28
- Confirmed: oasdiff compares OpenAPI specs and detects breaking changes, locally or in CI; Pact tests HTTP and message integrations with consumer-provider contracts; Confluent Schema Registry defines Backward, Forward and Full compatibility types.
- Removed: the CTAL-TA section reference, the oasdiff command line and --fail-on flag, can-i-deploy, the Avro/Protobuf rejection claim.

Method: documentation only; no commands were run.
