---
id: computing-software.cloud-infrastructure-engineering.google-cloud.creating-the-organization-resource-and-org-admins
name: creating-the-organization-resource-and-org-admins
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, organization, resource-manager, org-admins, cloud-identity, landing-zone, organization-resource-setup, organization-administrator-role]
level: practitioner
status: docs-checked
description: "Get a Google Cloud organization node created (Cloud Identity or Workspace domain), assign Organization Administrators via groups, and adopt no-organization projects."
sources: ["https://cloud.google.com/resource-manager/docs/creating-managing-organization", "https://cloud.google.com/resource-manager/docs/migrating-projects-billing", "https://cloud.google.com/docs/enterprise/setup-checklist"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Creating the organization resource and organization administrators

The organization node is not created with a command. It is created automatically once you have a
Google Workspace or Cloud Identity account associated with a domain. Each such account has exactly one
organization resource, and an organization is tied to exactly one domain.

## Steps
1. Sign up for Cloud Identity (or Workspace) with the company domain. Keep the super-admin
   accounts for identity administration only, not day-to-day management.
2. Timing: if you are new to Google Cloud, the organization is created when you sign in to the
   console and accept the terms. If you already use Google Cloud, it is created when you create a
   new project or billing account; earlier projects show under "No organization", which is normal.
   ```bash
   gcloud organizations list            # DISPLAY_NAME=example.com  ID=123456789012
   gcloud organizations get-iam-policy 123456789012
   ```
3. A super admin must assign Organization Administrator (`roles/resourcemanager.organizationAdmin`)
   to a user or group to actively adopt the organization. Create admin groups first and grant
   roles to groups, never users:
   ```bash
   ORG=123456789012
   gcloud organizations add-iam-policy-binding $ORG \
     --member=group:gcp-organization-admins@example.com --role=roles/resourcemanager.organizationAdmin
   gcloud organizations add-iam-policy-binding $ORG \
     --member=group:gcp-organization-admins@example.com --role=roles/orgpolicy.policyAdmin
   ```
4. Move projects created before the organization existed into it, following the "migrating
   projects" page; the gcloud form is
   `gcloud beta projects move <PROJECT> --organization=$ORG`.

## Gotchas
- Registering a domain that already has an organization gives "This domain is already in use".
- On creation, all users in the domain get Project Creator (`roles/resourcemanager.projectCreator`)
  and Billing Account Creator (`roles/billing.creator`) at the organization. The Organization
  Administrator decides when to remove them and tighten policies.
- Organization-level security baseline constraints are enforced automatically on creation.
- Organization Administrator is highly privileged: restrict it to a small group and review its use.

## Verify
- [ ] `gcloud organizations list` shows the domain organization.
- [ ] `get-iam-policy` shows only group principals on organizationAdmin.
- [ ] `gcloud projects list --filter='parent.type!=organization AND parent.type!=folder'` is empty.

## Checked
2026-10-28. Confirmed on the "Creating and managing organization resources" page: one organization per account and
per domain, creation timing, "No organization" projects, default Project Creator and Billing Account Creator
roles, security baseline, "domain already in use", Organization Administrator role id. gcloud commands passed
check_commands. Removed (not on the pages): "within minutes", secondary-domain behaviour, permissions needed to
move a project, claims about super admin self-granting and about deleting the account deleting the organization.
Method: documentation only; no commands were run.
