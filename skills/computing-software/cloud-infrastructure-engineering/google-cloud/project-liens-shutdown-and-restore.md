---
id: computing-software.cloud-infrastructure-engineering.google-cloud.project-liens-shutdown-and-restore
name: project-liens-shutdown-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, project-liens, project-shutdown, undelete-project, projects-delete, delete-requested, project-restore, liens, accidental-deletion, 30-day-grace, project-lifecycle]
level: practitioner
status: docs-checked
description: "Protect critical Google Cloud projects with liens (alpha gcloud commands, lienModifier role) and restore a deleted project with gcloud projects undelete within the 30-day window."
sources: ["https://cloud.google.com/resource-manager/docs/project-liens", "https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects", "https://cloud.google.com/sdk/gcloud/reference/projects/undelete"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project liens, shutdown and restore

**Goal:** nobody deletes a critical project by accident, and you know how to undo a deletion.

## 1. Liens (deletion guard)
Google describes project liens (Preview, Pre-GA terms) as protection of critical projects from being
accidentally or maliciously deleted: a lien blocks anyone from deleting a project until an Organization
Administrator or Project Owner removes it. Google Cloud can also place liens itself, for example on the
project that owns a service account attached to a resource in another project.
```bash
gcloud alpha resource-manager liens create --project=<PROJECT_ID> \
  --restrictions=resourcemanager.projects.delete \
  --origin="platform-team" --reason="Protected: deletion breaks dependants"
gcloud alpha resource-manager liens list
gcloud alpha resource-manager liens delete <LIEN_NAME>
```
- `--origin` is required but defaults to your email when omitted; `--reason` is a human-readable
  description, quoted.
- To modify liens you need `resourcemanager.projects.updateLiens`, included in the Project lien
  modifier role `roles/resourcemanager.lienModifier`; listing needs `resourcemanager.projects.get`.

## 2. Shutting a project down and quota
`gcloud projects delete <PROJECT_ID>` shuts a project down. Per the project-creation page, soft-deleted
projects still count against your project quota and are fully deleted after 30 days. The cited page
does not detail what stops at once or which resources are purged; check the Resource Manager page on
deleting and restoring projects before relying on specifics, and export data you need first.

## 3. Restore
```bash
gcloud projects undelete <PROJECT_ID_OR_NUMBER>
```
The reference says the command fails if there is no project with that ID or if the active account lacks
Owner or Editor permission on the project. Variants exist under `gcloud alpha` and `gcloud beta`.

## Verify
- [ ] Deleting a project that has a lien fails.
- [ ] A test project deleted and undeleted inside the window can be restored by an Owner.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the project liens page, the undelete reference and the project-quota text, and every
`gcloud` command above passed the command checker.
Removed because the cited pages do not state them: the DELETE_REQUESTED details, ID reservation after
deletion, purge behaviour of Pub/Sub and Memorystore, audit-log alert, Terraform resource and org-policy claims.
