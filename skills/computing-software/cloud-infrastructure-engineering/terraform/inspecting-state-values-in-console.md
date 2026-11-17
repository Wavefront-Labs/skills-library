---
id: computing-software.cloud-infrastructure-engineering.terraform.inspecting-state-values-in-console
name: inspecting-state-values-in-console
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, console-state, terraform-console, state-inspection, debugging]
level: practitioner
status: verified
description: "Query live state from terraform console: resource attributes, indexed instances, module outputs and locals, and how console locks and reads remote state."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/console", "https://developer.hashicorp.com/terraform/language/expressions/references"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting state in `terraform console`

`terraform console` loads configuration **and the current state**, so any reference
that has a value in state evaluates to the stored value.

```bash
terraform console
> aws_instance.web.private_ip
"10.0.1.23"
> aws_instance.web["api"].tags
> module.vpc.private_subnets
> [for k, v in aws_instance.web : "${k}=${v.private_ip}"]
> keys(aws_instance.web)
> local.common_tags
> var.environment
> data.aws_caller_identity.current.account_id
```

## Rules of thumb
- Values that are not in state (resource never applied) print `(known after apply)`.
- Data sources show the value from the **last** refresh stored in state, not a fresh
  read: after editing the file behind a `local_file` data source, plain console still showed
  the old content and `terraform console -plan` (Terraform 1.9+) showed the new one.
- Sensitive values print `(sensitive value)`; `nonsensitive(x)` in console reveals
  them for debugging, so treat the terminal as sensitive.
- Child-module locals are not addressable from the root scope (`module.m.local.x` gives
  `Unsupported attribute`); use outputs (`module.m.out`) or, on Terraform 1.16+,
  `terraform console -scope=module.m` and then `local.x` (the `-scope` flag is in the 1.16.0
  changelog; on Terraform 1.17.0 it printed the module local).

## Locking and workspaces
`terraform console` has no `-lock` flag (`terraform console -lock=false` fails with `flag
provided but not defined: -lock`) and in the local-backend test `terraform plan` ran
normally while a console session was open; in Terraform's source the console command builds
its operation without a state locker. It reads the configured backend's current state and
never modifies it. Console uses the selected workspace (`terraform workspace show`): in a
fresh workspace `terraform_data.web["api"].input` printed `(known after apply)`, in the
default workspace the stored value.

## Non-interactive
```bash
echo 'aws_instance.web.private_ip' | terraform console
echo 'jsonencode({for k, v in aws_instance.web : k => v.id})' | terraform console | jq -r . | jq .
```
Console prints HCL-formatted values; `jsonencode()` then `jq -r .` gives clean JSON.

## Versus `state show`
`terraform state show ADDR` prints all attributes of one instance as HCL; console
lets you compute across instances and modules.

## Verify
- [ ] Value matches the cloud console for the same object.
- [ ] Lock released after exiting (another `plan` can start).

## Checked
- Terraform 1.17.0 (random/local providers and `terraform_data`): resource attribute, `for` expression, `keys()`, local, variable and `module.m.out` expressions all printed as shown; an unapplied resource printed `(known after apply)`; a sensitive variable printed `(sensitive value)` and `nonsensitive()` revealed it; `module.m.local.secretish` failed with `Unsupported attribute` while `-scope=module.m` printed it; `jsonencode(...) | terraform console | jq -r . | jq .` produced a JSON object; the data-source staleness and `-plan` behaviour, the missing `-lock` flag and the workspace behaviour were run as described; `terraform state show ADDR` printed the attributes as HCL.
- Source check: `internal/command/console.go` and `meta_backend.go` in hashicorp/terraform (the state locker is a no-op unless a command enables locking); `-plan` is in the 1.9.0 changelog and `-scope` in 1.16.0. AWS-specific example expressions (`aws_instance.web...`, `data.aws_caller_identity.current.account_id`) are the same reference syntax; no AWS account was used.
