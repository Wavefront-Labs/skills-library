---
id: computing-software.cloud-infrastructure-engineering.azure.migrating-classic-pipelines-to-yaml
name: migrating-classic-pipelines-to-yaml
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-pipelines-yaml, classic-to-yaml, release-pipelines, environments, export-yaml]
level: advanced
status: docs-checked
description: "Migrate classic build and release pipelines to multi-stage YAML: export, map tasks, variable groups and approvals to environments, and retire classic safely."
sources: ["https://learn.microsoft.com/azure/devops/pipelines/release/from-classic-pipelines", "https://learn.microsoft.com/azure/devops/pipelines/get-started/pipelines-get-started", "https://learn.microsoft.com/azure/devops/pipelines/process/environments", "https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Classic to YAML pipelines

**Goal:** pipelines as code, reviewed in PRs, with the same deployment controls the classic release had.

## Map concepts
| Classic | YAML |
|---|---|
| Build pipeline | `stages: - stage: Build` |
| Release pipeline stages | `stages` with `deployment` jobs |
| Pre-deployment approvals, gates | **Environment** approvals and checks |
| Release variables / scoped variables | `variables:` per stage, variable groups, templates |
| Artifacts trigger (build completes) | `resources: pipelines:` trigger, or a single multi-stage pipeline |
| Task groups | Step/job templates (`template:`) |
| Deployment groups | Environment with VM resources |
| Manual intervention task | `ManualValidation@1` in an agentless job |

## Steps
1. **Export**: in the classic pipeline definition view (not a run), use the three-dots menu → *Export to YAML*; for release pipelines follow the Learn migration guide and rebuild stages by hand.
2. Create `azure-pipelines.yml` with Build stage, then deployment stages:
```yaml
- stage: Prod
  dependsOn: Staging
  jobs:
  - deployment: web
    environment: prod-web
    strategy: { runOnce: { deploy: { steps: [ { download: current, artifact: drop }, { task: AzureWebApp@1, inputs: { azureSubscription: sc-prod, appName: web-prod, package: '$(Pipeline.Workspace)/drop/*.zip' } } ] } } }
```
3. Recreate approvals/checks on the environments and on service connections/variable groups (protected resources).
4. Run both side by side for a few releases; compare artifacts and deployments.
5. Disable classic pipelines (keep for history), then delete after the retention period.

## Gotchas
- Classic release variables have no automatic YAML equivalent; map each one by hand.
- Do not carry secrets in exported YAML; use variable groups or Key Vault.

## Verify
- [ ] YAML pipeline deploys to every environment with the same approvals; classic pipelines disabled.

## Checked

2026-10-28. Confirmed on the Azure Pipelines classic migration page: Export to YAML is on the three-dots menu in the pipeline definition view (not a specific run) and downloads a YAML file; the azure-pipelines.yml file name is on the get-started page; ManualValidation@1 is agentless-only (see its reference). Removed: the View YAML per job claim, the release export claim, the organisation setting name, variable equivalents, the secrets-export claim and the deployment job checkout default.

Method: documentation only; no commands were run.
