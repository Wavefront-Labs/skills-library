---
id: computing-software.web-development.node-express.authorization-policy-engines
name: authorization-policy-engines
category: computing-software
field: web-development
product: node-express
tags: [policy-engine, opa-policy, cedar-policy, casbin, openfga, abac, rebac, authorization]
level: advanced
status: draft
description: "Externalising authorization with policy engines: OPA/Rego, Cedar, Casbin and Zanzibar-style OpenFGA/SpiceDB; PDP/PEP split, list filtering, testing and decision logs."
sources:
  - https://www.openpolicyagent.org/docs/latest/
  - https://docs.cedarpolicy.com/
  - https://openfga.dev/docs/concepts
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Authorization policy engines

When role checks sprawl across handlers (`if user.role === "admin" || (user.id === doc.ownerId && !doc.locked)`), move decisions into one policy layer.

## 1. Pick the model
| Model | Engine | Good for |
|---|---|---|
| RBAC/ABAC rules over attributes | OPA (Rego), Cedar, Casbin | "editors in the same department may update unpublished docs" |
| Relationship-based (ReBAC, Google Zanzibar) | OpenFGA, SpiceDB, Permify | sharing, folders, orgs/teams, "viewer of parent folder can view" |

## 2. Cedar example
```cedar
permit (principal, action == Action::"update", resource is Document)
when { resource.owner == principal || principal in resource.editors }
unless { resource.locked };
forbid (principal, action, resource) when { principal.suspended };
```
Explicit `forbid` overrides `permit`; default is deny. Use via `@cedar-policy/cedar-wasm` or AWS Verified Permissions.

## 3. OPA example
```rego
package app.authz
default allow := false
allow if { input.action == "read"; input.resource.tenant == input.user.tenant }
allow if { "admin" in input.user.roles }
```
Run as a sidecar (`POST /v1/data/app/authz/allow`), embedded via WASM, or as a library. Test with `opa test policies/ -v`.

## 4. Architecture
- **PEP** (enforcement point) in your app/gateway calls the **PDP** (decision point) with principal, action, resource attributes; one middleware, not scattered calls.
- **List filtering** ("show the documents I may read") is the hard part: per-row checks do not scale. Use the engine's partial evaluation / `ListObjects` (OpenFGA) to produce a filter, or keep a coarse SQL filter (tenant, owner) plus engine checks on the page.
- Cache decisions briefly; include policy version in logs.
- Keep authentication out: the engine receives verified identity claims.

## 5. Operate
- Policies in git, reviewed like code, with unit tests for each rule and regression tests for incidents.
- Decision logs (who, action, resource, result, policy version) to your audit pipeline.
- Fail closed when the PDP is unreachable.

## Verify
- [ ] Every protected route calls the PEP (test enumerates routes); policy tests cover allow and deny cases per role.
