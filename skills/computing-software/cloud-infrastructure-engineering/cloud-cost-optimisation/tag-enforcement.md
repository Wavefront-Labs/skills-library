---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.tag-enforcement
name: tag-enforcement
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-allocation, tag-enforcement, tag-policies, azure-policy, org-policy, untagged-spend, tag-remediation, policy-as-code]
level: practitioner
status: docs-checked
description: "Enforce and remediate cost tags: shift-left IaC checks, Azure Policy deny and modify, org policy constraints, detective reports and a burn-down process for untagged spend."
sources: ["https://learn.microsoft.com/azure/governance/policy/tutorials/govern-tags", "https://cloud.google.com/resource-manager/docs/organization-policy/overview", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tag enforcement and untagged spend remediation

## Layers (cheapest first)
1. **IaC defaults and CI checks**: provider-level default tags and a policy-as-code rule that fails pull requests
   without the mandatory tags.
2. **Preventive policy at the cloud**:
   - Azure Policy (governing tags tutorial): a `deny` effect can block creating or updating resource groups that lack
     a required tag (the tag must be supplied on the create request); a `modify` effect can add a tag to resources
     from the parent resource group when missing, leaving an existing value alone, or use `addOrReplace` when the
     value must not be overridden. Like deployIfNotExists, modify uses remediation tasks to fix existing
     non-compliant resources.
   - Google Cloud: an organization policy enforces one constraint on an organization, folder or project and is
     inherited by descendants; policies can run in active mode, dry-run mode or both, and custom constraints are
     defined by your organization. Check the constraint and custom-constraint supported-services lists before
     relying on a label or tag requirement.
   - AWS: use Organizations tag policies to standardise tag keys and values; read the tag policies page for which
     resource types they can enforce on.
3. **Detective**: a regular report of untagged or invalid resources by owner, using each cloud's compliance or asset
   inventory views.
4. **Auto-remediation**: copy tags from account or resource-group metadata for safe cases; notify owners for the rest.

## Burn-down process
- Weekly: untagged spend by account, top resources, sent to account owners.
- Agree a target for unallocated spend with finance, and escalate stale items.
- Agree upfront whether untagged non-prod resources may be stopped after notice.

## Gotchas
- A hard deny on day one breaks pipelines and console users: run audit or dry-run first, then enforce.
- Tag compliance is not allocation accuracy: valid-format wrong values (`team=unknown`) still pass.

## Checked
2026-11-01. Confirmed on the Azure Policy govern-tags tutorial (deny, modify, addOrReplace, remediation tasks) and
the Google organization policy overview (constraints, inheritance, dry-run, custom constraints). Removed: SCP
`aws:RequestTag` and `enforced_for` details, the claim that GCP has no require-label constraint, AWS Config
`required-tags`, CloudTrail identity copying, numeric targets.
Method: documentation only; no commands were run.
