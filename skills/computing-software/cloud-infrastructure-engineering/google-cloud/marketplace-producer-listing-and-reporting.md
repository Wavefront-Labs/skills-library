---
id: computing-software.cloud-infrastructure-engineering.google-cloud.marketplace-producer-listing-and-reporting
name: marketplace-producer-listing-and-reporting
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-marketplace, marketplace-producer-portal, listing-your-product, marketplace-usage-reporting, marketplace-billing-reports, partner-procurement-api, saas-integration]
level: advanced
status: draft
description: "List a product on Google Cloud Marketplace as a producer: Producer Portal setup, VM/Kubernetes/SaaS technical integration, Procurement API entitlements, usage reporting and disbursement reports."
sources: ["https://cloud.google.com/marketplace/docs/partners", "https://cloud.google.com/marketplace/docs/partners/integrated-saas", "https://cloud.google.com/marketplace/docs/partners/integrated-saas/technical-integration-setup", "https://cloud.google.com/marketplace/docs/partners/reports"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Marketplace producer: listing and reporting

## 1. Prerequisites
- Partner Advantage enrolment and a signed Marketplace agreement; a dedicated **producer project** (with Producer Portal access) separate from your product infrastructure.
- Decide product type: **VM** (image + Terraform deployment), **Kubernetes app** (images + Helm/deployer), or **SaaS** (your service, billed via Google).

## 2. Producer Portal flow
Product details → pricing (free, BYOL, usage-based, subscription/commitment plans) → technical
integration → review submission → publish. Keep marketing copy, support URL and EULA ready —
review rejects incomplete support/legal pages more than code.

## 3. SaaS technical integration
- Signup URL receives a JWT from Google on purchase; verify it, create the customer account, link to the **account ID**.
- Subscribe to the Pub/Sub topic Google provides for entitlement events (`ENTITLEMENT_CREATION_REQUESTED`, `..._ACTIVE`, `..._PLAN_CHANGE_REQUESTED`, `..._CANCELLED`).
- Approve accounts/entitlements via the Partner Procurement API:
```bash
curl -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" \
 "https://cloudcommerceprocurement.googleapis.com/v1/providers/<PROVIDER_ID>/entitlements/<ENT_ID>:approve" -d '{}'
```
- Usage-based plans: report metered usage per entitlement through Service Control `services.report` (hourly is typical), with the usage reporting ID from the entitlement.

## 4. Reports
Producer Portal → Analytics, plus scheduled report files delivered to a **GCS bucket** you designate:
daily usage reports (per customer, SKU, quantity) and monthly disbursement reports (what Google pays you
after fees). Load them into BigQuery and reconcile usage you reported vs usage billed vs disbursed.

## Gotchas
- Failing to approve an entitlement within the window leaves the customer stuck in pending; automate approval.
- Usage reports sent late or duplicated distort customer bills; make reporting idempotent with operation IDs.
- VM image products must pass Marketplace image scanning (no hardcoded credentials, current OS patches).

## Verify
- [ ] Test purchase with a staging listing creates an account and an ACTIVE entitlement end-to-end.
- [ ] Monthly reconciliation query shows < 0.1% difference between reported and billed usage.
