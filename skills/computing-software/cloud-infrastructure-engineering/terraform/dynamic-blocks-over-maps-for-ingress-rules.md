---
id: computing-software.cloud-infrastructure-engineering.terraform.dynamic-blocks-over-maps-for-ingress-rules
name: dynamic-blocks-over-maps-for-ingress-rules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, dynamic-map, dynamic-ingress, dynamic-block, map-of-objects]
level: practitioner
status: docs-checked
description: "Generate nested blocks from maps of objects with dynamic: key and value access, ingress and egress rule maps, optional attributes inside content, and the security group caveat."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks", "https://developer.hashicorp.com/terraform/language/expressions/type-constraints", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/security_group.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `dynamic` over maps (ingress/egress pattern)

```hcl
variable "ingress_rules" {
  type = map(object({
    port        = number
    protocol    = optional(string, "tcp")
    cidr_blocks = optional(list(string), [])
    sg_ids      = optional(list(string), [])
  }))
  default = {
    https = { port = 443, cidr_blocks = ["0.0.0.0/0"] }
    app   = { port = 8080, sg_ids = ["sg-0lb"] }
  }
}

resource "aws_security_group" "svc" {
  name   = "svc"
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      description     = ingress.key                 # map key
      from_port       = ingress.value.port
      to_port         = ingress.value.port
      protocol        = ingress.value.protocol
      cidr_blocks     = ingress.value.cidr_blocks
      security_groups = ingress.value.sg_ids
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Key points
- The iterator (named after the block label, here `ingress`) has `key`, the map key or list
  element index, and `value`, the current element. For a set, `key` equals `value` and should not be used.
- `for_each` takes any collection or structural value and needs one element per desired block;
  use a `for` expression to reshape data first.
- `optional(type, default)` in the variable's object type supplies a default when the attribute is
  omitted or set to null, so `content` needs no extra null checks for those attributes.
- Use a key as `description` to make diffs readable (design guidance).
- `dynamic` cannot generate meta-argument blocks such as `lifecycle` or `provisioner`.

## Caveat for security groups
The AWS provider docs warn against using inline `ingress`/`egress` arguments of
`aws_security_group` together with `aws_vpc_security_group_ingress_rule` /
`aws_vpc_security_group_egress_rule` or `aws_security_group_rule` resources: rule conflicts,
perpetual differences and overwritten rules. They also say to avoid inline rules altogether
and prefer the separate rule resources with one CIDR block per rule; for large or frequently
changing rule sets use `for_each` over the same map on those resources.

## Verify
- [ ] Adding a map entry plans one added rule and leaves existing rules unchanged.

## Checked
2026-11-08. Confirmed against the Terraform dynamic blocks page (iterator key/value, set caveat, for_each shape, meta-argument limit), the type constraints page (optional() defaults including null handling) and the AWS provider security group docs (read from the provider repository because the registry page is an empty stub; inline versus separate rule warning). Removed as unconfirmed: the lexical map iteration order and list ordering claims, and the null-omits-argument snippet.
Method: documentation only; no commands were run.
