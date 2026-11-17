---
id: computing-software.cloud-infrastructure-engineering.google-cloud.support-iam-roles-and-case-access
name: support-iam-roles-and-case-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, customer-care, support-iam-roles, tech-support-editor, support-cases, cloud-support-api]
level: practitioner
status: docs-checked
description: "Control who can open and view Google Cloud support cases: Tech Support Editor and Viewer roles, case sharing risk, and the Cloud Support REST API (v2) for automation."
sources: ["https://cloud.google.com/support/docs/manage-cases#access_control", "https://cloud.google.com/iam/docs/understanding-roles#cloudsupport-roles", "https://cloud.google.com/support/docs/reference/rest"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Support IAM roles and case access

## Roles (Customer Care manage-cases page)
| Role | Purpose |
|---|---|
| `roles/cloudsupport.techSupportViewer` (Tech Support Viewer) | view support cases |
| `roles/cloudsupport.techSupportEditor` (Tech Support Editor) | manage cases: view, create, update, escalate, close |
| `roles/cloudsupport.admin` (Support Account Administrator) | manage the support account and enable case sharing; grant on the organization |

Roles are granted on the project, folder or organization where the case is managed. Support cases can
only be created for organizations and projects. Listing cases for an organization shows all cases for the
organization; listing for a project shows only that project's cases. Anyone with the right roles can
update, reopen and close a case for a resource even if they did not create it.

## Grant at the organization
```bash
gcloud organizations add-iam-policy-binding <ORG_ID> \
  --member=group:gcp-support-openers@example.com --role=roles/cloudsupport.techSupportEditor
gcloud organizations add-iam-policy-binding <ORG_ID> \
  --member=group:gcp-engineers@example.com --role=roles/cloudsupport.techSupportViewer
```

## Case sharing caution
Case sharing lets users inside and outside your organisation follow a case by email and reply to comment.
Google warns that, when enabled, users can share cases with external email addresses; any user with
`cloudsupport.techCases.update` (in Tech Support Editor) can add recipients. Enabling it needs the
Support Account Administrator role on the organization.

## Automation
The Cloud Support API is at `https://cloudsupport.googleapis.com` with v2 and v2beta discovery documents.
The v2 `cases` resource has `create`, `list`, `get`, `patch`, `close`, `escalate` and `search`, plus comment
and attachment resources and `caseClassifications.search` to retrieve valid classifications for creating a
case. The `gcloud` CLI has no `support cases` command group per the command checker, so use client
libraries or REST.

## Hygiene
- Do not paste secrets or personal data into cases.
- Grant roles to groups so removing a leaver removes access.

## Verify
- [ ] Only the support group holds Tech Support Editor; engineers hold Viewer where needed.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Customer Care manage-cases page and the Cloud Support REST reference. Removed: the
`gcloud support cases list|create` commands (no such command, found by the command checker), the
`cloudsupport.viewer` role, billing-case role claims, `subscriberEmailAddresses` and the severity values.
