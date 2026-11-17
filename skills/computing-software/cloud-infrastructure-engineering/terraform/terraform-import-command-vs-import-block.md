---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-import-command-vs-import-block
name: terraform-import-command-vs-import-block
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, cli-import-command, terraform-import-command, import-block, legacy-import]
level: practitioner
status: docs-checked
description: "Choose between the terraform import CLI command and import blocks; run CLI import correctly with variables, address quoting, modules and provider configuration."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/import", "https://developer.hashicorp.com/terraform/language/import", "https://opentofu.org/docs/cli/commands/import/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform import` (CLI) vs `import` blocks

## Which to use
- The CLI page itself points to the `import` block as the alternative to importing by hand: the block makes Terraform
  import the resource when you run `terraform apply`, so imports can be automated in CI/CD pipelines.
- Block workflow (Terraform's Import overview): write an `import` block holding the resource's unique ID and the address
  it takes in state, plus a destination `resource` block at that address; run `terraform apply`. Alternatively write only
  the `import` block and run `terraform plan` with the `-generate-config-out` flag to generate the resource blocks.
- For many resources, the overview describes bulk import: define queries in HCL, add the results to the configuration
  and run `terraform apply`.
- The CLI command `terraform import [options] ADDRESS ID` still exists. It is the better fit for a quick one-off; for
  anything others must review or repeat, prefer a block.

## Running the CLI correctly
```bash
terraform import aws_instance.foo i-abcd1234
terraform import module.foo.aws_instance.bar i-abcd1234
terraform import 'aws_instance.baz[0]' i-abcd1234
terraform import 'aws_instance.baz["example"]' i-abcd1234     # Linux, macOS, UNIX shells
```
PowerShell needs `'aws_instance.baz[\"example\"]'`; cmd.exe needs `aws_instance.baz[\"example\"]` (no outer quotes).
- `ADDRESS` is any valid resource address, so it can target a module as well as the root. `ID` depends on the resource
  type (an EC2 instance ID, a Route53 zone ID, ...); the provider docs give the format. An invalid ID just gives an error.
- Import each remote object to only one resource address; importing the same object more than once can produce
  unwanted behaviour.
- Terraform loads the configuration in the working directory (or `-config=path`) to configure the provider. Provider
  configuration used for import must not depend on non-variable inputs (for example a data source). With no config,
  Terraform prompts for credentials or reads environment variables.
- Flags (all optional): `-config=path`, `-input=true`, `-lock=false` (dangerous if others run commands on the same
  workspace), `-lock-timeout=0s`, `-no-color`, `-parallelism=n` (default 10), `-var 'foo=bar'`, `-var-file=foo` (only
  useful with `-config`), and a deprecated `-provider=provider`. Terraform picks the provider from the target resource's
  configuration by default, which the docs call the best behaviour.
- With the HCP Terraform CLI integration or `remote` backend only, `-ignore-remote-version` is also accepted; with the
  local backend only, the legacy `-state`, `-state-out` and `-backup` are accepted.

## OpenTofu differences
`tofu import [options] ADDRESS ID` has the same shape and flags, plus `-json` (machine-readable output; implies
`-input=false`, so the configuration must have no unassigned variables) and `-json-into=out.json`. Using variables in
module sources, backend configuration or an encryption block requires assigning root module variables when running
`tofu import`.

## After any import
Run a plan and read it: the resource block in configuration must match the real object. Fix the configuration before
anyone applies, or an apply will change the real object to match the configuration.

## Verify
- [ ] The imported address in state points at the expected cloud object ID.
- [ ] The following `terraform plan` shows no unexpected changes.

## Checked

Checked 2026-11-08 against the Terraform `terraform import` command page, the Terraform Import resources overview and
the OpenTofu `tofu import` page: usage, address and ID rules, duplicate-address warning, provider configuration rule,
flags and defaults, per-shell quoting examples, `-json`/`-json-into`, and the import block and
`-generate-config-out` workflow. Removed (not on the fetched pages): the comparison table claims about plan review and
HCP/Atlantis, version gates for import blocks and `for_each`, the "Configuration for import target does not exist" error,
and the claim that sensitive HCP workspace variables are unreadable.

Method: documentation only; no commands were run.
