---
id: computing-software.cloud-infrastructure-engineering.azure.tag-operations-merge-replace-and-limits
name: tag-operations-merge-replace-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, tags, az-tag, tag-merge, tag-limits, tag-contributor, bulk-tagging]
level: practitioner
status: docs-checked
description: "Change Azure tags without wiping existing ones: az tag update merge/replace/delete, Tag Contributor role, bulk tagging from Resource Graph and the hard tag limits."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/management/tag-resources", "https://learn.microsoft.com/azure/azure-resource-manager/management/tag-resources-cli", "https://learn.microsoft.com/azure/azure-resource-manager/management/tag-support"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag operations: merge vs replace, limits

**Goal:** tag at scale without accidentally deleting everyone else's tags.

## The safe command
```bash
az tag update --resource-id <id> --operation Merge   --tags costCenter=1234 env=prod   # add/overwrite these keys
az tag update --resource-id <id> --operation Replace --tags env=prod                   # ALL other tags removed
az tag update --resource-id <id> --operation Delete  --tags env=prod                   # remove these tags
az tag list --resource-id <id>
```
Trap: `az resource tag --tags ...` **replaces** all tags unless you add `--is-incremental`; `az group update --tags`
also replaces. Use `az group update --set tags.env=prod` for a single key on a group.

## Bulk tag from Resource Graph
```bash
az graph query -q "resources | where resourceGroup =~ 'rg-app' and isnull(tags.costCenter) | project id" \
  --first 1000 --query "data[].id" -o tsv |
while read id; do az tag update --resource-id "$id" --operation Merge --tags costCenter=1234 -o none; done
```

## Permissions
`Tag Contributor` role (write on the `Microsoft.Resources/tags` type) lets FinOps tag resources without write access to them. It cannot tag resources or resource groups in the Azure portal (it can tag subscriptions there); use PowerShell, CLI or REST.
Tagging via the resource's own PUT (IaC) needs write on the resource.

## Limits and rules
- Max **50** tag name/value pairs per resource, resource group and subscription.
- Name up to 512 chars (128 for storage accounts), value up to 256 chars.
- Names are case-insensitive, values case-sensitive (`Prod` vs `prod` split your cost reports).
- Disallowed characters in names: `<`, `>`, `%`, `&`, `\`, `?`, `/`.
- Not every resource type supports tags; check the tag-support page.
- Tags are not inherited by resources - assign policy definitions for tag compliance to apply them.

## Gotchas
- IaC that declares a full tags object will remove tags added outside IaC on the next deploy (or policy modifies
  them back - an endless diff). Agree who owns which keys.

## Verify
- [ ] Spot-check with `az tag list` that existing keys survived; untagged count from ARG drops to zero.

## Checked
2026-10-28. Confirmed against Microsoft Learn tag-resources, tag-resources-cli and the az resource, az group and az graph reference pages: Merge/Replace/Delete operations, `az resource tag --is-incremental`, `--tags ""` clears tags on `az group update`, `az graph query --first`, Tag Contributor behaviour and portal limitation, 50 pairs, name 512 (128 storage accounts) and value 256 characters, case rules, disallowed characters, no inheritance. Removed: the PowerShell line, the Cost Management inheritance claim, the silent-ignore claim and the DINE/activity-log gotcha (not found in the pages).
Method: documentation only; no commands were run.
