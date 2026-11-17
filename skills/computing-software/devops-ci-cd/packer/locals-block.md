---
id: computing-software.devops-ci-cd.packer.locals-block
name: locals-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [locals, local, expressions, hcl2, block-locals]
level: practitioner
status: docs-checked
description: "Compute named values once with a locals block or singular local blocks, in definition order, with sensitive support."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/locals/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Local variables assign a name to an expression that can be used multiple times within a folder. The expression is evaluated at run time and can reference input variables, other locals, data sources and HCL functions. You cannot overwrite a local. Declare them in a plural `locals` block or one at a time with `local`.

```hcl
locals {
  default_name_prefix = "${var.project_name}-web"
  name_prefix         = "${var.name_prefix != "" ? var.name_prefix : local.default_name_prefix}"
}

local "mylocal" {
  expression = "${var.secret_api_key}"
  sensitive  = true
}
```

Reference them with the `local.` prefix, for example `output = "${local.name_prefix}-files"`.

Facts from the docs:

- `locals` defines one or more locals; names must be unique throughout a folder, and the value can be any expression valid in the folder.
- A local may refer to other locals, but reference cycles are not allowed: a local cannot refer to itself or to a variable that refers back to it.
- The singular `local` block defines exactly one local: the block label is the name, `expression` is the value, and the optional `sensitive` boolean filters the value from logs. Use it for secrets.
- The `locals` block is read as a map, and maps are not sorted, so evaluation time of complex locals is not deterministic. Singular `local` blocks are evaluated in the order they are defined, so order and time are always the same. Prefer them for complex locals.
- Group logically related locals in one block, and put unrelated ones in separate blocks.
- Locals can reference data sources, but data sources cannot reference locals (this avoids cyclic dependencies). To feed user input into a data source, use a `variable` block.
- Named local maps can be blended with instance-specific values, for example `tags = "${merge(local.common_tags, {"Name" = "awesome-app-server"})}"`.

## Checked

Method: docs-checked 2026-11-09 against the Packer locals block page, the Local variables page and its included known-limitations text (all read in full as published page source). Dropped the regex_replace example and the claim about variable defaults, which these pages do not support.
