---
id: computing-software.devops-ci-cd.packer.variable-block
name: variable-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [variable, input-variables, validation, sensitive, block-variable]
level: practitioner
status: docs-checked
description: "Declare input variables with type, default, description, validation and sensitive arguments."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/variable/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `variable` block declares an input variable. The label is its name, unique among all variables in the build, and the value is read in expressions as `var.<name>`.

```hcl
variable "image_id" {
  type        = string
  description = "The ID of the machine image (AMI) to use for the server."
  validation {
    condition     = length(var.image_id) > 4 && substr(var.image_id, 0, 4) == "ami-"
    error_message = "The image_id value must be a valid AMI ID, starting with \"ami-\"."
  }
}
```

Arguments:

- `type` restricts accepted values. Keywords: `string`, `number`, `bool`. Constructors: `list(<TYPE>)`, `set(<TYPE>)`, `map(<TYPE>)`, `object({...})`, `tuple([...])`. `any` accepts any type. Types are optional but recommended. With no type and no default, a value set from env vars or `-var` is always a string.
- `default` makes the variable optional. It requires a literal value and cannot reference other objects in the configuration. If both `type` and `default` are given, the default must be convertible to the type; with only `default`, its type is used.
- `description` documents the variable from the perspective of the build's user.
- `validation` blocks hold a `condition` and an `error_message`. The condition may refer only to the variable it validates and must not produce errors; use `can(...)` when failure of an expression decides validity, for example `can(regex("^ami-", var.image_id))`. The message should be at least one full sentence.
- `sensitive = true` obfuscates the variable's string values in Packer output (for example `<sensitive>` in `packer inspect`).

A variable's value must be known: with no default and no value supplied, the build errors with "foo needs to be set". Set `default = null` to make it optional; null is valid and errors only if a receiving field needs a value.

You cannot use an `input-variable` block inside another; use `locals` to derive values. Alternatively, a `variables { foo = "value" }` block declares several variables less precisely.

## Checked

Method: docs-checked 2026-11-09 against the Packer variable block page, the Input variables page and the included validation, sensitive and must-be-set sections (all read in full as published page source). Dropped the env() claim, which these pages do not confirm.
