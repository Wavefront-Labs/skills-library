---
id: computing-software.cloud-infrastructure-engineering.terraform.cleaning-up-generated-import-configuration
name: cleaning-up-generated-import-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, generated-config-cleanup, generate-config-out, import-block, refactoring]
level: practitioner
status: gated
description: "Turn -generate-config-out HCL into maintainable code: drop computed and default attributes, replace literals with references, fix conflicting arguments, then reach a no-op plan."
sources: ["https://developer.hashicorp.com/terraform/language/import/generating-configuration", "https://developer.hashicorp.com/terraform/language/import"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cleaning up generated configuration

```bash
terraform plan -generate-config-out=generated.tf
```
Terraform writes one resource block per import target with **every** attribute the
provider returned. It is a starting point, not finished code.

## Cleanup checklist
1. **Fix errors first.** Generated config can be invalid: mutually exclusive arguments
   both set (`Conflicting configuration arguments`), or values that are only valid
   when read. Remove the one you do not use; re-run plan.
2. **Delete null and default values.** Lines like `description = null`,
   `force_destroy = false`, `tags = {}` add noise. Remove anything equal to the
   provider default (check docs).
3. **Drop computed-only noise.** Attributes such as `arn`, `id`, `owner_id` are
   usually not emitted, but `tags_all` and some "optional+computed" values are; keep
   only what you intend to manage (gated: unconfirmed, source is paywalled or blocked) (no AWS provider here; the local `terraform_data` output had only `input = null` and `triggers_replace = null`).
4. **Replace literals with references.** `vpc_id = "vpc-0abc"` -> `vpc_id = aws_vpc.main.id`
   or a variable. This creates real dependencies.
5. **Split inline vs separate resources.** If AWS returns inline `ingress` blocks and
   you manage rules as `aws_vpc_security_group_ingress_rule`, delete the inline ones (gated: unconfirmed, source is paywalled or blocked).
6. **Move into modules** with `moved` blocks after import, not during.
7. **Rename** the generated resource names (`this`, `main`, meaningful keys) before
   applying; import targets follow the `to` address.
8. **Secrets**: generated config may contain passwords or keys read from the API;
   replace with variables/ephemeral values before committing.

## Converge
```bash
terraform fmt generated.tf
terraform plan     # goal: N to import, 0 to add, 0 to change, 0 to destroy
```
Any `~` after import means the code differs from reality; decide per attribute
whether to match reality or accept the change.

## Gotchas
- `-generate-config-out` refuses to overwrite an existing file (`Error: Target generated file already exists`); delete it or pick a new name to regenerate.
- The plan prints `Warning: Config generation is experimental` (still present in 1.17.0).
- It only generates for `import` blocks whose `to` resource has no config (ran: with one configured and one unconfigured target, only the unconfigured one was written), and only for root-module resources (`Only resources within the root module are eligible for config generation`).
- Sensitive values appear in clear text in the generated file (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Plan after cleanup: imports only, no changes.
- [ ] No hard-coded IDs remain where a reference exists; no secrets in VCS.

## Checked
- Terraform 1.17.0 with `terraform_data` import blocks: `plan -generate-config-out=generated.tf` wrote `# __generated__ by Terraform` plus a block with null attributes; a second run with the same file name failed with `Target generated file already exists`; a configured target was left alone and a module-instance target errored with the root-module-only message; `Plan: 1 to import, 0 to add...` shown.
- Gated: provider-specific attributes (`tags_all`, inline vs separate rules) and the clear-text secrets claim need a cloud provider.
