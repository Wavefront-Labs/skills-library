---
id: computing-software.cloud-infrastructure-engineering.azure.policy-assignments-exclusions-and-managed-identity
name: policy-assignments-exclusions-and-managed-identity
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-policy, policy-assignments, assignment-exclusions, not-scopes, enforcement-mode, non-compliance-messages, resource-selectors]
level: practitioner
status: docs-checked
description: "Assign Azure Policy definitions and initiatives at the right scope with parameters, notScopes, enforcement mode, resource selectors and a managed identity for Modify/DINE."
sources: ["https://learn.microsoft.com/azure/governance/policy/concepts/assignment-structure", "https://learn.microsoft.com/azure/governance/policy/assign-policy-azurecli", "https://learn.microsoft.com/azure/governance/policy/how-to/remediate-resources", "https://learn.microsoft.com/azure/governance/policy/how-to/policy-safe-deployment-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy assignments, exclusions and managed identity

**Goal:** every policy lands at the right scope with explicit parameters, a clear
non-compliance message, and (for Modify/DeployIfNotExists) an identity that has exactly the
roles the remediation needs.

## Scope choice
Assign at the **highest management group** where the rule is universally true; use `notScopes`
for structural exceptions (sandbox MG) and **exemptions** for time-boxed exceptions on single
resources.

## Assign (CLI)
```bash
az policy assignment create \
  --name deny-public-ip --display-name "Deny public IPs on NICs" \
  --policy 83a86a26-fd1f-447c-b59d-e51f44264114 \
  --scope /providers/Microsoft.Management/managementGroups/mg-corp \
  --not-scopes /subscriptions/<sandbox-sub> \
  --enforcement-mode Default \
  --params '{"effect":{"value":"Deny"}}'
az policy assignment non-compliance-message create -g "" --name deny-public-ip \
  --scope /providers/Microsoft.Management/managementGroups/mg-corp \
  --message "Public IPs are not allowed in corp landing zones. Use Front Door or App Gateway. See wiki/net-001."
```

## Identity for Modify / DeployIfNotExists
```bash
az policy assignment create --name diag-to-law --policy-set-definition <initiative-id> \
  --scope <mg-id> --mi-system-assigned --location westeurope \
  --params @diag-params.json
# grant the roles listed in the definition's roleDefinitionIds at the assignment scope
pid=$(az policy assignment show -n diag-to-law --scope <mg-id> --query identity.principalId -o tsv)
az role assignment create --assignee-object-id $pid --assignee-principal-type ServicePrincipal \
  --role "Log Analytics Contributor" --scope <mg-id>
```
An assignment can have one system-assigned or one user-assigned identity. A user-assigned identity shared by
all platform assignments (`--mi-user-assigned <id>`) makes role grants auditable in one place.

## Safe rollout
1. `--enforcement-mode DoNotEnforce` first: compliance is evaluated, nothing is denied or deployed.
2. **Resource selectors** for staged rollout by region:
```json
"resourceSelectors": [{ "name": "wave1", "selectors": [{ "kind": "resourceLocation", "in": ["westeurope"] }] }]
```
3. **Overrides** change effect without a new definition (`"overrides":[{"kind":"policyEffect","value":"Audit"}]`).
4. Promote to Default after reviewing compliance results. Remediation tasks for deployIfNotExists can run even in DoNotEnforce.

## Gotchas
- `notScopes` excludes child containers/resources from evaluation; an exemption is a separate construct.
- Changing the identity breaks remediation until roles are re-granted to the new principal.

## Verify
- [ ] `az policy assignment show -n <name> --scope <scope> --query "{mode:enforcementMode,notScopes:notScopes,identity:identity.type}"`.
- [ ] A deliberate violating deployment fails with the custom non-compliance message.
- [ ] A remediation task on a DINE assignment succeeds (proves identity roles).

## Checked

Date: 2026-10-28.

Confirmed against Learn (assignment-structure, remediate-resources, policy-safe-deployment-practices): enforcementMode Default/DoNotEnforce, notScopes versus exemptions, resourceSelectors with resourceLocation, overrides of kind policyEffect, identity required for deployIfNotExists/modify with one system- or user-assigned identity. CLI flags via check_commands.py.
Removed: 200-assignment limit, name length limits, 30-minute and 24-hour timings, portal-versus-CLI role grant claim, delegation claim and parameter re-evaluation claim (not on fetched pages).

Method: documentation only; no commands were run.
