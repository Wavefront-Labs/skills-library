---
id: computing-software.cloud-infrastructure-engineering.terraform.postconditions-with-self-and-check-blocks
name: postconditions-with-self-and-check-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, postcondition, postcondition-self, check-block, scoped-data-source, check-assertion, custom-conditions]
level: practitioner
status: verified
description: "Assert results with postconditions using self, and use check blocks with scoped data sources for non-blocking health checks; pick the right one for each guarantee."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/custom-conditions#postconditions", "https://developer.hashicorp.com/terraform/language/checks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Postconditions with `self` and `check` blocks

## Postcondition with self
Ran under Terraform 1.17.0 with `hashicorp/local` and `terraform_data`:
```hcl
data "local_file" "cfg" {
  filename = "${path.module}/cfg.txt"
  lifecycle {
    postcondition {
      condition     = self.content == "cfgv"
      error_message = "cfg content ${self.content} is unexpected."
    }
  }
}
resource "terraform_data" "pp" {
  input = "z"
  lifecycle {
    postcondition {
      condition     = self.output == "bad"
      error_message = "post failed."
    }
  }
}
```
- `self` = the object after read/apply; only valid inside postconditions.
- Failure **blocks** downstream objects that depend on this one (run: `pp` was created
  and saved, the resource referencing `pp.id` was not created, an unrelated sibling was).
- For data sources the failure came at plan after the read (`Planning failed`,
  `Resource postcondition failed`); for resources it comes after apply, or at plan if
  the values are already known (a count-instance `self.input` that was known at plan
  failed the plan).
## check blocks
```hcl
check "file_ok" {
  data "local_file" "scoped" {         # scoped data source: only visible inside the check
    filename = "${path.module}/missing.txt"
  }
  assert {
    condition     = data.local_file.scoped.content == "x"
    error_message = "Scoped content is ${data.local_file.scoped.content}."
  }
}
```
- Failing assertions are **warnings**: apply continued and exited 0 with
  `Warning: Check block assertion failed`.
- A scoped data source that errors (here a missing file) is also downgraded to a warning
  (`Read local file data source error`).
- Evaluated on every plan and apply (the warning appeared on both).
## Which one?
| Guarantee | Use |
|---|---|
| Must hold or nothing downstream should proceed | postcondition |
| Input sanity before acting | precondition / variable validation |
| Ongoing health signal, never block deploys | check block |

## Gotchas
- A check's scoped data source cannot be referenced outside the check (error `Reference to scoped resource`).
- Keep postconditions on `self`; references to other objects belong in preconditions or checks.
- `self` in a `count` resource is the current instance (the failing message named instance `i1`).

## Verify
- [ ] A forced bad value (change `cfg.txt`) fails the next plan with the postcondition message.
- [ ] A failing check shows as `Warning: Check block assertion failed` without failing the run.

## Checked
- Terraform 1.17.0 with `hashicorp/local` and `terraform_data`: data and resource postconditions with `self`, apply-time postcondition (resource saved, dependent blocked, sibling applied), a count resource with a known failing `self.input`, `check` blocks (assert failure and a scoped data source error both gave warnings and exit 0), and referencing a scoped data source outside its check (`Reference to scoped resource`).
- Replaced AWS AMI/S3/CloudFront examples with local equivalents; the claim about the graph edges of cross-object postconditions was removed as unchecked; continuous validation is attributed to the docs and not run.
