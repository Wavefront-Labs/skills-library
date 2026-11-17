---
id: computing-software.cloud-infrastructure-engineering.external-dns.webhook-provider-api-contract
name: webhook-provider-api-contract
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, webhook-provider, webhook-sidecar, adjustendpoints, webhook-annotations]
level: advanced
status: docs-checked
description: "ExternalDNS webhook provider contract: sidecar layout, routes and ports, negotiation, body and timeout limits, custom annotations and running an in-tree provider as a server."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/webhook-provider.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Webhook provider contract

ExternalDNS runs `--provider=webhook` as an HTTP client; the real provider is a separate program, ideally a sidecar in the same pod listening only on localhost.

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Negotiate `DomainFilter` (reads `Accept`, answers with `Content-Type` naming media type and version) |
| GET | `/records` | Get records |
| POST | `/adjustendpoints` | Provider-specific record adjustments |
| POST | `/records` | Apply changes |

- Provider port 8888, localhost only. Health and metrics: `/healthz` (liveness and readiness) and optional `/metrics` on 8080, bound to `0.0.0.0`.
- Only `20x` is success and only `5xx` is retried. Everything else, including `3xx`, is a failure.
- Bodies are capped at 32 MiB (about 60,000 records); change with `--webhook-provider-max-body-size` (0 disables). The server rejects larger requests with 413.
- `--webhook-provider-read-timeout` plus `--webhook-provider-write-timeout` is the total client round-trip deadline.
- Custom annotations use `external-dns.kubernetes.io/webhook-<custom-annotation>`; authors document the ones they support.

**Run an in-tree provider as a webhook server** (reference/testing): `--webhook-server --provider=aws --source=ingress` (the source is ignored), then run another ExternalDNS with `--provider=webhook`.

Authors must keep in sync with JSON of `plan.Changes`, `endpoint.Endpoint` and `endpoint.DomainFilter`; changes are announced in release notes.

## Checked

2026-11-04. Read the webhook provider tutorial (API guarantees, Implementation requirements, Custom Annotations, running an in-tree provider as a webhook). Confirmed the four routes, ports 8888 and 8080, 20x/5xx retry rule, the 32 MiB cap and 413, the timeout flags, the annotation format and the --webhook-server example. Removed nothing.

Method: documentation only; no commands were run.
