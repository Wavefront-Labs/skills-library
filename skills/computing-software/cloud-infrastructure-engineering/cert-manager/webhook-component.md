---
id: computing-software.cloud-infrastructure-engineering.cert-manager.webhook-component
name: webhook-component
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [webhook, admission, validation, mutation, conversion, cert-manager-webhook-ca]
level: intro
status: docs-checked
description: "Know what the cert-manager webhook does (validation, defaulting, conversion), how it manages its own CA and serving cert, and which platforms break it."
sources:
  - https://cert-manager.io/docs/concepts/webhook/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The webhook is a separate pod beside the controller and cainjector. It provides:
- Validation: rules beyond OpenAPI, for example rejecting an Issuer with more than one issuer type.
- Mutation/defaulting: changes resources on create and update, such as setting defaults.
- Conversion: serves the `cert-manager.io` API versions from `v1alpha2` through `v1`.

TLS: the API server must trust the webhook's serving certificate. The webhook creates `secret/cert-manager-webhook-ca` in its namespace holding a self-signed root CA that signs the serving certificate. Either supply cert and key files signed by that CA, or reference the CA Secret and let the webhook generate its certificate at startup. Dynamically generated certificates renew automatically; from cert-manager 1.21 renewal survives system suspend and VM live migration.

Known failure modes:
- GKE private cluster: the webhook runs but the API server cannot reach it.
- AWS EKS with custom CNI (Weave, Calico): control plane and workers use different CNIs; run the webhook on the host network.
- Shortly after install: transient API errors while the webhook performs leader election and creates its CA and certificate, and cainjector does its own election and then updates `caBundle`. Retry, or gate on post-install checks such as `kubectl --dry-run`.

The page does not specify failure policy or listening port. For fixes see the webhook troubleshooting skill.

## Checked

2026-11-03: Confirmed against the webhook concepts page: validation, mutation/defaulting and conversion (v1alpha2 through v1), the separate pod, `secret/cert-manager-webhook-ca` and the two TLS configuration options, automatic renewal and the 1.21 suspend and live-migration resilience, the GKE private cluster and EKS custom CNI host network problems, and the post-install leader election and caBundle delay with `kubectl --dry-run` checks. Nothing removed.

Method: documentation only; no commands were run.
