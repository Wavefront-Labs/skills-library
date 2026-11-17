---
id: computing-software.cloud-infrastructure-engineering.google-cloud.deny-supported-permissions-and-v2-permission-format
name: deny-supported-permissions-and-v2-permission-format
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam-deny-policies, deny-permission-format, supported-deny-permissions, permission-groups, denied-permissions]
level: practitioner
status: docs-checked
description: "Write deniedPermissions correctly: the service FQDN/resource.verb format, which permissions deny supports, wildcard permission groups, and denial conditions on tags."
sources: ["https://cloud.google.com/iam/docs/deny-permissions-support", "https://cloud.google.com/iam/docs/deny-overview#permissions", "https://cloud.google.com/iam/docs/deny-overview#conditions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deny-supported permissions and the v2 permission format

## Format
Allow policies use `service.resource.verb`. Deny policies use the **v2** format with the service's FQDN,
`SERVICE_FQDN/RESOURCE.ACTION` (Google APIs use `*.googleapis.com`):
```
<service-fqdn>/<resource>.<verb>
cloudresourcemanager.googleapis.com/projects.delete
iam.googleapis.com/roles.delete
```
Only permissions on the supported list (cloud.google.com/iam/docs/deny-permissions-support) are
accepted; check the list before writing a rule.

## Permission groups (wildcards)
```
cloudresourcemanager.googleapis.com/folders.*   # all folder permissions (pattern from the docs)
```
Wildcards work only for the permission groups listed on the supported-permissions page. A group covers all
current and future permissions matching the pattern.

## Deny conditions
Conditions on deny rules may only use resource tags:
```json
"denialCondition": {
  "title": "only prod-tagged",
  "expression": "resource.matchTag('12345678/env', 'prod')"
}
```
Denial conditions have the same structure as IAM Conditions but recognise only resource tag functions.

## Patterns worth denying
- `cloudresourcemanager.googleapis.com/projects.delete` on prod folders except a break-glass group.
- Custom role management (for example `iam.googleapis.com/roles.delete`) except for a central admin group.

## Gotchas
- `exceptionPermissions` lets you deny a group but keep specific members of it (the docs deny
  `cloudresourcemanager.googleapis.com/folders.*` except `folders.list` and `folders.get`).
- A permission you did not deny is still allowed: deny only blocks what you list.
- Test rules with a non-production principal.

## Verify
- [ ] Policy Troubleshooter shows the request denied by the named deny rule for a test principal.

## Checked
2026-10-28. Confirmed on the IAM deny overview (permissions and conditions sections): v2 format SERVICE_FQDN/RESOURCE.ACTION, `deniedPermissions`, `exceptionPermissions`, `denialCondition` with `resource.matchTag('<org>/env', 'prod')`, wildcards only in listed permission groups, denial conditions recognise only resource tag functions.
Removed: the `INVALID_ARGUMENT` message text, `*.googleapis.com/*.delete` wildcard, `matchTagId`, Compute and IAM key example permissions not in the fetched pages, and the listing-visibility claim.
Method: documentation only; no commands were run.
