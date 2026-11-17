---
id: computing-software.cloud-infrastructure-engineering.terraform.when-not-to-use-dynamic-blocks
name: when-not-to-use-dynamic-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, dynamic-overuse, dynamic-block, readability, module-design]
level: practitioner
status: docs-checked
description: "Recognise dynamic block over-use: write nested blocks literally where possible, reserve dynamic for clean reusable-module inputs, and know what dynamic cannot generate."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# When not to use dynamic blocks

## HashiCorp's guidance
"Overuse of dynamic blocks can make configuration hard to read and maintain." Use them
only when you need to hide details in order to build a clean user interface for a
re-usable module, and "always write nested blocks out literally where possible".

## Smells
- A `dynamic` block whose `for_each` is a fixed list in the same file: write the blocks
  literally instead.
- A module that defines most or all of a resource's arguments and nested blocks directly
  from corresponding attributes of an input variable. HashiCorp says this suggests the
  module is not creating a useful abstraction; it may be better for the calling module to
  define the resource and pass information about it into your module (see the "When to
  Write a Module" and "Module Composition" pages).
- Several levels of nested `dynamic` blocks. They are supported (nest `dynamic` in
  another block's `content`), but then take care with each iterator symbol; use the
  `iterator` argument when a nested block has the same type name as its parent.

## Where dynamic is the right tool
A repeatable nested block that must be built from caller input, such as Elastic
Beanstalk `setting` blocks from a variable:
```hcl
dynamic "setting" {
  for_each = var.settings
  content {
    namespace = setting.value["namespace"]
    name      = setting.value["name"]
    value     = setting.value["value"]
  }
}
```

## Limits to remember
- Supported inside `resource`, `data`, `provider` and `provisioner` blocks.
- It can only generate arguments that belong to the object being configured. It cannot
  generate meta-argument blocks such as `lifecycle` and `provisioner`, because Terraform
  must process these before expressions can be evaluated.
- `for_each` needs one element per generated block; derive that value with expressions,
  `flatten` or `setproduct` if the input is nested.
- For a set, `key` equals `value`, so do not use `key`.

## Checked
Date: 2026-11-07
Read in full: the "dynamic Blocks" page (the cited `#best-practices-for-dynamic-blocks` anchor is one section of it).
Confirmed: the best-practice quotes, module-abstraction warning, nested dynamic and iterator guidance, supported block types, meta-argument limit, `for_each`/`key` notes.
Removed (not on the page): the per-provider claims about replacing inline blocks with standalone resources (for example AWS security group rule resources), their advantages (state addressing, import, smaller diffs), the before/after refactor and migration advice, the 0/1-list toggle suggestion, and the Verify steps. The style guide source was dropped because it does not address dynamic blocks.
Method: documentation only; no commands were run.
