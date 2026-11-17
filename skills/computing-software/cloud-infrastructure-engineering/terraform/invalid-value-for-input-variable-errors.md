---
id: computing-software.cloud-infrastructure-engineering.terraform.invalid-value-for-input-variable-errors
name: invalid-value-for-input-variable-errors
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, invalid-variable-value, variables, type-constraints, tfvars, troubleshooting]
level: practitioner
status: verified
description: "Fix Invalid value for input variable errors: reading the type path in the message, object attribute mismatches, string-to-number conversion and tfvars versus CLI quoting."
sources: ["https://developer.hashicorp.com/terraform/language/values/variables#type-constraints", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints#conversion-of-primitive-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Invalid value for input variable"

```
Error: Invalid value for input variable
  on bad.tfvars line 1:
   1: nodes = { general = { size = "m5.large", count = "three" } }
The given value is not suitable for var.nodes declared at main.tf:1,1-17: a
number is required.
```
(Terraform 1.17.0 does not name the failing attribute for a wrong *type*; search the value for
a string where a number is expected.) A *missing* attribute does name its path:
`element "general": attribute "count" is required.` and `element 1: attribute "id" is required.`
for a list of objects. Fix exactly that spot.

## Common causes
| Message fragment | Cause | Fix |
|---|---|---|
| `a number is required` | `"three"`, or `"3 "` with a space | numeric literal; strings like `"3"` convert automatically |
| `attribute "x" is required` | object type without `optional()` and caller omitted it | add the attribute or make it `optional(type, default)` |
| (no message) | extra attribute in an object value (`extra = 1`) | silently dropped, no warning; add it to the type if you need it |
| `list of string required, but have string.` | passed a single string in tfvars | wrap in `[ ]` |
| `Variables not allowed` for `-var 'names=foo'` | unquoted `foo` is parsed as a reference | `-var 'names=["foo"]'` |
| `a bool is required` | `"yes"` | `true`/`false` (strings `"true"`/`"false"` convert) |
| `element "a": string required, but have object.` | nested map value in a `map(string)` | widen to `map(any)` or a proper object type |
| `Variables not allowed` (in tfvars) | references like `var.x` or `local.y` in tfvars | tfvars accept literals only |

## CLI and environment quoting
```bash
terraform plan -var='nodes={general={size="m5.large",count=3}}'
export TF_VAR_m='{"Team":"payments"}'         # complex values parsed as HCL
export TF_VAR_flag=false                      # primitives as plain strings
```
(the `-var` form, `TF_VAR_nodes='{general={size="m5.large",count=3}}'` and the two `TF_VAR_`
lines above all planned without error against the matching declarations)
Shell quoting mistakes produce parse errors before type errors; use a `.tfvars` file
for anything nested.

## Test types fast
```bash
echo 'tolist(["a"])' | terraform console
echo 'var.nodes' | terraform console -var-file=prod.tfvars
```

## Verify
- [ ] `terraform plan -var-file=<env>.tfvars` passes for every environment file (CI matrix).

## Checked
- Terraform 1.17.0 with `map(object)`, `list(string)`, `bool`, `map(string)` and an `optional()` object variable: each table row was produced by a real `.tfvars` file or `-var`; `"three"` and `"3 "` both gave `a number is required`; a missing `count` gave `element "general": attribute "count" is required.`; `flag = "true"` converted without error and `flag=yes` failed with `a bool is required`; an extra object attribute was dropped silently (output showed only `count` and `size`); `names = [var.x]` in a tfvars file gave `Variables not allowed`; `echo 'tolist(["a"])' | terraform console` and `echo 'var.nodes' | terraform console -var-file=ok.tfvars` ran (the second prints `tomap({...})`).
