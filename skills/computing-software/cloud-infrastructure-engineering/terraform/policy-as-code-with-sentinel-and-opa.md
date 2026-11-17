---
id: computing-software.cloud-infrastructure-engineering.terraform.policy-as-code-with-sentinel-and-opa
name: policy-as-code-with-sentinel-and-opa
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [enforcement-levels, policy-set, terraform, sentinel, opa, open-policy-agent, conftest, rego, policy-as-code, policy-sets, plan-json, soft-mandatory, hard-mandatory, advisory, guardrails, compliance-as-code, tfsec, checkov, tflint]
level: advanced
status: docs-checked
description: "Gate Terraform plans with Sentinel or OPA policy sets in HCP Terraform, or OPA/Conftest in open-source pipelines: write rules against plan JSON, pick enforcement level."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/manage-policy-sets", "https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/sentinel/docs/commands/test", "https://www.conftest.dev/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Policy as code for Terraform: Sentinel and OPA

**Goal:** a rule such as "no public buckets" or "every resource has a cost-centre
tag" is enforced automatically on every plan, with a clear pass/fail/advisory outcome
and a message telling the author what to fix.

## 1. Two ecosystems, same input
Both evaluate **plan data**, not raw HCL, so they see what will change, including
computed values.
- **Sentinel**: HashiCorp's policy language, run by HCP Terraform / Terraform
  Enterprise as part of the run. HCP Terraform supports three frameworks: Terraform
  policy, Sentinel and OPA.
- **OPA/Rego via Conftest**: open source, runs anywhere. Feed it the plan JSON from
  `terraform show -json`, whose format is documented in the Terraform JSON output
  page (`resource_changes[]`, each with `change.before`, `change.after`,
  `change.after_unknown`).
```bash
terraform plan -out=plan.tfplan
terraform show -json plan.tfplan > plan.json
conftest test --policy policy/ plan.json
```

## 2. Sentinel policy shape
```python
import "tfplan/v2" as tfplan

buckets = filter tfplan.resource_changes as _, rc {
  rc.type is "aws_s3_bucket" and rc.mode is "managed"
}

main = rule {
  all buckets as _, rc {
    rc.change.after.acl is not "public-read"
  }
}
```
Imports include `tfplan/v2`, `tfconfig/v2`, `tfstate/v2` and `tfrun`; pick the
import matching what you assert on.

## 3. Rego policy shape (OPA/Conftest)
```rego
package main

deny contains msg if {
  some rc in input.resource_changes
  rc.type == "aws_s3_bucket"
  rc.change.after.acl == "public-read"
  msg := sprintf("%s must not be publicly readable", [rc.address])
}
```
Conftest looks for `deny`, `violation` and `warn` rules; rules may carry a suffix
such as `deny_myrule`. Reserve `deny` for what must block a merge. Test Rego with
`conftest verify --policy ./policy`.

## 4. Enforcement levels in HCP Terraform
- **Sentinel:** advisory (failures never interrupt the run), soft mandatory (stops
  the run; admins can allow team members to override), hard mandatory (stops the
  run; no override unless the policy set allows overrides).
- **OPA:** advisory or mandatory; a mandatory failure stops the run but a user with
  the Manage Policy Overrides permission can override it.
- **Terraform policy:** advisory, mandatory overridable, mandatory.
- A policy set's "can be overridden in the event of mandatory failures" option takes
  precedence over each policy's level, even hard mandatory.
Start new policies as advisory and promote after watching their false-positive rate.

Policies can be published through the UI, a pre-written catalogue, a VCS repository
or the Policy Sets API / `tfe_policy_set` resource. Policy evaluations cannot access
cost estimation data; use policy checks for cost-based policies.

## 5. Testing
`sentinel test` runs tests from a `test/` directory with mock data; write one passing
and one failing case per rule. For Rego use `conftest verify`. A rule
with no failing-case test is unverified.

## Gotchas
- `change.after` is unset for delete actions and incomplete when values are unknown
  until apply (`after_unknown`); guard for this or destroy plans break the rule.
- Attribute names and shapes depend on the provider schema version; re-test policies
  after provider upgrades.
- Do not interpolate secret-bearing attributes into failure messages.

## Verify
- [ ] Every blocking policy has a fixture that should fail and does.
- [ ] A destroy-only plan does not crash any policy.
- [ ] New policies spend an advisory period before blocking.

## Checked
2026-11-09. Confirmed against HCP Terraform "Manage policy sets" (frameworks, enforcement levels for Sentinel, OPA and Terraform policy, override option, publishing workflows, evaluations cannot see cost data), the Terraform JSON output format page (`resource_changes`, `after`, `after_unknown`, unset before/after on delete/create), the Sentinel `tfplan/v2`, `tfconfig/v2`, `tfstate/v2`, `tfrun` import pages, the Sentinel `test` command page and the Conftest docs (`deny`/`violation`/`warn`, `conftest verify`, current `deny contains msg if` syntax).
Corrected: OPA in HCP Terraform does have an override tier (advisory/mandatory); hard mandatory can be overridden when the policy set allows it; Rego example moved to the current syntax.
Removed as unconfirmed: "sentinel policies run server-side only / no local dry run", the "one or two week" advisory period, `rc.change.after.acl[0]` list typo example, state-leak warning specifics, and `conftest test --input` advice.
Method: documentation only; no commands were run.
