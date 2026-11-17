---
id: computing-software.cloud-infrastructure-engineering.terraform.locals-for-derived-values
name: locals-for-derived-values
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, locals, local-values, derived-values, naming, tags, merge, for-expressions, dry, configuration, variables-vs-locals]
level: intro
status: docs-checked
description: "Use locals to name reused expressions such as name prefixes, tag maps and for-expression results: local.<name> references, module scope, merge precedence, filtering."
sources: ["https://developer.hashicorp.com/terraform/language/values/locals", "https://developer.hashicorp.com/terraform/language/expressions/for", "https://developer.hashicorp.com/terraform/language/functions/merge"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locals for derived values

Local values name an expression so you can use the name many times in a module instead of
repeating the expression, like function-scoped variables in other languages.

## Define and reference
```hcl
locals {
  # Naming convention
  resource_name = "${var.project_name}-${var.environment}"

  # Process the subnet list
  primary_public_subnet = var.subnet_ids[0]
  subnet_count          = length(var.subnet_ids)

  # Environmental deployment settings
  is_production      = var.environment == "prod"
  monitoring_enabled = var.monitoring || local.is_production
}

resource "aws_security_group" "web" {
  name = "${local.resource_name}-sg"
}
```
- Define in a `locals` block (plural), reference with `local.<NAME>` (singular).
- A local can hold any valid expression using variables, resource attributes, function
  outputs and other locals.
- Scope is the module that defines it: not visible in other modules, but you can pass a
  local to a child module as an argument.
- Use locals for a value reused in many places (change it in one spot) or for the result
  of a complex expression. They can also make a configuration harder to read because
  they hide where values come from, so do not overuse them.

## Building maps with `merge`
`merge` takes any number of maps or objects; when keys repeat, the later argument wins.
If argument types differ, the result is an object. Use the expansion symbol to merge a
list of maps:
```hcl
merge([{a="b", c="d"}, {}, {e="f", c="z"}]...)   # { a = "b", c = "z", e = "f" }
```
So in `merge(var.tags, { Project = var.project })` the explicit tags win over `var.tags`
for any shared key; reverse the order if the caller should win.

## `for` expressions in locals
- `[for s in var.list : upper(s)]` yields a tuple; `{for s in var.list : s => upper(s)}`
  yields an object (two result expressions joined by `=>`).
- Input can be a list, set, tuple, map or object; two symbols give key/index and value
  (`for k, v in var.map`).
- Filter with `if`: split a map into groups with one local each:
```hcl
locals {
  admin_users   = { for name, user in var.users : name => user if user.is_admin }
  regular_users = { for name, user in var.users : name => user if !user.is_admin }
}
```
- Object result keys must be unique or Terraform errors; add `...` after the value
  expression for grouping mode, which gives a map of lists
  (`{ for name, user in var.users : user.role => name... }`).
- Maps and objects iterate in lexical key order and sets of strings in lexical value
  order; sets of other types have arbitrary order. Wrap a result in `toset(...)` to show
  it is unordered.
- `for` cannot generate nested blocks; use `dynamic` blocks for those.

## Checked
Date: 2026-11-07
Read in full: Use locals to reuse expressions (language/values/locals), for Expressions (language/expressions/for) and merge Function (language/functions/merge).
Confirmed: every statement above, including the locals example, scope rule, readability caveat, merge precedence and expansion example, for result types, filtering, grouping, ordering and the dynamic blocks note.
Removed: the variable-versus-local comparison table, duplicate-name and self-reference errors, declaration-order claim, lookup-table, count and coalesce examples, the nested-subnet flatten example (composed, not shown on the pages), naming conventions and file layout advice, the unknown-at-plan and `-target` gotcha, "locals are evaluated even if unused", sensitivity claims, the `terraform console` tip and the Verify checklist.
Not opened: the locals block reference and the dynamic blocks page.
Method: documentation only; no commands were run.
