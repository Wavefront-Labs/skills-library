---
id: computing-software.cloud-infrastructure-engineering.google-cloud.linking-and-changing-a-project-billing-account
name: linking-and-changing-a-project-billing-account
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, link-billing-account, billing-account-linking, change-billing-account, billing-account, gcloud-billing-projects-link, billing-user, resourceassociations, billing-disabled, multiple-billing-accounts]
level: practitioner
status: docs-checked
description: "Link, re-link and unlink projects to billing accounts with gcloud billing projects link, with the exact IAM pair needed and what breaks when a project has no billing."
sources: ["https://cloud.google.com/billing/docs/how-to/modify-project", "https://cloud.google.com/sdk/gcloud/reference/billing/projects/link", "https://cloud.google.com/sdk/gcloud/reference/billing/projects/unlink", "https://cloud.google.com/sdk/gcloud/reference/billing/projects/list", "https://cloud.google.com/billing/docs/how-to/billing-access"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linking and changing a project's billing account

**Goal:** move projects between billing accounts (new cost centre, reseller change, sandbox to
prod) without a service outage and without handing out billing admin.

## 1. The IAM pair
You need permissions on both the project and the billing account.
| Action | Billing account | Project |
|---|---|---|
| Link to the target account | `billing.resourceAssociations.create` (Billing Account User or Administrator) | `resourcemanager.projects.createBillingAssignment` (Project Billing Manager or Project Owner), plus `serviceusage.services.list` and `serviceusage.effectivepolicy.get` |
| Unlink from the current account | `billing.resourceAssociations.delete` (Billing Account Administrator) **or** | `resourcemanager.projects.deleteBillingAssignment` (Project Billing Manager or Project Owner) |

Predefined role sets the page names: on the project, Project Billing Manager + Project Browser +
Service Usage Viewer, or Project Owner; on the current and target accounts, Billing Account User +
Billing Account Viewer, or Billing Account Administrator. A Billing Account Administrator granted
at organization level is enough. Linking is a sensitive action and may ask you to reauthenticate.

## 2. Commands
```bash
gcloud billing projects list --billing-account=<ACCOUNT_ID>   # projects linked to an account
gcloud billing projects describe <PROJECT_ID>                 # billing info for a project
gcloud billing projects link <PROJECT_ID> --billing-account=<ACCOUNT_ID>
gcloud billing projects unlink <PROJECT_ID>                   # disables billing
```
`gcloud billing accounts list` lists account IDs. To move a project, run `link` against the new
account: you do not need to unlink first, and Google says switching should not cause service
interruption. Charges up to the switch go to the former account (move on May 15: May 1-15 to the old
account, May 16-31 to the new), and some charges can take up to two days to be reported.

## 3. What happens with no billing account
Unlinking (or a closed or suspended account) disables billing: all billable Google Cloud services in the
project stop and some resources might be removed and not recoverable, so back up first. Re-enabling
can take up to 24 hours for resources to start, and some services need a manual restart. A project
that hosts a Shared VPC takes its service projects' dependent instances down with it. You cannot
disable billing on a project with active or pending committed use discounts. This is the mechanism
behind budget "kill-switch" automation (see `billing-kill-switch-disable-billing-on-budget`).

## 4. Before moving a project
- **Committed use discounts**: resource-based commitments move with the project and apply only in the
  destination account, to that project alone unless the destination has CUD sharing enabled; a
  prioritized attribution setup may need updating, and CUDs apply to the new account from midnight
  US and Canadian Pacific time (UTC-8).
- **Costs not tied to a project** (for example Support) stay on the account; find them under
  "[Charges not specific to a project]" in the Cost table or Reports.
- **Marketplace purchases** attached to the project must be transferred first.
- **Cloud Armor Enterprise Annual**: moving to an account without the subscription reverts the
  project to Cloud Armor Standard.
- Locked links (padlock in Account management) must be unlocked before changing.
- Switching to another customer's billing account to avoid fees can violate your terms.

## Gotchas
- Re-enabling billing on a recently restored project can fail with "User missing permission
  'resourcemanager.projects.createBillingAssignment'" until the project propagates; retry after about
  10 minutes, then a few hours; in rare cases up to 36 hours.
- Budgets and billing exports belong to a billing account (see `billing-accounts-and-budgets`).

## Verify
- [ ] `gcloud billing projects list --billing-account=<NEW_ACCOUNT_ID>` includes the project.
- [ ] Console Billing > My projects shows the new account and not "Billing is disabled".

## Checked
Date: 2026-11-07.
Method: documentation only; no commands were run.
Read in full: "Enable, disable, or change billing for a project" lines 1-170 (change account, permissions, enable billing, restored-project error, disable billing impact for Google Cloud and Shared VPC; the Firebase and AI Studio parts and later sections were not read), and the gcloud reference pages for `billing projects link`, `unlink`, `list` and `describe` (link read from API reference onward, with the synopsis seen by the command checker).
Corrections: `gcloud billing accounts projects list` is alpha-only (the command checker reported no GA command), replaced by `gcloud billing projects list --billing-account`; the IAM section corrected (unlink needs either the account or the project permission, not "project only"; link also needs service usage permissions); removed "within minutes", the list of services that stop, "buckets read-only-ish", the `403 ... billing account ... disabled` error string, "VMs do not auto-restart" (page: up to 24 hours and manual restarts), "free-tier APIs keep working", the Terraform note, the org policy aside, the reseller `accounts list` tip, the "no hint about which side" error, and the claim that exports move rows to the new account's table; the CUD gotcha was reversed (CUDs move with the project).
