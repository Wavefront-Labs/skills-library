---
id: computing-software.cloud-infrastructure-engineering.terraform.handling-not-found-data-source-results
name: handling-not-found-data-source-results
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, data-not-found, data-sources, plural-data-sources, preconditions, postconditions]
level: practitioner
status: docs-checked
description: "Handle data sources that find nothing: single-match filters, plural data sources returning ID lists, conditional lookups, and postconditions with clear error messages."
sources: ["https://developer.hashicorp.com/terraform/language/data-sources", "https://developer.hashicorp.com/terraform/language/expressions/custom-conditions", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/vpcs.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/subnets.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/route53_zone.html.markdown"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Data sources that find nothing

## Singular lookups expect one match
Each provider data source defines its own zero- and multi-match behaviour; read its page. For example the AWS
provider's `aws_route53_zone` states that "the given filter must match exactly one Hosted Zone", and that `zone_id`
and `name` are mutually exclusive.

## Use plural data sources for optional lookups
Plural data sources return a list of IDs: `aws_vpcs` exports `ids` ("List of all the VPC IDs found") and filters by
`tags` (each pair must exactly match) or `filter` blocks; `aws_subnets` exports `ids` the same way. The provider docs
size `count` from `length(data.aws_vpcs.foo.ids)`, so an empty result simply yields zero instances.
```hcl
data "aws_vpcs" "tagged" {
  tags = { Name = "shared-${var.env}" }
}
locals {
  vpc_found = length(data.aws_vpcs.tagged.ids) > 0
  vpc_id    = local.vpc_found ? tolist(data.aws_vpcs.tagged.ids)[0] : null
}
resource "aws_vpc" "fallback" {
  count      = local.vpc_found ? 0 : 1
  cidr_block = "10.50.0.0/16"
}
```

## Conditional lookup
`count` and `for_each` are allowed on `data` blocks, and each instance is indexed separately.
```hcl
data "aws_route53_zone" "this" {
  count = var.zone_name == null ? 0 : 1
  name  = var.zone_name
}
locals { zone_id = length(data.aws_route53_zone.this) == 0 ? null : data.aws_route53_zone.this[0].zone_id }
```

## Fail with a useful message
`precondition` and `postcondition` blocks can be added to `data` blocks (Terraform v1.2.0 or later). Terraform
evaluates postconditions after reading from a data source; `self` refers to the data source; a failing condition
raises your `error_message` and stops the operation.
```hcl
data "aws_subnets" "private" {
  filter {
    name   = "tag:Tier"
    values = ["private"]
  }
  lifecycle {
    postcondition {
      condition     = length(self.ids) >= 2
      error_message = "Need at least two private subnets tagged Tier=private in ${var.env}."
    }
  }
}
```

## Gotchas
- Terraform reads data sources during planning, but defers the read to apply when an argument refers to a resource
  attribute or other value it cannot predict at plan time (for example a resource configured to change in the current
  plan); the plan output indicates deferred reads and dependent values show as computed. Absence is therefore not known
  at plan time in that case.
- The docs recommend postconditions for static guardrails and `check` blocks (v1.5.0 or later, warnings only) for
  dynamic validation against changing conditions.

## Verify
- [ ] A plan in an environment without the object takes the fallback path or fails with your message.

## Checked
Confirmed 2026-11-08 against the Terraform data sources and validate (custom conditions) pages and the AWS provider
docs for `aws_vpcs`, `aws_subnets` and `aws_route53_zone`. Removed: `one()` and `try()` examples (not on the cited
pages), the claim that singular lookups always error, and the eventual-consistency note.
Method: docs-only read of cited pages, 2026-11-08
