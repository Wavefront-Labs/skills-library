---
id: computing-software.cloud-infrastructure-engineering.terraform.targeting-data-sources-and-outputs
name: targeting-data-sources-and-outputs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, target-data-source, target, outputs, data-sources, refresh-only]
level: practitioner
status: docs-checked
description: "How -target selects addresses, why it is for exceptional cases, and how refresh-only mode and outputs fit when you need fresh state without infra changes."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#resource-targeting", "https://developer.hashicorp.com/terraform/cli/commands/plan#planning-modes", "https://developer.hashicorp.com/terraform/language/values/outputs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting, refresh-only and outputs

## What -target selects
`-target=ADDRESS` focuses planning on the matching resource instances and every object they depend on, directly or indirectly. An address can name:
- one instance (for `count` or `for_each` resources the index is required, for example `aws_instance.example[0]`),
- a whole resource (all its current instances), or
- a module instance (all resources in it and its child modules).

HashiCorp reserves `-target` for exceptional circumstances such as recovering from mistakes or working around Terraform limitations. Routine use risks undetected configuration drift. For very large configurations, split them into several smaller configurations applied independently, and use data sources to read objects created elsewhere.

## Refreshing without changing infrastructure
Refresh-only mode (`terraform plan -refresh-only`, available from Terraform v0.15.4) creates a plan whose goal is only to update state and root module output values to match remote objects changed outside Terraform. It is mutually exclusive with `-destroy` and cannot be combined with `-refresh=false` or `-minimal-refresh`.

```bash
terraform apply -refresh-only
```

`-refresh=false` and `-minimal-refresh` skip refreshing and can make the plan incomplete or incorrect, since external changes are ignored; avoid them when upgrading provider versions.

## Outputs
Root module outputs are shown after apply, and other configurations can read them through the `terraform_remote_state` data source. Because consumers read what was last stored, re-plan downstream configurations after upstream outputs change. Mark secrets with `sensitive = true`; sensitive outputs are still stored in state and `terraform output -json` or `-raw` prints them in plain text.

## Verify
- [ ] `terraform output` after the operation shows current values.
- [ ] Downstream configurations were re-planned after upstream outputs changed.

## Checked
2026-11-08. Read in full: the terraform plan command page (planning modes, planning options, resource targeting) and the "Use outputs to expose module data" page. Removed unconfirmed claims about targeting data sources directly, outputs going stale only under -target, `terraform console -plan`, and the deferred-read marker, because the cited pages do not document them.
Method: documentation only; no commands were run.
