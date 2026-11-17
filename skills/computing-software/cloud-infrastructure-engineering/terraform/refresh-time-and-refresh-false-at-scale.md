---
id: computing-software.cloud-infrastructure-engineering.terraform.refresh-time-and-refresh-false-at-scale
name: refresh-time-and-refresh-false-at-scale
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, refresh-time, refresh-false, large-state-performance, target, drift-detection, api-rate-limits]
level: practitioner
status: docs-checked
description: "Manage refresh cost in large Terraform states: measuring it, when -refresh=false is safe, scheduled drift jobs and splitting state."
sources:
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://developer.hashicorp.com/terraform/tutorials/state/refresh
  - https://developer.hashicorp.com/terraform/cloud-docs/workspaces/health
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Refresh time and -refresh=false trade-offs at scale

By default Terraform refreshes prior to creating a plan. With thousands of resources, refresh dominates plan time and can hit provider API rate limits.

## Measure
```bash
time terraform plan -refresh-only -out=/dev/null      # mostly refresh cost
time terraform plan -refresh=false                     # config evaluation and diff only
terraform state list | wc -l
terraform state list | cut -d. -f1-2 | sed 's/\[.*//' | sort | uniq -c | sort -rn | head   # which resource types dominate
```

## -refresh=false
Plan uses state as-is, without reading real infrastructure.
Safe-ish when:
- You just refreshed (e.g. second plan in the same pipeline after a refresh-only plan).
- Iterating locally on config changes where drift doesn't matter for the review.
Risky because:
- The plan won't show drift; apply may **revert** out-of-band changes or fail when real objects differ (deleted resources, changed attributes).
- Terraform refreshes a resource regardless when its schema version changes, so avoid `-refresh=false` (and `-minimal-refresh`) when upgrading provider versions.
Never use it for production applies without a recent refresh-only check.

## Better structural fixes
1. **Split state**: smaller roots by component/lifecycle (network, data, apps). The docs recommend several smaller, independently applied configurations over `-target` for very large ones.
2. **Parallelism**: `-parallelism=n` limits concurrent operations (default 10); raise it only if the API allows, lower it when throttled.
3. **Scheduled drift detection** instead of refresh on every plan: a scheduled `terraform plan -refresh-only -detailed-exitcode` per root (exit code 2 = succeeded with a non-empty diff), alerting on it. HCP Terraform health assessments periodically run drift detection in a workspace (Standard and Premium editions; check the page for requirements).

## -target is not a performance tool
`-target` focuses planning on the matched resource instances and what they depend on. The docs say to use it in exceptional circumstances only, such as recovering from mistakes, because routine use can lead to undetected configuration drift.

## Verify
- [ ] Plan time per root measured and tracked; slow roots have a plan to split.
- [ ] Drift detection runs on a schedule; production applies always follow a refresh.

## Checked
Date: 2026-10-28.
Confirmed in the plan command page: `-refresh-only`, `-refresh=false` and `-minimal-refresh` wording, schema-version refresh note, `-target` guidance and splitting advice, `-detailed-exitcode` (2 = non-empty diff), `-parallelism` default 10. Confirmed in the data sources page: refresh by default before planning. Confirmed in the HCP Terraform health page: periodic drift detection, Standard/Premium editions.
Removed as unconfirmed: provider retry tuning, claims about which resources skip refresh, route53/IAM scaling advice, the 5 minute threshold.
Method: documentation only; no commands were run.
