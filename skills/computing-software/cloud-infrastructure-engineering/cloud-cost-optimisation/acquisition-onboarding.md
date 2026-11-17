---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.acquisition-onboarding
name: acquisition-onboarding
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-onboarding, acquisition-onboarding, mergers-and-acquisitions, billing-consolidation]
level: advanced
status: docs-checked
description: "Onboard an acquired company's cloud estate into FinOps: discovery, billing consolidation (AWS invitations, Azure transfers), commitments, allocation mapping."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_invites.html", "https://learn.microsoft.com/azure/cost-management-billing/manage/billing-subscription-transfer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Onboarding acquired company cloud estates

## Steps
1. **Discovery**: providers and billing accounts, monthly spend and trend, active commitments (RIs, savings plans, CUDs,
   reservations) with expiry, enterprise agreements and remaining obligation, marketplace contracts, SaaS, support
   plans, resellers, tagging and allocation maturity.
2. **Read-only access first**: cross-account read roles or billing exports shared to your data platform so FinOps
   reporting starts before any migration.
3. **Contracts**: check change-of-control and assignment clauses; whether commitments and discounts can transfer or
   merge with yours; time consolidation to renewal dates.
4. **Billing consolidation** (per provider; confirm in current docs):
   - AWS: the management account invites the existing account; the account owner accepts. Invitations must be answered
     within 15 days or expire, and an account can only join one organization. After acceptance the management account
     becomes responsible for all charges and the member's own payment method is no longer used. Billing history and
     reports (Cost and Usage Reports, Cost Explorer, Savings Plans and RI reports) stay with the management account of
     the organization, so export what you need before moving. `OrganizationAccountAccessRole` is not created
     automatically for an invited account; add it if you want administrative access. Policies on the root or OU apply
     immediately, and organisation-level services (such as CloudTrail organization trails) can extend to the new
     account and duplicate existing account-level setups.
   - Azure: the transfer page covers MOSP (pay-as-you-go) subscriptions, moved by the account administrator; Enterprise
     Agreement customers have their enterprise administrator transfer billing ownership between accounts. Read the
     subscription and reservation transfer hub first to confirm your transfer type is supported; subscriptions cannot be
     transferred to a Microsoft Entra B2B or Azure B2C tenant.
5. **Allocation mapping**: map acquired accounts and tags to your business units and cost centres; apply your tag policy
   with a grace period.
6. **Governance**: apply guardrails and budgets progressively; keep their team engaged as owners.
7. **Synergy tracking**: report savings from consolidated discounts, removed duplicate tools and rationalised commitments.

## Gotchas
- Moving accounts mid-term can strand reservations or break reseller agreements; sequence moves around renewals.
- Applying strict organisation policies on day one can break production workloads built under different assumptions.

## Verify
- [ ] Acquired spend is visible in FinOps reporting within the time you set for the integration.
- [ ] Contract and commitment register for the acquired estate is complete.

## Checked
2026-11-09: confirmed the AWS invitation behaviour (15 days, one organization, charges, billing history, role, policy
and service extension) on the AWS Organizations invitations page and the Azure MOSP/EA transfer points on the Learn
billing transfer page. Removed: GCP project moves, "commitment sharing follows org settings", the 30-day targets, and
the FinOps onboarding-workloads source (404).
Method: documentation only; no commands were run.
