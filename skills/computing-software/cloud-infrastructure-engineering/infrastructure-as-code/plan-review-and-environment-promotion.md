---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.plan-review-and-environment-promotion
name: plan-review-and-environment-promotion
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, terraform, opentofu, pulumi, terraform-plan, plan-review, policy-as-code, opa, rego, conftest, checkov, tfsec, trivy, sentinel, drift-detection, gitops, atlantis, environment-promotion, pull-request-workflow, prevent-destroy, infracost, cdk-diff, bicep-what-if]
level: practitioner
status: gated
description: "Review IaC plans like code: read the diff for replaces and destroys, gate with OPA/Conftest/Checkov, detect drift on a schedule, and promote one artifact through dev, stage, prod."
sources: ["HashiCorp Terraform docs - terraform plan and JSON output format", "Open Policy Agent docs - Conftest and Rego", "Checkov documentation", "Atlantis documentation", "Microsoft Learn - Bicep what-if"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IaC plan review and environment promotion — no surprise destroys reach prod

**Goal:** every infrastructure change is a PR whose plan a human reads for the risky
parts, machines check for policy, and the same versioned code moves from dev to prod
with only variables changing.

## 1. Produce a reviewable plan
- CI on every PR: `fmt -check` → `validate` → `tflint` → static scan → `plan -out=tfplan`
  → `show -json tfplan > plan.json` → policy check → post summary as a PR comment
  (Atlantis, HCP Terraform, Spacelift, env0, Digger, or a plain pipeline).
- Equivalents: `pulumi preview --diff`, `cdk diff`, `az deployment group what-if` (Bicep),
  `gcloud infra-manager previews` (these non-Terraform commands and the PR-automation products named above were not run here: gated: unconfirmed, tools not installed).
- Apply the **saved plan** after merge (or on `atlantis apply` before merge, then merge);
  if the plan is stale (state changed), re-plan — Terraform refuses a stale saved plan (checked on 1.9.8: applying an old `tfplan` after another apply gave "Error: Saved plan is stale").

## 2. Read the plan like a reviewer
Check the summary line `Plan: X to add, Y to change, Z to destroy` first, then hunt for:
- `-/+ ... must be replaced` (verified in plan output) and, for provider resources, the `# forces replacement` attribute annotation (not shown for `terraform_data.triggers_replace` in my test, so it is provider-dependent) — a renamed DB,
  changed subnet or AZ often means data loss.
- Any `destroy` you did not intend: commonly a `count` index shift, a module address change
  (needs a `moved` block); a shrinking `count` list shows as `list[1] will be updated in-place` plus `list[2] will be destroyed (because index [2] is out of range for count)` (checked), or a provider upgrade changing defaults.
- IAM and security-group changes: `0.0.0.0/0`, `"*"` actions, new trust principals.
- `(known after apply)` on identifiers that feed other resources — cascade replacements.
- Changes outside the PR's intent: that is **drift** someone made by hand; decide to
  adopt (update code) or revert (apply) before merging.
Mechanise the scary part:
```bash
jq -r '.resource_changes[] | select(.change.actions | index("delete")) | .address' plan.json
```
Fail or require a second approver when the list is non-empty for prod. Checked with jq on a real `terraform show -json` of a replacement: it printed the replaced address (a replace has actions `delete` and `create`, so it is caught too).

## 3. Policy as code
- **Static scanners** on HCL/templates: Checkov (`checkov -d .`), Trivy config
  (`trivy config .`, successor to tfsec), KICS. Fast, catch encryption/public access/logging.
- **Plan-time policy** on `plan.json` with OPA/Conftest:
  ```rego
  package main
  import rego.v1
  deny contains msg if {
    rc := input.resource_changes[_]
    rc.type == "aws_s3_bucket_public_access_block"
    rc.change.after.block_public_acls == false
    msg := sprintf("%s disables public ACL blocking", [rc.address])
  }
  ```
  `conftest test plan.json -p policy/` (ran with Conftest 0.71.1: `FAIL ... disables public ACL blocking`, exit 1). Plan-time sees resolved values that static scans miss.
- Commercial equivalents: Sentinel / OPA in HCP Terraform, Pulumi CrossGuard.
- Severity tiers: hard-fail (public data, missing encryption), soft-fail with documented
  waiver (`#checkov:skip=CKV_AWS_18:reason`), advisory. Waivers expire and are reviewed.
- Add **Infracost** to show cost delta per PR.

## 4. Promote, don't copy
- One module version, many environments: `live/dev`, `live/stage`, `live/prod` reference
  `modules/app?ref=v1.8.0`; promotion is a PR bumping the ref in the next environment
  after the previous one is healthy.
- Alternatively one root with per-env `.tfvars` and per-env backend config — keep
  differences to sizes, counts and IDs, never to structure (`count = var.env == "prod"`
  scattered everywhere hides untested paths).
- Gate prod applies with protected environments / required reviewers, and use a separate
  CI identity per environment so a dev pipeline cannot touch prod.
- Protect stateful resources: `lifecycle { prevent_destroy = true }` on databases, KMS keys,
  state buckets; provider-level deletion protection where offered.

## 5. Drift detection
- Scheduled `terraform plan -detailed-exitcode -refresh-only` (nightly): exit 0 = clean,
  2 = drift, 1 = error. Alert on 2. (`terraform plan -help`: 0 no diff, 1 error, 2 diff; clean refresh-only run returned 0; a real drift case was not reproduced here.)
- Built-in options: HCP Terraform health assessments, Spacelift drift detection, driftctl
  (maintenance mode per its README, last release v0.40.0 in Dec 2023, repo not archived — do not adopt new).
- Reduce drift at source: read-only console roles in prod, changes only via pipeline.

## Gotchas
- `-target` applies leave state partially reconciled; never as a habit in CI.
- The human-readable plan masks `(sensitive value)`, but `plan.json` contains the real values
  (flagged in `after_sensitive`): policies can check them, and the JSON must be handled as a secret.
- Providers that normalise values (JSON policies, tags casing) show perpetual diffs; fix
  with `jsonencode` or `ignore_changes`, not by ignoring the noise.
- `prevent_destroy` lives inside the resource block: delete the block from code and the protection goes with it, so the destroy proceeds. With it set, a replacement plan fails at plan time ("Error: Instance cannot be destroyed"), which is a useful early stop (checked).
- Applying from a laptop bypasses every gate above; remove human write access to state.

## Verify
- [ ] Every PR shows plan summary, policy result and cost delta as a comment.
- [ ] A test PR that replaces a prod database is blocked or needs extra approval.
- [ ] Conftest/Checkov failures fail the pipeline; waivers have reasons and expiry.
- [ ] The same module version is running in stage before prod's ref is bumped.
- [ ] Nightly drift check runs and alerts on exit code 2.
- [ ] Prod applies are possible only from the pipeline identity.

Related: computing-software.cloud-infrastructure-engineering.terraform.remote-state-and-module-layout
