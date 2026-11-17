---
id: computing-software.cloud-infrastructure-engineering.azure.abac-queue-conditions-index-tags-and-environment-attributes
name: abac-queue-conditions-index-tags-and-environment-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, abac, queue-conditions, blob-index-tags-condition, environment-attributes, role-assignment-conditions, storage]
level: advanced
status: gated
description: "Write Azure ABAC role assignment conditions for queue names, blob index tags (read and write) and environment attributes like private link and time."
sources: ["https://learn.microsoft.com/azure/storage/queues/queues-auth-abac-attributes", "https://learn.microsoft.com/azure/storage/blobs/storage-auth-abac-attributes", "https://learn.microsoft.com/azure/role-based-access-control/conditions-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ABAC conditions: queues, index tags, environment

**Goal:** one role assignment that only works on the right queue, the right tagged blobs, or only over a private
endpoint - instead of one storage account per team.

## Condition shape
```
(
 (
  !(ActionMatches{'<action>'})
 )
 OR
 (
  <attribute expression>
 )
)
```
Read as: "if the request is this action, the expression must be true". Always condition version 2.0.

## Queue name (Storage Queue Data Message Processor/Sender/Reader)
The exact attribute id `...queues:name` (gated: unconfirmed, source is paywalled or blocked); copy it from the portal code view.
```
(
 (
  !(ActionMatches{'Microsoft.Storage/storageAccounts/queueServices/queues/messages/read'})
  AND !(ActionMatches{'Microsoft.Storage/storageAccounts/queueServices/queues/messages/process/action'})
 )
 OR
 (
  @Resource[Microsoft.Storage/storageAccounts/queueServices/queues:name] StringEquals 'orders'
 )
)
```

## Blob index tags
- Existing blob tags (read): `@Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs/tags:Project<$key_case_sensitive$>] StringEquals 'Cascade'` (gated: unconfirmed, source is paywalled or blocked)
- Tags supplied on write (prevent untagged uploads): use `@Request[...blobs/tags:Project<$key_case_sensitive$>]` with
  actions `.../blobs/write` and `.../blobs/add/action`.

## Environment attributes
- `@Environment[isPrivateLink] BoolEquals true` - only via any private endpoint.
- `@Environment[Microsoft.Network/privateEndpoints] StringEqualsIgnoreCase '<private-endpoint-resource-id>'`.
- `@Environment[Microsoft.Network/virtualNetworks/subnets] StringEqualsIgnoreCase '<subnet-id>'` (service endpoint path).
- `@Environment[UtcNow] DateTimeLessThan '2026-12-31T00:00:00.0Z'` - time-boxed access.

## Apply
```bash
az role assignment create --assignee <principalId> --role "Storage Queue Data Message Processor" \
  --scope <storage-account-id> --condition "$(cat cond.txt)" --condition-version 2.0
```

## Gotchas
- Check which actions your condition covers: the attributes page lists List blobs (`blobs/read`) as its own action.
- Conditions only work on data actions of supported roles; they do nothing for keys/SAS (disable shared key).
- Condition syntax errors fail at assignment time - build in the portal's visual editor, then copy the code view.

## Verify
- [ ] Access to the allowed queue/blob succeeds and to another fails with 403.

## Checked
2026-10-28. Confirmed on the Learn queue and blob ABAC attribute pages and conditions-format: `isPrivateLink`, `Microsoft.Network/privateEndpoints`, `Microsoft.Network/virtualNetworks/subnets`, `UtcNow`, the queue `messages/process/action` data action, Queue name and blob index tag attributes exist. Removed: the claim that list operations are not filtered by tags, the named 403 error code. Gated: exact attribute id strings for queue name and index tags (stripped pages omit them).
Method: documentation only; no commands were run.
