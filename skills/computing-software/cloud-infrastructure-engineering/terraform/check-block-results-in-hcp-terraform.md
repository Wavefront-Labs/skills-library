---
id: computing-software.cloud-infrastructure-engineering.terraform.check-block-results-in-hcp-terraform
name: check-block-results-in-hcp-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, check-results, check-block, continuous-validation, health-assessments, hcp-terraform]
level: practitioner
status: docs-checked
description: "Write and read check block results: non-blocking warnings in CLI runs, scoped data sources, HCP Terraform continuous validation and health tab, and Check failed notifications."
sources: ["https://developer.hashicorp.com/terraform/language/block/check", "https://developer.hashicorp.com/terraform/language/validate", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/health", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/notifications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# check block results

```hcl
check "health_check" {
  data "http" "endpoint" {
    url = "https://api.example.com/health"
  }

  assert {
    condition     = data.http.endpoint.status_code == 200
    error_message = "Health check failed: ${data.http.endpoint.url} returned ${data.http.endpoint.status_code}"
  }
}
```

## What a check block is
- Needs Terraform v1.5.0 or later (preconditions and postconditions need v1.2.0).
- Runs as the last step of a plan or apply, after postconditions. If an assertion fails, Terraform reports a warning and continues; it is the only validation that does not block operations.
- Needs at least one `assert` block (`condition` and `error_message` both required); a check can have several. For a check to pass, every assertion must be true.
- Optional nested `data` block: fetched as the final step of the plan or apply, referenceable only inside its parent check, and its provider errors are masked as warnings.
- The nested data block accepts the `depends_on` and `provider` meta-arguments. With `depends_on = [aws_db_instance.main]` Terraform waits for the upstream resource and prints "known after apply" instead of a false warning until it exists.
- `condition` may reference nested data sources plus variables, resources, data sources and module outputs of the current module.

## In HCP Terraform
- Enabling health assessments on a workspace makes HCP Terraform validate check blocks, preconditions and postconditions continuously (continuous validation). Checks also run every time a health assessment runs. Health assessments are available in the Standard and Premium editions.
- Workspace requirements: Terraform 1.3.0+ for drift detection plus continuous validation; remote or agent execution mode; the latest run must have succeeded, otherwise assessments pause until a successfully applied run.
- Enable: workspace Settings > Health > Enable under Health Assessments > Save settings (not possible when the organization enforces assessments).
- Results: workspace Health > Continuous validation lists each object with pass/fail and the error messages of failed assertions; a check block shows as the prefix `check` plus its name. For a resource/output/data source with several preconditions and postconditions, individual results show only when they fail.
- The overview Health bar summarises passed, failed and unknown check statuses; the organization Workspaces page shows a Health warning for failed continuous validation.
- Notifications: workspace Settings > Notifications, workspace event **Check failed** ("one or more failed continuous validation checks"), only available when health assessments are enabled. Destinations are generic webhook, Slack, Microsoft Teams or email.

## False positives
Assessments run a speculative plan, and checks are evaluated as the last step of it. If a data source's queried value has changed since the last run, the plan includes the change and the check can fail although your infrastructure has not changed. To avoid it, have checks use nested data sources that query actual resource configuration rather than a computed latest value (the health page's AMI example uses `hcp_packer_artifact`).

## Gotchas
- Checks are not a guard: a failed assertion never stops a run. Use variable validation, preconditions or postconditions when you need to block.
- `terraform show -json` documents an experimental "checks" representation (status values `pass`, `fail`, `error`, `unknown`); the page lists only `resource` and `output_value` address kinds, so do not assume check blocks appear there without testing it.

## Checked
Date: 2026-11-07. Read in full: the check block reference, the "Validate your configuration" page, the HCP Terraform Health page (requirements, scheduling, continuous validation, false-positive section) and the Workspace notifications page; also the JSON output format "Checks Representation" section. Removed as unsupported: the literal CLI warning text, the `retry { attempts = 3 }` advice, the "roughly daily" schedule and Plus-tier claim, the `jq` pipeline over `.checks[]` and its address fields, the claim that unknown status appears on first plan of new resources, and the Verify step. Linked tutorials and the Explorer page were not opened.
Method: documentation only; no commands were run.
