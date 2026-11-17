---
id: computing-software.cloud-infrastructure-engineering.azure.alz-accelerator-bicep-and-terraform-deployment
name: alz-accelerator-bicep-and-terraform-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, alz, alz-accelerator, alz-bicep, alz-terraform, avm, bootstrap, platform-pipelines]
level: advanced
status: docs-checked
description: "Deploy Azure Landing Zones with the ALZ IaC accelerator: bootstrap repo, identity and pipelines with ALZ PowerShell, choose Bicep or Terraform AVM starter modules, run plan/apply."
sources: ["https://azure.github.io/Azure-Landing-Zones/accelerator/", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/deploy-landing-zones-with-terraform", "https://github.com/Azure/ALZ-PowerShell-Module"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy ALZ with the Bicep or Terraform accelerator

**Goal:** the platform landing zone (management groups, policies, connectivity, management)
deployed from a Git repo by pipelines with OIDC identities — not clicked in the portal.

## Phase 0 — decisions before running anything
- IaC: **Terraform** or **Bicep** (see the accelerator docs for the starters).
- VCS: GitHub or Azure DevOps (hosted versions).
- Connectivity: hub-and-spoke VNet vs Virtual WAN; regions (primary + secondary).
- Subscriptions: create the platform subscriptions (management, identity, connectivity) up front and have their IDs ready.
- Intermediate root MG name/ID (`alz` default) — changing later means migrating everything.

## Phase 1 — prerequisites
- The accelerator Phase 1 page lists the Azure permissions, tools and VCS token you need; follow it rather than a summary.
```powershell
Install-Module -Name ALZ -Scope CurrentUser
az login --tenant <tenant-id>
Deploy-Accelerator -inputs "inputs.yaml"
```
`inputs.yaml` holds the IaC type, bootstrap and starter module choices, subscription IDs, regions and VCS organisation; see the accelerator docs for the key names.

## Phase 2: what bootstrap creates
Per the accelerator overview: a resource group and storage account for Terraform state (Terraform only), plus the repositories, identities and pipelines or workflows for your chosen VCS; the overview page has the full component list.

## Phase 3: customise and deploy
- Edit the starter configuration files in the repo (address spaces, policy parameters and so on), open a PR, review the plan, merge, then approve the apply.

## Phase 4: remove bootstrap privileges
Remove any tenant-root permissions you granted to a human for bootstrap once it is done, and keep the deployment identity at the narrowest scope that works. Store `inputs.yaml` (no secrets) in the repo.

## Gotchas
- Pin module and library versions and read release notes before upgrading; policy changes can change effects.

## Verify
- [ ] The management group hierarchy from your chosen starter exists and subscriptions are placed.
- [ ] Policy compliance blade shows ALZ initiatives assigned at intermediate root.
- [ ] A no-op PR produces an empty plan; pipeline identities have no secrets.

## Checked
2026-10-28. Confirmed on the ALZ accelerator docs and ALZ PowerShell module README: `Install-Module -Name ALZ`, `Deploy-Accelerator -inputs "inputs.yaml"`, GitHub and Azure DevOps supported (hosted versions), a state resource group and storage account for Terraform only.
Removed (not confirmed): tenant-root Owner and PowerShell 7.4 prerequisites, inputs.yaml key names, `-output` parameter, identity and pipeline details, the 1-2 h run time, gotchas, and the 404 Bicep deployment source.

Method: documentation only; no commands were run.
