---
id: computing-software.cloud-infrastructure-engineering.google-cloud.folder-creation-and-folder-iam
name: folder-creation-and-folder-iam
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, folders, folder-creation, folder-iam, gcloud-resource-manager-folders, resource-hierarchy, folder-admin, folder-structure, resourcemanager-folders, nested-folders]
level: practitioner
status: docs-checked
description: "Create nested folders with gcloud resource-manager folders, grant folder-scoped IAM, and respect the 10-level and 300-per-parent limits so inheritance does the work."
sources: ["https://cloud.google.com/resource-manager/docs/creating-managing-folders", "https://cloud.google.com/resource-manager/docs/access-control-folders", "https://cloud.google.com/sdk/gcloud/reference/resource-manager/folders"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Folder creation and folder IAM

**Goal:** a folder tree that mirrors how access and policy are actually delegated, created
reproducibly, with IAM granted at the folder so you never bind the same role on 40 projects.

## 1. Who can create folders
`roles/resourcemanager.folderCreator` on the parent (org or folder) lets a principal browse the hierarchy and create folders;
`roles/resourcemanager.folderViewer` gets and lists folders and projects below a resource; `roles/resourcemanager.folderAdmin`
provides all permissions for working with folders. Grant `folderCreator` to the platform team's group, never to individuals.

## 2. Create and nest
```bash
gcloud resource-manager folders create --display-name="prod" --organization=<ORG_ID>
# returns name: folders/123456789012
gcloud resource-manager folders create --display-name="payments" --folder=123456789012
gcloud resource-manager folders list --organization=<ORG_ID>        # top level
gcloud resource-manager folders list --folder=123456789012            # children
gcloud resource-manager folders describe 123456789012
```
Limits that shape the design (Resource Manager docs): nest up to **10 levels**, at most **300 direct child folders per parent**,
display name unique within the same level, 3-30 characters of letters, digits, spaces, hyphens and underscores, starting and ending
with a letter or digit. `folders delete` fails if the folder is not empty.

Terraform:
```hcl
resource "google_folder" "prod" {
  display_name = "prod"
  parent = "organizations/${var.org_id}"
}
resource "google_folder" "payments" {
  display_name = "payments"
  parent = google_folder.prod.name
}
```

## 3. Folder IAM
```bash
gcloud resource-manager folders add-iam-policy-binding 123456789012 \
  --member="group:payments-devs@example.com" --role="roles/viewer"
gcloud resource-manager folders get-iam-policy 123456789012 --format=yaml
```
Bindings inherit downward to every project and resource below. So grant **broad read** (viewer, logging viewer, monitoring viewer) at
the folder and **write** roles as close to the project as possible. Use groups as members.

## 4. Shape that works
```
org
├─ bootstrap            (seed/CI projects; folderAdmin = platform team only)
├─ common               (logging, network hub, shared services)
├─ prod / nonprod       (environment first, because org policies differ by env)
│   └─ <business-unit>  (team IAM lives here)
└─ sandbox              (loose org policy, budget-capped)
```
Environment above team means a single `compute.vmExternalIpAccess` or `iam.disableServiceAccountKeyCreation`
policy on `prod` covers everyone. Team above environment makes you repeat each policy per team.

## Gotchas
- Folder display names are not globally unique; scripts must use the numeric id (`folders/N`).
- `gcloud resource-manager folders delete` only works on empty folders; `gcloud resource-manager folders undelete` exists to reverse a deletion.
- IAM on a folder does not appear in a project's `get-iam-policy`; use Policy Analyzer or
  `gcloud asset analyze-iam-policy` to see effective access.
- An org policy with `inheritFromParent: false` replaces the parent's values for that constraint instead of merging.

## Verify
- [ ] `gcloud resource-manager folders list --organization=<ORG_ID>` shows the tree you designed and nothing else at top level.
- [ ] `gcloud projects get-ancestors <PROJECT_ID>` prints the expected folder chain.
- [ ] A member of the folder group can list projects in that folder with no project-level binding.

## Checked

- Date: 2026-10-27
- Confirmed against the Resource Manager folders guide (10 levels, 300 direct children, unique display names, 3-30 characters, allowed characters), the folder access-control page (folderAdmin, folderCreator, folderViewer descriptions), gcloud references for `resource-manager folders create/list/add-iam-policy-binding/delete/undelete`, `projects get-ancestors`, `asset analyze-iam-policy`, and the org-policy hierarchy page (`inheritFromParent` merge behaviour). Constraint names `compute.vmExternalIpAccess` and `iam.disableServiceAccountKeyCreation` exist on the constraints list.
- Removed: the "30-day soft delete" and "even in DELETE_REQUESTED" claims, the claim that only deny policies stop inheritance, and the folderViewer requirement to see a new folder.

Method: documentation only; no commands were run.
