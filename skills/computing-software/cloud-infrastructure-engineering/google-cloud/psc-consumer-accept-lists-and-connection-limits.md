---
id: computing-software.cloud-infrastructure-engineering.google-cloud.psc-consumer-accept-lists-and-connection-limits
name: psc-consumer-accept-lists-and-connection-limits
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-service-connect, psc-consumer-accept-list, psc-connection-preference, service-attachments, accept-manual, connection-limit]
level: practitioner
status: docs-checked
description: "Control who can connect to a PSC published service: ACCEPT_AUTOMATIC vs ACCEPT_MANUAL, consumer accept and reject lists by project or network, connection limits, and approval."
sources: ["https://cloud.google.com/vpc/docs/manage-private-service-connect-services", "https://cloud.google.com/sdk/gcloud/reference/compute/service-attachments/create", "https://cloud.google.com/sdk/gcloud/reference/compute/service-attachments/update", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSC consumer accept lists and connection limits

## Connection preference
- `ACCEPT_AUTOMATIC`: any consumer that knows the attachment URI can connect. Fine internally,
  risky for SaaS.
- `ACCEPT_MANUAL`: only consumers on the accept list connect; others are `PENDING` (or rejected).

```bash
gcloud compute service-attachments create saas-api --region=europe-west2 \
  --producer-forwarding-rule=saas-ilb-fr --nat-subnets=psc-nat-ew2 \
  --connection-preference=ACCEPT_MANUAL \
  --consumer-accept-list=customer-a-prod=10,customer-b-prod=4 \
  --consumer-reject-list=suspicious-project
gcloud compute service-attachments update saas-api --region=europe-west2 \
  --consumer-accept-list=customer-a-prod=20,customer-c-prod=5
```
Accept-list entries are projects or VPC network URLs, each with a **connection limit** (the number of consumer endpoints that can connect). A list cannot mix projects and networks: the accept and reject lists of one attachment contain either only projects or only networks. `update` also accepts individual endpoints (limit optional). The same value in both lists is rejected, and `--consumer-accept-list` on `update` replaces the existing list.

## Reviewing connections
```bash
gcloud compute service-attachments describe saas-api --region=europe-west2 \
  --format="table(connectedEndpoints[].endpoint,connectedEndpoints[].status,connectedEndpoints[].consumerNetwork)"
```
Statuses: `ACCEPTED`, `PENDING`, `REJECTED`, `CLOSED`, and `NEEDS_ATTENTION` (accepted, but the producer must take further action before the endpoint can serve traffic).
By default, list changes affect only new or pending connections: removing a consumer does not drop accepted connections unless connection reconciliation is enabled (`--reconcile-connections` on create or update, `--no-reconcile-connections` to disable).

## Onboarding flow for SaaS
1. Customer sends project ID (or VPC URL).
2. Add to accept list with a limit.
3. Customer creates endpoint (`gcloud compute forwarding-rules create ... --target-service-attachment=ATTACHMENT_URI`).
4. Verify `ACCEPTED`; share DNS name conventions.

## Gotchas
- The attachment's NAT subnets need enough free addresses for each accepted endpoint; otherwise the update fails with an insufficient IPv4 capacity error, so add or expand a NAT subnet first.
- Organization policy can override acceptance: constraint `constraints/compute.restrictPrivateServiceConnectProducer` ("Restrict allowed Private Service Connect Producers") limits which service attachments consumers may connect to, and `constraints/compute.restrictPrivateServiceConnectConsumer` limits which consumers may connect to a producer's attachments.
- `--enable-proxy-protocol` turns on the PROXY protocol for the attachment.

## Verify
- [ ] A non-listed project's endpoint stays PENDING or is REJECTED; a listed one is ACCEPTED within the limit.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: the create example mixed a project and a network URL in one accept list, which the gcloud reference forbids (lists contain only projects or only networks). NEEDS_ATTENTION was described as NAT exhaustion; the Compute API describes it as an accepted connection where the producer must take further action. The old sources entry for connection preference was a dead anchor and was replaced.
- Confirmed (gcloud reference, service-attachments create/update): --connection-preference ACCEPT_AUTOMATIC (default) and ACCEPT_MANUAL, --consumer-accept-list PROJECT_OR_NETWORK=LIMIT, --consumer-reject-list, --reconcile-connections and --no-reconcile-connections, --enable-proxy-protocol, endpoint entries on update.
- Confirmed (Compute API discovery document): connection status values ACCEPTED, CLOSED, NEEDS_ATTENTION, PENDING, REJECTED. Confirmed (service attachment management page): reconciliation behaviour, accept-and-reject conflict rule, NAT subnet capacity error, organization policy override.
- Confirmed (organization policy constraints list): compute.restrictPrivateServiceConnectProducer and compute.restrictPrivateServiceConnectConsumer and what each restricts.
- Removed: the claim that PROXY protocol gives per-tenant connection IDs (not in the pages read).

Method: documentation only; no commands were run.
