---
id: computing-software.cloud-infrastructure-engineering.google-cloud.moving-projects-between-folders-and-organizations
name: moving-projects-between-folders-and-organizations
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, move-project, project-migration-between-folders, gcloud-projects-move, resource-hierarchy, analyze-move, org-migration, project-move-iam, projects-move]
level: advanced
status: docs-checked
description: "Move a project between folders or organizations with gcloud projects move: run analyze-move first, grant the paired IAM, and predict which inherited policies and IAM vanish."
sources: ["https://cloud.google.com/resource-manager/docs/moving-projects-folders", "https://cloud.google.com/resource-manager/docs/project-migration", "https://cloud.google.com/sdk/gcloud/reference/asset/analyze-move"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moving projects between folders and organizations

**Goal:** relocate a project without breaking it — knowing beforehand which inherited IAM,
org policies and VPC-SC membership change at the moment of the move.

## 1. What a move changes
Project-level IAM, resources, billing link, data: **unchanged**. Everything inherited from the
old ancestry: **gone**, replaced by the new ancestry's. That means folder-level role bindings,
org policy constraints (allowed regions, external IP, SA key creation), hierarchical firewall
policies, tags inherited from the folder, and — for cross-org moves — VPC-SC perimeters,
access levels, Shared VPC host attachment and the org's Cloud Identity domain restriction.

## 2. Analyse first
```bash
gcloud asset analyze-move --project=<PROJECT_ID> --destination-folder=<DEST_FOLDER_ID>
# or --destination-organization=<ORG_ID>; add --blockers-only to see only hard stops
```
See the `gcloud asset analyze-move` reference for the output; review the policy and IAM differences it reports before moving.

## 3. Permissions (both sides)
Google's guide: you need the Project Mover role (`roles/resourcemanager.projectMover`) on both the source folder and the destination folder (or on the
organisation resource when the project is not in a folder). The required permissions are `resourcemanager.projects.update` on the project and
`resourcemanager.projects.move` on the source and destination parents. The constraints list includes the legacy managed constraints
`resourcemanager.allowedExportDestinations` and `resourcemanager.allowedImportSources` for cross-organisation moves; check the
*project migration* guide for how to use them:
```bash
gcloud org-policies set-policy export.yaml   # constraint: resourcemanager.allowedExportDestinations, values under:organizations/<DEST_ORG>
```

## 4. Move
```bash
gcloud beta projects move <PROJECT_ID> --folder=<DEST_FOLDER_ID>
gcloud beta projects move <PROJECT_ID> --organization=<DEST_ORG_ID>   # into an organisation
gcloud projects get-ancestors <PROJECT_ID>                             # confirm
```
`gcloud projects move` is not in the GA gcloud reference (the page returns 404); the command exists under `beta` and `alpha`.
Google's project-migration page says the migration updates the project's parent without downtime, and the project's security posture changes
the moment it is attached to the new parent.

## 5. Pre-move checklist
- Export the effective IAM (`gcloud asset analyze-iam-policy` or `search-all-iam-policies`) and
  effective org policies (`gcloud org-policies describe <CONSTRAINT> --project=<P> --effective`, or `gcloud asset analyze-org-policies`) — compare after the move.
- Billing: Google's project-migration page says the project stays linked to its original billing account.
- Quotas: inherited organisation-level quotas are lost; project-level quotas remain (same page).

## Gotchas
- Folder-level IAM, org policies and other inherited settings come from the new parent after the move; use `analyze-move` first.

## Verify
- [ ] `gcloud projects get-ancestors <PROJECT_ID>` shows the new chain.
- [ ] The effective org policies and IAM after the move match what you expected from `analyze-move`.
- [ ] A smoke test of the workload (deploy, read a bucket, call an API) passes post-move.

## Checked

- Date: 2026-10-27
- Confirmed against the moving-projects guide (Project Mover role on source and destination folders or the organisation; `resourcemanager.projects.update` and `resourcemanager.projects.move`), the project-migration page (parent changes without downtime, billing account unchanged, inherited organisation quotas lost, security posture changes at once), the gcloud reference for `beta projects move` (`PROJECT_ID_OR_NUMBER`, `--folder`, `--organization`), `asset analyze-move` (`--project`, `--destination-folder`, `--destination-organization`, `--blockers-only`) and the constraints list (`resourcemanager.allowedExportDestinations`, `resourcemanager.allowedImportSources`).
- Fixed: `gcloud projects move` is not in the GA reference (use `gcloud beta projects move`); the destination permission is `resourcemanager.projects.move`, not `projects.create`; `gcloud org-policies list --effective` is not a valid flag. Removed: analyze-move output field names, Shared VPC, VPC-SC, liens, billing-visibility, CMEK, log-sink and Cloud Asset API claims, and the dead analyze-move source URL.

Method: documentation only; no commands were run.
