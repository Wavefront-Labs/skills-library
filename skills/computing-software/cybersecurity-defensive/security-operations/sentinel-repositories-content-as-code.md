---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-repositories-content-as-code
name: sentinel-repositories-content-as-code
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, sentinel-repositories, detection-as-code, arm-templates, bicep, github-actions, azure-devops, content-deployment]
level: advanced
status: docs-checked
description: "Manage Sentinel analytics rules, workbooks and playbooks as code with Repositories: connection setup, ARM/Bicep layout, smart deployments, and drift between portal and repo."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/ci-cd", "https://learn.microsoft.com/en-us/azure/sentinel/ci-cd-custom-deploy", "https://learn.microsoft.com/en-us/azure/sentinel/ci-cd-custom-content"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel Repositories (content as code)

## What it does
Sentinel > Content management > Repositories connects a GitHub or Azure DevOps repo. On each
commit to the chosen branch a generated pipeline deploys supported content to the workspace:
analytics rules, automation rules, hunting queries, parsers, playbooks, workbooks.

## Setup
1. Repo with folders per content type (any layout works; the deployment script scans for ARM
   JSON or Bicep files).
2. Connect: choose repo, branch, content types. Sentinel creates a workflow or pipeline in the repo. You need the Owner role on the resource group that contains the workspace to create the connection.
3. Commit content exported as ARM: in the portal, Analytics > select rule > Export gives the ARM template.

## Rule template essentials
```json
{
  "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
  "apiVersion": "<API_VERSION>",
  "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/', 'b6f2...guid')]",
  "kind": "Scheduled",
  "properties": { "displayName": "...", "query": "...", "queryFrequency": "PT1H",
    "queryPeriod": "PT1H", "triggerOperator": "GreaterThan", "triggerThreshold": 0,
    "severity": "Medium", "enabled": true, "tactics": ["CredentialAccess"] }
}
```
Export the template from the portal to get the current property names and API version.

## Smart deployments
Enabled by default: only content modified since the last deployment deploys; you can turn it off.
`sentinel-deployment.config` in the repo sets `prioritizedcontentfiles`, `excludecontentfiles`, and
parameter file mapping per workspace (dev/prod with different parameters).

## Workflow
- Branch, edit KQL, open a PR, review, merge; the pipeline deploys.
- Add a CI job before merge: KQL syntax validation and JSON schema checks.

## Drift
Microsoft recommends editing content in a connected repository only in the repository, not in Sentinel. Make the repo the only write path for connected content.

## Gotchas
- Check the ci-cd pages for what a deployment does and does not remove before relying on deletes.

## Verify
Change a rule's description in a PR, merge, watch the workflow succeed, and confirm the portal
shows the change.

## Checked

Date: 2026-10-28

- Confirmed in the ci-cd pages: GitHub and Azure DevOps connections, Owner role on the workspace resource group, supported content types, smart deployments (on by default, can be turned off), configuration file options (prioritised order, exclusions, parameter-file mapping per workspace), edit connected content only in the repo.
- Removed (not found): generated workflow file name, service principal/OIDC wording, ARM apiVersion value, tracking-table file name, "Source: Repositories" label, GUID, delete, Content hub and playbook-connection gotchas, KQL validation tool names.
Method: documentation only; no commands were run.
