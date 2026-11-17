---
id: computing-software.cloud-infrastructure-engineering.google-cloud.analysing-org-policies-and-governed-assets
name: analysing-org-policies-and-governed-assets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-asset-inventory, analyze-org-policies, governed-assets, governed-containers, org-policy-analysis]
level: practitioner
status: docs-checked
description: "Use Cloud Asset Inventory org policy analysis to see where a constraint is set, which folders and projects it governs, and which existing assets fall under it."
sources: ["https://docs.cloud.google.com/sdk/gcloud/reference/asset/analyze-org-policies", "https://docs.cloud.google.com/sdk/gcloud/reference/asset/analyze-org-policy-governed-assets", "https://docs.cloud.google.com/asset-inventory/docs/reference/rest/v1/TopLevel/analyzeOrgPolicies", "https://docs.cloud.google.com/asset-inventory/docs/reference/rest/v1/TopLevel/analyzeOrgPolicyGovernedAssets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analysing org policies and governed assets

## Three commands
```bash
ORG=organizations/<ORG>; C=constraints/compute.vmExternalIpAccess
# 1. where is the policy set, and what is it, on every node
gcloud asset analyze-org-policies --scope=$ORG --constraint=$C
# 2. which folders/projects are governed and their effective policy
gcloud asset analyze-org-policy-governed-containers --scope=$ORG --constraint=$C
# 3. which existing resources are governed (custom constraints and the constraints listed in the API reference)
gcloud asset analyze-org-policy-governed-assets --scope=$ORG --constraint=$C
```
The scope can only be an organization.

## Uses
- Before enforcing a constraint: list the existing resources the constraint governs.
- Audit: prove a constraint is effective in every prod project.
- Find stray project-level overrides that weaken org policy.

## Filters
All three are list commands, so `--filter`, `--limit`, `--page-size` and `--sort-by` apply (see `gcloud topic filters`).

## Gotchas
- Governed-assets analysis supports custom constraints and only the canned constraints listed in the `analyzeOrgPolicyGovernedAssets` API reference.
- Permissions: the caller needs `cloudasset.assets.searchAllResources` on the scope for `analyze-org-policies`, and also `cloudasset.assets.searchAllIamPolicies` for governed assets.
- The governed-assets call returns only resource types supported by the search APIs, or IAM policies.

## Checked
2026-10-31. Confirmed against the gcloud reference for `asset analyze-org-policies` and `asset analyze-org-policy-governed-assets` (organization-only scope, required permissions, list-command flags) and the `analyzeOrgPolicyGovernedAssets` REST reference (custom constraints plus a list of canned constraints; search-API resource types or IAM policies). Removed unconfirmed: output field names in `--format`, filter strings, wrong permission names, index lag claim, the claim that supported constraints are mostly compute/storage/IAM, the `customConstraints/custom.<name>` form, and the dead concept-page source. The governed-containers command was verified by check_commands.
Method: documentation only; no commands were run.

## Verify
- [ ] Governed-containers output shows every prod project with the enforced rule.
