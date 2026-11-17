---
id: computing-software.cloud-infrastructure-engineering.terraform.opa-rego-over-plan-json-with-conftest
name: opa-rego-over-plan-json-with-conftest
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, opa-plan-json, rego-terraform, conftest-ci, conftest, open-policy-agent, policy-as-code]
level: advanced
status: gated
description: "Write OPA Rego policies over terraform show -json plan output and run them with conftest in CI, including tests, namespaces and exceptions."
sources: ["https://www.openpolicyagent.org/docs/latest/terraform/", "https://www.conftest.dev/", "https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/opa"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPA/Rego over plan JSON with conftest

## Produce the input
```bash
terraform plan -out=tfplan -input=false
terraform show -json tfplan > plan.json
```

## Policy (Rego v1 syntax)
The `import rego.v1` / `contains ... if` syntax below is not shown on the fetched pages; check it against your OPA and conftest versions (gated: unconfirmed, source is paywalled or blocked).
```rego
# policy/s3.rego
package main

import rego.v1

deny contains msg if {
  some rc in input.resource_changes
  rc.type == "aws_s3_bucket_public_access_block"
  rc.change.actions[_] in {"create", "update"}
  not rc.change.after.block_public_acls
  msg := sprintf("%s must set block_public_acls = true", [rc.address])
}

warn contains msg if {
  some rc in input.resource_changes
  "delete" in rc.change.actions
  startswith(rc.type, "aws_db_")
  msg := sprintf("%s will be deleted", [rc.address])
}
```
conftest evaluates `deny`, `violation`, `warn` rules in package `main` by default
(`--namespace` / `--all-namespaces` for others).

## Run in CI
```bash
conftest test plan.json --policy policy/ --output github     # annotations in PRs
```
Run `conftest test` before apply and fail the job on its result; check the conftest docs for exit-code and warning behaviour (`--fail-on-warn` is not on the fetched pages).

## Unit tests for policies
```rego
# policy/s3_test.rego
package main
import rego.v1

test_denies_public_bucket if {
  count(deny) == 1 with input as {"resource_changes": [{
    "address": "aws_s3_bucket_public_access_block.x",
    "type": "aws_s3_bucket_public_access_block",
    "change": {"actions": ["create"], "after": {"block_public_acls": false}}
  }]}
}
```
`conftest verify --policy policy/` (or `opa test policy/`).

## Exceptions
Keep explicit allow-lists in data files keyed by address with an owner and expiry, rather than editing rules; see the conftest docs for loading data.

## HCP Terraform
Native OPA policy sets use package/rule conventions per HCP docs (query like
`data.terraform.policies.<name>.deny`) and input `input.plan`; adapt paths if reusing conftest policies.

## Gotchas
- `after_unknown` mirrors `after` with unknown leaf values set to `true` and known values omitted, so combine the two; don't treat a missing `after` field as false.
- `resource_changes` entries carry the full absolute address (for example `module.child.aws_instance.foo[0]`) plus `module_address`.

## Verify
- [ ] `conftest verify` passes; a deliberately bad fixture fails.
- [ ] CI job fails on a plan that violates a deny rule.

## Checked

2026-11-02. Confirmed against conftest.dev, the OPA Terraform tutorial and the Terraform JSON output format and HCP Terraform OPA pages: `terraform show -json <plan file>`; conftest evaluates `deny`, `violation` and `warn` rules in the `main` namespace, with `--namespace`, `--all-namespaces`, `--policy` and `--output github`; `conftest verify --policy`; `resource_changes`, `actions`, `address`, `module_address`, `after_unknown` semantics; HCP Terraform uses `input.plan` and queries like `data.terraform.policies.<name>.deny`. Removed as not on the fetched pages: `--fail-on-warn`, exit-code claim, `--data`, the OPA 1.0 deprecation remark and the nested `configuration` remark. Gated: the Rego v1 syntax (`import rego.v1`, `contains ... if`) and the unit-test form.

Method: documentation only; no commands were run.
