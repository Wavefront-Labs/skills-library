---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.billing-hierarchy
name: billing-hierarchy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, billing-concepts, billing-hierarchy, payer-account, consolidated-billing, billing-account, enterprise-agreement, microsoft-customer-agreement]
level: practitioner
status: docs-checked
description: "Map and design the billing hierarchy per provider: AWS management and member accounts, Azure EA and MCA billing profiles and invoice sections, Google billing accounts."
sources: ["https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html", "https://learn.microsoft.com/azure/cost-management-billing/manage/view-all-accounts", "https://learn.microsoft.com/azure/cost-management-billing/manage/mca-section-invoice", "https://cloud.google.com/billing/docs/concepts", "https://learn.microsoft.com/azure/cost-management-billing/dataset-schema/cost-usage-details-focus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing account and payer hierarchy

The billing hierarchy decides who gets invoiced, where discounts pool and what scopes cost tools
can see. It is separate from the resource hierarchy (OUs, management groups, folders), and the two
are often confused.

## Per provider
**AWS**
- Every organization in AWS Organizations has a **management account** that pays the charges of all
  member accounts. Consolidated billing gives one bill for the accounts in the same seller of
  record; accounts from several sellers of record get one bill each.
- Combined usage shares volume pricing discounts, Reserved Instance discounts and Savings Plans
  across the organization, at no extra fee.
- Member account bills are informational; the management account may reallocate the extra
  discounts a member receives.
- A member that leaves the organization loses access to the Cost Explorer data generated while it
  was a member; the management account keeps it.
- Billing transfer gives centralised access to cost data and individual consolidated bills from
  several organizations.

**Azure**
- **Enterprise Agreement**: the billing account is the EA enrollment, which holds departments and
  accounts; the invoice is generated at the enrollment scope. Account owners create subscriptions
  billed to the enrollment.
- **Microsoft Customer Agreement**: billing account -> **billing profiles** -> **invoice sections**.
  A billing profile represents an invoice and its payment methods and billing address; one monthly
  invoice per profile. An invoice section groups costs within that invoice (one is created
  automatically per profile). Subscriptions are linked to a profile and section.
- Tiered prices are computed per billing profile; usage is not aggregated across profiles, so many
  profiles can raise the total.
- Reservations with shared scope apply only to subscriptions within a single billing profile.
- You cannot change the invoice section of a reservation, savings plan or seat-based subscription.
  Moving a subscription to another section shows on the next invoice; past invoices are not amended.
- **Microsoft Partner Agreement** (CSP): the partner's billing account holds billing profiles and
  customers; subscriptions are associated to the customer scope.

**Google Cloud**
- A **Cloud Billing account** pays for the projects linked to it. Ownership of a billing account is
  limited to one organization, but a billing account can pay for projects of another organization.
- Projects do not inherit IAM permissions from the billing account they are linked to.
- **Subaccounts** are for resellers: a subaccount is a billing account owned by the reseller's parent
  account, which pays its charges and must be on invoiced billing. Subaccounts group charges on a
  separate section of the invoice.

FOCUS cost data has `BillingAccountId` and `SubAccountId` columns. `SubAccountId` is described as an
identifier for a grouping of resources or services used to manage access or cost; the Azure FOCUS
dataset pairs it with `SubAccountType`, which names the kind of entity it is.

## Design steps
1. One invoice per legal entity that pays, unless finance prefers central payment with
   intercompany chargeback.
2. Keep discount pooling as wide as contracts allow: one management account / billing account per
   provider per group where possible. On Azure MCA, remember sharing stops at the billing profile.
3. Map every subaccount to an owner and cost centre in a maintained table.
4. Restrict billing-admin roles; management accounts run no workloads.
5. Document which hierarchy each tool reads (the AWS management account's data exports, Azure
   exports at billing-account scope, one BigQuery export per billing account).

## Gotchas
- Purchasing commitments in the wrong Azure billing profile limits which subscriptions can use them.
- A member account that leaves an AWS organization loses its view of the history generated inside it.

## Verify
- [ ] A diagram shows management/billing accounts, their children and where discounts share.
- [ ] Every subaccount maps to an owner; the unmapped list is empty or ticketed.

## Checked

Method: docs-checked 2026-11-09 against AWS consolidated billing page, Azure view-all-accounts (partial, key terms), Azure MCA invoice sections page, Google Cloud Billing concepts (searched, not read in full), Azure FOCUS dataset page (SubAccount columns). Removed unconfirmed: per-account discount sharing toggle, cost categories and Billing Conductor, multiple-payer CUR merging, project-to-one-account rule, CUD sharing scope, EA-to-MCA export notes, account-move history note.
