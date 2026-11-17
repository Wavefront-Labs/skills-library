---
id: computing-software.cloud-infrastructure-engineering.terraform.nested-dynamic-blocks-iterator-and-labels
name: nested-dynamic-blocks-iterator-and-labels
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, nested-dynamic, iterator, dynamic-iterator, dynamic-labels, content-block, dynamic-blocks]
level: advanced
status: gated
description: "Write nested dynamic blocks with the iterator argument to avoid name clashes, generate labelled blocks via labels, and know when dynamic blocks hurt readability."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks", "https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks#multi-level-nested-block-structures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested dynamic blocks, `iterator`, `labels`

## Anatomy
```hcl
dynamic "<block type>" {
  for_each = <collection>
  iterator = <name>          # optional; default = block type name
  labels   = [<expr>, ...]   # only for block types that take labels
  content { ... }            # the block body; use <iterator>.key / .value
}
```

## Nested
```hcl
# (gated: unconfirmed, source is paywalled or blocked) (the aws_wafv2_web_acl schema was not run; the iterator and nesting rules are from the Terraform docs and ran on one level with archive_file)
variable "rules" {
  type = list(object({
    name     = string
    priority = number
    ip_sets  = list(string)
  }))
}

resource "aws_wafv2_web_acl" "this" {
  # ...
  dynamic "rule" {
    for_each = var.rules
    iterator = r
    content {
      name     = r.value.name
      priority = r.value.priority
      statement {
        or_statement {
          dynamic "statement" {
            for_each = r.value.ip_sets
            iterator = ip
            content {
              ip_set_reference_statement {
                arn = ip.value
              }
            }
          }
        }
      }
      visibility_config { ... }
    }
  }
}
```
Without `iterator`, inner `statement.value` shadows nothing here, but in nested
blocks of the **same type** (e.g. `statement` inside `statement`) the inner default
name hides the outer one — always set distinct iterators at each level.

## Labels
Only for nested block types whose schema declares labels (rare in provider schemas;
most nested blocks are unlabelled, so `labels` usually errors: ran on `archive_file` `source`, `Unsupported argument ... labels`). Shape:
```hcl
dynamic "task" {
  for_each = var.tasks
  labels   = [task.key]
  content {
    driver = task.value.driver
  }
}
```

## Readability rules
- One level of dynamic is fine; two needs comments; three — restructure the input
  or split into separate resources (e.g. standalone rule resources).
- Do not wrap a fixed, always-present block in `dynamic` just to look generic.
- Prefer separate resources where the provider offers them
  (`aws_vpc_security_group_ingress_rule` over dynamic `ingress`).

## Gotchas
- `dynamic` cannot generate meta-argument blocks (`lifecycle`, `provisioner`); ran: `Unsupported block type` for both, and the dynamic-blocks doc says the same.
- `iterator.key` is the map key or list index; `.value` is the element.
- Unknown `for_each` collections do not error in a `dynamic` block (ran with `archive_file`: the data source was deferred to apply); only resource and module `for_each` raise `Invalid for_each argument`.

## Verify
- [ ] `terraform plan` shows the expected number of nested blocks for a sample input.
- [ ] `terraform validate` passes with an empty list for each level.

## Checked
- Terraform 1.17.0 with `archive_file` `source` blocks: one-level `dynamic` with `iterator`, `.key`/`.value`, an empty collection, `labels` on an unlabeled block, dynamic `lifecycle`/`provisioner`, unknown `for_each`. The nested-iterator shadowing rule and the meta-argument limit were read in the Terraform dynamic-blocks page (hashicorp/web-unified-docs v1.17.x language/expressions/dynamic-blocks.mdx).
- Gated: the AWS WAF example and any two-level nesting (no local provider with a nested block of a nested block).
