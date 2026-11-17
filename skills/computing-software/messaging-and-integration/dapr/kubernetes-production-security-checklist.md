---
id: computing-software.messaging-and-integration.dapr.kubernetes-production-security-checklist
name: kubernetes-production-security-checklist
category: computing-software
field: messaging-and-integration
product: dapr
tags: [kubernetes, security, mtls, api-token, serviceaccount, seccomp, injector-watchdog]
level: advanced
status: docs-checked
description: "Production hardening for Dapr on Kubernetes: mTLS, API tokens both ways, secret stores, dedicated namespace, automountServiceAccountToken, seccompProfile, injector watchdog."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-production.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page lists settings to verify before production:

1. mTLS is enabled (on by default); consider bringing your own certificates.
2. App to Dapr API authentication: enable token-based authentication so apps are authorised to call the sidecar (api-token).
3. Dapr to app API authentication: enable token authentication so Dapr tells the app it is communicating with an authorised application (app-api-token).
4. Component secrets live in a secret store, not hard-coded in component YAML.
5. Control plane runs in a dedicated namespace such as `dapr-system`.
6. Optionally scope components to specific apps.

Service account tokens: Kubernetes auto-mounts one into every container. Consider `automountServiceAccountToken: false` in pod specs unless the app calls the Kubernetes API or uses Dapr components that do (Kubernetes secret store, Kubernetes Events binding). Dapr does not set it for you. Component secrets stored as Kubernetes secrets and referenced from component YAML do not need the token; only calling the Kubernetes secret store at runtime does.

Injector watchdog: part of the Operator, disabled by default on Kubernetes. It detects pods deployed without the `daprd` sidecar, for example after a total cluster failure, and remediates; see the operator service page for enabling it.

Restricted Pod Security namespaces: the sidecar is injected with no `seccompProfile` by default, so set it through the annotations described in the arguments and annotations reference.

Tracing and metrics are on by default; configure a tracing backend and scrape Prometheus on port 9090, or disable them if you already have your own.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; wording tightened where it went beyond the page, the remaining claims are unchanged.

Method: documentation only; no commands were run.
