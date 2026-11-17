---
id: computing-software.cloud-infrastructure-engineering.terraform.attributes-as-blocks-mode-and-dynamic
name: attributes-as-blocks-mode-and-dynamic
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, attributes-as-blocks, dynamic-block, nested-blocks, empty-list]
level: practitioner
status: docs-checked
description: "Handle attributes-as-blocks arguments (like ingress on aws_security_group): block vs attribute syntax, assigning [] to remove all, and how dynamic interacts with them."
sources: ["https://developer.hashicorp.com/terraform/language/attr-as-blocks", "https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attributes-as-blocks mode

Most resource types use repeatable nested blocks for sub-objects. Rarely, a resource
type also accepts an argument with the same name as a nested block type, and purges
any sub-objects of that type if the argument is set to an empty list (`<ATTR> = []`).
Terraform documents this as "attributes as blocks" mode. The AWS provider documents
`ingress` and `egress` on `aws_security_group` as processed in this mode. Each
resource's documentation links to the Terraform appendix page when an argument works
this way.

## Two syntaxes are accepted
Block syntax (the docs recommend it for a fixed collection of objects):
```hcl
resource "aws_security_group" "x" {
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```
Argument syntax (valid only for these special arguments) assigns a list of objects:
```hcl
resource "aws_security_group" "x" {
  ingress = [{
    from_port = 443, to_port = 443, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"]
    description = null, ipv6_cidr_blocks = null, prefix_list_ids = null, security_groups = null, self = null
  }]
}
```
With argument syntax every object attribute must be assigned, even if only an explicit
`null`: an argument declaration overrides defaults, so the usual handling of optional
arguments does not apply. The two forms cannot be mixed (explicit zero objects plus
explicit blocks). Assigning `[]` to a true nested block, where this special behaviour
does not apply, is not valid.

## Removing all elements
Omitting all blocks is read as "ignore any existing objects", so existing rules stay:
the AWS provider docs say removing `ingress`/`egress` from the configuration does not
destroy the managed rules. To remove them all, use argument syntax with an empty list:
```hcl
ingress = []
egress  = []
```

## dynamic blocks
A `dynamic` block generates normal nested blocks (supported in resource, data, provider
and provisioner blocks). For attributes-as-blocks arguments, the Terraform docs
call an argument-syntax `for` expression the better pattern than a `dynamic` block,
because an empty input then assigns an explicit empty list instead of assigning nothing
and so retaining and ignoring existing objects:
```hcl
ingress = [for r in var.rules : {
  from_port = r.port, to_port = r.port, protocol = "tcp", cidr_blocks = r.cidrs,
  description = r.name, ipv6_cidr_blocks = null, prefix_list_ids = null, security_groups = null, self = null
}]
```
In a reusable module that takes a list of objects, the docs suggest `merge` to fill in
attributes the caller omitted, giving callers the effect of optional arguments:
```hcl
example = [for ex in var.examples : merge({ foo = null }, ex)]
```
`dynamic` blocks remain required for dynamically generating normal nested blocks.

## JSON syntax
In JSON syntax these arguments are always written as a JSON list of objects; JSON
cannot use the nested-block processing mode for them.

## Checked
Date: 2026-11-07

Read in full (stripped text): the Terraform "Attributes as Blocks" page and the "dynamic Blocks" page. For `aws_security_group`, the registry page renders empty to a plain fetch, so I read the provider's docs source file on GitHub (the ingress, egress and "Removing All Ingress and Egress Rules" sections); no code tabs were present.

Trimmed as unconfirmed: "legacy SDKv2"; `route` on `aws_route_table` and `setting` as examples (the dynamic-blocks page shows `setting` as an ordinary nested block); "Optional+Computed"; the `Incorrect attribute value type ... "self" is required` error text; the claim that `providers schema -json` shows these as attributes; the "provider docs often say can be specified as an attribute" line; the Verify step. Added the `merge` pattern, no-mixing rule and JSON note from the page. Added the registry page for `aws_security_group` to `sources`.

Method: documentation only; no commands were run.
