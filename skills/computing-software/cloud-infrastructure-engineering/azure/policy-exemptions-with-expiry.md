---
id: computing-software.cloud-infrastructure-engineering.azure.policy-exemptions-with-expiry
name: policy-exemptions-with-expiry
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-policy, policy-exemptions, exemptions, waiver, mitigated, exemption-expiry, policy-governance]
level: practitioner
status: docs-checked
description: "Grant Azure Policy exemptions (Waiver vs Mitigated) on a resource or scope with an expiry date, per-definition references and an audit trail; report expiring exemptions."
sources: ["https://learn.microsoft.com/azure/governance/policy/concepts/exemption-structure", "https://learn.microsoft.com/azure/governance/policy/tutorials/create-and-manage#exempt-a-non-compliant-or-denied-resource-using-exemption", "https://learn.microsoft.com/cli/azure/policy/exemption"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy exemptions with expiry

**Goal:** exceptions to policy are explicit, narrow, owned and time-boxed — never a silent
`notScopes` edit or a disabled assignment.

## Exemption vs alternatives
| Need | Use |
|---|---|
| A resource legitimately can't comply for now | Exemption, category **Waiver**, expiry |
| Requirement met by another control (3rd-party firewall) | Exemption, category **Mitigated** |
| Whole MG/sub permanently out of scope (sandbox) | `notScopes` on the assignment |
| Rule wrong for everyone | Fix the definition |

## Create
```bash
az policy exemption create \
  --name ex-legacy-vm-public-ip \
  --display-name "Legacy FTP VM needs public IP until migration (CHG0012345)" \
  --policy-assignment /providers/Microsoft.Management/managementGroups/mg-corp/providers/Microsoft.Authorization/policyAssignments/corp-baseline \
  --policy-definition-reference-ids deny-public-ip-nic \
  --exemption-category Waiver \
  --expires-on 2026-12-31T23:59:59Z \
  --scope /subscriptions/<sub>/resourceGroups/rg-legacy/providers/Microsoft.Network/networkInterfaces/nic-ftp01 \
  --description "Owner: app-team-ftp. Risk accepted by CISO 2026-10-10." \
  --metadata requestedBy=jdoe approvedBy=ciso ticket=CHG0012345
```
- `--policy-definition-reference-ids` limits the exemption to chosen policies inside an initiative assignment;
  omit it and the scope is exempt from the whole assignment.
- An exemption covers a resource hierarchy or an individual resource; keep the scope as small as possible.
- Normally the exemption scope must be at or under the assignment scope. `assignmentScopeValidation` (`Default` or
  `DoNotValidate`) lets an exemption bypass that check; use it rarely.
- `expiresOn` is optional and must be ISO 8601 `yyyy-MM-ddTHH:mm:ss.fffffffZ`. Exemptions also accept `resourceSelectors`
  (up to 10) and free-form `metadata` for requester, approver and ticket.

## Report and expire
```kusto
// Azure Resource Graph
policyresources
| where type == "microsoft.authorization/policyexemptions"
| extend expires = todatetime(properties.expiresOn), category = tostring(properties.exemptionCategory)
| where isnull(expires) or expires < now() + 30d
| project name, category, expires, scope = tostring(properties.policyAssignmentId), description = tostring(properties.description)
```
At the `expiresOn` date the exemption is no longer honoured but the object is kept for record-keeping; clean them up on a schedule.
Flag exemptions with no `expiresOn` as a governance finding.

## Gotchas
- Exempt resources show as **Exempt** and count toward overall compliance, so dashboards can hide risk; report exemptions separately.

## Verify
- [ ] `az policy exemption list --scope <scope> -o table` shows category and expiry.
- [ ] The previously denied deployment now succeeds; other policies in the initiative still apply.
- [ ] Monthly ARG report of expiring exemptions is sent to owners.

## Checked
2026-10-28. Confirmed in Learn exemption-structure: Waiver and Mitigated meanings, expiresOn format and behaviour at expiry, metadata,
resourceSelectors limit of 10, assignmentScopeValidation values and purpose, Exempt counting toward compliance. The CLI flags
passed check_commands. Removed: the permission actions section, the claim that deny evaluation needs the exemption to exist
beforehand, the assignment-recreation gotcha, and the explicit resource/RG/subscription/MG scope list.
Method: documentation only; no commands were run.
