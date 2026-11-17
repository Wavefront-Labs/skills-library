---
id: computing-software.cloud-infrastructure-engineering.google-cloud.billing-subaccounts-for-resellers-and-chargeback
name: billing-subaccounts-for-resellers-and-chargeback
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, billing-subaccounts, reseller-billing, chargeback, cloud-billing, billing-account]
level: practitioner
status: docs-checked
description: "Create and manage Cloud Billing subaccounts under a reseller or master billing account to separate customer or business-unit invoices, and query them in billing export."
sources: ["https://cloud.google.com/billing/docs/concepts#subaccounts", "https://cloud.google.com/billing/docs/reference/rest/v1/billingAccounts/create", "https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables", "https://cloud.google.com/sdk/gcloud/reference/billing/budgets/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing subaccounts for resellers and chargeback

A subaccount is a Cloud Billing account owned by a reseller's parent billing account. Subaccounts are
intended for resellers: the usage charges of all subaccounts are paid by the parent account, and the
parent must be on invoiced billing. Charges of projects linked to a subaccount are grouped and
subtotalled on the invoice (or on multiple invoices when split invoicing applies).

## Behaviour
A subaccount behaves like a billing account in most ways: projects can be linked to it, billing data
exports can be configured on it, and IAM roles can be defined on it, so access control can be
fully segregated per customer or chargeback group.

## Create
- Method: `billingAccounts.create` (`POST https://cloudbilling.googleapis.com/v1/billingAccounts`)
  creates billing subaccounts. The optional query parameter `parent` is the parent account in the
  form `billingAccounts/{billing_account_id}`; the request body is a `BillingAccount`.
- The caller needs the `billing.accounts.update` IAM permission on the parent account (typically
  billing account administrators). The method returns an error if the parent account has not been
  provisioned for subaccounts.
- Google Cloud resellers should use the Channel Services APIs (`accounts.customers.create` and
  `accounts.customers.entitlements.create`) rather than this method.
- Link projects to the subaccount with
  `gcloud billing projects link <PROJECT_ID> --billing-account=<SUBACCOUNT_ID>`.
- Suggested split of roles: `roles/billing.user` on the subaccount for the business unit's project
  factory, `roles/billing.viewer` for its finance contact, and `roles/billing.admin` kept on the parent.

## Reporting
- Exports (standard usage cost table `gcp_billing_export_v1_<BILLING_ACCOUNT_ID>`, detailed
  `gcp_billing_export_resource_v1_<BILLING_ACCOUNT_ID>`) can be configured on a subaccount.
- `gcloud billing budgets create` has `--filter-subaccounts=billingAccounts/{account_id}` to
  scope a budget to subaccounts; if set to the parent's own name, parent usage is included; if
  omitted, usage from the parent and all its subaccounts is included.

## Verify
- [ ] The new account lists the intended parent, and linked projects appear under the subaccount in billing reports.

## Checked
Date: 2026-11-07.
Method: documentation only; no commands were run.
Read in full: the "Subaccounts" section of the Cloud Billing concepts page (lines 124-128), the REST `billingAccounts.create` page, and the `billing budgets create` reference page. The BigQuery tables page was read for the table names only. The `BillingAccount` resource page was not opened, so body field names are not asserted.
Corrections: removed the `masterBillingAccount` JSON body (the create page documents a `parent` query parameter), the curl command, the `gcloud billing accounts list --filter=masterBillingAccount:` command, "enterprise agreement" and Partner Advantage claims, "parent export includes all subaccounts" and the `billing_account_id` column claim, the SQL query, "subaccounts cannot have their own payment method", "closing the parent affects all", and the month-split gotcha, none of which the pages state. Added the Channel Services note and the invoiced-billing requirement.
