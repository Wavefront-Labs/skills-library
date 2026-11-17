---
id: computing-software.cloud-infrastructure-engineering.google-cloud.removing-default-project-creator-and-billing-creator-grants
name: removing-default-project-creator-and-billing-creator-grants
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, default-org-roles-cleanup, project-creator-role-removal, billing-account-creator, domain-wide-grants, resource-manager, iam]
level: practitioner
status: docs-checked
description: "Replace the domain-wide Project Creator and Billing Account Creator roles a new Google Cloud organization grants with named principals, once an Organization Administrator exists."
sources: ["https://cloud.google.com/resource-manager/docs/default-access-control", "https://cloud.google.com/resource-manager/docs/creating-managing-organization#adding_an_organization_administrator", "https://cloud.google.com/billing/docs/how-to/billing-access"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Removing default Project Creator and Billing Account Creator grants

When the organization resource is created, all users in your domain get Project Creator
(`roles/resourcemanager.projectCreator`) and Billing Account Creator (`roles/billing.creator`) at the
organization level, so they can keep creating projects without disruption. Google says these defaults
are not intended for day-to-day operations. Billing Account Creator can create self-serve billing
accounts (permissions `billing.accounts.create`, `resourcemanager.organizations.get`) and Google
advises minimizing who has it to prevent untracked cloud spend.

## Steps
1. A Google Workspace or Cloud Identity super administrator assigns the Organization Administrator
   role (`roles/resourcemanager.organizationAdmin`) to a user or group, ideally not themselves
   (separation of duties). In gcloud:
   ```bash
   gcloud organizations add-iam-policy-binding ORGANIZATION_ID \
       --member="user:EMAIL_ADDRESS" \
       --role="roles/resourcemanager.organizationAdmin"
   ```
   `gcloud organizations list` shows organization IDs. That role does not include creating folders or
   projects; the administrator needs further roles for that.
2. Grant Billing Account Creator and Project Creator to the principals you designate (console: Manage
   resources, select the organization, Info Panel > Permissions, add the principal, pick
   Billing > Billing Account Creator or Resource Manager > Project Creator, Add). Billing Account
   Creator is also what a user needs to migrate existing billing accounts into the organization.
3. Remove the defaults (console: same page, expand the role under Permissions, click remove next to
   the domain principal, confirm in "Remove principal?", repeat for each role).

Do step 2 before step 3 so people who need the roles keep a path.

## Gotchas
- If you cannot view the organization resource you can still create projects and billing accounts;
  they land under the organization anyway.
- Removing the roles restricts creation going forward; the page says nothing about projects or
  billing accounts users already created, so inventory those separately.

## Verify
- [ ] The organization's IAM page no longer lists the domain under Project Creator or Billing Account
      Creator, and the designated principals are listed instead.

## Checked
Date: 2026-11-07.
Method: documentation only; no commands were run.
Read in full: "Managing default organization roles" (grant and removal console steps), the "Set up a Google Cloud organization resource" page through the add-Organization-Administrator section (default grants, super administrator guidance, console and gcloud steps), and the Billing Account Creator lines of the billing access page (searched by keyword; role description and permissions).
Corrections: removed the `gcloud organizations remove-iam-policy-binding` and `get-iam-policy` commands (no cited page shows them), the `gcp-project-creators` group examples, the project-factory/Terraform advice and the 0-bootstrap module claim, the `gcloud asset search-all-resources` inventory command, the "creators keep Owner" and "PERMISSION_DENIED" assertions, and the `domain:` member filter, none of which the cited pages confirm.
