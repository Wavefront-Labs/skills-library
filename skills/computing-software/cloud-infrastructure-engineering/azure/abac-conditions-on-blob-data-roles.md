---
id: computing-software.cloud-infrastructure-engineering.azure.abac-conditions-on-blob-data-roles
name: abac-conditions-on-blob-data-roles
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, abac, abac-conditions, blob-conditions, condition-syntax, role-assignment-conditions, blob-index-tags, storage-data-roles]
level: advanced
status: docs-checked
description: "Add ABAC conditions to Storage Blob Data role assignments: restrict by container, path prefix or blob index tag, with correct condition syntax and testing."
sources: ["https://learn.microsoft.com/azure/role-based-access-control/conditions-overview", "https://learn.microsoft.com/azure/storage/blobs/storage-auth-abac", "https://learn.microsoft.com/azure/storage/blobs/storage-auth-abac-examples", "https://learn.microsoft.com/azure/role-based-access-control/conditions-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ABAC conditions on blob data role assignments

**Goal:** one storage account shared by many tenants/teams, each principal limited to its own
container or prefix by a condition on the role assignment instead of one account per team.

## Condition anatomy
```
(
 (
  !(ActionMatches{'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read'})
 )
 OR
 (
  @Resource[Microsoft.Storage/storageAccounts/blobServices/containers:name] StringEquals 'team-a'
 )
)
```
Read it as: "if the action is not blob read, this condition doesn't apply; otherwise the
container must be `team-a`". Every condition follows this **!(action) OR (expression)** shape —
forget the first half and the condition blocks *other* actions too.

## Common expressions
| Restrict by | Attribute |
|---|---|
| Container | `@Resource[Microsoft.Storage/storageAccounts/blobServices/containers:name] StringEquals 'x'` |
| Path prefix | `@Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs:path] StringLike 'tenant1/*'` |
| Blob index tag on the existing blob | `@Resource[.../blobs/tags:Project<$key_case_sensitive$>] StringEquals 'cascade'` |
| Tag being written | `@Request[.../blobs/tags:Project<$key_case_sensitive$>] StringEquals 'cascade'` |
| Private endpoint used | `@Environment[Microsoft.Network/privateEndpoints] ForAnyOfAnyValues:StringEquals '<pe-id>'` |

## Assign with a condition
```bash
cond="((!(ActionMatches{'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read'}) AND !(ActionMatches{'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/write'})) OR (@Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs:path] StringLike 'tenant1/*'))"
az role assignment create --assignee <object-id> --assignee-principal-type Group \
  --role "Storage Blob Data Contributor" --scope <storage-account-id> \
  --condition "$cond" --condition-version "2.0"
```
Portal: Add role assignment → **Conditions** tab → visual builder; switch to Code view and
store the text in Git.

## Gotchas
- **List** operations: `blobs/read` covers both get and list; path conditions on list need the
  `prefix` sub-operation handling — use the documented example "read blobs with a path prefix"
  which includes `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read` with
  `@Request[...:prefix]`.
- Shared Key authorization is a separate access path: prevent it on the account (`allowSharedKeyAccess=false`, see the
  "Prevent Shared Key authorization" article) so access goes through Microsoft Entra authorization and your conditions.
- Blob index tag conditions require tags to be set at write; `@Request` conditions on write stop
  users tagging themselves into other projects.

## Verify
- [ ] As the principal: `az storage blob list --account-name <acct> -c data --prefix tenant1/ --auth-mode login` succeeds.
- [ ] Same with `--prefix tenant2/` is denied.
- [ ] `az storage account show --query allowSharedKeyAccess` is `false`.

## Checked
2026-10-27. Confirmed on Microsoft Learn: conditions-format (`ActionMatches`, `SubOperationMatches` with `Blob.List`, `@Resource`/`@Request`/`@Environment` attribute sources, `StringLike`,
`ForAnyOfAnyValues`, `<$key_case_sensitive$>`, `Microsoft.Network/privateEndpoints`), storage-auth-abac and storage-auth-abac-examples (container name, `blobs:path`, index tag conditions, prefix handling),
CLI reference for `az role assignment create` (--condition, --condition-version 2.0, --assignee-principal-type), shared-key-authorization-prevent (`allowSharedKeyAccess`).
Removed: encryption-scope row, 8 KB condition limit, the "Owner/Contributor do not support conditions" claim, "SAS bypasses ABAC entirely" wording, the exact error code.

Method: documentation only; no commands were run.
