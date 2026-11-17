---
id: computing-software.cloud-infrastructure-engineering.terraform.string-functions-format-regex-and-replace
name: string-functions-format-regex-and-replace
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, string-functions, format-function, regex-function, replace, join, split, naming]
level: practitioner
status: verified
description: "Build and parse strings in HCL: format/formatlist, join/split, replace with regex, regex/regexall capture groups, trim family, case, substr, and startswith/endswith."
sources: ["https://developer.hashicorp.com/terraform/language/functions/format", "https://developer.hashicorp.com/terraform/language/functions/regex", "https://developer.hashicorp.com/terraform/language/functions/replace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String functions

## Building
```hcl
format("%s-%s-%03d", var.project, var.env, 7)        # "acme-prod-007"
formatlist("arn:aws:s3:::%s/*", var.buckets)          # list in, list out
join(",", var.cidrs)
lower(var.name); upper(...); title(...)
substr("abcdef", 0, 3)                                # "abc"
```
Prefer interpolation `"${a}-${b}"` for simple joins; `format` when padding, widths or
`%q` (quoted) / `%v` (any) matter.

## Parsing
```hcl
split("/", "arn:aws:iam::123456789012:role/app/deployer")   # list
element(split(":", var.arn), 4)                             # account id
regex("^arn:aws:iam::(\\d{12}):role/(.+)$", var.arn)        # ["123...", "app/deployer"]
regex("(?P<acct>\\d{12})", var.arn).acct                    # named group -> object
regexall("[0-9]+", "a1b22c333")                             # ["1","22","333"]
length(regexall("^prod-", var.name)) > 0                    # boolean test
```
- `regex` **errors** on no match — wrap with `can()`/`try()` or use `regexall`.
- Double the backslashes in HCL strings: `"\\d"`; RE2 syntax.

## Replacing and trimming
```hcl
replace(var.name, "_", "-")
replace(var.name, "/[^a-z0-9-]/", "")      # regex when wrapped in slashes
trimspace(file("${path.module}/token.txt"))
trimprefix(var.path, "/"); trimsuffix(var.host, ".")
trim("--x--", "-")                         # removes any of the chars from both ends
chomp(data.local_file.x.content)           # strip trailing newlines
```

## Predicates
`startswith(s, "prod-")` and `endswith(s, ".com")` (Terraform 1.3+), `strcontains(s, "test")` (1.5+) (versions from the Terraform changelog).

## Naming helper example
```hcl
locals {
  name = substr(lower(replace("${var.project}-${var.env}-${var.component}", "/[^a-zA-Z0-9-]/", "-")), 0, 63)
}
```

## Gotchas
- `substr` with a length beyond the end is fine; negative offsets count from the end.
- `title` upper-cases the first letter of each word (`title("élan vital")` gives `Élan Vital`); it is not meant for identifiers, and `upper("straße")` leaves `ß` unchanged, so do not rely on case-folding for uniqueness.
- `split` on an empty string returns `[""]`, not `[]` — check `var.x == ""` first.
- Test expressions in `terraform console` before committing.

## Verify
- [ ] `echo 'regex("^arn:aws:iam::(\\d{12})", "arn:aws:iam::123456789012:role/x")' | terraform console` prints `["123456789012"]` (a one-element list, since the group is unnamed).
- [ ] Generated names respect provider length/charset limits (validate with a precondition).
