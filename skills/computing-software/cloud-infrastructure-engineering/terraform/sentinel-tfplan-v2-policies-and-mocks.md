---
id: computing-software.cloud-infrastructure-engineering.terraform.sentinel-tfplan-v2-policies-and-mocks
name: sentinel-tfplan-v2-policies-and-mocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, hcp-terraform, sentinel, tfplan-v2, sentinel-imports, sentinel-test, sentinel-mocks, policy-as-code]
level: advanced
status: docs-checked
description: "Write Sentinel policies against tfplan/v2 (resource_changes, actions, after values), download mocks from a real run, and unit-test policies with sentinel test."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/import-reference/tfplan-v2", "https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/test/sentinel", "https://developer.hashicorp.com/sentinel/docs/commands/test", "https://developer.hashicorp.com/sentinel/docs/language/undefined"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel with tfplan/v2, mocks and tests

## Policy
```python
# restrict-instance-types.sentinel
import "tfplan/v2" as tfplan

allowed = ["t3.micro", "t3.small", "m6i.large"]

instances = filter tfplan.resource_changes as _, rc {
  rc.type is "aws_instance" and
  rc.mode is "managed" and
  (rc.change.actions contains "create" or rc.change.actions contains "update")
}

violations = filter instances as addr, rc {
  rc.change.after.instance_type not in allowed
}

print("Disallowed instance types:", keys(violations))

main = rule { length(violations) is 0 }
```
- `resource_changes` is indexed by the complete resource address (with `:deposed` appended when `deposed` is non-empty). It lists all resources in configuration and state, including no-op changes, so filter on the change type. For an exact match use list comparison, such as `rc.change.actions is ["create"]`.
- `rc.change.actions` is a list: a normal replacement is `["delete", "create"]`, a create-before-destroy replacement is `["create", "delete"]`. The action names are create, read, update, delete and no-op.
- `rc.change.after` holds planned values; unknown values are not in `after` and are flagged in `after_unknown`. For create-only changes `before` is unset/null, for delete-only changes `after` is unset/null.
- Under targeted runs `resource_changes` only contains the targets; the page suggests checking `tfrun.target_addrs` to prohibit targeted runs.
- Sibling imports are `tfconfig/v2` (configuration) and `tfstate/v2` (state), and `tfrun` (run data).
- The policy uses built-ins `filter`, `keys`, `length` and `print`, and operators `contains` / `not in`, from the Sentinel language reference; `print` output behaviour in HCP Terraform is not covered here.

## Mocks from a real run
In HCP Terraform, expand the plan status section of the run page and click **Download Sentinel mocks** (the button is hidden if the plan is ineligible or you lack permission to download mocks). The tarball holds `mock-tfconfig-v2.sentinel`, `mock-tfplan-v2.sentinel`, `mock-tfstate-v2.sentinel`, `mock-tfrun.sentinel` (plus the v1 files) and a sample `sentinel.hcl`. Mocks expose configuration, plan and state data; HCP Terraform tries to scrub sensitive data but does not guarantee it, so treat them with care. Via the Plan Export API use export type `sentinel-mock-bundle-v0`; the download is available for up to an hour after the export finishes.

## Test layout
Place test data in a subdirectory so `sentinel test` does not try to evaluate it as a policy.
```
policies/
  restrict-instance-types.sentinel
  test/restrict-instance-types/
    pass.hcl
    fail.hcl
  testdata/
    mock-tfplan-v2.sentinel
```
```hcl
# test/restrict-instance-types/fail.hcl  (paths are relative to this file)
mock "tfplan/v2" {
  module { source = "../../testdata/mock-tfplan-v2.sentinel" }
}
test {
  rules = { main = false }
}
```
```bash
sentinel test                       # runs all tests under test/<policy>/
sentinel test -run=restrict -verbose
```
`sentinel test` expects cases at `test/<policy>/*.hcl|json`, ignores the root `sentinel.hcl`, so each case must declare every mock it needs. `-run=regexp` filters tests and `-verbose` shows traces and logs for passing tests too. `sentinel apply` uses the mock mappings in `sentinel.hcl` (paths relative to the working directory).

## Gotchas
- Filter on `actions`: a plan lists no-op changes, and delete-only changes have no `after`, which makes attribute lookups undefined.
- A missing value is `undefined`, and `main` returning undefined counts as false. Recover with `else`, such as `rc.change.after.x else ""`.

## Checked
Date: 2026-11-07. Read in full: tfplan/v2 import reference (collections, change representation, actions, targeted runs), "Generate mock Sentinel data with Terraform" (now at policy-enforcement/test/sentinel), `sentinel test` command page and the Sentinel "Undefined" page. The Sentinel language spec (about 45 KB) was only searched for `keys`, `length`, `print`, `filter`, `contains`, `in` and `not` set operators, not read in full. Fixes: the old source sentinel/docs/terraform/tfplan-v2 is 404 (replaced by the HCP Terraform import reference); mocks are downloaded from the plan status section, not "Policy check". Removed as unconfirmed: `sentinel apply -trace`, "print output shows in the policy check details", `tfrun` described as "workspace, cost estimate, VCS info", the claim that policy helpers can be imported via modules declared in `sentinel.hcl`, the mock-tfplan-pass/fail file names, and the Verify checklist. The `fail.hcl` expectation `main = false` mirrors the page's `main = true` example. The instance-type policy itself is an illustrative example, not from the docs.
Method: documentation only; no commands were run.
