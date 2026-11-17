---
id: computing-software.cloud-infrastructure-engineering.pulumi.pulumi-packages-and-schema
name: pulumi-packages-and-schema
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, package-schema, pulumi-package, gen-sdk, terraform-bridge]
level: practitioner
status: docs-checked
description: "Pulumi packages: source-based vs executable-based distribution, and consuming any Terraform provider with pulumi package add terraform-provider."
sources:
  - https://www.pulumi.com/docs/iac/guides/building-extending/packages/
  - https://www.pulumi.com/docs/iac/concepts/providers/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_package/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packages

A Pulumi package bundles components or a provider with a plugin so Pulumi can generate an SDK for any supported language. Authors choose between two distribution models:
- **Source-based**: consumed via `pulumi package add` (also straight from Git); Pulumi generates the SDK in the consumer's language on demand. Suits the Pulumi IDP Private Registry or no registry.
- **Executable-based**: a cross-compiled plugin binary with a `pluginDownloadURL` and usually pre-published per-language SDKs; no consumer runtime dependency, needed for the public Pulumi Registry. Supported tooling for authoring executable plugins is Go (`pulumi-go-provider`); other languages require hand-authoring the schema and serialization.

Consuming a provider has two routes: add its SDK with your language's package manager (the common case), or run `pulumi package add`, used mainly for parameterized providers. Parameterized providers accept parameters at install time and generate a local SDK. The Any Terraform Provider takes a Terraform or OpenTofu provider as its parameter:

```bash
pulumi package add terraform-provider hashicorp/random
```
This generates a local SDK in your program's language and adds the package to `Pulumi.yaml` under the `packages` key (Pulumi 3.163.0 or later), with `source: terraform-provider` and the bridge version.

## Gotchas
- The generated SDK includes a `.gitignore`, so it is safe to commit; the provider binary is cached outside the working directory and not committed.
- If you use `pulumi install` to install packages from the project file, remove generated SDK files from version control and `.gitignore` the SDK directory, otherwise the generated files stay tracked.
- The first `pulumi preview`/`up` installs any required provider missing from the plugin cache.
- For schema field details use the Schema Reference linked from the packages guide.

## Checked
2026-11-03. Confirmed on the Packages guide (two models, Go tooling note, schema reference link) and the Providers concept page (`pulumi package add terraform-provider`, `packages` key, 3.163.0, `.gitignore`, `pulumi install` warning). Removed: `get-schema`, `gen-sdk`, `package publish`, the schema JSON excerpt, `pkg:module:Type`/alias claims and the Verify paragraph, none of which appear on the pages read.
Method: documentation only; no commands were run.
