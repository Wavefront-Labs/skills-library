---
id: computing-software.cloud-infrastructure-engineering.azure.bicep-what-if-gating-in-ci
name: bicep-what-if-gating-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bicep, what-if, what-if-gating, what-if-preview, arm-templates, pull-request-checks]
level: practitioner
status: docs-checked
description: "Run ARM/Bicep what-if in pull requests: post the change summary, fail on deletes or unexpected resource changes, filter noise, and approve the exact plan before deploy."
sources: ["https://learn.microsoft.com/azure/azure-resource-manager/templates/deploy-what-if", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/deploy-what-if", "https://learn.microsoft.com/cli/azure/deployment/group#az-deployment-group-what-if"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# What-if previews in CI

**Goal:** every infra PR shows reviewers exactly what will be created, modified or deleted, and
dangerous changes block merge automatically.

## Run what-if
```bash
az deployment group what-if -g rg-orders-prd -f main.bicep -p main.prd.bicepparam \
  --result-format FullResourcePayloads --no-pretty-print > whatif.json
# scopes: az deployment sub|mg|tenant what-if --location <loc> ...
```
`--result-format ResourceIdOnly` for a compact list (default `FullResourcePayloads`); `--exclude-change-types Ignore NoChange` to cut noise (accepted values: Create, Delete, Deploy, Ignore, Modify, NoChange, Unsupported).
Change types in the output also include `NoEffect`; with `ResourceIdOnly` you may see `Deploy` instead of `Modify`/`NoChange`.

## Gate in the pipeline
```bash
deletes=$(jq '[.changes[] | select(.changeType=="Delete")] | length' whatif.json)
if [ "$deletes" -gt 0 ] && [ "$ALLOW_DELETES" != "true" ]; then
  jq -r '.changes[] | select(.changeType=="Delete") | .resourceId' whatif.json
  echo "::error::What-if reports deletions; set ALLOW_DELETES with approval"; exit 1
fi
```
Complete-mode deployments and deployment stacks set to delete unmanaged resources are where deletes come from — gate them hardest.
Post the human-readable output as a PR comment (GitHub: `gh pr comment --body-file`; ADO: PR thread REST API) truncated to the changed resources.

## Approve what you previewed
- Same commit, same parameters, same identity for what-if and deploy.
- Use environment approvals between the what-if stage and the deploy stage; show the what-if artifact in the approval.
- Re-run what-if if the target changed (drift) between preview and approval — or deploy within a short window.

## Noise
What-if can report properties as changed or deleted when they are not in the template but are set automatically as defaults during deployment (documented as "noise"). Track noisy properties and filter them in the gate
(`select(.delta[]?.path | test("tags|etag") | not)`) rather than ignoring all modifies.
What-if expands nested templates only up to 500 nested templates, 800 resource groups and 5 minutes; beyond a limit the remaining resources show change type `Ignore`.

## Gotchas
- What-if has the same permission requirements as the deployment itself (write on the resources plus `Microsoft.Resources/deployments/*`); a PR pipeline identity needs a role that grants them.
- A clean what-if can still fail on deploy; treat it as a preview, not a guarantee.
- `--mode Complete` in what-if lists all unmanaged resources in the RG as Delete — that's real.

## Verify
- [ ] A PR deleting a resource fails the gate and shows the resource ID.
- [ ] Deploy stage uses the same parameter file hash as the what-if stage (log it).

## Checked
2026-10-28. Confirmed against Microsoft Learn Bicep/ARM what-if articles and the az deployment group what-if reference: `--result-format` values and default, `--exclude-change-types` accepted values, `--no-pretty-print`, change types incl. NoEffect and Deploy, what-if limits (500 nested templates, 800 resource groups, 5 minutes, then Ignore), same permissions as deploy, noise from default-set properties. Removed: the whatIf/action permission, Unsupported-at-5-levels, the Azure Policy claim and the `--action-on-unmanage` flag detail (not in these pages).
Method: documentation only; no commands were run.
