---
id: computing-software.cloud-infrastructure-engineering.gateway-api.backendtrafficpolicy-retry-budget
name: backendtrafficpolicy-retry-budget
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [backendtrafficpolicy, retryconstraint, retry-budget, budgetpercent, policy-attachment, experimental]
level: advanced
status: docs-checked
description: "Cap retry storms with BackendTrafficPolicy RetryConstraint: a retry budget as a percentage of active requests, a 503 when exceeded, targeting Services (Experimental)."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/policy/backendtrafficpolicy.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-retries.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`BackendTrafficPolicy` is Experimental channel since v1.3.0. It configures client behaviour toward a backend and is a **Direct Policy Attachment**.

Purpose: HTTPRoute `retry` says whether and how often a request may be retried; a **retry budget** is a fail-safe limiting the *overall* volume of retries to a backend so excessive retries do not cause cascading failure or retry storms.

Spec:

- `targetRefs`: required; valid targets are backends (Service, ServiceImport or an implementation-specific backendRef) by name, kind and group. Currently targetRefs cannot be scoped to specific ports.
- `retryConstraint`: `budget` (`budgetPercent`, `budgetInterval`) and `minRetryRate`.
- `sessionPersistence`: session persistence for the backend.

Behaviour:

- The budget is the percentage of active request volume that may be retries over the interval.
- Retrying the same original request several times counts each retry toward the budget.
- Once exceeded, further retries to that backend are rejected and **MUST return 503** to the client.
- All Routes that target the referenced backend should respect the policy.

Status: `status.ancestors` lists, per parent reference, the controller name and conditions (`PolicyAncestorStatus`).

## Checked

2026-11-04. Confirmed on the Gateway API BackendTrafficPolicy reference (backendtrafficpolicy.md): Experimental channel since v1.3.0, Direct Policy Attachment, retry budget semantics, 503, spec fields, targetRefs limits, ancestor status. Removed the XBackendTrafficPolicy kind remark, the pairing advice and the implementation-support tip (not on the page).

Method: documentation only; no commands were run.
