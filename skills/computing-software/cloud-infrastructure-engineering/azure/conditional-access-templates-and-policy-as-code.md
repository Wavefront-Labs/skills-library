---
id: computing-software.cloud-infrastructure-engineering.azure.conditional-access-templates-and-policy-as-code
name: conditional-access-templates-and-policy-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, conditional-access, ca-templates, ca-as-code, ca-graph-api, microsoft365dsc, terraform-azuread]
level: advanced
status: docs-checked
description: "Deploy Conditional Access from templates and manage it as code via Graph, Terraform or Microsoft365DSC, with naming, backups, testing and drift control."
sources: ["https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-policy-common", "https://learn.microsoft.com/graph/api/conditionalaccessroot-post-policies", "https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/conditional_access_policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional Access templates and policy-as-code

**Goal:** reproducible, reviewable CA across tenants instead of hand-clicked policies nobody can explain.

## Start from templates
CA > Create new policy from templates: categories Secure foundation, Zero Trust, Remote work, Protect
administrator, Emerging threats. Template policies exclude only the user who creates them from the template, so edit the excluded users and groups
to add your break-glass accounts; review each policy's state before enabling it.

## Naming convention
`CA<nnn>-<Persona>-<Apps>-<Control>`, e.g. `CA001-AllUsers-AllApps-RequireMFA`, `CA010-Admins-AllApps-PhishResistant`.
Persona-based sets (Admins, Internals, Externals, Guests, Workload identities) scale better than app-based ones.

## Graph
```bash
# backup every policy as JSON
az rest --method GET --url https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies > ca-backup.json
# create
az rest --method POST --url https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies \
  --headers Content-Type=application/json --body @CA001.json
```
Permissions: `Policy.ReadWrite.ConditionalAccess` plus `Policy.Read.All` and `Application.Read.All`.
Strip `id`, `createdDateTime`, `modifiedDateTime` before re-posting a backup.

## PowerShell and other tooling
Graph PowerShell: `New-MgIdentityConditionalAccessPolicy -BodyParameter $params` (the Graph policy reference has examples).
Terraform and tenant-configuration tools can manage the same objects; check their own documentation for current resource names.

## Testing
Keep a test user per persona and check sign-in outcomes after each rollout.

## Gotchas
- Group, user, app and named-location references are object IDs - parameterise per tenant.
- Portal edits create drift; enforce "changes only via pipeline" with a weekly export diff.
- Deploying `enabled` directly can lock everyone out - pipelines should only ever create in report-only and a
  human flips state after reviewing impact.

## Verify
- [ ] Nightly backup JSON exists; the pipeline's deployed state matches the backup; every policy excludes break-glass.

## Checked
2026-10-27. Confirmed on Microsoft Learn: concept-conditional-access-policy-common (template categories Secure foundation, Zero Trust, Remote work, Protect administrator, Emerging threats;
templates exclude only the creating user), Graph conditionalaccessroot-post-policies (POST /identity/conditionalAccess/policies, permissions Policy.ReadWrite.ConditionalAccess, Policy.Read.All,
Application.Read.All, `New-MgIdentityConditionalAccessPolicy`, `builtInControls` mfa).
Removed: Terraform resource example (the provider page returned nothing readable), Microsoft365DSC and Maester references, the claim that templates are created in report-only.

Method: documentation only; no commands were run.
