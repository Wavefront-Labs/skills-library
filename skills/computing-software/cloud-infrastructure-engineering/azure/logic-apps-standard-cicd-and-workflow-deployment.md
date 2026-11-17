---
id: computing-software.cloud-infrastructure-engineering.azure.logic-apps-standard-cicd-and-workflow-deployment
name: logic-apps-standard-cicd-and-workflow-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, logic-apps, logic-apps-standard, logic-apps-consumption, logic-apps-cicd, workflow-deployment, connections-json, parameters-json, zip-deploy, azure-pipelines, github-actions, bicep, api-connections]
level: practitioner
status: docs-checked
description: "Ship Logic Apps through CI/CD: Standard project layout, parameterised connections.json and app settings, IaC for infra and API connections, zip deploy, Consumption ARM deploys."
sources: ["https://learn.microsoft.com/en-us/azure/logic-apps/set-up-devops-deployment-single-tenant-azure-logic-apps", "https://learn.microsoft.com/en-us/azure/logic-apps/parameterize-workflow-app", "https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-azure-resource-manager-templates-overview", "https://learn.microsoft.com/en-us/azure/logic-apps/create-parameters-workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logic Apps CI/CD and workflow deployment

**Goal:** workflows edited in Git, deployed identically to dev/test/prod by a pipeline, with
environment differences in parameters and app settings — never edited in the prod portal.

## 1. Standard: separate infrastructure from workflows
Repository layout (VS Code Logic Apps Standard project):
```text
logic/
  connections.json  parameters.json
  order-intake/workflow.json   invoice-sync/workflow.json
infra/
  main.bicep   (plan, Logic App site, storage, identity, API connections + access policies, app settings)
```
- `connections.json` references app settings, not literal values:
  `"connectionRuntimeUrl": "@appsetting('BLOB_CONNECTION_RUNTIMEURL')"`.
- `parameters.json` values use `@appsetting('...')` too, so one artefact serves all environments.
- **Managed (API) connections** are Azure resources (`Microsoft.Web/connections`); create them per environment in your IaC.

## 2. Pipeline
Deploy the infrastructure first, then zip-deploy the `logic` folder to the Standard logic app (the set-up-devops page covers build and release pipelines for this). The Standard resource needs the Workflow Standard hosting plan, which is based on the Azure Functions Premium plan.

## 3. Consumption
- A Consumption Logic App is deployed as an ARM template with the workflow definition inline; parameterise values such as `$connections`, endpoints and schedules.
- Deploy with `az deployment group create` per environment; API connections in the same template;
  authorize OAuth connections once per environment (or use managed identity connectors to avoid it).

## Gotchas
- Portal edits in prod drift from Git silently; restrict with RBAC and treat drift as an incident.

## Verify
- [ ] Same `logic.zip` deploys to dev and prod; differences only in app settings/Bicep parameters.
- [ ] Pipeline run shows infra then workflow deployment; workflows appear and run in the target environment.
- [ ] No API connection uses a personal OAuth identity in prod; all use managed identity or service principal.

## Checked
2026-10-28. Confirmed on the set-up DevOps deployment, parameterize and ARM template pages: `@appsetting(...)` in `parameters.json` and `connections.json`, `connectionRuntimeUrl` pattern, API connection resources of type `Microsoft.Web/connections`, zip deploy for Standard logic apps, Workflow Standard plan based on Functions Premium.
Removed (not confirmed): `host.json` in the layout, ManagedServiceIdentity authentication snippet, the access policy claim, pipeline task YAML, deployment slots, built-in connector advice, the Logic App Operator role, and the designer-export and trigger gotchas.

Method: documentation only; no commands were run.
