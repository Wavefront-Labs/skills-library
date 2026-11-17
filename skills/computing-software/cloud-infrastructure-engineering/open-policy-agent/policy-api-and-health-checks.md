---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.policy-api-and-health-checks
name: policy-api-and-health-checks
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [rest-api, policy-api, health-api, readiness, bundle-activation]
level: practitioner
status: docs-checked
description: "Manage policies through PUT /v1/policies/<id> and its bundle-ownership limit, and wire /health with bundles and plugins parameters into Kubernetes-style readiness checks."
sources:
  - https://www.openpolicyagent.org/docs/rest-api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: push policy for development and gate traffic on OPA readiness.

Policy API: `PUT /v1/policies/<id>` with `Content-Type: text/plain` creates a policy module or replaces it if it exists. The server parses, compiles and installs the module before accepting it, and returns 400 if any step fails. Status codes are 200, 400 and 500. Query parameters are `pretty` and `metrics` (compiler performance metrics).

Limits: bundles are the preferred way to update policies, offering eventually consistent updates and better support for multi-instance deployments. If a package path is owned by a loaded bundle, the Policy API cannot update that path.

Health API: `GET /health` runs a simple built-in policy query to check the server operates.
- `?bundles` also requires all configured bundles (including discovery bundles) to have activated
- `?plugins` also requires all plugins to be in an OK state
- `exclude-plugin=<name>` (repeatable) removes a plugin from the check; it does nothing without `plugins`

```
GET /health?plugins&exclude-plugin=decision-logs&exclude-plugin=status
```

200 means healthy, returning `{}`. 500 means not healthy; with `bundles` the body names them, for example `{"error": "one or more bundles are not activated: authz, data"}`.

Caveat: the bundle check covers only initial activation. Later download failures do not change the result, so use the Status API (see status-reporting-api) for fine-grained bundle monitoring.

Use `/health?bundles` as a readiness probe so traffic is not routed to an instance still holding no policy.

Check: start OPA with a bundle URL that is unreachable and confirm `/health?bundles` returns 500 naming the bundle.

## Checked

2026-11-04. Confirmed against the OPA docs REST API page: Create or Update a Policy (text/plain, parse-compile-install with 400 on failure, status codes 200/400/500, pretty and metrics parameters, bundle preference, package paths owned by a bundle cannot be updated) and the Health API (bundles including discovery bundles, plugins, exclude-plugin repeatable and ignored without plugins, 200 returning {}, 500 with the bundles-not-activated error, initial activation only and the Status API for finer monitoring). The Check line is a suggested exercise, not a documented example. Nothing removed.

Method: documentation only; no commands were run.
