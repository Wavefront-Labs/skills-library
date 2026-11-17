---
id: computing-software.devops-ci-cd.packer.hcl-syntax-basics
name: hcl-syntax-basics
category: computing-software
field: devops-ci-cd
product: packer
tags: [hcl2, syntax, comments, identifiers, hcl-syntax]
level: intro
status: docs-checked
description: "HCL2 syntax rules for Packer templates: comments, identifiers, encoding, arguments, blocks and types."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/syntax/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Packer's HCL templates are built from two constructs: arguments and blocks.

An argument assigns a value to a name: `image_id = "abc123"`. What value types are valid depends on context (each source type has a schema), but many arguments accept arbitrary expressions.

A block is a container with a type, a number of labels set by the block type, and a body delimited by `{` and `}` in which arguments and blocks can nest:

```hcl
source "amazon-ebs" "example" {
  ami_name = "abc123"

  tags = {
    # ...
  }
}
```

Here the `source` block type expects two labels (`amazon-ebs` and `example`); the nested `tags` needs none. Most Packer features (input variables, data sources and so on) are top-level blocks, which can appear outside any other block.

Syntax rules from the docs:

- Identifiers (argument names, block types, names of variables and similar) can contain letters, digits, underscores and hyphens. The first character must not be a digit. Packer implements the Unicode identifier syntax, extended with the ASCII hyphen.
- Comments: `#` begins a single-line comment and is the default style; `//` is an alternative that formatting tools may convert to `#`; `/*` and `*/` delimit a comment that may span lines.
- Configuration files must be UTF-8. Non-ASCII characters are accepted in identifiers, comments and string values.
- Unix (LF) and Windows (CRLF) line endings are both accepted, but LF is idiomatic and formatting tools may convert CRLF to LF.

```hcl
# single-line
source "null" "example" {
  communicator = "none"
}
/* multi-line
   comment */
```

For the full language definition see the HCL native syntax specification; for HCL constructs written in JSON see the JSON syntax reference page.

## Checked

Method: docs-checked 2026-11-09 against the Packer HCL syntax reference page (read in full as published page source). Dropped the file-naming, block-order, types list and packer fmt/validate remarks, which this page does not cover.
