---
id: computing-software.cloud-infrastructure-engineering.azure.subscription-rename-cancel-reactivate-and-delete
name: subscription-rename-cancel-reactivate-and-delete
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, subscriptions, subscription-rename, subscription-cancel, subscription-reactivate, subscription-states, decommission]
level: practitioner
status: docs-checked
description: "Rename, cancel, reactivate and delete Azure subscriptions: pre-cancel checklist, what cancellation does, delete conditions, retention windows and subscription states."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/manage/cancel-azure-subscription", "https://learn.microsoft.com/azure/cost-management-billing/manage/subscription-states", "https://learn.microsoft.com/cli/azure/account/subscription"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subscription rename, cancel, reactivate and delete

**Goal:** decommission (or recover) a subscription without surprise data loss or orphaned billing.

## CLI (experimental account extension)
The `az account subscription` group is part of the `account` extension (Azure CLI 2.38.0 or higher), installs on first use, and is marked experimental. Commands: `cancel`, `enable`, `list`, `list-location`, `rename`, `show`. All take `--id`/`--subscription-id`; `rename` takes `--name`/`--subscription-name`/`-n`; `cancel` has `--yes`/`-y` to skip the prompt.
```bash
az account subscription rename --subscription-id <subId> --name "sub-payments-prod"
az account subscription cancel --subscription-id <subId>
az account subscription enable --subscription-id <subId>
```

## Before you cancel
Microsoft recommends (not required): back up data, stop running services, consider migrating data, delete all resources and resource groups (needed before a manual delete; immutable blobs can prevent it), and remove the subscription from the `AssignableScopes` of custom roles (updating a role after cancellation may error). Cancel your SaaS subscriptions manually first; only pay-as-you-go SaaS is cancelled automatically.

## Who can cancel
Subscription owner without a condition, for subscriptions from the Azure website sign-up, Enterprise Agreement and Enterprise Dev/Test, and Azure plan and Azure plan for DevTest. An account administrator without the owner role cannot cancel.

## After cancellation
Billing stops immediately (it can take up to 10 minutes to show in the portal). Services are disabled: VMs deallocated, temporary IPs freed, storage read-only. Data is kept; there is no charge for it. After the last subscription is cancelled the billing cycle closes within 72 hours and the final invoice follows. Cancelling a support plan is billed for the rest of the month with no prorated refund. The page says Microsoft waits 30 to 90 days before permanently deleting data, and also that the subscription is automatically deleted 90 days after cancellation.

## Reactivate
A pay-as-you-go subscription cancelled by accident can be reactivated in the portal. For other types, contact support within 90 days of cancellation. Contacting Microsoft Support to remove a subscription allows only seven days to reactivate.

## Delete early
In the portal, select the subscription and Delete (Subscription Owner role needed). The option is unavailable until 3 days after cancel for customer-led subscriptions, or 7 days for field and partner channel subscriptions. The page shows required conditions with green checks: resources deleted (allow about 10 minutes for status to update) and the manual deletion date. Hidden resources can block deletion: Subscriptions > subscription > Resources > Manage view > Show hidden types.

## Subscription states
- Active/Enabled: all operations available.
- Past Due: outstanding payment, still active, all operations available.
- Warned: GET/DELETE only; resources go offline but can be recovered; not charged.
- Disabled: credit expired, spending limit, past-due bill, card problem or explicit cancel; PUT, PATCH and POST disabled, GET/DELETE work; ownership transfer disabled; stays 1 to 90 days by type, then permanently deleted.
- Expired: cancelled; can be reactivated; PUT/PATCH/POST disabled.
- Deleted: no operations.

## Checked
Confirmed against "Cancel and delete your Azure subscription" and "Azure subscription states" (both last updated 2026-06-07) and the `az account subscription` reference, 2026-11-08. Removed: the REST rename call, the "RBAC and policy unchanged" note, the Recovery Services, reservation and private endpoint checklist items, the resource-state-after-reactivation advice, the `az account show` state query, management group and offer-type gotchas, because the pages do not state them.
Method: docs-only read of cited pages, 2026-11-08
