---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.beyond-twelve-factor
name: beyond-twelve-factor
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor-build, beyond-twelve-factor, fifteen-factor, api-first, telemetry, authentication-authorization, cloud-native]
level: practitioner
status: draft
description: "Apply the beyond-twelve-factor additions: API first, telemetry, and authentication and authorisation, plus updated readings of the original factors for modern cloud apps."
sources: ["https://www.oreilly.com/library/view/beyond-the-twelve-factor/9781492042631/", "https://12factor.net/", "https://opentelemetry.io/docs/", "https://github.com/twelve-factor/twelve-factor"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Beyond twelve-factor (API first / telemetry / security)

## Background
Kevin Hoffman's *Beyond the Twelve-Factor App* (O'Reilly/Pivotal, 2016) reorders the factors
and adds three: **API first**, **telemetry**, and **authentication and authorization**
(often called the fifteen-factor app). The twelve-factor project itself was open-sourced in
2024 for community modernisation.

## Steps
1. **API first**: design the contract before code (OpenAPI/AsyncAPI/protobuf), review it with
   consumers, lint it (Spectral), mock it for parallel work, and version it. Contracts live in
   the repo and are tested (contract tests such as Pact).
2. **Telemetry**: beyond logs, emit metrics, traces and health/business events. Instrument with
   OpenTelemetry SDKs; export via OTLP to a collector; follow semantic conventions; add
   domain metrics (orders per minute). Telemetry config is environment config (factor III).
3. **Authentication and authorisation**: every endpoint authenticates (OIDC/JWT, mTLS for
   services) and authorises (RBAC/ABAC, policy engines like OPA/Cedar); workload identity
   instead of static keys; audit security decisions.
4. **Revisit the original factors** with Hoffman's updates: one codebase per app (not per
   system), explicit dependency vendoring in images, config including credentials from a
   secrets store, logs as event streams, backing services bound at runtime.
5. Add to the team's twelve-factor checklist and review in design reviews.

## Gotchas
- API-first without consumer review produces specs nobody uses.
- Telemetry with unbounded label cardinality (user IDs as metric labels) breaks backends.
- Authentication at the gateway only, with open internal endpoints, fails zero-trust reviews.

## Verify
- [ ] Each service has a published, linted API contract.
- [ ] Traces span all hops of critical journeys.
- [ ] No unauthenticated internal endpoints except health probes.
