---
id: computing-software.cloud-infrastructure-engineering.google-cloud.psc-endpoint-global-access
name: psc-endpoint-global-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-service-connect, psc-global-access, allow-psc-global-access, cross-region-clients, hybrid-access]
level: practitioner
status: docs-checked
description: "Enable global access on PSC endpoints so clients in other regions or on-prem via other-region attachments reach a regional published service."
sources: ["https://cloud.google.com/vpc/docs/configure-private-service-connect-services", "https://cloud.google.com/sdk/gcloud/reference/compute/forwarding-rules/update", "https://cloud.google.com/sdk/gcloud/reference/compute/forwarding-rules/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSC endpoint global access

A PSC endpoint for a published service is a regional forwarding rule. By default only clients in
the **same region** (VMs, or on-prem via Cloud VPN/Interconnect attachments in that region) can
reach it.

## Enable
```bash
gcloud compute forwarding-rules create saas-ep --region=europe-west2 --network=prod \
  --address=saas-ep-ip --target-service-attachment=ATTACHMENT_URI --allow-psc-global-access
# existing endpoint
gcloud compute forwarding-rules update saas-ep --region=europe-west2 --allow-psc-global-access
gcloud compute forwarding-rules describe saas-ep --region=europe-west2 --format="value(allowPscGlobalAccess)"
```
Now clients in any region of the VPC can connect to the endpoint. You can change only the global access setting of an existing endpoint for a published service; other fields need a new endpoint.

## Design notes
- Traffic from other regions travels to the endpoint's region, adding latency; check Google Cloud pricing for inter-region network charges. Where the producer offers attachments in several regions, consider one endpoint per region.
- PSC endpoints for **Google APIs** use global internal IPs; this flag applies to endpoints for published services.

## Gotchas
- The endpoint IP must come from a regular subnet in the same region as the service attachment.
- Egress firewall rules in the client VPC must allow the endpoint IP.

## Verify
- [ ] A VM in us-central1 connects to the europe-west2 endpoint after enabling; disabled = timeout.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (configure endpoints for published services page): endpoints are available only from their own region by default; `--allow-psc-global-access` on `forwarding-rules create` (API field allowPscGlobalAccess); only the global access field can be updated on an existing endpoint for a published service; the endpoint subnet and region must match the service attachment's region.
- Confirmed (gcloud reference): `forwarding-rules update --allow-psc-global-access`.
- Removed: the on-premises hybrid-attachment claim, the statement that the producer sees no change, the inter-region charge statement and the per-product Cloud SQL note (not found in the pages read).

Method: documentation only; no commands were run.
