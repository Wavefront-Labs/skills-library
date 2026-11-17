---
id: computing-software.cloud-infrastructure-engineering.azure.policy-evaluation-troubleshooting-and-requestdisallowedbypolicy
name: policy-evaluation-troubleshooting-and-requestdisallowedbypolicy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-policy, policy-troubleshooting, policy-evaluation, requestdisallowedbypolicy, policy-aliases]
level: advanced
status: docs-checked
description: "Debug Azure Policy: decode RequestDisallowedByPolicy, alias and array [*] mistakes, effect order, DINE delays and remediation identity failures."
sources: ["https://learn.microsoft.com/azure/governance/policy/troubleshoot/general", "https://learn.microsoft.com/azure/governance/policy/concepts/definition-structure-alias", "https://learn.microsoft.com/azure/governance/policy/concepts/effect-basics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot Azure Policy evaluation

**Goal:** explain why a deployment was denied (or wasn't), and why a policy reports unexpected compliance.

## RequestDisallowedByPolicy
The error names the policy assignment and policy definition that denied the request (inside an initiative, the definition is
identified by its `policyDefinitionReferenceId`). Look those up:
```bash
az policy assignment show --name <assignmentName> --scope <assignmentScope> --query "{name:displayName,scope:scope,params:parameters}"
az policy definition show --name <definitionName> --query policyRule
```
Fix paths: change the resource to comply; create an exemption with expiry; or fix the policy.

## Policy not matching what you expect
- **Alias wrong**: list real aliases and their paths:
```bash
az provider show -n Microsoft.Storage --expand "resourceTypes/aliases" \
  --query "resourceTypes[?resourceType=='storageAccounts'].aliases[].name" -o tsv | grep -i tls
```
  Check the resource's actual JSON with Resource Graph to see the value the alias reads.
- **Arrays**: `alias[*]` is an array alias: it represents the collection of values from the array's elements
  (`ipRules[*].action` is the `action` of each element of `ipRules`). Confirm which form your condition uses.
- **Mode**: `Indexed` only evaluates resource types that support tags and location, so
  `Microsoft.Network/routeTables/routes` is skipped; Microsoft recommends `All` in most cases.
- **Effect order**: `disabled` is checked first; `append` and `modify` are evaluated next and can alter the request,
  which may stop an `audit` or `deny` from triggering.

## DeployIfNotExists / modify
- `deployIfNotExists` and `auditIfNotExists` are non-compliant only when the `if` condition is true and the existence
  condition is false; compliance information lags changes (a new assignment takes about five minutes to apply).
- Remediation failing: unless the portal granted roles for you, the assignment's managed identity must be given the
  required roles manually or the remediation deployment fails.

## Other
- `enforcementMode: DoNotEnforce` evaluates compliance without enforcing the effect or writing deny entries to the
  Activity log; remediation tasks can still be started for `deployIfNotExists`. Check the assignment.
- `notScopes` and exemptions explain "why isn't it applying".

## Verify
- [ ] Reproduced with a minimal test deployment in a sandbox scope; `az policy state trigger-scan --resource-group <rg>` then shows the expected state.

## Checked
2026-10-28. Confirmed in Learn effect-basics (order of evaluation, DINE/AINE condition logic), assign-policy and
definition pages (enforcementMode, managed identity roles, Indexed mode, array alias, trigger-scan) and compliance
pages (five minute assignment delay). Removed: `--ids` flag on `az policy assignment show`/`definition show` (not
available; replaced with `--name`/`--scope`), `evaluationDetails`, the deny/action activity log operation,
`evaluationDelay` and its ~10 min default, `az policy remediation deployment list`, the `count`/`where` and case
claims, and the compliance Error state tip.
Method: documentation only; no commands were run.
