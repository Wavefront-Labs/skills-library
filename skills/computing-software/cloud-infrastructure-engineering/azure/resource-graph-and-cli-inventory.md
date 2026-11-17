---
id: computing-software.cloud-infrastructure-engineering.azure.resource-graph-and-cli-inventory
name: resource-graph-and-cli-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, resource-graph, azure-resource-graph, resource-queries, kql, azure-cli, azure-powershell, az-graph, az-rest, cloud-shell, jmespath, query-output, inventory, orphaned-resources, resource-changes, change-analysis, shared-queries, arg-explorer, pagination, az-login, service-principal-login]
level: practitioner
status: draft
description: "Fleet-wide inventory in seconds: Resource Graph KQL (joins, orphans, change history), pagination, and Azure CLI/PowerShell idioms (JMESPath, az rest, non-interactive login)."
sources: ["Microsoft Learn - Azure Resource Graph query language and starter queries", "Microsoft Learn - Get resource changes (Resource Graph)", "Microsoft Learn - Azure CLI output formats and JMESPath queries", "Microsoft Learn - Sign in with Azure CLI (service principal, managed identity, workload identity)", "Microsoft Learn - az rest"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resource Graph and CLI inventory — one query instead of a loop over subscriptions

**Goal:** fleet-wide questions (orphans, missing tags, who changed what, which VMs are
on an old image) answered by one KQL query with results you can pipe into automation.

## 1. Resource Graph basics
`az extension add -n resource-graph`, then `az graph query -q "<KQL>"` (or PowerShell
`Search-AzGraph`, or the portal *Resource Graph Explorer* which also saves **shared
queries** as ARM resources). Reads across every subscription you can read; results are
near-real-time (resource provider pushes updates), no per-subscription throttling.
Tables: `resources`, `resourcecontainers` (subscriptions/RGs/management groups),
`resourcechanges`, `policyresources`, `securityresources`, `advisorresources`,
`patchassessmentresources`, `networkresources`, `kubernetesconfigurationresources`.

```kusto
// VMs by size and OS, with subscription name
resources
| where type =~ "microsoft.compute/virtualmachines"
| extend size = tostring(properties.hardwareProfile.vmSize), os = tostring(properties.storageProfile.osDisk.osType)
| join kind=leftouter (resourcecontainers | where type =~ "microsoft.resources/subscriptions" | project subscriptionId, subName = name) on subscriptionId
| summarize count() by subName, os, size | order by count_ desc
```
```kusto
// orphans: unattached disks, unused public IPs, NICs without a VM
resources | where type =~ "microsoft.compute/disks" and properties.diskState == "Unattached" | project name, resourceGroup, sku.name, properties.diskSizeGB
| union (resources | where type =~ "microsoft.network/publicipaddresses" and isnull(properties.ipConfiguration) | project name, resourceGroup)
```
```kusto
// who changed what in the last 24 h
resourcechanges
| extend t = todatetime(properties.changeAttributes.timestamp), who = tostring(properties.changeAttributes.changedBy), ct = tostring(properties.changeType)
| where t > ago(24h) and ct != "Create" | project t, who, ct, resourceId = tostring(properties.targetResourceId), changes = properties.changes
```
Rules: `=~` for case-insensitive type matching; property paths are case-sensitive;
`tostring()`/`tolower()` before `==`; `mv-expand` for arrays (NSG rules, IP configs);
`tags['cost-centre']` for hyphenated keys. `join` is limited (3 per query, `leftouter`/`inner`),
and only ~400 results per subscription without pagination.

## 2. Pagination and limits
`az graph query -q "..." --first 1000 --skip-token "<token>"` — loop while `skip_token`
is set (CLI returns it in `skip_token`); PowerShell `Search-AzGraph -First 1000 -SkipToken`.
Max 1000 rows per page; queries over ~5 s time out — add `where` early, `project` to trim.
Quota: ~15 queries per 5 s per user; batch rather than hammering.

## 3. Azure CLI idioms
- `--query` is **JMESPath**: `az vm list --query "[?powerState=='VM running'].{n:name,rg:resourceGroup}" -o table`,
  `--query "[].id" -o tsv | xargs -n1 az vm deallocate --ids`.
- `-o tsv` for scripting (no quotes), `-o json` + `jq` for anything nested, `-o table` for humans.
- `az rest --method get --url "https://management.azure.com/subscriptions/<sub>/providers/Microsoft.Compute/virtualMachines?api-version=2024-07-01"`
  for APIs the CLI lacks; also `--url https://graph.microsoft.com/v1.0/...` (auto token).
- Non-interactive: `az login --service-principal -u <appId> -p <cert.pem|secret> --tenant <t>`,
  `az login --identity` (VM/Arc/App Service), `az login --federated-token "$(cat $AZURE_FEDERATED_TOKEN_FILE)"` (workload identity).
  `az account set -s <sub>` after login; `az account show` to confirm.
- `az config set core.only_show_errors=true extension.use_dynamic_install=yes_without_prompt`
  for CI logs; `az --version` + `az upgrade` quarterly; pin the CI image version.
- Concurrency: `az <cmd> --no-wait` + `az <type> wait --created`; `--ids` accepts many resource IDs.
- PowerShell equivalents (`Get-AzResource`, `Search-AzGraph`, `Invoke-AzRestMethod`) are better on Windows admins' boxes and for pipelines already in PowerShell; mixing both in one script is a smell.

## 4. Cloud Shell
Browser shell with az/Az/kubectl/terraform preinstalled, authenticated as you, 20-min
idle timeout, optional mounted file share for persistence, VNet isolation available.
Good for one-offs and Bastion-less admin; not for anything that needs secrets on disk.

## Gotchas
- Resource Graph needs read RBAC on the scope; results silently omit subscriptions you can't read — no error.
- `resourcechanges` keeps 14 days; for longer, export Activity Log to Log Analytics.
- JMESPath string comparisons are case-sensitive and need backticks for literals in some shells (`\`true\``).
- `az` on Windows with Git Bash mangles `/subscriptions/...` paths (MSYS path conversion): set `MSYS_NO_PATHCONV=1`.
- The CLI caches tokens in `~/.azure`; on shared build agents call `az logout` or use ephemeral `AZURE_CONFIG_DIR`.

## Verify
- [ ] `az graph query -q "resources | count"` returns the fleet total you expect across all subscriptions.
- [ ] Orphan query output drives a cleanup script; re-run shows zero.
- [ ] Shared query saved in a `rg-governance` RG and visible to the ops team.
- [ ] CI login uses federated credentials; `az account show` prints the right subscription.
