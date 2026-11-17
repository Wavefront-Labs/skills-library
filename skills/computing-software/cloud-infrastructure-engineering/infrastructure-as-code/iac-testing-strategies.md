---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-testing-strategies
name: iac-testing-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, testing, iac-testing, test-pyramid, terraform-test, tftest, opentofu, terratest, kitchen-terraform, pulumi-testing, pulumi-mocks, cdk-assertions, aws-cdk, bicep, arm-ttk, terraform-validate, tflint, unit-tests, integration-tests, contract-tests, mock-providers, ephemeral-environments, test-isolation, cleanup, cloud-nuke, localstack]
level: advanced
status: gated
description: "Test infrastructure code in layers: static validate/lint, plan-level unit tests with terraform test or mocks, real-cloud integration tests in throwaway accounts, and reliable cleanup."
sources: ["Terraform documentation - Tests (terraform test)", "Terratest documentation (Gruntwork)", "Pulumi documentation - Testing", "AWS CDK documentation - Testing constructs"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IaC testing strategies — prove modules work before anyone plans them

**Goal:** reusable infrastructure modules that are tested at the right level — cheap checks
on every commit, real-cloud tests where only real cloud can answer — without leaking
resources or bills.

Plan review and policy gates on *environment* changes are a separate concern
(`computing-software.cloud-infrastructure-engineering.infrastructure-as-code.plan-review-and-environment-promotion`);
this skill is about testing the *code*, mainly modules and constructs.

## 1. The IaC test pyramid
| Layer | Tooling | Runtime | Catches |
|---|---|---|---|
| Static | `terraform fmt -check`, `terraform validate`, TFLint (with provider rulesets), `bicep build`, `cdk synth` | seconds | syntax, typos, invalid instance types, deprecated args |
| Unit (plan-level, no cloud) | `terraform test` with `command = plan` and `mock_provider` (Terraform ≥ 1.7 / OpenTofu), Pulumi mocks, CDK `Template.fromStack` assertions | seconds | variable logic, conditionals, `count`/`for_each` maths, naming, tags |
| Integration (real apply) | `terraform test` with `command = apply`, Terratest (Go), pytest + boto3 | minutes | IAM actually works, resources reachable, provider quirks |
| End-to-end | deploy a full stack + smoke tests | 10s of min | composition of modules, networking paths |

Checked here (Terraform 1.9.8, aws provider ~> 5.0 via `terraform init`): `terraform fmt -check`, `terraform validate` and `terraform test` ran. TFLint, `bicep build`, `cdk synth`, Pulumi mocks, Terratest, pytest+boto3, aws-nuke/cloud-nuke and LocalStack were not run (gated: unconfirmed, tools not installed here), so treat their rows as unconfirmed descriptions. Most value per minute is in static + unit. Integration tests are for modules many teams consume.

## 2. Plan-level unit tests (Terraform native)
```hcl
# tests/naming.tftest.hcl
mock_provider "aws" {}
variables {
  name = "orders"
  environment = "prod"
}
run "bucket_name_and_tags" {
  command = plan
  assert {
    condition     = aws_s3_bucket.this.bucket == "orders-prod"
    error_message = "unexpected bucket name"
  }
  assert {
    condition     = aws_s3_bucket.this.tags["environment"] == "prod"
    error_message = "environment tag missing"
  }
}
run "rejects_bad_env" {
  command = plan
  variables { environment = "qa1" }
  expect_failures = [var.environment]   # tests the validation block
}
```
Run with `terraform test`. Both runs above passed against a small module (an `aws_s3_bucket` named `${var.name}-${var.environment}` with an `environment` tag and a `contains(["dev","prod"], ...)` validation). Values only known after apply (ARNs, IDs) can't be asserted at plan time: `assert { condition = aws_s3_bucket.this.arn != "" }` in a `command = plan` run failed with "Unknown condition value" and the next run was skipped. Under `command = apply` with `mock_provider "aws" {}` the same attributes get random placeholder strings (here `arn = "o4kcdm4e"`, not ARN-shaped), so do not assert ARN formats against a mock. The Terraform 1.7.0 changelog introduces `mock_provider` (and mock resources/data sources) for `terraform test`.

CDK: `Template.fromStack(stack).hasResourceProperties('AWS::S3::Bucket', {...})`; Pulumi: `pulumi.runtime.setMocks` then assert on outputs.

## 3. Integration tests that don't leak
- Run in a **dedicated sandbox account/subscription/project**, never shared dev.
- Unique name suffix per run (`random_id`, Terratest `random.UniqueId()`), so parallel CI runs don't collide.
- Always destroy: `defer terraform.Destroy(t, opts)` in Terratest; `terraform test` destroys apply-run resources automatically at the end of the file (in reverse order).
- Backstop with a scheduled sweeper (aws-nuke / cloud-nuke style, tag-filtered) because failed destroys *will* happen.
- Assert behaviour, not attributes: hit the endpoint, assume the role, write to the bucket.
- Add retries: eventual consistency (IAM propagation can take seconds) causes flaky first calls.

## 4. What to test where
- Module repos: static + unit on every PR; integration on PR for changed modules (or nightly if slow/expensive).
- Root/live configs: static + plan + policy; skip integration (the environments are the test).
- Emulators (LocalStack, Azurite) are useful for fast feedback on app-level SDK calls but diverge from real IAM and edge behaviour — don't treat them as proof.

## Gotchas
- `terraform validate` passes code that the provider rejects at apply (e.g. invalid CIDR overlaps, quota) — only apply finds those.
- Tests that pin provider versions differently from consumers test the wrong thing; test with the min and max supported versions.
- Integration tests cost real money; long-lived resources (NAT gateways, clusters) dominate. Tag with run ID and TTL.
- Snapshot tests of synthesized templates break on every harmless upgrade — prefer targeted assertions.

## Verify
- [ ] fmt/validate/lint run on every commit and block merge.
- [ ] Each module has plan-level tests covering its conditionals and validations.
- [ ] Integration tests run in an isolated account with unique names and guaranteed destroy.
- [ ] A sweeper removes orphaned test resources older than their TTL.
- [ ] Test matrix includes the minimum and latest supported provider versions.

Uncertain: `mock_provider` and `expect_failures` syntax is from Terraform 1.7+ docs; confirm against the version you run, and OpenTofu parity.
