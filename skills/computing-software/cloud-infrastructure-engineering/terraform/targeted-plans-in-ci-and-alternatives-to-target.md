---
id: computing-software.cloud-infrastructure-engineering.terraform.targeted-plans-in-ci-and-alternatives-to-target
name: targeted-plans-in-ci-and-alternatives-to-target
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, target-ci, targeted-plan-file, target-alternatives, avoid-target, state-splitting, unknown-for-each]
level: advanced
status: docs-checked
description: "Run a targeted plan in CI through a saved plan file when unavoidable, and remove the causes (unknown for_each keys, one huge configuration) so -target is not needed."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#resource-targeting", "https://developer.hashicorp.com/terraform/language/meta-arguments/for_each#limitations-on-values-used-in-for_each", "https://developer.hashicorp.com/terraform/cli/commands/apply#apply-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting in CI, and how to stop needing it

## What the docs say about -target
`-target=ADDRESS` focuses planning on the matching resource instances and on every
object they depend on, directly or indirectly. The address is read as follows:
- an address naming one instance selects that instance alone; for `count` or
  `for_each` resources it must include the index, like `aws_instance.example[0]`;
- an address naming a resource as a whole selects all its instances;
- an address naming a module instance selects all resources in it and in its
  child modules.

HashiCorp says to use it only in exceptional circumstances, such as recovering from
mistakes or working around Terraform limitations, and not for routine operations,
since it can lead to undetected configuration drift and confusion about how real
resources relate to configuration.

## When CI must run a targeted change
Make the target an explicit, reviewed input, never a default. Use the saved-plan
workflow from the automation docs so the reviewed plan is the one applied:
```bash
terraform plan -target=ADDRESS -out=tfplan -input=false
terraform show tfplan                       # inspect the saved plan
terraform apply -input=false tfplan
```
- Applying a saved plan runs it without a confirmation prompt, and you cannot add
  planning modes or options to the apply: the plan file holds those decisions.
- The plan file stores your configuration, all planned values and the plan options,
  including input variables. Sensitive data is saved in cleartext even when the
  terminal output hides it, so treat the file as a sensitive artifact. Do not give it
  a `.tf` suffix.
- Judgement, not from the docs: because targeting can hide drift, follow a targeted
  apply with an untargeted `terraform plan` and investigate any diff.

## Root causes and their documented fixes
- `for_each` keys must be known before Terraform performs any remote operation. If
  they are not, Terraform returns an error saying `for_each` has dependencies that
  cannot be determined before apply and that a `-target` may be needed. Build the
  map or set from values known at plan time (for example `toset([...])` of names
  from variables or locals) rather than from attributes of resources not yet
  created, such as generated IDs. Keys also cannot depend on impure functions such
  as `uuid`, `bcrypt` or `timestamp`, or on sensitive values.
- To operate on isolated parts of a very large configuration, the docs prefer
  breaking it into several smaller configurations that can each be applied
  independently. Data sources can read information about resources created in other
  configurations.

## Checked
Date: 2026-11-07
Read in full: the terraform plan command page (Planning Options, Resource Targeting,
Other Options including -out, -input) and the terraform apply command page (Saved
Plan Mode, Apply Options); the for_each reference page sections Usage and
Limitations on values (the rest of that page was also read).
Removed because the pages do not state them: the GitHub Actions workflow
(workflow_dispatch inputs, artifact upload and download, environment approval),
the claim that targeting is baked into the plan file, `-exclude`, the 20-minute
plan figure, the region, provider and bootstrap rows of the fix table, the
`ignore_changes` suggestion, and the Verify checklist. The unknown-keys skill
cross-reference was dropped.
Method: documentation only; no commands were run.
