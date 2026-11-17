---
id: computing-software.cloud-infrastructure-engineering.terraform.choosing-validation-precondition-or-check
name: choosing-validation-precondition-or-check
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, condition-choice, variable-validation, precondition, postcondition, check-block]
level: practitioner
status: verified
description: "Pick the right custom condition: variable validation, resource or output precondition, postcondition, or check block, based on what is checked, when, and whether it should block."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/custom-conditions", "https://developer.hashicorp.com/terraform/language/checks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validation vs precondition vs postcondition vs check

| Mechanism | Checks | Evaluated | On failure | Can reference |
|---|---|---|---|---|
| `variable { validation }` | one input value | as soon as the value is known (plan) | error | the variable; other variables/objects since TF 1.9 |
| `precondition` (resource, data, output) | assumptions before an object is planned/applied | plan (or apply if unknown) | error, object not changed | anything in the module |
| `postcondition` (resource, data) | guarantees about the result | after plan for known values, after apply otherwise | error, downstream blocked | `self` + anything |
| `output { precondition }` | contract of module outputs | plan | error | module internals |
| `check { assert }` | ongoing health of the whole system | end of every plan/apply, and continuous validation | **warning** only | anything; scoped data source |

## Decision rules
1. Is it about **an input's format/range**? -> variable validation.
2. Is it an **assumption about data from elsewhere** (AMI architecture, existing VPC has
   enough subnets)? -> precondition on the consuming resource or postcondition on the
   data source.
3. Is it a **guarantee** your module promises (bucket is encrypted, cert issued)? ->
   postcondition on the resource.
4. Should failing **not block** deployments (health check, expiry warnings)? -> check.

## Example set
```hcl
variable "instance_type" {
  type = string
  validation {
    condition     = can(regex("^(t3|m6i)\\.", var.instance_type))
    error_message = "Only t3 and m6i families are allowed."
  }
}
data "aws_ami" "app" {
  # ...
  lifecycle {
    postcondition {
      condition     = self.architecture == "x86_64"
      error_message = "AMI must be x86_64."
    }
  }
}
resource "aws_instance" "app" {
  lifecycle {
    precondition {
      condition     = data.aws_ami.app.root_device_type == "ebs"
      error_message = "AMI must be EBS-backed."
    }
  }
}
check "cert_expiry" {
  assert {
    condition     = timecmp(aws_acm_certificate.c.not_after, timeadd(plantimestamp(), "720h")) > 0
    error_message = "Certificate expires within 30 days."
  }
}
```

## Verify
- [ ] Each condition sits at the earliest point that has the needed information.
- [ ] Non-blocking concerns use check blocks, blocking ones do not.

## Checked
- Terraform 1.9.8 with `terraform_data` and the local provider: variable validation fails at plan (`Invalid value for variable` with the message) and can reference another variable (`max >= min`); a failing `output` precondition aborts the plan (`Module output value precondition failed`); a condition that references nothing from the configuration is rejected (`The condition expression must refer to at least one object`); a `postcondition` on an attribute unknown at plan passes the plan and the plan JSON shows its check as `unknown`; `check` blocks fail as warnings (`Check block assertion failed`) with apply exit code 0 and plan `-detailed-exitcode` 2 for changes, and the `check` also failed in the plan JSON; `plantimestamp()` and `timecmp` work inside a check. The `aws_ami`/`aws_instance`/`aws_acm_certificate` blocks were not run (no AWS here); in HCL the regex needs a doubled backslash (`\.`) or `[.]`.
