---
id: computing-software.cloud-infrastructure-engineering.terraform.preconditions-on-resources-data-sources-and-outputs
name: preconditions-on-resources-data-sources-and-outputs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, precondition, resource-precondition, data-precondition, output-precondition, error-message, error-messages, custom-conditions]
level: practitioner
status: verified
description: "Write precondition blocks on resources, data sources and outputs that fail plans early with clear error_message text, and know when each one is evaluated."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/custom-conditions#preconditions-and-postconditions", "https://developer.hashicorp.com/terraform/language/expressions/custom-conditions#error-messages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preconditions (resources, data sources, outputs)

A precondition is an assumption that must hold **before** Terraform acts on the
object. Failure stops the plan/apply with your message.

## Resource precondition
All blocks below ran under Terraform 1.17.0 with `hashicorp/local` and `terraform_data`:
```hcl
data "local_file" "cfg" {
  filename = "${path.module}/cfg.txt"
}
resource "terraform_data" "a" {
  input = var.mode
  lifecycle {
    precondition {
      condition     = data.local_file.cfg.content == "cfgv" && var.mode != "rbad"
      error_message = "Resource precondition failed for mode ${var.mode}."
    }
  }
}
```
Use it for conditions combining several inputs/objects — the things a single
variable validation cannot see.
## Data source precondition
```hcl
data "local_file" "cfg" {
  filename = "${path.module}/cfg.txt"
  lifecycle {
    precondition {
      condition     = var.mode != "dsbad"
      error_message = "Data precondition failed for mode ${var.mode}."
    }
  }
}
```
It failed the plan as `Resource precondition failed` (the same title for data sources)
before the read. Use **postconditions** to check what came back.
## Output precondition
```hcl
output "o" {
  value = terraform_data.a.output
  precondition {
    condition     = var.mode != "obad"
    error_message = "Output precondition failed."
  }
}
```
Failure reported `Module output value precondition failed`. Guards a module's
contract: callers never receive a value that violates it.
## When evaluated
- During plan when all referenced values are known: all three failures above stopped the
  plan before anything was created.
- Otherwise during apply just before the object is changed. Run: a precondition on
  `terraform_data.late` comparing `terraform_data.indep.output` (unknown at plan)
  failed at apply while the independent `indep` and `other` resources were created
  and kept in state (`terraform state list`).
## Writing error_message
- Full sentences, start with a capital, end with `.` or `?` (a style choice: a lowercase message without a period produced no warning from `validate` or `plan`).
- Say what is wrong, show the actual value, and what to do.
- Avoid sensitive values in the message (a sensitive variable in a test `error_message`
  was not printed; see the test-variables skill).

## Gotchas
- Preconditions are not validation of the provider's own rules; don't duplicate
  what the API rejects anyway unless the message adds value.
- `condition` is evaluated at apply when it was unknown at plan, so it may fail late (see above).

## Verify
- [ ] Plan with a violating input fails with your exact message and the block location.
- [ ] `terraform test` run with `expect_failures = [terraform_data.a]` and `command = plan` passes (an `apply` run reports `Expected failure while planning`).

## Checked
- Terraform 1.17.0 with `hashicorp/local` and `terraform_data`: resource, data source and output preconditions (each failed the plan with the titles `Resource precondition failed` / `Module output value precondition failed`), an apply-time precondition on an unknown value (independent resources were created and kept in state), message style (no warning for a lowercase message without a period), and `terraform test` `expect_failures` plan vs apply.
- AWS examples (`aws_instance`, `aws_lb`, `aws_vpc`) were replaced by local equivalents; the claim that preconditions must not be unknown at apply was corrected.
