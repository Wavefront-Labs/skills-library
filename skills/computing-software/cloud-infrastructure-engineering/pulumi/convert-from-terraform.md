---
id: computing-software.cloud-infrastructure-engineering.pulumi.convert-from-terraform
name: convert-from-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-convert, terraform-conversion, tf2pulumi, convert-from]
level: practitioner
status: docs-checked
description: "Convert Terraform HCL to a Pulumi program with pulumi convert --from terraform and adopt existing resources from a Terraform state file with pulumi import --from."
sources:
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_convert/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_import/
  - https://www.pulumi.com/docs/iac/guides/migration/import/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting Terraform

`pulumi convert` converts a program from a source program into another Pulumi language. Source defaults to the current directory. Valid source (`--from`): yaml, terraform, bicep, arm, kubernetes (default yaml). Valid targets (`--language`): typescript, python, csharp, go, java, yaml.

```bash
cd tf-project
pulumi convert --from terraform --language typescript --out ../pulumi-app
```
Flags: `--generate-only` (do not install dependencies), `--mappings` (mapping files), `--name` (project name, defaults to the source directory), `--out` (output directory, default `.`), `--strict` (fail on errors such as missing variables). Some target languages need additional arguments.

**Adopt existing resources from Terraform/OpenTofu state** instead of recreating them: when a state file already describes them, skip the import file and run from the project directory (it reads your `.tf` files alongside the state):
```bash
pulumi import --from hcl terraform.tfstate
```
`pulumi import` flags: `--from` (invoke a converter to import), `--generate-code` (default true), `--out` (file for generated declarations), `--file` (JSON list of resources to import in bulk), `--generate-resources` (with `--from`, write the discovered importable resources as JSON to a path).

## Gotchas
- Import files name resources by Pulumi type tokens (`aws:ec2/vpc:Vpc`), so keep the `pulumi/aws` provider. The Terraform aws provider's `aws_vpc` and `aws_subnet` register under different tokens (`aws:index:Vpc`), so Pulumi would see new resources, not the imported ones.
- The bulk import JSON requires `resources`, each with `id`, `type`, `name` (`id` not needed for components).

## Checked
2026-11-03. Confirmed on the `pulumi convert` and `pulumi import` CLI pages and the import migration guide. Removed: the `--from terraform` state-import form, `terraform.state.RemoteStateReference` example, the list of unconvertible constructs, module conversion, zero-creates preview rule and Verify paragraph; none are on pages read.
Method: documentation only; no commands were run.
