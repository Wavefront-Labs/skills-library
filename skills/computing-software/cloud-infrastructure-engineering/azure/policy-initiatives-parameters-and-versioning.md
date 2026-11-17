---
id: computing-software.cloud-infrastructure-engineering.azure.policy-initiatives-parameters-and-versioning
name: policy-initiatives-parameters-and-versioning
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-policy, policy-initiatives, policy-set-definition, policy-versioning, assignment-overrides, policy-groups]
level: advanced
status: docs-checked
description: "Author Azure Policy initiatives: parameter pass-through, reference IDs, groups, overrides and selectors, safe parameter changes and policy definition versioning."
sources: ["https://learn.microsoft.com/azure/governance/policy/concepts/initiative-definition-structure", "https://learn.microsoft.com/azure/governance/policy/concepts/assignment-structure", "https://learn.microsoft.com/azure/governance/policy/concepts/definition-structure-basics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy initiatives, parameters and versioning

**Goal:** bundle policies into a maintainable initiative that can evolve without breaking existing assignments.

## Structure
```json
{
  "properties": {
    "displayName": "Org baseline - storage",
    "metadata": { "category": "Storage" },
    "version": "1.2.0",
    "parameters": {
      "effect": { "type": "String", "allowedValues": ["Audit","Deny","Disabled"], "defaultValue": "Audit" }
    },
    "policyDefinitionGroups": [ { "name": "network", "displayName": "Network isolation" } ],
    "policyDefinitions": [
      {
        "policyDefinitionReferenceId": "storage-min-tls",
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/<builtin-guid>",
        "parameters": { "effect": { "value": "[parameters('effect')]" } },
        "groupNames": ["network"]
      }
    ]
  }
}
```
```bash
az policy set-definition create -n org-storage-baseline --management-group mg-contoso \
  --definitions @defs.json --params @params.json --definition-groups @groups.json
```

## Parameter rules
- Once an initiative is assigned, initiative-level parameters cannot be altered, so give every parameter a `defaultValue`.
- Use one effect parameter per policy (`effect-storage-min-tls`) when teams need different enforcement per control.
- Keep `policyDefinitionReferenceId` stable: exemptions and overrides reference it.

## Overrides instead of forks
Assignment `overrides` change effects of member policies without a new initiative; `resourceSelectors` roll out by
location or resource type (safe deployment practice). One override can cover up to 50 `policyDefinitionReferenceId` values,
and a selector's `in`/`notIn` list holds up to 50 values; an assignment can contain up to 10 `resourceSelectors`:
```json
"overrides": [{ "kind": "policyEffect", "value": "Deny",
  "selectors": [{ "kind": "policyDefinitionReferenceId", "in": ["storage-min-tls"] }] }],
"resourceSelectors": [{ "name": "wave1", "selectors": [{ "kind": "resourceLocation", "in": ["westeurope"] }] }]
```

## Versioning
- Versions use `{Major}.{Minor}.{Patch}`; a preview definition carries a `-preview` suffix and `deprecated` is a metadata flag.
  The docs recommend the `version` property over `metadata.version`.
- Custom initiative versioning is in public preview, with up to four versions per custom initiative.
- For built-in and custom definitions an assignment can set `definitionVersion`; by default it uses the latest major
  version and ingests minor and patch changes automatically.

## Verify
- [ ] Updated initiative deploys without assignment errors; each reference ID in overrides and exemptions still exists.

## Checked
2026-10-28. Confirmed in Learn initiative-definition-structure and assignment-structure: parameters cannot be altered after assignment and
defaultValue is recommended, groupNames/policyDefinitionGroups, `version` vs `metadata.version`, preview versioning and four-version
cap, definitionVersion default, override and resourceSelector limits (50 and 10), set-definition create example. Removed: the claim
that missing defaults make assignment updates fail, never-rename rule, EPAC tooling, the 'hundreds' cap on policies per initiative,
the portal slowdown claim, and the groupNames portal check.
Method: documentation only; no commands were run.
