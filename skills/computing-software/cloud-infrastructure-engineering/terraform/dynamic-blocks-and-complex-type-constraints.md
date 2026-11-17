---
id: computing-software.cloud-infrastructure-engineering.terraform.dynamic-blocks-and-complex-type-constraints
name: dynamic-blocks-and-complex-type-constraints
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, hcl, dynamic-blocks, type-constraints, object-type, optional-attributes, for-expressions, for-each, complex-variables, nested-objects, type-coercion, null-handling, try, coalesce, lookup, defaults-function, variable-validation]
level: advanced
status: gated
description: "Generate repeated nested blocks with dynamic{} and model nested object/map variables with precise optional() type constraints, defaults, and null-safe expressions."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform dynamic blocks and complex type constraints

**Goal:** a module's interface accepts a realistic shape of input (a list of rules, a
map of environments, a tree of tags) without copy-pasted repeated blocks, and fails at
`plan` with a readable message when the caller passes the wrong shape — not a cryptic
"inconsistent conditional result types" three layers deep.

## 1. `dynamic` blocks — when and when not
`dynamic` generates **nested blocks** (not top-level resources — use `for_each` on the
resource for that). Classic case: variable number of `ingress` rules on a security
group.
```hcl
# (gated: unconfirmed, source is paywalled or blocked) (the aws_security_group resource was not run; the same dynamic shape ran with archive_file `source` blocks)
variable "ingress_rules" {
  type = list(object({
    port        = number
    protocol    = optional(string, "tcp")
    cidr_blocks = list(string)
  }))
  default = []
}

resource "aws_security_group" "this" {
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```
Rule of thumb: if the block only ever appears 0 or 1 times, use a normal
`optional`-conditioned argument, not `dynamic` — a `dynamic` block that only ever
iterates zero or one time is a tell that the schema should be a plain nested object
instead. Nesting `dynamic` inside `dynamic` is legal but unreadable past two levels;
flatten the input shape instead.

## 2. Precise object types with `optional()`
`optional(type)` makes an object attribute absent-able; `optional(type, default)` gives
it a default when the caller omits it **or passes `null`** (ran: `engine = null` came out as `"postgres"`). Without a default an omitted or null optional attribute is `null` (ran: `lifecycle_days = null`).
```hcl
variable "buckets" {
  type = map(object({
    versioning = optional(bool, false)
    lifecycle_days = optional(number)
    tags = optional(map(string), {})
  }))
}
```
Terraform **type-converts** the caller's value to match this constraint structurally —
missing optional keys get their default, a missing required key is an error, and **extra keys are silently dropped** (ran on Terraform 1.17.0 for a `-var` value, a variable default and a module call: `{ engine = "mysql", bogus = 1 }` and `{ engine = "x", dayz = 3 }` were accepted and the extra key vanished, so a misspelled optional key silently falls back to its default). All of this happens
before your module body ever runs. This is why validation errors on complex objects
point at the variable declaration, not a resource three files deep: fix the shape there.

## 3. `defaults()` for uniform fill-in
`defaults()` is gone: it was an experiment that ended when `optional(type, default)` became stable in Terraform 1.3 (ran on 1.17.0: `Call to unknown function`). Put the defaults in the type constraint, or use `merge()` over a locals object.

## 4. Null-safety in expressions
- `try(a.b.c, null)` short-circuits a chain where an intermediate key may not exist —
  use sparingly; it also swallows real type errors, so prefer `optional()` typing first
  and reach for `try()` only at the edges (e.g. reading an unpredictable API response
  via a data source).
- `coalesce(a, b, "default")` errors if **all** arguments are null or empty (ran: `Error in function call`); `coalescelist` is
  the list equivalent. `coalesce` skips empty strings as well as nulls — ran: `coalesce("", "x")` returned `"x"` and `coalesce(null, "", "d")` returned `"d"`.
- `lookup(map, key, default)` is the null-safe map read; indexing (`map[key]`) errors
  on a missing key.

## 5. Validation that catches shape errors early
```hcl
variable "ingress_rules" {
  type = list(object({ port = number, cidr_blocks = list(string) }))
  validation {
    condition     = alltrue([for r in var.ingress_rules : r.port > 0 && r.port < 65536])
    error_message = "Each rule's port must be between 1 and 65535."
  }
}
```
`alltrue`/`anytrue` over a `for` expression is the standard pattern for validating every
element of a complex collection in one `validation` block — cheaper than one block per
field.

## Gotchas
- `for_each` on a **resource or module** needs a set or map with known keys at plan time: `toset([terraform_data.t.id])` produced `Invalid for_each argument ... values derived from resource attributes that cannot be determined until apply`. A `dynamic` block does not error: with the same unknown set (ran with `archive_file` `source`) the plan simply showed the data source as `read during apply`. Key resource `for_each` on stable inputs, not computed attributes.
- Mixing `optional()` objects of different shapes in the same list (via `list(any)`
  escape hatches) defeats type checking entirely — every element silently becomes
  dynamically typed; avoid `any` in a public module interface (gated: unconfirmed, source is paywalled or blocked).
- `dynamic "tags" {}`-style blocks for provider-level `tags` arguments are usually
  unnecessary — most providers accept a plain `map(string)` for tags directly.
- Changing an `optional()` default in a later module version is a silent behavior
  change for every caller that omitted the key — document it as a breaking change in
  the changelog even though `terraform validate` won't flag it.
- Unconfirmed: exact error text for nested-object type mismatches has changed across
  Terraform 1.x minor versions — don't hardcode a parser against it.

## Verify
- [ ] A caller object with a missing required key fails at plan; an extra or misspelled optional key is dropped silently, so add a `validation` that compares `keys(var.x)` against the allowed list if you need to reject it.
- [ ] Omitting every optional key from a caller's object still plans cleanly with the documented defaults applied.
- [ ] A `dynamic` block with an empty `for_each` list renders zero nested blocks (ran with `archive_file`: the only error was the provider's own missing-source check).
- [ ] No `for_each`/`dynamic` input derives from a not-yet-created resource attribute.

## Checked
- Terraform 1.17.0 with local variables/modules and `archive_file`: `optional()` defaults, explicit null, extra keys (dropped, including via a module call), required key missing, `nullable = false` with null, `defaults()` (unknown function), `coalesce`/`coalescelist`/`lookup`, `alltrue` validation (plan rejected port 70000), dynamic `source` blocks with `iterator`, `labels` on an unlabeled block (`Unsupported argument`), `dynamic "lifecycle"` and `dynamic "provisioner"` (both `Unsupported block type`), unknown dynamic and resource `for_each`.
- Gated: the AWS security-group snippet and the `list(any)` claim.
