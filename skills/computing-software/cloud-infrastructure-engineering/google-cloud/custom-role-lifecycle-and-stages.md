---
id: computing-software.cloud-infrastructure-engineering.google-cloud.custom-role-lifecycle-and-stages
name: custom-role-lifecycle-and-stages
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, custom-roles, custom-role-lifecycle, role-stages, gcloud-iam-roles, org-level-custom-roles, role-copy, testing-permissions, unsupported-permissions, role-deletion-undelete, roles-yaml, iam-roles-terraform]
level: practitioner
status: docs-checked
description: "Create custom IAM roles from a predefined role minus the excess, at org level, with launch stages, YAML in git, role limits and safe deletion and undelete."
sources: ["https://cloud.google.com/iam/docs/creating-custom-roles", "https://cloud.google.com/sdk/gcloud/reference/iam/roles", "https://cloud.google.com/iam/docs/custom-roles-permissions-support", "https://cloud.google.com/iam/docs/roles-overview#custom"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom role lifecycle and stages

**Goal:** a small set of org-level custom roles, versioned in git, that give teams exactly
what a predefined role gives minus the dangerous bits — and that can be changed without
breaking every binding.

## 1. Design rules
- Create at **org level** (`--organization`) so one role serves every project; project-level custom roles cannot be used elsewhere and multiply.
- Start from a predefined role, remove permissions: `gcloud iam roles describe roles/compute.instanceAdmin.v1 --format=yaml > base.yaml`, edit.
- Limits: 300 custom roles per organization (and 300 per project), **3,000 permissions** per role, and 64 KB for the title, description and permission names together. Wildcards (`*`) are not allowed in permission names. Some permissions are *not supported* in custom roles (`gcloud iam list-testable-permissions` shows `customRolesSupportLevel`, for example `NOT_SUPPORTED` or `TESTING`).
- Role ID: up to 64 bytes of letters, digits, underscores and periods, e.g. `computeOperatorNoDelete`; it cannot be changed or reused until deletion completes. Title and description for humans.

## 2. Create and update from YAML
```yaml
# roles/computeOperatorNoDelete.yaml
title: Compute operator (no delete)
description: Start/stop/reset VMs and read everything in compute; no create or delete.
stage: BETA
includedPermissions:
- compute.instances.get
- compute.instances.list
- compute.instances.start
- compute.instances.stop
- compute.instances.reset
- compute.zones.list
```
```bash
gcloud iam roles create computeOperatorNoDelete --organization=<ORG_ID> --file=roles/computeOperatorNoDelete.yaml
gcloud iam roles update computeOperatorNoDelete --organization=<ORG_ID> --file=roles/computeOperatorNoDelete.yaml
gcloud iam roles update computeOperatorNoDelete --organization=<ORG_ID> --add-permissions=compute.instances.suspend
gcloud iam roles describe computeOperatorNoDelete --organization=<ORG_ID>
gcloud iam roles copy --source=roles/viewer --destination=orgViewerPlus --dest-organization=<ORG_ID>
```
`update --file` is a full replace: include the current `etag` from `describe` so concurrent changes are not overwritten; if it is stale, describe again and retry. Binding member string: `organizations/<ORG_ID>/roles/computeOperatorNoDelete`.

## 3. Stages
Launch stages are `EAP`, `ALPHA`, `BETA`, `GA`, `DEPRECATED` and `DISABLED`. Most stages are
informational and help track whether a role is ready for widespread use; `DISABLED` is the one that
disables the role, a safe first step before deletion. Agree a team convention for what each
informational stage promises.

## 4. Find the permissions you need
```bash
gcloud iam list-testable-permissions //cloudresourcemanager.googleapis.com/projects/<PROJECT_ID> \
  --filter='name:compute.instances' --format='value(name,customRolesSupportLevel)'
# what does a predefined role contain
gcloud iam roles describe roles/run.developer --format='value(includedPermissions)'
# what permission did a denied call need: read the audit log entry's authorizationInfo.permission
```

## 5. Delete and undelete
```bash
gcloud iam roles update computeOperatorNoDelete --organization=<ORG_ID> --stage=DISABLED
gcloud iam roles delete computeOperatorNoDelete --organization=<ORG_ID>
gcloud iam roles undelete computeOperatorNoDelete --organization=<ORG_ID>
```
A deleted role can be undeleted within 7 days. After that, permanent deletion takes up to 30 more days; the role ID can be reused up to 44 days after the delete request. Bindings that refer to a deleted role stay in allow policies but have no effect; clean them up.

## Gotchas
- A custom role is a copy: permissions added later to the predefined role do not appear in it, so diff them periodically (`roles describe` both and compare).
- Updating from a stale file fails on `etag`; two pipelines managing the same role will conflict.

## Verify
- [ ] A user with only the custom role can start/stop a test VM and gets `PERMISSION_DENIED` on delete.
- [ ] `gcloud iam roles describe` shows the stage and permission list identical to the YAML in git.

## Checked

2026-10-28. Confirmed against: IAM "Create and manage custom roles" page (3,000 permissions and 64 KB limits, 300 custom roles per organization and per project, launch stages EAP/ALPHA/BETA/GA/DEPRECATED/DISABLED and which are informational, etag on update, 7-day undelete, 30-day permanent deletion, 44-day ID reuse, no wildcards, `customRolesSupportLevel` values) and the IAM roles overview (role ID length and characters). Commands were checked against the gcloud reference.

Removed: the Terraform example (not in the pages read), the 3 to 64 minimum role ID length, the `ABORTED` error name, the `deprecated` field advice, the 2-week soak, and gotchas about TESTING permissions, `iam.roles.get` for grantors and folder or org references to project roles.

Method: documentation only; no commands were run.
