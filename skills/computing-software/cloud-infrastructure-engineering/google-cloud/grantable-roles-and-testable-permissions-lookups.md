---
id: computing-software.cloud-infrastructure-engineering.google-cloud.grantable-roles-and-testable-permissions-lookups
name: grantable-roles-and-testable-permissions-lookups
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, grantable-roles, testable-permissions, test-iam-permissions, role-permissions-lookup, custom-roles]
level: practitioner
status: docs-checked
description: "Find which roles can be granted on a resource, which permissions a custom role may include there, which role holds a permission, and test the caller's own permissions."
sources: ["https://docs.cloud.google.com/iam/docs/viewing-grantable-roles", "https://docs.cloud.google.com/iam/docs/reference/rest/v1/permissions/queryTestablePermissions", "https://docs.cloud.google.com/resource-manager/reference/rest/v3/projects/testIamPermissions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grantable roles and testable permissions lookups

## Roles grantable on a resource
```bash
gcloud iam list-grantable-roles //cloudresourcemanager.googleapis.com/projects/<P> \
  --filter="name:roles/storage." --format="table(name,title)"
gcloud iam list-grantable-roles //storage.googleapis.com/projects/_/buckets/<BUCKET>
```
The argument is a full resource name. A role is grantable on a resource if it contains any permission for that resource type, and also above it in the hierarchy (for example, `roles/storage.admin` can be granted on a bucket, a project or an organization), but only the permissions applicable to the level it is granted at take effect.

## Permissions a custom role can contain (at a level)
```bash
gcloud iam list-testable-permissions //cloudresourcemanager.googleapis.com/projects/<P> \
  --filter="customRolesSupportLevel!=NOT_SUPPORTED AND name:compute.instances." \
  --format="table(name,stage,customRolesSupportLevel)"
```
`customRolesSupportLevel`: `SUPPORTED` (fully supported for custom roles), `TESTING` (being tested for custom role compatibility), `NOT_SUPPORTED`.

## Which role contains a permission
```bash
gcloud iam roles describe roles/compute.instanceAdmin.v1 --format="value(includedPermissions)" | tr ';' '\n' | grep setMetadata
# reverse lookup: search the role catalogue
for r in $(gcloud iam roles list --format="value(name)" --filter="name:roles/compute."); do
  gcloud iam roles describe $r --format="value(includedPermissions)" | grep -q "compute.instances.setMetadata" && echo $r
done
```

## Test what the caller has
```bash
curl -s -X POST -H "Authorization: Bearer $(gcloud auth print-access-token)" -H "Content-Type: application/json" \
  https://cloudresourcemanager.googleapis.com/v3/projects/<P>:testIamPermissions \
  -d '{"permissions":["compute.instances.create","iam.serviceAccounts.actAs"]}'
```
Returns the subset of the listed permissions the caller holds on that resource.

## Gotchas
- Check each permission's `stage` (for example deprecated) in the `list-testable-permissions` output before putting it in a custom role.

## Checked
2026-10-31. Confirmed against the IAM pages on viewing grantable roles (full resource names, grantable on and above a resource, only permissions applicable to the level apply) and `permissions.queryTestablePermissions` (stage field, CustomRolesSupportLevel enum SUPPORTED, TESTING, NOT_SUPPORTED). gcloud commands and flags were verified by check_commands. Removed unconfirmed: org-level-only permission claim, permissions-reference link, testIamPermissions deny/condition caveat, console behaviour claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Custom role creation succeeds with only SUPPORTED/TESTING permissions at the chosen level.
