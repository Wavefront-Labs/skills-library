---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.billing-tenant-design
name: billing-tenant-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, billing-tenant-design, billing-account, enterprise-agreement, mca, aws-organizations-management-account, entra-tenant, caf-design-area]
level: practitioner
status: draft
description: "Design the billing and tenant layer of a landing zone: billing accounts and agreements, management account, Entra tenant count, invoice sections and who can create subscriptions."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/azure-billing-ad-tenant", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html", "https://cloud.google.com/billing/docs/concepts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Billing and tenant design area

## Decisions
| Decision | Guidance |
|---|---|
| Number of identity tenants (Entra ID) / organisations | One for production estate unless legal separation requires more; separate tenants complicate identity and policy |
| Billing agreement | Azure EA / MCA / CSP; AWS Organizations consolidated billing via management account; Google Cloud billing account(s) linked to org |
| Management/payer account | AWS management account runs nothing but org/billing; restrict access tightly |
| Invoice structure | Azure MCA billing profiles and invoice sections per business unit / legal entity |
| Who creates subscriptions/accounts | Automation (vending) with a service identity, not individuals |
| Currency and legal entity | Per billing profile or billing account where entities invoice separately |

## Steps
1. Gather legal entity, invoicing and cost centre requirements from finance.
2. Choose tenant/org count (document why if >1).
3. Set up billing structure and roles (billing admin, invoice reader) with least privilege.
4. Enable cost exports from the billing scope on day one.
5. Delegate subscription/account creation to the vending pipeline.

## Gotchas
- Using the AWS management account for workloads (SCPs do not apply to it).
- Multiple Entra tenants created by accident through trials; consolidate early.
- CSP arrangements may limit some features (e.g. certain reservations, support plans).

## Verify
- [ ] Billing roles reviewed; no personal accounts as sole billing owner.
- [ ] Cost export from the top billing scope running.
