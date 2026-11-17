---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-ingress-settings-and-invoker-iam
name: cloud-run-ingress-settings-and-invoker-iam
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run, cloud-run-ingress-settings, cloud-run-invoker, allusers, internal-and-cloud-load-balancing, invoker-iam-check]
level: practitioner
status: docs-checked
description: "Lock down Cloud Run services: ingress all, internal or internal-and-cloud-load-balancing, invoker IAM vs allUsers, disabling the invoker IAM check, private calls."
sources: ["https://docs.cloud.google.com/run/docs/securing/ingress", "https://docs.cloud.google.com/run/docs/authenticating/public", "https://docs.cloud.google.com/run/docs/authenticating/service-to-service"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run ingress settings and invoker IAM

Two independent layers: **ingress** (network path allowed) and **IAM** (`roles/run.invoker`).

## Ingress
```bash
gcloud run services update api --region=<R> --ingress=internal-and-cloud-load-balancing
```
| Value | Allowed sources |
|---|---|
| `all` | internet and everything |
| `internal` | internal Application Load Balancer, VPC networks in the same project, the Shared VPC network the service sends traffic to, resources inside a VPC Service Controls perimeter, and products in the same project or perimeter that use the default `run.app` URL (Cloud Scheduler, Cloud Tasks, Eventarc, Pub/Sub subscriptions, Workflows, BigQuery and others listed on the ingress page) |
| `internal-and-cloud-load-balancing` | everything in `internal` plus the external Application Load Balancer (use for Cloud Armor, IAP, CDN); direct internet requests to `run.app` are not allowed |
Requests from other sources cannot reach the service at the `run.app` URL, a custom URL or a custom domain. Disable the default URL with `--no-default-url` (restore with `--default-url`) to force traffic through the LB.

## Invoker IAM
```bash
# private: only these identities
gcloud run services add-iam-policy-binding api --region=<R> \
  --member=serviceAccount:frontend@<P>.iam.gserviceaccount.com --role=roles/run.invoker
# public
gcloud run services add-iam-policy-binding web --region=<R> --member=allUsers --role=roles/run.invoker
# public by disabling the invoker IAM check (the documented recommendation; works under domain restricted sharing)
gcloud run services update web --region=<R> --no-invoker-iam-check
```
Service-to-service: caller fetches an ID token with audience = the service URL (or custom
audience) and sends `Authorization: Bearer`.

## Patterns
- Public site with WAF: ingress `internal-and-cloud-load-balancing` + `allUsers` invoker (or no IAM check) + Cloud Armor on the LB.
- Internal API: ingress `internal` + invoker granted to caller SAs.
- IAP: ingress via LB, IAP on backend service, grant invoker to IAP service agent.

## Gotchas
- `allUsers` grants fail under a policy that restricts granting roles to `allUsers`: use `--no-invoker-iam-check` instead. Administrators can prevent disabling the check with the managed constraint `constraints/run.managed.requireInvokerIam` (not enforced by default).
- Org policy `run.allowedIngress` restricts which ingress values developers can select.

## Verify
- [ ] `curl` from the internet to `run.app` cannot reach the service; via the LB it returns 200; a caller without `roles/run.invoker` is denied.

## Checked

2026-10-24, Cloud Run ingress and public-access pages on docs.cloud.google.com. Confirmed: the three ingress values and their allowed sources, `--no-default-url`, `--no-invoker-iam-check` as the recommended public option under domain restricted sharing, `constraints/run.managed.requireInvokerIam` (not enforced by default), `run.allowedIngress`, the `allUsers` binding command. Removed the unconfirmed 404/403 status claim and the Private Google Access routing claim.

Method: documentation only; no commands were run.
