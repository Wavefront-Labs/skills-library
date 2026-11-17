---
id: computing-software.cloud-infrastructure-engineering.google-cloud.listing-constraints-and-effective-org-policies
name: listing-constraints-and-effective-org-policies
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, org-policy, effective-org-policy, describe-effective-policy, list-available-constraints, gcloud-org-policies, policy-audit]
level: practitioner
status: docs-checked
description: "Audit organization policies with gcloud org-policies: list available constraints, list set policies per node, show effective policy, and sweep a hierarchy into a report."
sources: ["https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-policies#viewing_policies", "https://cloud.google.com/sdk/gcloud/reference/org-policies", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listing constraints and effective org policies

## Commands
```bash
# built-in constraints: see the Organization policy constraints reference page (gcloud has no list-constraints command)
# custom constraints defined on an organisation
gcloud org-policies list-custom-constraints --organization=<ORG>
# policies explicitly set on a node
gcloud org-policies list --project=<P>
gcloud org-policies list --folder=<F> --show-unset   # includes unset constraints
# the result after inheritance/merge
gcloud org-policies describe compute.vmExternalIpAccess --project=<P> --effective
gcloud org-policies describe iam.allowedPolicyMemberDomains --organization=<ORG>   # raw set policy (spec + dryRunSpec)
```

## Hierarchy sweep
Run `gcloud org-policies describe <CONSTRAINT> --project=<P> --effective` per project and constraint, or at scale use Cloud Asset Inventory:
`gcloud asset analyze-org-policies --scope=organizations/<ORG> --constraint=constraints/<C>` (both flags are required).

## Reading output
- `spec.rules[].enforce: true` (boolean) / `values.allowedValues` (list).
- `dryRunSpec` = not enforced, only logged.


## Gotchas
- Use `gcloud org-policies` for dry-run specs and custom constraints (the group lists `list-custom-constraints`, `describe-custom-constraint`, `set-custom-constraint`).

## Verify
- [ ] Every project in scope shows the baseline constraints in its effective policy.

## Checked

- Date: 2026-10-27
- Confirmed against the gcloud `org-policies` group page (commands: delete, describe, list, list-custom-constraints, set-policy, set-custom-constraint), the `org-policies list` reference (`--folder|--organization|--project`, `--show-unset`), `org-policies describe` (`--effective`), `asset analyze-org-policies` (`--constraint` and `--scope` required), and the dry-run page (`dryRunSpec`).
- Removed: `gcloud org-policies list-available-constraints` (no such command; the reference page returns 404), `--show-unset=false`, the `projects list` loop, BigQuery `ORG_POLICY` export, audit-log service name, the legacy-v1 comparison and the permission and role claims.

Method: documentation only; no commands were run.
