---
id: computing-software.cloud-infrastructure-engineering.google-cloud.marketplace-procurement-governance-and-request-approval
name: marketplace-procurement-governance-and-request-approval
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-marketplace, marketplace-procurement-approval, marketplace-request-procurement, private-marketplace, consumer-procurement]
level: practitioner
status: docs-checked
description: "Govern Cloud Marketplace purchases: Consumer Procurement roles, request-procurement approvals, Private Marketplace curation, and billing account control."
sources: ["https://cloud.google.com/marketplace/docs/access-control", "https://cloud.google.com/marketplace/docs/governance/private-marketplace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Marketplace procurement governance and request approval

Marketplace purchases bill to a Cloud Billing account and can commit spend (SaaS plans, private
offers). Without controls, whoever holds purchasing roles on the billing account can subscribe.

## Roles
| Role | Purpose | Assign at |
|---|---|---|
| `roles/billing.admin` (Billing Account Administrator) | Google recommends it for users who purchase from Cloud Marketplace, so restrict who holds it | billing account |
| `roles/consumerprocurement.orderAdmin` | Manage purchases (place, modify, cancel orders) | billing account or organization |
| `roles/consumerprocurement.orderViewer` | Inspect purchases | billing account or organization |
| `roles/consumerprocurement.entitlementManager` | Manage entitlements and enable or disable services for a consumer project; required for most products | project or organization |
| `roles/consumerprocurement.entitlementViewer` | Inspect entitlements and service states | project or organization |
| `roles/consumerprocurement.procurementAdmin` | Manage purchases and consents at billing account and project level | per the roles table |

- Users who access the purchased services need the Viewer role at a minimum.
- A few products (Google Cloud Dataprep by Trifacta, Neo4j Aura Professional, Redis Enterprise Cloud) require the Project Editor role in the project.
- Grant billing-account roles to a small procurement group only. Granting at billing account level needs `roles/billing.admin`; at organization level it needs `roles/resourcemanager.organizationAdmin`.
- Custom roles are supported for finer control.

## Private Marketplace
- Private Marketplace holds curated lists of products, called collections, available to chosen projects and folders or to the whole organization.
- It is turned on and off at the organization level. When on, users can only access products in collections shared with them and cannot deploy products that have not been shared.
- Admin roles: `roles/commerceorggovernance.admin` and `roles/resourcemanager.organizationViewer`, both at organization level, to turn it on and to manage collections.
- Google recommends turning on **Product Requests** so users can request access to specific products instead of working around the block.
- Supported: third-party ISV listings. It blocks API deployment of unapproved Kubernetes apps and container images on GKE (version 1.32.1-gke.1376000 or later), container images on Cloud Run, virtual image disk creations, procurable Vertex AI models and procurable BigQuery datasets. Not supported: Google-provided public OS images, Google-provided public datasets, and products owned and managed by Google.
- Approval of a procurable Vertex AI model cannot be revoked: users can still procure it.
- GKE images deployed from non-Marketplace repositories by tag are not blocked; use Binary Authorization for those.

## Verify
- [ ] A user without procurement roles cannot place an order on the billing account.
- [ ] A user outside the shared collections cannot see or deploy an unapproved product, and can submit a product request.

## Checked
2026-11-09. Confirmed in the Cloud Marketplace access-control page (role IDs, recommended Billing Account Administrator, assign levels, Project Editor products, Viewer minimum, who can grant) and the Private Marketplace page (collections, organization-level toggle, admin roles, Product Requests recommendation, supported and unsupported products, Vertex AI revocation note, Binary Authorization note). Removed: the request-products page (404), the `commerceorggovernance.marketplaceServices` and `compute.trustedImageProjects` constraint advice, the billing-export seller_name filter and the commit-eligibility claim (not on the pages read).
Method: documentation only; no commands were run.
