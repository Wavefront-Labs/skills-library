---
id: computing-software.cloud-infrastructure-engineering.terraform.conditions-on-unknown-values
name: conditions-on-unknown-values
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, condition-unknown, known-after-apply, preconditions, postconditions, unknown-values]
level: practitioner
status: verified
description: "Understand when custom conditions are deferred because values are unknown at plan time, what fails mid-apply as a result, and how to move checks to known inputs."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/custom-conditions#conditions-checked-only-during-apply", "https://developer.hashicorp.com/terraform/language/expressions/references#values-not-yet-known"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditions on unknown values

## Rule
Terraform evaluates a condition as early as possible. If the condition references
values that are **unknown during plan** (attributes of resources not yet created, or
being replaced), evaluation is deferred to **apply**.

Consequence: the plan looks fine, apply starts, some resources are created, then a
postcondition fails mid-apply. You are left with a partial apply.

```hcl
resource "aws_instance" "web" {
  # ...
  lifecycle {
    postcondition {
      condition     = self.public_ip == ""        # public_ip unknown until created
      error_message = "Instance must not have a public IP."
    }
  }
}
```
On first create: checked after the instance exists; failure means the instance is
already created (and stays, marked as created; downstream resources are not created).

## Make checks plan-time where possible
- Check the **input** that determines the outcome instead of the result:
  `condition = var.associate_public_ip == false` (validation or precondition), or
  `!self.associate_public_ip_address` if that argument is set from config (known).
- Validate data sources (known at plan unless deferred) instead of created resources.
- Keep postconditions for things only knowable after creation, and accept they run at apply.

## Seeing deferral
- Plan JSON: `.checks[]` with `status = "unknown"`.
- First plans for new environments show many unknown conditions; second plan
  (after apply) evaluates them.

## Gotchas
- Preconditions referencing `data` sources with `depends_on` are deferred too
  (data read during apply).

## Verify
- [ ] Security/compliance conditions reference known inputs and fail at plan, not apply.

## Checked
- Terraform 1.9.8 with `terraform_data`: a postcondition on an attribute unknown during plan (`self.output`) lets the plan succeed (`Plan: 3 to add`) and the plan JSON `.checks[]` lists it with status `unknown`; on apply the first two resources were created, the postcondition then failed (`Resource postcondition failed`), the downstream resource was not created and the failed resource stayed in state; the next plan evaluated the condition against the known value and failed immediately; a data source with `depends_on` a not-yet-created resource shows `will be read during apply`. The `-refresh=false` staleness note and the AWS `public_ip` example were not run.
