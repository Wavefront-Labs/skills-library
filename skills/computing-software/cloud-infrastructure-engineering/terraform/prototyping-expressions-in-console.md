---
id: computing-software.cloud-infrastructure-engineering.terraform.prototyping-expressions-in-console
name: prototyping-expressions-in-console
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, console-prototyping, terraform-console, for-expression, functions]
level: practitioner
status: verified
description: "Prototype function calls, for-expressions and type conversions in a scratch terraform console before putting them in config, including multi-line input and fixtures."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/console", "https://developer.hashicorp.com/terraform/language/expressions/for", "https://developer.hashicorp.com/terraform/language/functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prototyping expressions in `terraform console`

## Scratch directory pattern
Do not experiment inside a real root module (console locks its state). Use an empty
directory with fixture locals:
```bash
mkdir /tmp/tfscratch && cd /tmp/tfscratch
cat > main.tf <<'EOF'
locals {
  subnets = [
    { name = "a", cidr = "10.0.0.0/24", az = "eu-west-1a", public = true },
    { name = "b", cidr = "10.0.1.0/24", az = "eu-west-1b", public = false },
  ]
}
EOF
terraform console
```
No `init` is needed when there are no providers or modules (console ran in a directory holding only `main.tf`).

## Things worth prototyping
```hcl
> { for s in local.subnets : s.name => s if s.public }
> [for s in local.subnets : s.cidr]
> { for s in local.subnets : s.az => s.name... }        # grouping mode -> map of lists
> cidrsubnets("10.0.0.0/16", 8, 8, 4)
> flatten([for s in local.subnets : [for p in [80, 443] : "${s.name}:${p}"]])
> type({ a = 1, b = "x" })                              # object({a: number, b: string})
> try(local.subnets[5].name, "none")
> formatdate("YYYY-MM-DD", timestamp())
> regex("^arn:aws:iam::(\\d{12}):", "arn:aws:iam::123456789012:role/x")
```

## Multi-line input
Interactive console accepts multi-line expressions while brackets are open (added
in 1.9, per the 1.9 changelog; I did not drive the interactive mode, which needs a
TTY). Piped stdin is line-based: a multi-line expression in
`terraform console < file` fails with `Missing expression`, so a piped file must
hold single-line expressions, and only the last result prints:
```bash
terraform console < expr.hcl
```

## Iterate fast
- Edit `main.tf` fixtures and restart console; locals are read at startup.
- Use `jsonencode(...)` to compare output with expected JSON.
- `type()` is console-only: in a `locals` block it fails validation with `Call to unknown function`.

## Gotchas
- `fileexists("main.tf")` was `true` from the scratch dir (filesystem functions resolve against the working directory).
- `uuid()` returned a different value on each call (`uuid() == uuid()` was `false`); `timestamp()` was identical within one run, so it differs between runs.
- Provider-defined functions (1.8+) need the provider in `required_providers` and `terraform init`.

## Verify
- [ ] The expression copied into the real module produces the same plan values.

## Checked
- Terraform 1.17.0 in a scratch dir: ran the for-expression, grouping `...`, `cidrsubnets`, `flatten`, `try`, `regex` (with doubled backslash, returns `["123456789012"]`), `formatdate` (fixed input gives `2026-10-22`) and `type()` expressions through `terraform console`; `type()` in `locals` fails validation (`Call to unknown function`); `uuid()` differs per call; piped multi-line input fails; console works with no `init`.
- Changelog v1.9 for interactive multi-line input; v1.8 for provider functions. Interactive TTY mode itself was not driven (the claim is attributed to the changelog).
