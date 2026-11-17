---
id: computing-software.cloud-infrastructure-engineering.terraform.numeric-functions-min-max-ceil-parseint
name: numeric-functions-min-max-ceil-parseint
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, numeric-functions, parseint, functions, expressions]
level: practitioner
status: verified
description: "Use Terraform numeric functions correctly: min/max with lists via expansion, ceil/floor/abs/log/pow/signum, parseint for hex and binary, and number precision gotchas."
sources: ["https://developer.hashicorp.com/terraform/language/functions/min", "https://developer.hashicorp.com/terraform/language/functions/parseint", "https://developer.hashicorp.com/terraform/language/functions/ceil"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric functions

| Function | Example | Result |
|---|---|---|
| `abs` | `abs(-3)` | 3 |
| `ceil` / `floor` | `ceil(5.1)` / `floor(5.9)` | 6 / 5 |
| `max` / `min` | `max(2, 7, 4)` | 7 |
| `log` | `log(16, 2)` | 4 |
| `pow` | `pow(2, 10)` | 1024 |
| `signum` | `signum(-4)` | -1 |
| `parseint` | `parseint("ff", 16)` | 255 |
| `sum` (collection fn) | `sum([1, 2, 3])` | 6 |

## Lists need expansion
`max` and `min` take variadic arguments, not a list:
```hcl
max(var.sizes...)          # correct: expand the list
max(var.sizes)             # Error: Invalid function argument ("number required")
```
Empty list -> error (`max()` fails with "must pass at least one number"); guard with `length(var.sizes) > 0 ? max(var.sizes...) : 0`.

## Practical uses
```hcl
# nodes per AZ, rounding up
per_az = ceil(var.total_nodes / length(var.azs))
# subnet newbits for N subnets
newbits = ceil(log(var.subnet_count, 2))
# clamp a value
replicas = min(max(var.replicas, 1), 10)
# hex IDs / permissions
mode = parseint("0755", 8)              # 493
```

## parseint details
- Base 2 to 62 inclusive (`parseint("zz", 62)` is 2205); input must be a string (`parseint(12, 10)` errors); prefixes like `0x` are **not** accepted:
  `parseint(trimprefix(var.hex, "0x"), 16)`.
- Invalid digits error, so wrap in `try()` when parsing user input.

## Precision
Terraform numbers are arbitrary-precision internally (`9007199254740993 + 1` gives `9007199254740994` in the console; `1/3` prints 100+ digits), but a provider attribute typed as a float or 64-bit integer may round very large values; check the attribute type and keep large IDs as strings. Division yields fractions (`5 / 2` = 2.5); use `floor()`
for integer division.

## Verify
- [ ] `terraform console` evaluates each expression to the expected number for edge inputs (0, 1, empty).
