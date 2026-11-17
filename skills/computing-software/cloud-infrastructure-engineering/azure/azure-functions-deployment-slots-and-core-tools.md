---
id: computing-software.cloud-infrastructure-engineering.azure.azure-functions-deployment-slots-and-core-tools
name: azure-functions-deployment-slots-and-core-tools
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-functions, functions-deploy, func-core-tools, functions-slots, one-deploy, run-from-package, zip-deploy]
level: practitioner
status: docs-checked
description: "Deploy Azure Functions reliably: Core Tools publish, zip/run-from-package and Flex Consumption one deploy, CI pipelines, deployment slots and sticky settings."
sources: ["https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-slots", "https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-how-to", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions", "https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-azure-devops"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Functions deployment, slots and Core Tools

**Goal:** repeatable function deployments from CI, zero-downtime swaps where the plan supports
them, and the same artifact promoted through environments.

## Local: Core Tools
```bash
func init orders --worker-runtime python && cd orders && func new --template "HTTP trigger" --name GetOrder
func start                                       # local host with local.settings.json
func azure functionapp publish func-orders-dev   # builds remotely for Python/Node when needed
func azure functionapp fetch-app-settings func-orders-dev   # pull settings into local.settings.json
```
`local.settings.json` is for local only — never commit secrets.

## Deployment methods by plan
| Plan | Method |
|---|---|
| Flex Consumption | Flex Consumption package deployment (`az functionapp deployment source config-zip` uploads the package to the deployment storage container) |
| Elastic Premium / Dedicated / Windows Consumption (legacy) | ZIP deployment (the recommended technology), which runs from package (`WEBSITE_RUN_FROM_PACKAGE=1`) |
| Any of these | Run from an external package URL (`WEBSITE_RUN_FROM_PACKAGE=<url>`); Linux Consumption is retired |
| Containers | Image tag update (Premium/Dedicated/Container Apps) |
```bash
az functionapp deployment source config-zip -g rg -n func-orders-prd --src build/orders.zip --build-remote true
```
- Remote build: do not set `WEBSITE_RUN_FROM_PACKAGE` when you request a remote build on Windows; on Linux Premium and Dedicated apps remote build is enabled with `ENABLE_ORYX_BUILD=true` and `SCM_DO_BUILD_DURING_DEPLOYMENT=true`.
GitHub Actions: `Azure/functions-action@v1` with OIDC `azure/login`; Azure DevOps: `AzureFunctionApp@2`.
Build once, deploy the same zip to dev → test → prod.

## Slots
- Slots including production: Consumption (legacy) 2, Premium 3, Dedicated 1-20 depending on tier; **not supported on Flex Consumption** (use the rolling-updates site update strategy) and not applicable to Functions on Container Apps (use revisions).
```bash
az functionapp deployment slot create -g rg -n func-orders-prd --slot staging
az functionapp deployment source config-zip -g rg -n func-orders-prd --slot staging --src orders.zip
az functionapp deployment slot swap -g rg -n func-orders-prd --slot staging --target-slot production
```
- Mark settings tied to event sources and bindings as slot (sticky) settings (`az functionapp config appsettings set --slot-settings`) *before you start a swap*, so events and outputs go to the proper instance; when you create a new slot the portal copies all existing settings regardless of stickiness.
- Staging slots are live apps; a staging slot that points at the same queues or event sources as production can process the same events. Point it at separate resources.

## Gotchas
- Deploying with any method other than the portal's source of truth makes the app read-only in the portal editor.
- Slot swaps do not guarantee zero downtime: executing functions can be terminated and scaled apps can see degraded availability during a swap; write idempotent handlers.
- Core Tools and the VS Code extension request a remote build by default when deploying to Linux, and always for Python on Flex Consumption.

## Verify
- [ ] `az functionapp function list -g rg -n func-orders-prd -o table` shows expected functions after deploy.
- [ ] Staging slot has triggers disabled or separate queues; swap completes with warm-up.

## Checked
Checked 2026-10-24 against azure-docs azure-functions pages (functions-deployment-slots, functions-deployment-technologies, functions-run-local, functions-core-tools-reference, functions-how-to-github-actions, functions-how-to-azure-devops, flex-consumption-how-to, functions-scale) and the azure-docs-cli functionapp reference (deployment source, deployment slot, config appsettings flags exist). Confirmed: slot counts per plan (Consumption 2, Premium 3, Dedicated 1-20, Flex none), ZIP deployment as the recommended method, ENABLE_ORYX_BUILD and SCM_DO_BUILD_DURING_DEPLOYMENT for Linux remote build, no WEBSITE_RUN_FROM_PACKAGE with a Windows remote build, Azure/functions-action@v1 and AzureFunctionApp@2, config-zip for Flex deployment. Found stale and fixed: Linux Consumption listed as a current deployment target (retired); slot support described incorrectly for Consumption and Premium. Removed unconfirmed: the .gitignore default, the AzureWebJobs.<fn>.Disabled tip, the read-only wwwroot claim, the Flex alwaysReady advice.

Method: documentation only; no commands were run.
