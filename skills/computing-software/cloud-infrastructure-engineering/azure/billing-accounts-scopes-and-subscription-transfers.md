---
id: computing-software.cloud-infrastructure-engineering.azure.billing-accounts-scopes-and-subscription-transfers
name: billing-accounts-scopes-and-subscription-transfers
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, billing-scopes, billing-account, subscription-transfer, ea, mca, mpa, enrollment-account, invoice-section, billing-profile, billing-roles, billing-ownership-transfer, change-directory, ea-to-mca, cost-management-scopes, invoices]
level: practitioner
status: draft
description: "Navigate Azure billing scopes (EA departments/accounts, MCA profiles/invoice sections, MPA), assign billing roles, transfer billing ownership, and move a subscription between tenants."
sources: ["Microsoft Learn - Understand and work with scopes (Cost Management)", "Microsoft Learn - Billing roles for Microsoft Customer Agreement", "Microsoft Learn - Transfer billing ownership of an Azure subscription", "Microsoft Learn - Transfer an Azure subscription to a different Microsoft Entra directory", "Microsoft Learn - Azure product transfer hub"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Billing accounts, scopes and transfers — know which lever moves money vs. access

**Goal:** the right people can see invoices and create subscriptions, cost is attributable to
the right department, and a subscription can be moved between billing owners or tenants
without losing resources.

## 1. The three agreement shapes
| | EA | MCA | MPA (CSP) |
|---|---|---|---|
| Top | Billing account = enrollment | Billing account | Billing account (partner) |
| Middle | Department → Enrollment account | Billing profile (invoice) → Invoice section | Customer |
| Who creates subs | Enrollment account owner | Invoice section owner/contributor, *Azure subscription creator* | Partner admin agent |
| Portal roles | EA admin, Department admin, Account owner (EA portal/Cost Management + Billing) | Billing account/profile/invoice section Owner, Contributor, Reader, Invoice manager | Partner Center |
```bash
az billing account list -o table
az billing account show --name <BA-ID> --expand "soldTo,billingProfiles,billingProfiles/invoiceSections"
az billing role-assignment list --account-name <BA-ID>          # MCA billing roles
az billing invoice list --account-name <BA-ID> --profile-name <BP-ID> --period-start-date 2026-01-01 --period-end-date 2026-10-01
```
Billing roles are **not** Azure RBAC: an MCA billing account Owner has no access to resources,
and a subscription Owner cannot see invoices unless given a billing reader role (or Cost
Management Reader on the subscription for cost, not invoices).

## 2. Map cost ownership to scopes
- Department (EA) / invoice section (MCA) = the unit that gets a separate invoice line or budget.
  Create one per business unit; put each subscription under the right one at creation.
- Cost Management scopes: billing account → department/profile → enrollment account/invoice
  section → subscription → RG. Budgets at invoice-section scope catch a whole BU.
- Moving a subscription between invoice sections (MCA) is a billing change with no resource impact:
  Cost Management + Billing → Subscriptions → *Change invoice section*; EA equivalent is
  *Change account owner* (transfers to another enrollment account owner in the same enrollment).

## 3. Transfer billing ownership (different billing owner, same or different tenant)
Cost Management + Billing → Billing scopes → subscription → **Transfer billing ownership** →
recipient email → they accept within 2 weeks (needs matching agreement types; see the product
transfer hub matrix: EA→EA, EA→MCA, MOSP→MCA supported; MCA→EA via support).
What transfers: resources, RBAC (when staying in the tenant). What does **not**: reservations
and savings plans must be moved separately (*Reservations → Change scope/ownership*), Marketplace
subscriptions may not, support plans stay with the sender, classic resources must be migrated first.

## 4. Change the subscription's directory (tenant)
Subscription → **Change directory** (needs Owner on the subscription + a user that exists in
the target tenant, and *Subscription policy* "Subscriptions entering/leaving directory" permitting it).
Breaks: **every RBAC assignment**, managed identities (system-assigned must be recreated;
user-assigned must be recreated), Key Vault access policies/RBAC, AKS Entra integration,
SQL Entra admin, Policy assignments' identities, Lighthouse. Checklist before: export role
assignments (`az role assignment list --all -o json > rbac.json`), list managed identities
(`az resource list --query "[?identity!=null].{id:id,type:identity.type}"`), record Key Vault
tenant id (`az keyvault show --query properties.tenantId`), then after the move update
`az keyvault update --tenant-id` isn't supported — vault must be recovered via the documented
"change tenant" procedure. Only do this for near-empty subscriptions; otherwise redeploy.

## 5. Cancel / reactivate
`az account subscription cancel --id <id>` (Owner, or billing role): resources are disabled
after cancellation and deleted after 90 days; reactivate within that window via portal.
Disabled-for-non-payment subscriptions reactivate on payment, keep resources for the grace period.

## Gotchas
- An EA with "Dev/Test" offer subscriptions cannot transfer those to MCA invoice sections directly; convert offer first.
- Transferring to a recipient in another tenant also *changes directory* implicitly — all the breakage in §4 applies.
- EA enrollment renewals/transfers to a new enrollment number keep subscription ids but reset enrollment-account owners.
- MCA invoice section Contributor can't create subscriptions unless also *Azure subscription creator*.
- Cost exports and budgets at the old scope keep running against nothing after a transfer; recreate at the new scope.

## Verify
- [ ] `az billing role-assignment list` shows named groups (not individuals) as billing account Owners, and at least two.
- [ ] Every subscription appears under a department/invoice section that matches its `costCentre` tag.
- [ ] After a transfer: `az account show --subscription <id>` shows the expected `tenantId`/`managedByTenants`; reservations re-scoped; RBAC re-applied from the export.
