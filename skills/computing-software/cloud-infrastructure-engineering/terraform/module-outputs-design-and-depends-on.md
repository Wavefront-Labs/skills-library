---
id: computing-software.cloud-infrastructure-engineering.terraform.module-outputs-design-and-depends-on
name: module-outputs-design-and-depends-on
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-outputs, module-output-design, output-depends-on, module-design, outputs]
level: practitioner
status: docs-checked
description: "Design module outputs: descriptions, child-to-parent access, sensitive and ephemeral outputs, standard file layout, and when depends_on on an output is justified."
sources: ["https://developer.hashicorp.com/terraform/language/values/outputs", "https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on", "https://developer.hashicorp.com/terraform/language/modules/develop/structure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing module outputs

## What outputs are for
Output blocks let child modules expose resource attributes to parent modules, show root
values in CLI output (and in the HCP Terraform workspace overview), let other
configurations read root outputs through `terraform_remote_state`, and pass information
from a Terraform run to automation.

A parent reads a child output as `module.<CHILD_MODULE_NAME>.<OUTPUT_NAME>`:
```hcl
output "instance_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.web.private_ip
}
# in the parent
records = [module.web_server.instance_ip]
```
`value` can be any valid expression.

## Layout and documentation
In the standard module structure, outputs go in `outputs.tf`, and all variables and
outputs should have one or two sentence descriptions that explain their purpose, which
tooling uses for documentation. The README need not list inputs and outputs because
tooling generates that.

## Sensitive and ephemeral outputs
- `sensitive = true` makes CLI output show `<sensitive>`, e.g.
  `terraform output database_password` prints `database_password = <sensitive>`.
- Warning from the docs: sensitive outputs are still stored in state, and `terraform
  output -json` or `-raw` print them in plain text.
- `ephemeral` on an output keeps the value out of state and plan files, at the cost of
  restrictions on what can be assigned to it. See the Manage sensitive data page.

## `depends_on` on an output
Outputs are a supported construct for `depends_on`, but they typically do not need it.
When you add one, put a comment saying why. The docs' example:
```hcl
output "instance_ip_addr" {
  value       = aws_instance.server.private_ip
  description = "The private IP address of the main server instance."

  depends_on = [
    # Services are unreachable unless the security group rule is created
    # before exposing this IP address.
    aws_security_group_rule.local_access,
  ]
}
```
The general advice applies: use `depends_on` only as a last resort, because it can make
plans more conservative, with more values "known after apply". Prefer expression
references that imply the dependency.

## Checked
Date: 2026-11-07
Read in full: Use outputs to expose module data (language/values/outputs), the depends_on meta-argument page (language/meta-arguments/depends_on; added to sources because the cited anchor on the outputs page does not exist there), and Standard Module Structure (language/modules/develop/structure).
Confirmed: purposes of outputs; child output reference syntax; sensitive behaviour, state storage warning, `-json`/`-raw` exposure; ephemeral outputs; description and file layout guidance; output depends_on example, comment recommendation, supported constructs and last-resort caveat.
Removed: "avoid whole-resource outputs", "key collections like the input" and `one(...)` null-output advice, `ephemeral = true` in child modules only, the claim that output `depends_on` is better than caller `depends_on = [module.x]` and "defers every data source", deprecation and renaming advice, "depends_on takes resources/modules, not attributes", the "Output refers to sensitive values" error text, `terraform-docs`, and the Verify checklist.
Not opened: the output block reference and Manage sensitive data.
Method: documentation only; no commands were run.
