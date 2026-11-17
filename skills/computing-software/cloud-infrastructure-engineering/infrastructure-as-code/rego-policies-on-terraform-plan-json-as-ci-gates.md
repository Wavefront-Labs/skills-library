---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.rego-policies-on-terraform-plan-json-as-ci-gates
name: rego-policies-on-terraform-plan-json-as-ci-gates
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, policy-as-code, plan-json, rego-terraform, policy-gate, conftest, opa]
level: advanced
status: verified
description: "Write OPA Rego policies against terraform show -json output, test them with opa test, and enforce them as a CI gate with conftest before apply."
sources: ["Open Policy Agent - Terraform tutorial (https://www.openpolicyagent.org/docs/latest/terraform/)", "Conftest documentation (https://www.conftest.dev/)", "Terraform - JSON output format (https://developer.hashicorp.com/terraform/internals/json-format)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rego policies on Terraform plan JSON as CI gates

Static HCL scanning misses computed values and module internals; the **plan JSON** has the final
resource attributes.

```bash
terraform plan -out=tfplan && terraform show -json tfplan > plan.json
conftest test plan.json --policy policy/ --namespace terraform
```

## Policy
```rego
# policy/terraform/s3.rego
package terraform

import rego.v1

changes contains rc if {
  some rc in input.resource_changes
  rc.change.actions[_] in {"create", "update"}
}

deny contains msg if {
  some rc in changes
  rc.type == "aws_s3_bucket_public_access_block"
  not rc.change.after.block_public_acls
  msg := sprintf("%s must block public ACLs", [rc.address])
}

deny contains msg if {
  some rc in changes
  rc.type == "aws_instance"
  not rc.change.after.tags.owner
  msg := sprintf("%s is missing the owner tag", [rc.address])
}

warn contains msg if {
  some rc in input.resource_changes
  "delete" in rc.change.actions
  msg := sprintf("%s will be deleted", [rc.address])
}
```
Conftest: `deny`/`violation` fail, `warn` prints (checked on Conftest 0.71.1 / OPA 1.21.1 with a hand-written plan JSON: 2 FAIL lines, 1 WARN line, exit code 1; a warn-only plan exits 0, and `--fail-on-warn` exits 2). `--output junit` reports warnings as failures too, so do not count junit failures as hard denies. The `terraform plan -out` / `show -json` pipeline emitted `format_version 1.2` with `resource_changes[].change.{actions,before,after,after_unknown,after_sensitive}` (Terraform 1.9.8, checked with a `terraform_data` resource). Values known only after apply appear in
`change.after_unknown` — treat unknown as "cannot verify" explicitly rather than passing.

## Tests for policies
```rego
# policy/terraform/s3_test.rego
package terraform
import rego.v1
test_untagged_instance_denied if {
  count(deny) > 0 with input as {"resource_changes": [{"address": "aws_instance.x", "type": "aws_instance",
    "change": {"actions": ["create"], "after": {"tags": {}}}}]}
}
```
`opa test policy/ -v` in CI on policy changes (the test above passes: `PASS: 1/1`). Keep fixtures from real (sanitised) plans.

## The gate
```yaml
policy:
  stage: validate
  script:
    - terraform plan -out=tfplan
    - terraform show -json tfplan > plan.json
    - conftest test plan.json -p policy/ --output junit > policy.xml
  artifacts: {reports: {junit: policy.xml}}
```
Make the job a required check; apply jobs depend on it. Exceptions: a reviewed `exceptions.rego`
data file listing addresses + ticket + expiry date, checked by the policy, not ad hoc skips.

Alternatives: HCP Terraform policy sets enforce at run time server-side. Per HashiCorp's policy-set docs, Sentinel has advisory, soft mandatory and hard mandatory levels, while OPA policies have only advisory and mandatory (overridable by users with the Manage Policy Overrides permission).

## Gotchas
- Modules nest addresses (`module.vpc.aws_subnet.a[0]`); match on `type`, not address prefixes.
- `rego.v1` syntax (`if`, `contains`) needs OPA 0.59 or later (the `rego.v1` import arrived with 0.59.0 per the OPA release notes) and a conftest built with it; pin versions.
- Plan JSON contains sensitive values in `after` unless marked sensitive — protect artifacts.

## Verify
- [ ] `opa test` passes; a PR adding a public bucket fails the gate with a readable message.
