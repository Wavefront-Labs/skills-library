---
id: computing-software.cloud-infrastructure-engineering.terraform.templatestring-function
name: templatestring-function
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, templatestring, templatefile, string-templates, dynamic-templates]
level: practitioner
status: verified
description: "Render templates held in variables or data sources with templatestring (Terraform 1.9+), its reference-only restriction, and when templatefile is still the right tool."
sources: ["https://developer.hashicorp.com/terraform/language/functions/templatestring", "https://developer.hashicorp.com/terraform/language/functions/templatefile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `templatestring`

`templatefile(path, vars)` renders a file shipped with the module. `templatestring(ref, vars)`
(Terraform 1.9+, per the 1.9 changelog) renders a template that arrives as a **value** — from a variable,
an S3 object, an SSM parameter or a data source.

```hcl
# `body` is only populated for human-readable Content-Type objects (provider docs)
data "aws_s3_object" "motd_template" {
  bucket = "acme-config"
  key    = "templates/motd.tftpl"
}

locals {
  motd = templatestring(data.aws_s3_object.motd_template.body, {
    env   = var.env
    owner = var.owner
  })
}
```

## The restriction
The first argument must be a **direct reference** to a named value (`var.x`,
`local.x`, `data.x.y.attr`) — not a literal string or an expression:
```hcl
templatestring("Hello", {...})                # error: "templatestring is only for rendering templates retrieved dynamically"
templatestring(upper(local.tpl), {...})       # error: must be a direct reference to a single string
templatestring(local.tpl, {...})              # ok
```
This prevents double-interpolation confusion: in a literal, HCL would evaluate
`${name}` itself before the function ever saw it.

## Escaping in stored templates
Templates stored outside HCL use normal template syntax (`${var}`, `%{ for }`).
If the template itself is written in an HCL string (e.g. a variable default), escape
it there: `default = "Hello $${name}"`, so the stored value is `Hello ${name}`.

## When to use which
| Template source | Function |
|---|---|
| File in the module | `templatefile` |
| Supplied by caller as a variable | `templatestring(var.tpl, ...)` |
| Fetched at plan (S3/SSM/http) | `templatestring(data...., ...)` |

## Gotchas
- Not available in Terraform < 1.9: set `required_version = ">= 1.9"`. OpenTofu added its own `templatestring` in 1.7.0 (its changelog), so check the version before depending on it.
- Wrapping the reference in interpolation (`"${var.tpl}"`) is rejected too.
- Templates from external sources are still logic: they can call Terraform functions (`upper()` works inside a rendered template), though filesystem functions such as `file()` are rejected ("cannot use filesystem access functions like file in templatestring templates"). Restrict write access to the source anyway.
- Unknown template values (from resources being created) make the result unknown (a `terraform_data.a.id` variable plans as `(known after apply)`).

## Verify
- [ ] `terraform console` → `local.motd` renders with the expected substitutions.
- [ ] `required_version` constraint updated.
