---
id: computing-software.cloud-infrastructure-engineering.cert-manager.dns01-webhook-solver
name: dns01-webhook-solver
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [webhook-solver, groupname, solvername, dns01, external-provider, out-of-tree]
level: practitioner
status: docs-checked
description: "Wire an out-of-tree DNS01 provider into a cert-manager ACME issuer through the webhook solver using groupName, solverName and a provider-specific config."
sources:
  - https://cert-manager.io/docs/configuration/acme/dns01/webhook/
  - https://cert-manager.io/docs/configuration/acme/dns01/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The webhook solver is a generic ACME solver: the work is done by an external service. It is configured at `spec.acme.solvers[].dns01.webhook` on an Issuer or ClusterIssuer (`apiVersion: cert-manager.io/v1`).

Required fields:
- `groupName`: the webhook's API group name
- `solverName`: the solver name inside that webhook

`config` carries provider-specific settings; its schema depends on the provider and is not defined by cert-manager's page, so read the provider's own docs. The page's example is a template with placeholders, not an applyable manifest.

Not covered on the page: how a webhook solver is installed, or valid `groupName` and `solverName` values. Those come from the webhook's own documentation (the DNS01 overview lists community webhooks such as alidns, gandi, hetzner, ovh, pdns and scaleway). To find others, search GitHub for the `cert-manager-webhook` topic. To write a new provider, see the development documentation linked from the DNS01 overview.

Practical rule: treat `groupName` and `solverName` as values copied from the provider's own documentation, not guessed.

## Checked

2026-11-03. Confirmed on the cert-manager Webhook page (configuration/acme/dns01/webhook) and the DNS01 overview: webhook is a generic solver done by an external service, groupName and solverName are required, config is provider specific, the GitHub topic, listed providers. Removed: the claim of about 40 webhooks (not stated) and the deploy-and-register-first rule (not on the page).
Method: documentation only; no commands were run.
