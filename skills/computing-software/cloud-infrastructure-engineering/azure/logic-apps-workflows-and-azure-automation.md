---
id: computing-software.cloud-infrastructure-engineering.azure.logic-apps-workflows-and-azure-automation
name: logic-apps-workflows-and-azure-automation
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, logic-apps, logic-apps-standard, logic-apps-consumption, workflow-automation, connectors, managed-connectors, built-in-connectors, triggers, actions, workflow-definition-language, managed-identity-connections, api-connections, stateful-workflows, stateless-workflows, run-history, retry-policy, azure-automation, runbooks, automation-account, hybrid-runbook-worker, powershell-runbooks, schedules, webhooks, desired-state-configuration, ops-automation, automation-managed-identity, automation-modules]
level: practitioner
status: docs-checked
description: "Automate operations: Logic Apps Standard vs Consumption, managed-identity connections, error handling, run history, CI/CD; Azure Automation runbooks, hybrid workers, schedules."
sources: ["https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config", "https://learn.microsoft.com/en-us/azure/logic-apps/error-exception-handling", "https://learn.microsoft.com/en-us/azure/automation/automation-webhooks", "https://learn.microsoft.com/en-us/azure/automation/automation-runbook-execution", "https://learn.microsoft.com/en-us/azure/automation/automation-runbook-types", "https://learn.microsoft.com/en-us/cli/azure/logicapp"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Logic Apps and Azure Automation — ops workflows that run on their own

**Goal:** integrations and operational automations expressed as workflows and
runbooks that authenticate with identities, retry on transient failures, land in
source control, and tell you when a run fails.

## 1. Which tool
| Need | Use |
|---|---|
| Integrate SaaS/Azure services with many connectors, approvals, scheduled jobs, event handlers | **Logic Apps** |
| PowerShell/Python against VMs, AD, on-prem servers; configuration drift; scheduled scripts with a worker you control | **Azure Automation** (runbooks, hybrid workers) |
| Code-first event handlers at scale | Azure Functions (see its skill) |
| Container-based jobs | Container Apps Jobs |

## 2. Logic Apps: Consumption vs Standard
- **Consumption**: multi-tenant, one workflow per resource, quick to start.
- **Standard**: single-tenant, many **workflows per app**, **stateful** (run history, long-running) or **stateless** (in-memory, faster; for each is capped at 100 array items by default versus 100,000 for stateful), **built-in connectors** run in-process and **managed connectors** go through the shared connector runtime. Local dev in VS Code, CI/CD like a Function app (`workflow.json` per workflow + `connections.json` + app settings).
```bash
az logicapp create -g rg -n la-ops-prod -p asp-la-prod --storage-account stlaprod   # Standard; then `az logicapp identity assign` for the managed identity
az logicapp deployment source config-zip -g rg -n la-ops-prod --src workflows.zip
```
- Standard needs a storage account for workflow state; if the account is network-restricted, give the app private endpoints to it.

## 3. Build a workflow that survives production
- **Trigger** (Recurrence, HTTP request, connector polling) -> **actions** with **scopes** (`Try`/`Catch` pattern via *run after* settings: configure the Catch scope to run after *Failed, TimedOut, Skipped*), **Until**/**For each** (set concurrency; sequential when order matters), **Compose/Parse JSON** with schemas, conditions, switch.
- **Connections with managed identity**: for Azure connectors choose *managed identity* auth and grant RBAC/data roles, so no secrets and no owner-bound OAuth connections that break when someone leaves.
- Secrets: read them from Key Vault with a managed identity and mark sensitive inputs/outputs as secure so run history does not display them.
- **Retry policy** per action (`"retryPolicy": {"type": "exponential", "count": 5, "interval": "PT10S", "maximumInterval": "PT1H"}`). Default is 4 attempts; Consumption allows at most 90. Consumption retry intervals run from 5 seconds (PT5S) to 1 day (P1D). See the error-handling page for the HTTP action timeout and asynchronous pattern.
- Idempotency: Logic Apps do not dedupe for you; HTTP request triggers need a client-supplied key stored somewhere durable.
- Limits: run duration and history retention default to 90 days in multitenant (minimum 7, maximum 365); message size 100 MB (use chunking); stateful `For each` 100,000 items. Design for them (split into child workflows, buffer with a queue).

## 4. Operate and ship
- **Run history** with per-action inputs/outputs (secured ones hidden); send diagnostic settings to Log Analytics and alert on failed runs; Application Insights is available for Standard.
- CI/CD: Consumption -> ARM/Bicep with parameters per environment; Standard -> repo with `workflow.json` files, `connections.json` using app settings for environment values, deployed by pipeline (zip deploy) + Bicep for the app/plan.
- Lock production workflows (no portal edits).
- Cost: see the Logic Apps pricing page; Consumption bills per action execution, including polling triggers.

## 5. Azure Automation runbooks
```bash
az automation account create -g rg-ops -n aa-ops-prod -l uksouth --sku Basic   # then system-assigned identity + RBAC for what the runbooks touch
az automation runbook create -g rg-ops --automation-account-name aa-ops-prod -n Stop-DevVMs --type PowerShell --location uksouth
az automation runbook replace-content ... -n Stop-DevVMs --content @Stop-DevVMs.ps1 ; az automation runbook publish ... -n Stop-DevVMs
az automation schedule create ... -n nightly --frequency Day --interval 1 --start-time 2026-11-01T19:00:00+00:00
az automation runbook start ... -n Stop-DevVMs --parameters env=dev   # or via webhook
```
- Runtime: PowerShell runbooks (supported per the runbook-types page: 7.6, 7.4 and 5.1; 7.1 and 7.2 are no longer supported), Python 3.10 (2.7 and 3.8 no longer supported). PowerShell 7.4 is only available in the runtime environment experience.
- **Hybrid Runbook Worker**: runs runbooks on your own machines with local/network access, and is not limited by the three-hour fair share limit.
- Assets: **variables**, **credentials**, **certificates**, **connections**; prefer Key Vault via the identity for anything secret.
- Jobs: Azure sandbox jobs running more than three hours are unloaded by fair share (hybrid workers have no such limit); Azure Automation keeps job logs for a maximum of 30 days, so export them via diagnostic settings and alert on failed jobs.

## Gotchas
- Automation webhooks: the URL is the only credential and a webhook is valid for 10 years, after which it expires and must be removed and recreated; treat it like a key.

## Verify
- [ ] Workflow test: trigger -> actions succeed; force a transient failure downstream and confirm retries appear in run history; a hard failure routes to the Catch scope and raises the failed-run alert.
- [ ] Every Azure connector connection uses managed identity (no OAuth owner); secure inputs/outputs hidden in history.
- [ ] Deployment from the repo to a test logic app produces identical `workflow.json` (diff in pipeline); production has no manual edits (Activity log).
- [ ] Runbook job: managed-identity sign-in succeeds; scheduled run appears in job history; failed-job alert tested with a deliberate `throw`.

## Checked
2026-10-31. Confirmed against the Logic Apps limits page, the Logic Apps error-handling page, and the Automation runbook
types, runbook execution and webhooks pages: 90-day run duration and history retention (7 to 365), 100,000 stateful and
100 stateless For each items, 100 MB message size, default 4 and maximum 90 retry attempts, PT5S to P1D Consumption
retry interval, PowerShell 7.6/7.4/5.1 and Python 3.10 runtimes, three-hour fair share and its hybrid worker exemption,
30-day job log retention, 10-year webhook validity. `az logicapp` and `az automation` commands were checked for
existence and flags against the CLI reference. Removed as unconfirmed: plan SKU names, the default For each
concurrency, diagnostic category and metric names, KQL snippets, Update Manager and DSC retirement claims, and
cost arithmetic.
Method: documentation only; no commands were run.
